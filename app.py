from flask import Flask, render_template, request, jsonify
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
import torch
import requests
import os
import logging
from dotenv import load_dotenv

load_dotenv()

# Server-side logger — exceptions are recorded here, never leaked to the user.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("safechat")

app = Flask(__name__)

# ==========================================
# CONFIG
# ==========================================

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY environment variable is not set. Add it to a .env file.")

MODEL_PATH = r"C:\Users\rithi\vs_code_proj\Safe_Chat\SafeChat_RoBERTa"

LABELS = [
    "toxic",
    "severe_toxic",
    "obscene",
    "threat",
    "insult",
    "identity_hate"
]

# Per-label moderation thresholds (probability above which a label is "detected").
# A single flat cutoff causes false positives on rare / subjective labels
# like identity_hate and threat, so each label gets its own tuned value.
THRESHOLDS = {
    "toxic":         0.50,
    "severe_toxic":  0.50,
    "obscene":       0.60,
    "threat":        0.70,
    "insult":        0.55,
    "identity_hate": 0.75,
}

# ==========================================
# LOAD SAFECHAT MODEL
# ==========================================

print("Loading SafeChat model...")

model_loaded = AutoModelForSequenceClassification.from_pretrained(
    MODEL_PATH
)

tokenizer_loaded = AutoTokenizer.from_pretrained(
    MODEL_PATH
)

classifier = pipeline(
    "text-classification",
    model=model_loaded,
    tokenizer=tokenizer_loaded,
    top_k=None,
    device=0 if torch.cuda.is_available() else -1
)

print("Model Loaded Successfully")


# ==========================================
# MODERATION FUNCTION
# ==========================================

def moderate_message(text):

    results = classifier(text)[0]

    detected = []

    for i, item in enumerate(results):

        label = LABELS[i]
        score = item["score"]

        threshold = THRESHOLDS.get(label, 0.50)

        if score > threshold:
            detected.append(
                {
                    "label": label,
                    "score": round(score * 100, 2)
                }
            )

    if len(detected) > 0:

        return {
            "safe": False,
            "reasons": detected
        }

    return {
        "safe": True,
        "reasons": []
    }


# ==========================================
# GENTLE REMINDER (auto-reply on blocked messages)
# ==========================================

def gentle_reminder():
    return (
        "Let's keep the conversation respectful and constructive. "
        "I'm happy to help with questions, ideas, or discussions in a positive way. "
        "Please use respectful language — I'm here to help with healthy and constructive conversations. "
        "Feel free to rephrase your message and continue the discussion."
    )


# ==========================================
# OPENROUTER CALL
# ==========================================

def get_ai_reply(user_message, history=None):

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    # Build the messages list: system prompt + prior turns + new user turn.
    # The frontend is responsible for never sending toxic content as a
    # "user" turn — it should send a placeholder (e.g. "[blocked]") instead.
    messages = [
        {
            "role": "system",
            "content":
            """
            You are SafeChat AI.
            Be friendly, helpful and conversational.
            Keep responses concise.
            """
        }
    ]

    if history:
        # Only keep well-formed entries with allowed roles to avoid
        # poisoning the prompt with arbitrary client-supplied content.
        for turn in history:
            if not isinstance(turn, dict):
                continue
            role = turn.get("role")
            content = turn.get("content")
            if role not in ("user", "assistant"):
                continue
            if not isinstance(content, str):
                continue
            messages.append(
                {"role": role, "content": content}
            )

    messages.append(
        {"role": "user", "content": user_message}
    )

    payload = {
        "model": "deepseek/deepseek-v4-flash",
        "messages": messages
    }

    try:

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]["content"]

    except Exception as e:

        # Log the full exception server-side for debugging, but return a
        # generic, user-friendly fallback so the raw error never reaches
        # the chat UI.
        logger.exception("OpenRouter call failed")

        return (
            "⚠️ I'm having trouble reaching the AI service right now. "
            "Please try again in a moment."
        )


# ==========================================
# ROUTES
# ==========================================

@app.route("/")
def home():

    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    user_message = data["message"]

    # Optional conversation history from the frontend. Each item is
    # {"role": "user" | "assistant", "content": "..."}. Toxic user turns are
    # never echoed back, so the frontend should send placeholder entries
    # (e.g. role="user", content="[blocked]") if it wants to keep the
    # conversation aligned turn-by-turn.
    history = data.get("history", []) or []

    moderation = moderate_message(
        user_message
    )

    # ======================================
    # BLOCK MESSAGE
    # ======================================

    if not moderation["safe"]:

        return jsonify(
            {
                "blocked": True,
                "reasons": moderation["reasons"],
                "reply": gentle_reminder()
            }
        )

    # ======================================
    # SAFE MESSAGE
    # ======================================

    ai_reply = get_ai_reply(
        user_message,
        history=history
    )

    return jsonify(
        {
            "blocked": False,
            "reply": ai_reply
        }
    )


# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":

    # use_reloader=False prevents Flask from spawning a child process that
    # would re-import this module and reload the ~500MB RoBERTa model twice.
    # The model is already loaded at import time above.
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000,
        use_reloader=False
    )