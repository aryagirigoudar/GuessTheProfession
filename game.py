import pygame
from audio import AudioRecorder
import threading
from handle_ai import HandleAI

class GameThread:
    """
    Main game thread for the Guess the Profession game.
    Initializes the game and runs the main loop.
    """

    def __init__(self, window_size=(800, 800)):
        self.RUN = True
        self.NO_COUNT = 0
        self.chat_user = list()
        self.chat_participant = list()
        self.chat_coordinator = list()
        self.pygame = pygame
        pygame.init()
        self.canvas = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Guess the Profession Game")
        self.font = pygame.font.SysFont("Arial", 28)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.audio_recorder = None
        self.handle_ai = HandleAI()
        self.transcript = None
    
    def start(self):
        while self.RUN:
            self.canvas.fill(self.black)  # Fill background with black
            self.check_for_events()

            y_offset = 50
            line_height = 30
            max_height = 800

            for index, message in enumerate(self.chat_user):
                txtsurf = self.font.render(message, True, self.white)
                self.canvas.blit(txtsurf, (10, y_offset))
                y_offset += line_height

            # If we exceed the max height, remove oldest messages
            while y_offset > max_height and len(self.chat_user) > 0:
                self.chat_user.pop(0)
                y_offset -= line_height
            pygame.display.update()  # Update the display


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
                        self.chat_user.append(self.transcript)
                        self.handle_ai.text = self.transcript
                        self.handle_ai.get_user_question()
                        self.transcript = None
                        print(self.handle_ai.chat_coordinator)
                        print(self.handle_ai.chat_participant)
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

