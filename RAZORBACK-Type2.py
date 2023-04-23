#Version with a quantity of keystrokes given to operate said program continously until reaching the maximum amount.

import time
import random

def random_time(delay, seed):
    random.seed(seed)
    return delay + random.uniform(-0.5, 0.5)

def simulate_keystrokes(keystrokes, delays, seed, duration=None, num_keystrokes=None):
    assert (duration is not None) != (num_keystrokes is not None), "Specify either duration or num_keystrokes"

    start_time = time.time()
    keystroke_count = 0

    while True:
        for i in range(len(keystrokes)):
            keystroke_count += 1
            print(f"Keystroke {keystroke_count}: {keystrokes[i]}")

            delay = delays[i]
            if seed is not None:
                delay = random_time(delay, seed)

            time.sleep(delay)

            if duration is not None and time.time() - start_time >= duration:
                print("Program finished due to duration limit.")
                return

            if num_keystrokes is not None and keystroke_count >= num_keystrokes:
                print("Program finished due to keystroke limit.")
                return
