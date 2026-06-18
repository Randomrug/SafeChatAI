# 🛡️ SafeChat AI

SafeChat AI is an intelligent content moderation and conversational AI system designed to create safer and healthier online interactions. Unlike traditional keyword-based filters, SafeChat AI understands the context, intent, and semantic meaning behind a message before making moderation decisions.

The project is powered by a fine-tuned RoBERTa model trained on the Jigsaw Toxic Comment Classification Dataset, a large-scale collection of real-world online comments annotated across multiple toxicity categories. During experimentation, traditional machine learning and transformer-based approaches were explored, with RoBERTa emerging as the final model due to its superior contextual understanding and moderation performance.

Every user message is analyzed in real time and classified into multiple toxicity categories:

* Toxic
* Severe Toxic
* Obscene
* Threat
* Insult
* Identity Hate

Messages identified as harmful are intercepted before reaching the chatbot, while safe messages are forwarded to the language model for natural conversation. This moderation-first architecture helps reduce harmful interactions while preserving meaningful discussions.

---

## 📊 Dataset Overview

The moderation engine was trained using the **Jigsaw Toxic Comment Classification Dataset**, one of the most widely used benchmarks for online toxicity detection.

### Dataset Characteristics

* Real user-generated comments
* Multi-label classification problem
* Six toxicity categories
* Highly imbalanced real-world distribution
* Rich linguistic diversity
* Suitable for content moderation and online safety applications

The dataset enables the model to learn subtle toxic patterns, contextual abuse, identity-based attacks, threats, insults, and offensive language beyond simple keyword matching.

---

## ✨ Features

* 🧠 Context-aware toxicity detection using RoBERTa
* ⚡ Real-time moderation before AI response generation
* 🚫 Automatic blocking of harmful content
* 📊 Multi-label toxicity classification
* 💬 Conversational AI integration
* 🎨 Interactive chat interface
* 🔒 Safe and moderation-first architecture
* 📈 Confidence-based toxicity scoring
* 🛠️ Configurable moderation thresholds
* 🚀 Fast inference with transformer-based NLP

---

## 🏗️ System Workflow

```text
User Message
      ↓
RoBERTa Moderation Engine
      ↓

  Safe? ───── No ───► Block Message
     │                 ↓
    Yes           Moderation Feedback
     │
     ↓
 Conversational AI
     ↓
 AI Response
     ↓
 Display to User
```

---

## 🛠️ Technologies Used

### Backend

* Python
* Flask

### Deep Learning & NLP

* PyTorch
* Hugging Face Transformers
* RoBERTa
* Tokenizers

### Frontend

* HTML
* CSS
* JavaScript

### AI Integration

* OpenRouter API
* DeepSeek LLM

### Utilities

* NumPy
* Pandas
* Requests
* python-dotenv

---

## 📦 Required Libraries

```bash
pip install flask
pip install torch
pip install transformers
pip install tokenizers
pip install pandas
pip install numpy
pip install requests
pip install python-dotenv
```

Or simply:

```bash
pip install -r requirements.txt
```

---

## 🎯 Why SafeChat AI?

Many moderation systems rely heavily on keyword matching. While effective in simple cases, they often struggle to understand context, intent, sarcasm, gaming slang, technical discussions, educational content, and everyday expressions.

SafeChat AI leverages RoBERTa's contextual language understanding to analyze what a user actually means rather than reacting to individual words.

### ❌ Traditional Keyword-Based Moderation

Consider the word **"kill"**:

🔴 "I will kill you."

🔴 "I'm going to kill you."

🟢 "Bro, you're killing the game!"

🟢 "You're killing the vibe right now."

🟢 "That exam absolutely killed me."

🟢 "This memory leak might kill the server."

A keyword-based system may flag every sentence simply because it contains the word *kill*.

### ✅ SafeChat AI

Understands the difference between:

* Genuine threats
* Friendly slang
* Compliments
* Technical discussions
* Figurative expressions

---

Consider the word **"hate"**:

🔴 "I hate you."

🔴 "I hate people like you."

🟢 "I do not hate you."

🟢 "The dataset contains hate speech examples."

🟢 "We're studying hate speech detection using NLP."

A basic keyword filter may incorrectly flag every sentence containing the word *hate*.

SafeChat AI analyzes the complete context before making a moderation decision.

---

Consider identity-related discussions:

🔴 "People from that community are worthless."

🔴 "They should not exist."

🟢 "The model detects identity hate speech."

🟢 "We are analyzing hate speech targeting different communities."

The same sensitive terms can appear in both harmful and educational contexts. SafeChat AI learns to distinguish between them.

---

Gaming and internet slang create another challenge:

🟢 "Bro absolutely destroyed that match."

🟢 "That player murdered the competition."

🟢 "We got annihilated in ranked."

🔴 "I'm going to hurt you."

Many moderation systems struggle with these expressions because they appear aggressive despite being harmless.

SafeChat AI uses contextual understanding to differentiate genuine threats from common online language.

---

### 🧠 The Difference

**Traditional Filters**

Keyword ➜ Flag Message

**SafeChat AI**

Sentence ➜ Context ➜ Intent ➜ Moderation Decision

Instead of asking:

> "Does this sentence contain a bad word?"

SafeChat AI asks:

> "What does this sentence actually mean?"

This results in fewer false positives, better moderation accuracy, and safer, more natural online conversations.

---

## 🌟 Future Improvements

* Real-time multilingual moderation
* Adaptive toxicity thresholds
* Explainable AI moderation reports
* User reputation scoring
* Fine-tuning on domain-specific communities
* Deployment as a scalable moderation API

---

⭐ If you found this project interesting, consider giving it a star!

Heyyyy guyssss 👋

Got questions, crazy ideas, collaboration plans, bug reports, feature requests, or just want to geek out about NLP, Transformers, and AI Safety?

📧 **[rithikaarulmozhi21@gmail.com](mailto:rithikaarulmozhi21@gmail.com)**

Let's build safer AI systems, smarter conversations, and cooler technology together 🚀✨

**Happy coding and stay awesome! 💙**

— **Randomrug** 🛸🌙
