class GameObject:
    """
    A game object
    """

    def __init__(self, pos, speed, movable=False, oscillator=None):
        self.pos = pos
        self.speed = speed
        self.movable = movable
        if oscillator is None:
            oscillator = [None, None]
        self.oscillator = oscillator
        self.oscillation_step = 0

    def lambda_eval(self, formula, step):
        return formula(step)

    def oscillate(self):
        if self.oscillator[0] is not None:
            self.speed.x = self.lambda_eval(self.oscillator[0], self.oscillation_step)
            self.oscillation_step += 1
        if self.oscillator[1] is not None:
            self.speed.y = self.lambda_eval(self.oscillator[1], self.oscillation_step)
            self.oscillation_step += 1
