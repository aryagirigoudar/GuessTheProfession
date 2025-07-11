# this file will be main file for the game and main thread 
from game import GameThread
import signal
import sys

class HandleObjectsWithCleanUp:
    def __init__(self):
        self.game_obj = GameThread()

    def stop(self):
        print("\n[INFO] Graceful shutdown initiated.")
        # ✅ Your cleanup logic here
        print("Doing cleanup work...")
        self.game_obj.pygame.quit()

    def handle_ctrl_c(self, signum, frame):
        print("\n[Signal] Caught Ctrl+C (SIGINT)")
        self.stop()
        sys.exit(0)

    def handle_ctrl_z(self, signum, frame):
        print("\n[Signal] Caught Ctrl+Z (SIGTSTP)")
        self.stop()
        sys.exit(0)

    def run(self):
        print("Running... Press Ctrl+C or Ctrl+Z to stop.")
        self.game_obj.start()

if __name__ == "__main__":
    process = HandleObjectsWithCleanUp()
    signal.signal(signal.SIGINT, process.handle_ctrl_c)
    signal.signal(signal.SIGTSTP, process.handle_ctrl_z)
    process.run()