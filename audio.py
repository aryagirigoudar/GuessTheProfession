import pyaudio
import wave
from constants import CHUNK, CHANNELS, RATE, WAVE_OUTPUT_FILENAME
from datetime import datetime
from logger import logger

class AudioRecorder:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.RUN = None
        self.file_name = WAVE_OUTPUT_FILENAME
        self.stream = self.p.open(format=pyaudio.paInt16,
                             channels=CHANNELS,
                             rate=RATE,
                             input=True,
                             frames_per_buffer=CHUNK)

    def record_audio(self):
        print("Recording")
        logger.info("Recording...")
        frames = []

        while self.RUN:
            data = self.stream.read(CHUNK)
            frames.append(data)

        logger.info("Finished recording.")
        print("Finished recording.")

        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        self.file_name = self.file_name.format("user", datetime.now().strftime("%d-%m-%Y_%H:%M:%S"))
        with wave.open(self.file_name, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
        
    def stop(self):
        logger.info("Audio recording stopped.")
        self.RUN = False
    
    def start(self):
        logger.info("Starting audio recording...")
        self.RUN = True
        self.record_audio()