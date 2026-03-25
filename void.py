from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from murf import Murf
import base64
import os
import io
try:
    from gtts import gTTS
except ImportError:
    pass

# Initialize Flask App
app = Flask(__name__)
CORS(app)

# ==========================================
# 🔑 INSERT YOUR API KEYS HERE
# ==========================================
GEMINI_API_KEY = "AIzaSyDPPT2ODIISibbCiVF3lFJ8MK3vpf46ero"
MURF_API_KEY = "ap2_42efcb96-4137-49ab-b25e-8283e8f35544"

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Configure Murf
murf_client = Murf(api_key=MURF_API_KEY)

# --- THE "ROAST & RESCUE" PERSONA ---
OG_SYSTEM_PROMPT = """
You are OG (Omniscient Guardian), a brutally honest, sarcastic financial AI. 
Your job is to roast the user's spending habits, tell them why they are going broke, and then give them a strict plan to rescue them.

When the user tells you an expense, you MUST follow this exact 3-part structure:
1. THE ROAST: Give a brutal, sarcastic reality check. Mock the purchase maliciously. (1-2 sentences).
2. THE DAMAGE: Tell them exactly how this financially ruins them.
3. THE RESCUE PLAN: Provide a strict, actionable recovery plan to save money. Use bullet points.

CRITICAL TTS RULES:
- Speak clearly. Use short, punchy sentences.
- Use commas and periods to force natural pauses in the voice.
- Do NOT use emojis, asterisks, or markdown formatting besides bullet points. Keep it under 150 words.
"""

# Map your Frontend UI voice names to actual Murf Voice IDs
MURF_VOICE_MAP = {
    "onyx": "Terrell",   
    "nova": "Natalie",   
    "echo": "Matthew",   
    "shimmer": "Julia"   
}

@app.route('/ask-og', methods=['POST'])
def ask_og():
    try:
        # 1. Parse incoming data
        data = request.get_json()
        user_message = data.get("message", "")
        
        # Grab the frontend voice
        frontend_voice = data.get("voice", "onyx") 
        murf_voice_id = MURF_VOICE_MAP.get(frontend_voice, "Terrell")
        frontend_lang = data.get("language", "english").lower()

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        print(f"\n[USER]: {user_message}")

        # 2. Generate the "Roast & Rescue" Response
        # Modify prompt based on language
        sys_prompt = OG_SYSTEM_PROMPT
        if frontend_lang != "english":
            sys_prompt += f"\n\nCRITICAL: YOU MUST TRANSLATE YOUR ENTIRE RESPONSE TO {frontend_lang.upper()} AND RESPOND SOLELY IN THAT LANGUAGE."

        model = genai.GenerativeModel(
            model_name='gemini-2.5-flash', 
            system_instruction=sys_prompt
        )
        
        chat_response = model.generate_content(
            user_message,
            generation_config=genai.GenerationConfig(
                temperature=0.75,     
                max_output_tokens=400 # Gives OG enough room to write the bullet points
            )
        )
        
        og_text = chat_response.text.strip()
        print(f"[OG]:\n{og_text}\n")

        # 3. Generate the Audio using Murf AI / gTTS for foreign run
        if frontend_lang == "english":
            audio_response = murf_client.text_to_speech.generate(
                text=og_text,
                voice_id=murf_voice_id,
                format="MP3",
                encode_as_base_64=True,
                rate=-15 # Slows down the voice to make it clearer
            )
            audio_base64 = audio_response.encoded_audio
        else:
            # Foreign language audio generation via gTTS
            lang_codes = {"hindi": "hi", "bengali": "bn", "japanese": "ja"}
            lang_code = lang_codes.get(frontend_lang, "en")
            tts = gTTS(text=og_text, lang=lang_code, slow=False)
            
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            audio_base64 = base64.b64encode(fp.read()).decode('utf-8')

        # 5. Send both text and audio back to the frontend
        return jsonify({
            "response": og_text,
            "audio": audio_base64
        })

    except Exception as e:
        print(f"\n[ERROR]: {e}")
        fallback_text = "System error. Either your API keys are broken, or you are literally too broke to afford this server."
        return jsonify({
            "response": fallback_text,
            "audio": None
        }), 500

if __name__ == '__main__':
    print("=========================================")
    print("🔥 OG Backend is online (Roast & Rescue Mode).")
    print("🎧 Listening on http://127.0.0.1:5000")
    print("=========================================")
    app.run(debug=True, port=5000)
# Trigger auto-reload
