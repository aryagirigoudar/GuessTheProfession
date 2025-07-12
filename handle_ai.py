from google import genai
from google.genai import types
from constants import API_KEY, SYSTEM_INSTRUCTIONS, ROLE_MAPPING_DICT, PROFESSIONS
import whisper
import json
import pydash
import traceback

class HandleAI:
    def __init__(self):
        self.whisper_model = whisper.load_model("base")
        self.audio_path = None
        self.text = None
        self.client = genai.Client(api_key=API_KEY)
        self.chat = self.client.chats.create(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTIONS)
        )
    
    def send_to_client_ai(self, text):
        return self.chat.send_message(text)

    def generate_transcript(self):
        result = self.whisper_model.transcribe(self.audio_path)
        self.text = result["text"]
     
    def get_transcript(self):
        return self.text

    def parse_response(self, response ):
        if not response:
            print("Empty response.")
            return {}

        response = response if isinstance(response, dict) else response.to_json_dict()
        candidates = response.get('candidates', [])
        if not candidates:
            print("No candidates found.")
            return {}
        try:
            for candidate in candidates:
                parts = pydash.get(candidate, 'content.parts', [])
                if not parts:
                    continue

                for part in parts:
                    text = part.get('text', '').strip()
                    if not text:
                        continue

                    clean_text = text.replace('```json', '').replace('```', '').strip()
                    parsed_json = json.loads(clean_text)
                    both = parsed_json.get('guess_the_profession_game', {})
                    return both
        except Exception as e:
            traceback.print_exc()
            print(f"Error parsing response: {e}")
            return None
        
    def get_user_question(self):

        response = self.chat.send_message(self.text)
        return self.parse_response(response)

