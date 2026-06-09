import pytest
import numpy as np
from src.interview_assistant.audio_buffer import AudioRingBuffer

def test_audio_ring_buffer():
    buffer = AudioRingBuffer(max_seconds=5, sample_rate=16000, channels=2)
    # 1 second of data
    data1 = np.ones((16000, 2), dtype=np.float32)
    buffer.append(data1)
    
    assert buffer.get_length_seconds() == 1.0
    
    # Add 5 more seconds (total 6, should truncate to 5)
    data2 = np.zeros((16000 * 5, 2), dtype=np.float32)
    buffer.append(data2)
    
    assert buffer.get_length_seconds() == 5.0
    
    # Get last 2 seconds
    slice_data = buffer.get_last_seconds(2)
    assert slice_data.shape == (32000, 2)
    assert np.all(slice_data == 0) # Should be all zeros from data2
