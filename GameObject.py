class GameObject:
    """
    A game object
    """
    def __init__(self, pos, speed, movable=False):
        self.pos = pos
        self.speed = speed
        self.movable = movable
