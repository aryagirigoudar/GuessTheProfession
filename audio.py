import pyaudio
import wave
from constants import CHUNK, CHANNELS, RATE, RECORD_SECONDS, WAVE_OUTPUT_FILENAME

class AudioRecorder:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.RUN = None

    def record_audio(self):
        stream = self.p.open(format=pyaudio.paInt16,
                             channels=CHANNELS,
                             rate=RATE,
                             input=True,
                             frames_per_buffer=CHUNK)

        print("Recording...")
        frames = []

        while self.RUN:
            data = stream.read(CHUNK)
            frames.append(data)

        print("Finished recording.")

        stream.stop_stream()
        stream.close()
        self.p.terminate()

        with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))