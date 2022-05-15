from contextlib import nullcontext
from pydealer import Stack

class Player(Stack):
    def __init__(self):
        super().__init__()

        self.name = None
        self.eliminated = None
        self.index = None
        self.result = None