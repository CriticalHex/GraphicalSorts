from random import shuffle, randint
import pygame
from math import inf


class Sort:
    def __init__(self, elements) -> None:
        self.space = 1000 // elements
        self.to_sort: list[int] = [val for val in range(self.space, 1001, self.space)]
        shuffle(self.to_sort)
        self.current_index = 0
        self.second_index = 0
        self.done = False

    def draw(self, screen):
        if not self.done:
            for i, val in enumerate(self.to_sort):
                rect = ((i * self.space) + 1, 1000 - val, self.space - 2, val)
                if i == self.current_index or i == self.second_index:
                    pygame.draw.rect(screen, (200, 50, 50), rect)
                else:
                    pygame.draw.rect(screen, (200, 200, 200), rect)
        else:
            for i, val in enumerate(self.to_sort):
                rect = ((i * self.space) + 1, 1000 - val, self.space - 2, val)
                pygame.draw.rect(screen, (0, 255, 0), rect)


class Selection(Sort):
    def __init__(self, elements) -> None:
        super().__init__(elements)
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
            self.second_index += 1
            self.second_index %= len(self.to_sort)
            self.current_index = self.second_index
            self.smallest = inf

    def swap(self):
        temp = self.to_sort[self.second_index]
        self.to_sort[self.second_index] = self.smallest
        self.to_sort[self.smallest_index] = temp

    def run(self, screen):
        self.draw(screen)
        self.step()


class Bozo(Sort):
    def __init__(self, elements) -> None:
        super().__init__(elements)
        self.completed = sorted(self.to_sort)

    def pick_random(self):
        return randint(0, len(self.to_sort) - 1), randint(0, len(self.to_sort) - 1)

    def select_indexes(self):
        self.current_index, self.second_index = self.pick_random()

    def swap(self):
        temp = self.to_sort[self.current_index]
        self.to_sort[self.current_index] = self.to_sort[self.second_index]
        self.to_sort[self.second_index] = temp

    def check(self):
        if self.to_sort == self.completed:
            self.done = True

    def run(self, screen):
        self.select_indexes()
        self.draw(screen)
        if not self.done:
            self.swap()
            self.check()


class Bogo(Sort):
    def __init__(self, elements) -> None:
        super().__init__(elements)
        self.completed = sorted(self.to_sort)

    def swap(self):
        shuffle(self.to_sort)

    def check(self):
        if self.to_sort == self.completed:
            self.done = True

    def run(self, screen):
        self.draw(screen)
        if not self.done:
            self.swap()
            self.check()


class Bubble(Sort):
    def __init__(self, elements) -> None:
        super().__init__(elements)
        self.second_index = 1

    def step(self):
        if self.to_sort[self.current_index] < self.to_sort[self.second_index]:
            temp = self.to_sort[self.current_index]
            self.to_sort[self.current_index] = self.to_sort[self.second_index]
            self.to_sort[self.second_index] = temp
        self.increment()

    def increment(self):
        if self.to_sort == range(self.space, 1001, self.space):
            self.done = True
        self.current_index += 1
        self.current_index %= len(self.to_sort)
        self.second_index += 1
        self.second_index %= len(self.to_sort)

    def run(self, screen):
        self.draw(screen)
        if not self.done:
            self.step()
