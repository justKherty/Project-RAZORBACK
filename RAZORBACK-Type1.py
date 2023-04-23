import time
import random
import hashlib

keystrokes = input("Enter keystrokes (comma-separated): ").strip().split(",")
delays = input("Enter delays (comma-separated): ").strip().split(",")

seed_str = str(time.time()) + ''.join(keystrokes) + ''.join(delays)
seed_bytes = seed_str.encode('utf-8')
seed_hash = hashlib.sha256(seed_bytes).digest()
seed = int.from_bytes(seed_hash, byteorder='big')

def randomize_time_delay(delay):
    delay *= random.uniform(0.9, 1.1)
    return delay

for keystroke, delay in zip(keystrokes, delays):
    delay = float(delay)
    delay = randomize_time_delay(delay)
    time.sleep(delay)
