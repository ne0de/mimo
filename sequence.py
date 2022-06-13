

from .step import Step
from datetime import datetime

class Sequence:
    def __init__(self):
        self.name = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.steps = []
        self.velocity = 0.1
    
    def set_name(self, name: str) -> None:
        self.name = name
        return
    
    def add_step(self, step: Step) -> None:
        self.steps.append(step)
        return