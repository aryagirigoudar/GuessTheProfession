import pygame
from audio import AudioRecorder
import threading
from handle_ai import HandleAI
from constants import ROLE_MAPPING_DICT, PROFESSIONS
import random

class GameThread:
    """
    Main game thread for the Guess the Profession game.
    Initializes the game and runs the main loop.
    """

    def __init__(self, window_size=(800, 800)):
        self.RUN = True
        self.NO_COUNT = 0
        self.chat= list()
        self.pygame = pygame
        pygame.init()
        self.canvas = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Guess the Profession Game")
        self.font = pygame.font.SysFont("Arial", 18)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.audio_recorder = None
        self.handle_ai = HandleAI()
        self.transcript = None
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.approved_questions = 0
        self.rejected_questions = 0
        self.no_of_nose = 0
        self.no_of_yeses = 0
        self.total_score = 0
        self.chat_coordinator = list()
        self.chat_participant = list()
        self.approved_questions = 0
        self.rejected_questions = 0
        self.no_of_nose = 0
        self.no_of_yeses = 0
        self.total_score = 0
        self.level = 1
        self.start_game()
        self.recent_co_message = ""
    
    def start_game(self):
        self.handle_ai.send_to_client_ai(f'Profession: ' + self.get_random_profession())
    
    def get_random_profession(self):
        profession_list = PROFESSIONS.get("level_" + str(self.level))
        random_number = random.randint(1, len(profession_list) - 1)
        return profession_list[random_number]

    def start(self):
        while self.RUN:
            self.canvas.fill(self.BLACK)  # Fill background with black
            self.check_for_events()
            self.check_for_nose()

            y_offset = 50
            line_height = 30
            max_height = 800

            for chat in self.chat:
                who = chat.get('who', "Unkown")
                text = chat.get("text", "")
                color = chat.get('color', self.WHITE)
                message = who + text
                txtsurf = self.font.render(message, True, color)
                self.canvas.blit(txtsurf, (10, y_offset))
                y_offset += line_height

            # If we exceed the max height, remove oldest messages
            while y_offset > max_height and len(self.chat) > 0:
                self.chat.pop(0)
                y_offset -= line_height
            pygame.display.update()  # Update the display

    def check_for_nose(self):
        if self.no_of_nose >= 10:
            print('You have lost the game: Restarting')
            self.restart_game()

    def check_for_events(self):
        """
        Check for pygame events and handle them.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.RUN = False
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_q]:
                    self.RUN = False
                if event.key == pygame.K_SPACE:
                    self.audio_recorder = AudioRecorder()
                    self.audio_recorder_thread = threading.Thread(target=self.audio_recorder.start)
                    self.audio_recorder_thread.start()
                if event.key == pygame.K_RETURN:
                    if self.transcript:
                        self.handle_ai.text = self.transcript
                        text = self.handle_ai.get_user_question()
                        self.print_message(text.get('coordinator', {}), 1)
                        self.print_message(text.get('participant', {}), 2)
                        self.chat.append(dict(text=self.transcript, color=self.RED, who='User: '))
                        self.transcript = None
                        self.chat.append(dict(text=self.get_latest_message(chat_list=self.chat_coordinator), color=self.WHITE, who='Co-or: '))
                        self.chat.append(dict(text=self.get_latest_message(chat_list=self.chat_participant), color=self.GREEN, who='Participant: '))
                        print("Approved: " + str(self.approved_questions))
                        print("No of noes" + str(self.no_of_nose))
        
                if event.key == pygame.K_n:
                    self.transcript = None
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.audio_recorder.stop()
                    self.audio_recorder_thread.join()
                    self.whisper_thread = threading.Thread(target=self.handle_ai.generate_transcript, )
                    self.handle_ai.audio_path = self.audio_recorder.file_name
                    self.whisper_thread.start()
                    self.whisper_thread.join()
                    self.transcript = self.handle_ai.get_transcript()
                    print("is this what you said?", self.transcript)

    def restart_game(self):
        self.approved_questions = 0
        self.rejected_questions = 0
        self.no_of_nose = 0
        self.no_of_yeses = 0
        self.total_score = 0


    def get_latest_message(self, chat_list):
        try:
            chat = chat_list[-1]
            if chat == self.recent_co_message:
                return "Same as previous"
            self.recent_co_message = chat
            return chat
        except Exception as e:
            print("Error: " + str(e))
            return ""
        

    def print_message(self, message_dict, role):
        print("*"*20)
        print(message_dict, role)
        print("*"*20)
        role_name = ROLE_MAPPING_DICT.get(role)
        if not role_name or not message_dict:
            return

        for key, value in message_dict.items():
            if value:
                if key.lower() in ["message", 'answer']:
                    if role == 1:  # Coordinator
                        self.chat_coordinator.append(value)
                    if role == 2:  # Participant
                        self.chat_participant.append(value)
                if key.lower() in ['status', 'state']:
                    if role == 1 and value.lower() in ['approved', 'corrected', 'correct']:
                        self.approved_questions += 1
                    if role == 1 and value.lower() in ['disapproved', 'incorrect', 'no']:
                        self.rejected_questions += 1
                
                if key.lower() in ['answer', 'status', 'state']:
                    if role == 2 and value.lower() in ['yes', 'correct']:
                        self.no_of_yeses += 1
                    if role == 2 and value.lower() in ['no', 'nah', 'nope']:
                        self.no_of_nose += 1

                print(f"{role_name} {key.capitalize()}: {value}")

