import threading
import time
import random

N = 5
M_POLL_INTERVAL = 0.5  # seconds (your M)
N_EXTRA_EAT = 4.0      # seconds (your N - extra eating time after seeing a raised chopstick)

chopsticks = [threading.Lock() for _ in range(N)]
eating = [False] * N
raising = [False] * N

print_lock = threading.Lock()

def log(msg):
    with print_lock:
        current_time = time.strftime("%M:%S", time.localtime())
        print(f"[{current_time}] {msg}")

class Philosopher(threading.Thread):
    def __init__(self, i):
        super().__init__(name=f"Philosopher-{i}")
        self.i = i
        self.left_c = i                    # left chopstick  = i
        self.right_c = (i + 1) % N         # right chopstick = i+1
        self.left_neighbor = (i - 1) % N   # the neighbor whose raised chopstick I check

    def think(self):
        think_time = random.uniform(3, 8)
        log(f"P{self.i} is thinking for {think_time:.1f}s")
        time.sleep(think_time)

    def run(self):
        while True:
            self.think()

            log(f"P{self.i} is now hungry")

            # Hungry phase - wait until we successfully start eating
            while not eating[self.i]:
                time.sleep(M_POLL_INTERVAL)

                # If we have our left chopstick available and aren't raising it yet → raise it
                if not raising[self.i] and not chopsticks[self.left_c].locked():
                    raising[self.i] = True
                    log(f"P{self.i} raises left chopstick {self.left_c}")

                # If we are raising AND our right chopstick just became available → grab both and eat
                if raising[self.i] and not chopsticks[self.right_c].locked():
                    chopsticks[self.left_c].acquire()   # pick left first
                    time.sleep(0.01)                    # tiny delay to simulate sequential pickup
                    chopsticks[self.right_c].acquire()  # then right
                    raising[self.i] = False
                    eating[self.i] = True
                    log(f"P{self.i} ███████ starts eating (holds {self.left_c} & {self.right_c})")

            # Eating phase
            release_at = None
            while eating[self.i]:
                time.sleep(M_POLL_INTERVAL)

                # Check if left neighbor is raising their chopstick
                if raising[self.left_neighbor]:
                    if release_at is None:  # first time we see the signal
                        release_at = time.time() + N_EXTRA_EAT
                        log(f"P{self.i} sees P{self.left_neighbor} raising → will release in {N_EXTRA_EAT}s")

                # Time to release?
                if release_at and time.time() >= release_at:
                    chopsticks[self.left_c].release()
                    chopsticks[self.right_c].release()
                    log(f"P{self.i} ███████ finished eating and released {self.left_c} (to left) & {self.right_c} (to right)")
                    eating[self.i] = False
                    break


if __name__ == "__main__":
    philosophers = [Philosopher(i) for i in range(N)]
    for p in philosophers:
        p.start()

    # Give threads a moment to start
    time.sleep(2)

    # === Your required initialization ===
    # Start with two non-adjacent philosophers eating (P0 and P2)
    initial_eaters = [0, 2]
    for i in initial_eaters:
        left = i
        right = (i + 1) % N
        chopsticks[left].acquire()
        chopsticks[right].acquire()
        eating[i] = True
        log(f">>> INITIALIZATION: P{i} starts eating (holds {left} & {right})")

    log(">>> Simulation running - watch the eating pair rotate counter-clockwise forever!")
    log("    Current eaters: P0 & P2  (free chopstick = 4)")

    # Let it run forever (Ctrl+C to stop)
    try:
        while True:
            time.sleep(10)
            # Optional periodic status
            current_eaters = [i for i, e in enumerate(eating) if e]
            log(f"    === Current eaters: {current_eaters} ===")
    except KeyboardInterrupt:
        log("\nSimulation stopped by user")
