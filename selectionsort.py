from math import inf
import pygame
from random import shuffle


class SelectionSort:
    def __init__(self) -> None:
        self.to_sort: list[int] = [val for val in range(40, 1001, 40)]
        shuffle(self.to_sort)
        self.swap_index = 0
        self.current_index = 0
        self.smallest_index = 0
        self.smallest = inf
        self.done = False

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

    def draw(self, screen):
        if not self.done:
            for i, val in enumerate(self.to_sort):
                rect = ((i * 40) + 1, 1000 - val, 38, val)
                if i == self.current_index or i == self.smallest_index:
                    pygame.draw.rect(screen, (200, 50, 50), rect)
                else:
                    pygame.draw.rect(screen, (200, 200, 200), rect)
        else:
            for i, val in enumerate(self.to_sort):
                rect = ((i * 40) + 1, 1000 - val, 38, val)
                pygame.draw.rect(screen, (0,255,0), rect)

    def update(self, screen):
        self.draw(screen)
        self.step()
