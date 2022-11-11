from math import inf
from sorts import Sort


class Selection(Sort):
    def __init__(self) -> None:
        super().__init__()
        self.swap_index = 0
        self.smallest_index = 0
        self.smallest = inf

    def step(self):
        if self.to_sort[self.current_index] < self.smallest:
            self.smallest_index = self.current_index
            self.smallest = self.to_sort[self.smallest_index]
        self.increment()

    def increment(self):
        self.current_index += 1
        if self.current_index % len(self.to_sort) == 0:
            if self.smallest == 1000:
                self.done = True
            self.swap()
            self.swap_index += 1
            self.swap_index %= len(self.to_sort)
            self.current_index = self.swap_index
            self.smallest = inf

    def swap(self):
        temp = self.to_sort[self.swap_index]
        self.to_sort[self.swap_index] = self.smallest
        self.to_sort[self.smallest_index] = temp

    def run(self, screen):
        self.draw(screen)
        self.step()
