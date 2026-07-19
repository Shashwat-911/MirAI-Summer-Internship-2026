# 📖 AI Multi-Modal Visual Novel

An interactive **AI-powered Visual Novel** built with **Streamlit**, **Google Gemini**, **Pollinations AI**, and **Microsoft Edge TTS**. Every story is generated dynamically based on the selected genre and art style, allowing users to shape the narrative through AI-generated choices.

---

## ✨ Features

- 🎭 Multiple story genres and art styles
- 🤖 AI-generated interactive storytelling with Google Gemini
- 📦 Structured JSON parsing for story flow
- 🖼️ AI-generated illustrations using Pollinations AI
- 🔊 AI narration powered by Microsoft Edge TTS
- 🎮 Dynamic choices that influence the story
- 💾 Stateful conversations with Streamlit Session State
- 🛡️ Graceful error handling using `try...except`

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Google Gemini API
- Pollinations AI
- Microsoft Edge TTS
- JSON
- Requests
- Asyncio

---

## 🚀 Getting Started

### Clone the repository

```bash
git clone <repository-url>
cd Assignment-5
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Create a `.env` file

```env
GEMINI_API_KEY=your_api_key_here
```

### Run the application

```bash
streamlit run assignment5.py
```

---

## 🎥 Demo

A short demonstration of the application is available in the **`demo/`** folder.

---

## 📂 Project Structure

```text
Assignment-5/
│
├── assignment5.py      # Main Streamlit application
├── README.md
├── requirements.txt    
└── demo/               # Project demonstration video
```

---

## 📚 About the Project

This project was developed as the **Capstone Mini Project (Assignment 5)** for the **MirAI School of Technology – Virtual Summer Internship 2026**.

The application demonstrates:

- Structured JSON parsing
- Dynamic UI generation
- Multi-modal AI (Text + Image + Audio)
- Stateful Streamlit architecture
- Graceful error handling
