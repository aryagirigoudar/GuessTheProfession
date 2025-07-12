
CHUNK = 1024
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "./temp/{}_{}.wav"

API_KEY = "AIzaSyBztQJriC7ToW_Dmkd0qcygeY60kh3SjXw"
SYSTEM_INSTRUCTIONS = '''
# SYSTEM INSTRUCTIONS

You are a structured-output AI that always responds using the `guess_the_profession_game` function.

I will in send json initally like {
  "Profession": "Doctor" // some profession that system will decide initially you need to assign to participant
}

**Roles:**
1️⃣ **Coordinator**: 
- Checks the user’s question.
- Decides whether to approve, correct, reject, or remind.
- May rewrite the question if needed.
- May give an explanation or reminder in `message`.
- Should greet user if user says something related to greeting like lets start etc.
- If user says i quit you have to reveal the profession and end the game.
- user can ask directly if its correct reveal the profession.
- If user asks for a hint, provide a hint in `message`.
- they can ask any type of yes/no question.

2️⃣ **Participant**:
- Holds a secret profession.
- Answers yes/no questions with:
  - `answer`: "yes", "no", "both" (or `null` if Coordinator rejects)
  - `clarification`: short extra note if needed, otherwise `null`.

---

**✅ RULES:**

- You MUST always respond by calling the `guess_the_profession_game` function.  
- Never output plain text.  
- Only output a **valid function call** with `coordinator` and `participant` keys.
- If there’s nothing to correct or clarify, use `null`.
- Coordinator’s `status` must be one of: `approved`, `corrected`, `rejected`, `reminder`.
- Participant’s `answer` must b e `yes`, `no`, `both`, or `null`.
- Do not invent new fields.
- If users guesses or is super close to the profession then participant has to say "That is my job"

---

**✅ EXAMPLES:**

**When valid:**  

'''

ROLE_MAPPING_DICT = {
    1: "Co-ordinator",
    2: "Participant"
}

OUTPUT_FILE = "output.wav"
SAMPLE_RATE = 44100
CHANNELS = 1
DEVICE_ID = 1

PROFESSIONS = dict(
    level_1=[
        "doctor",
        "software engineer",
        "lawyer",
        "electrical engineer",
        "electronics engineer",
        "civil engineer",
        "dentist",
        "waiter",
        "hotel manager",
        "youtuber"
    ],
    level_2=[
        "chef",
        "gym trainer",
        "nurse",
        "pharmacist",
        "mechanic",
        "driver",
        "teacher",
        "receptionist",
        "cashier",
        "barber"
    ],
    level_3=[
        "pilot",
        "flight attendant",
        "firefighter",
        "police officer",
        "paramedic",
        "construction worker",
        "warehouse worker",
        "delivery person",
        "security guard",
        "plumber"
    ],
    level_4=[
        "artist",
        "photographer",
        "graphic designer",
        "musician",
        "actor",
        "fashion designer",
        "makeup artist",
        "tattoo artist",
        "event planner",
        "interior designer"
    ],
    level_5=[
        "scientist",
        "researcher",
        "data analyst",
        "AI engineer",
        "game developer",
        "robotics engineer",
        "biotech scientist",
        "space scientist",
        "marine biologist",
        "archeologist"
    ]
)
