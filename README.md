# 🏴‍☠️ OG.sys — The Roast & Rescue Finance AI
### Because your wallet deserves honesty, not sympathy.

## 🚀 Overview
OG.sys (Omniscient Guardian) is an AI-powered financial assistant that helps students manage money through a unique **Roast & Rescue** approach.

Instead of boring tracking apps, OG:
- Roasts your bad spending habits
- Shows the real financial damage
- Gives a strict rescue plan

## 😤 The Problem
Students with budgets like ₹1000–₹3000/month:
- Ignore small expenses
- Hate manual tracking
- Get no real guidance

Result: Overspending → regret → repeat

## 🛟 The Solution
A voice-enabled AI assistant that tracks, roasts, and guides users in real-time.

## ✨ Features
- Roast & Rescue AI (structured responses)
- Voice output (Murf + gTTS)
- Multilingual support
- Cinematic One Piece themed UI
- Budget dashboard
- Interactive chat interface
- Theme engine
- File upload support

## 🏗️ Architecture
Frontend → Flask Backend → Gemini AI → TTS → Audio Response

## ⚙️ Tech Stack
Frontend: HTML, CSS, JS  
Backend: Flask, Gemini AI, Murf AI, gTTS  

## 🔌 API Endpoint
POST /ask-og

Request:
{
  "message": "Spent ₹200 on snacks",
  "voice": "onyx",
  "language": "english"
}

Response:
{
  "response": "Roast + Damage + Plan",
  "audio": "base64-audio"
}

## 🛠️ Setup
pip install flask flask-cors google-generativeai murf gtts python-dotenv  
python app.py  

## 🎮 Usage
1. Login  
2. Enter expense  
3. Get roasted + guided  

## 🏆 Why This Stands Out
- Not just tracking → real guidance  
- Not boring → engaging UI  
- Not passive → interactive AI  

## 🔮 Future Improvements
- Database integration  
- Voice input  
- Smart analytics  
- OCR receipt scanning  

## 💬 Final Thought
This is not just a finance tracker.  
It’s a financial reality check engine.
