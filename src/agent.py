class Agent:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def position(self):
        """
        Return the current position of the agent as an (x, y) tuple.
        """
        return self.x, self.y