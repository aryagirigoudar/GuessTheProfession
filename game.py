import pygame
from audio import AudioRecorder
import threading
from handle_ai import HandleAI
from constants import ROLE_MAPPING_DICT, PROFESSIONS
import random
from logger import logger

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
        logger.info('Profession is: ' + self.get_random_profession())
    
    def get_random_profession(self):
        profession_list = PROFESSIONS.get("level_" + str(self.level))
        random_number = random.randint(1, len(profession_list) - 1)
        return profession_list[random_number]

    def start(self):
        while self.RUN:
            self.canvas.fill(self.BLACK)
            self.check_for_events()
            self.check_for_nose()
            self.display_chat()
            self.check_for_win_statement()
            pygame.display.update()

    def check_for_win_statement(self):
        pass

    def check_for_nose(self):
        if self.no_of_nose >= 10:
            print('You have lost the game: Restarting')
            logger.info('You have lost the game: Restarting')
            self.restart_game()

    def check_for_events(self):
        """
        Check for pygame events and handle them.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.RUN = False
            if event.type == pygame.KEYDOWN:
               self.handle_key_down(event)
            if event.type == pygame.KEYUP:
                self.handle_key_up(event)

    def restart_game(self):
        self.approved_questions = 0
        self.rejected_questions = 0
        self.no_of_nose = 0
        self.no_of_yeses = 0
        self.total_score = 0
    
    def handle_key_up(self, event):
        if event.key == pygame.K_SPACE:
            self.audio_recorder.stop()
            self.audio_recorder_thread.join()
            self.whisper_thread = threading.Thread(target=self.handle_ai.generate_transcript, )
            self.handle_ai.audio_path = self.audio_recorder.file_name
            self.whisper_thread.start()
            self.whisper_thread.join()
            self.transcript = self.handle_ai.get_transcript()
            print("User said: ", self.transcript)
            logger.info("User said: " + self.transcript)
    
    def handle_key_down(self, event):
        if event.key in [pygame.K_ESCAPE, pygame.K_q]:
            logger.info("Quitting")
            self.RUN = False
        if event.key == pygame.K_SPACE:
            self.audio_recorder = AudioRecorder()
            self.audio_recorder_thread = threading.Thread(target=self.audio_recorder.start)
            self.audio_recorder_thread.start()
        if event.key == pygame.K_RETURN:
            self.submit_answer()

        if event.key == pygame.K_n:
            self.transcript = None
    
    def submit_answer(self):
        if not self.transcript:
            return
        self.handle_ai.text = self.transcript
        text = self.handle_ai.get_user_question()
        self.print_message(text.get('coordinator', {}), 1)
        self.print_message(text.get('participant', {}), 2)
        self.chat.append(dict(text=self.transcript, color=self.RED, who='User: '))
        self.transcript = None
        co_ordinator_message = self.get_latest_message(chat_list=self.chat_coordinator)
        participant_messgae = self.get_latest_message(chat_list=self.chat_participant)
        if co_ordinator_message.replace('!', '').lower() in ['you\'ve guessed it'] and participant_messgae == 'yes':
            logger.info("You have won the game. Restarted")
            print("You have won the game. Restarted")
            self.restart_game()
        self.chat.append(dict(text=co_ordinator_message, color=self.WHITE, who='Co-or: '))
        self.chat.append(dict(text=participant_messgae, color=self.GREEN, who='Participant: '))
        logger.info("Approved: " + str(self.approved_questions))
        logger.info("No of noes" + str(self.no_of_nose))

    def display_chat(self):
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


    def get_latest_message(self, chat_list):
        try:
            chat = chat_list[-1]
            if chat == self.recent_co_message:
                return "Same as previous"
            logger.info("Chat: " + chat)
            self.recent_co_message = chat
            return chat
        except Exception as e:
            print("Error: " + str(e))
            return ""
        

    def print_message(self, message_dict, role):
        role_name = ROLE_MAPPING_DICT.get(role)
        logger.info('Print_message: ' + str(message_dict) + "role: " + str(role))
        if not role_name or not message_dict:
            return

        for key, value in message_dict.items():
            if not value:
                continue

            key_l = key.lower()

            if key_l in ["message", "answer"]:
                if role == 1:
                    self.chat_coordinator.append(value)
                elif role == 2:
                    self.chat_participant.append(value)

            if key_l in ["status", "state"]:
                if role == 1:
                    if value.lower() in ["approved", "corrected", "correct"]:
                        self.approved_questions += 1
                    elif value.lower() in ["disapproved", "incorrect", "no"]:
                        self.rejected_questions += 1

            if key_l in ["answer", "status", "state"]:
                if role == 2:
                    ans = value.lower()
                    if ans in ["yes", "correct"]:
                        self.no_of_yeses += 1
                    elif ans in ["no", "nah", "nope"]:
                        self.no_of_nose += 1

            logger.info(f"{role_name} {key.capitalize()}: {value}")
