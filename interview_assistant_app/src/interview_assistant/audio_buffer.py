import numpy as np

class AudioRingBuffer:
    def __init__(self, max_seconds: int = 120, sample_rate: int = 16000, channels: int = 2):
        self.max_seconds = max_seconds
        self.sample_rate = sample_rate
        self.channels = channels
        self.max_samples = max_seconds * sample_rate
        self.buffer = np.zeros((0, channels), dtype=np.float32)

    def append(self, data: np.ndarray):
        if data.shape[1] != self.channels:
            raise ValueError(f"Expected {self.channels} channels, got {data.shape[1]}")
        
        self.buffer = np.vstack((self.buffer, data))
        
        if len(self.buffer) > self.max_samples:
            self.buffer = self.buffer[-self.max_samples:]

    def get_length_seconds(self) -> float:
        return len(self.buffer) / self.sample_rate

    def get_last_seconds(self, seconds: float) -> np.ndarray:
        samples_needed = int(seconds * self.sample_rate)
        return self.buffer[-samples_needed:]

    def clear(self):
        self.buffer = np.zeros((0, self.channels), dtype=np.float32)
