import numpy as np

class FlowRoutine:
    def __init__(self, section_transitions, modality_transitions, dwell_ranges, alpha=0.6):
        self.section_transitions = section_transitions      # transitions between session sections
        self.modality_transitions = modality_transitions    # transitions between modalities
        self.dwell_ranges = dwell_ranges                    # (min, max) minutes per state
        self.alpha = alpha                                  # balance between section vs modality influence

        self.sections = list(section_transitions.keys())
        self.modalities = list(modality_transitions.keys())
        self.states = [(s, m) for s in self.sections for m in self.modalities]

    def next_state(self, current, time_left, budget, t_trigger=6, early_penalty=0.1, late_boost=4.0):
        sec, mod = current
        scores = []
        for sec2, mod2 in self.states:
            ps = self.section_transitions[sec].get(sec2, 0)
            pm = self.modality_transitions[mod].get(mod2, 0)
            score = self.alpha * ps + (1 - self.alpha) * pm
            if sec == "cooldown" and sec2 != "cooldown":
                score *= 0.05  # make cooldown “sticky”
            # time-aware: make cooldown unlikely early, likely late
            if sec2 == "cooldown":
                score *= (early_penalty if time_left > t_trigger else late_boost)
            scores.append(score)
        probs = np.array(scores, dtype=float)
        if probs.sum() == 0:
            probs = np.ones_like(probs)
        probs /= probs.sum()
        idx = np.random.choice(len(self.states), p=probs)
        return self.states[idx]

    def dwell_time(self, state):
        if state in self.dwell_ranges:
            lo, hi = self.dwell_ranges[state]
        else:
            lo, hi = (3, 6)   # default
        return int(np.random.randint(lo, hi + 1))

    def build_session(self, start=("warmup","mobility"), budget=30, hard_end=True):
        plan, time_left, state = [], budget, start
        while time_left > 0:
            dur = min(self.dwell_time(state), time_left)
            plan.append((state, dur))
            time_left -= dur
            if hard_end and time_left <= 3 and state[0] != "cooldown":
                state = ("cooldown","stretch")
            else:
                state = self.next_state(state, time_left, budget)
        if plan[-1][0][0] != "cooldown":
            plan.append((("cooldown","stretch"), max(2, budget//10)))
        return plan


def main():

    section_transitions = {
        "warmup":   {"warmup":0.1, "work":0.75,"cooldown":0.15},
        "work":     {"warmup":0.05, "work":0.7, "cooldown":0.25},
        "cooldown": {"warmup":0.02, "work":0.01, "cooldown":0.97}
    }

    modality_transitions = {
        "mobility": {"mobility":0.4, "yoga":0.25, "pilates":0.2, "strength": 0.05, "cardio": 0.08, "stretch":0.02},
        "yoga":     {"mobility":0.25, "yoga":0.4, "pilates":0.2, "strength": 0.05, "cardio": 0.08, "stretch":0.02},
        "pilates":  {"mobility":0.2, "yoga":0.25, "pilates":0.4, "strength": 0.05, "cardio": 0.08, "stretch":0.02},
        "strength": {"mobility":0.08, "yoga":0.2, "pilates":0.2, "strength": 0.4, "cardio": 0.1, "stretch":0.02},
        "cardio":   {"mobility":0.05, "yoga":0.1, "pilates":0.18, "strength": 0.2, "cardio": 0.45, "stretch":0.02},
        "stretch":  {"mobility":0.15, "yoga":0.08, "pilates":0.02, "strength": 0.03, "cardio": 0.02, "stretch":0.7}
    }

    dwell_ranges = {
        ("work","strength"): (4,8),
        ("work","cardio"): (3,6),
        ("mind","breath"): (2,5),
        ("cooldown","stretch"): (3,7)
    }

    routine = FlowRoutine(section_transitions, modality_transitions, dwell_ranges, alpha=0.6)
    session = routine.build_session(start=("warmup","mobility"), budget=30)

    print("Generated session:")
    total = 0
    for i, (st, dur) in enumerate(session, 1):
        total += dur
        print(f"{i:02d}. [{dur}m] {st[0]} | {st[1]}")
    print("Total:", total, "minutes")

if __name__ == "__main__":
    main()