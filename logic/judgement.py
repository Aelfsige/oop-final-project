from math import isclose


class JudgementSystem:
    def __init__(self, perfect=0.050, good=0.100):
        if not 0 <= perfect <= good:
            raise ValueError("Timing windows must satisfy 0 <= perfect <= good.")
        self.perfect = perfect
        self.good = good

    def judge(self, press_time, note_time):
        delta = abs(press_time - note_time)
        if delta <= self.perfect or isclose(delta, self.perfect, rel_tol=0, abs_tol=1e-12):
            return "perfect"
        if delta <= self.good or isclose(delta, self.good, rel_tol=0, abs_tol=1e-12):
            return "good"
        return "miss"
