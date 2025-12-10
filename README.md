# Chopstick Chase
A novel, fair, and maximally concurrent solution to the Dining Philosophers problem (n=5 or any odd n)

**Author:** Douglas Dohmeyer
**License:** MIT

### The Idea – in one sentence
Two non-adjacent philosophers start eating; a single “free” chopstick circulates counter-clockwise forever, forcing the pair of eaters to chase it around the table in strict round-robin order.

### Why it’s different (and better for many real systems)

| Property                       | Classic solutions (hierarchy, Chandy/Misra, etc.) | Chopstick Chase |
|--------------------------------|---------------------------------------------------|-----------------|
| Guaranteed concurrency        | Usually 1, sometimes 2                            | Always ⌊n/2⌋ (2 for n=5) |
| Strict round-robin fairness    | Not guaranteed                                    | Yes – deterministic cycle |
| Bounded waiting time           | Sometimes unbounded                               | Yes – ≤ 2.5 × eating time |
| Minimum eating quantum        | No                                                | Yes (the N extra units after seeing a raised chopstick) |
| State per philosopher          | Often needs IDs, flags, queues                    | Identical code + one boolean “raising” |
| Initialisation requirement     | Works from any state                              | Needs correct initial pair (trade-off for the above wins) |

### Live Demo (Python 3)

```bash
git clone https://github.com/Dorgenbjorn/chopstick-chase.git
cd chopstick-chase
python3 chopstick_chase.py
```

You will see logs like:

```
>>> INITIALIZATION: P0 starts eating (holds 0 & 1)
>>> INITIALIZATION: P2 starts eating (holds 2 & 3)
P4 raises left chopstick 4
P0 sees P4 raising → will release in 4.0s
P0 finished eating and released 0 (to left) & 1 (to right)
P4 starts eating (holds 4 & 0)
...
```

The eating pair forever rotates:
(0,2) → (2,4) → (4,1) → (1,3) → (3,0) → (0,2) → …

### When to use it

- Fixed odd number of processes (especially 5)
- You control initialisation
- You need provable fairness + maximum concurrency + bounded latency
- Polled/time-triggered systems (the periodic check is essentially free)

### Reference implementation

- `chopstick_chase.py` – 120-line fully working simulation with clear comments
- Uses only `threading.Lock` and boolean flags – no semaphores, no monitors, no central arbiter

### Citation (if you use it in a paper or blog)

```bibtex
@misc{dohmeyer2025chopstick,
  author = {Douglas Dohmeyer},
  title = {Chopstick Chase: A Rotating-Pair Solution for Odd-Sized Dining Philosophers},
  year = {2025},
  url = {https://github.com/Dorgenbjorn/chopstick-chase}
}
```

Enjoy the chase!
