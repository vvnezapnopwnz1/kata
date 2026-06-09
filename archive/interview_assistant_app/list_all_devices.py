import pyaudio

p = pyaudio.PyAudio()
print("All Audio Devices (Including 0 channels):")
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print(f"Index {i}: {info['name']} (In: {info['maxInputChannels']}, Out: {info['maxOutputChannels']})")
p.terminate()
