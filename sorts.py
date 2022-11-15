from random import shuffle, randint
import pygame
from math import inf


class Sort:
    def __init__(self, elements, *, seperators=True) -> None:
        self.space = 1000 // elements
        self.to_sort: list[int] = [val for val in range(self.space, 1001, self.space)]
        self.sorted = self.to_sort.copy()
        shuffle(self.to_sort)
        self.current_index = 0
        self.second_index = 0
        self.done = False
        self.seperators = seperators

    def draw(self, screen):
        for i, val in enumerate(self.to_sort):
            rect = (
                (i * self.space) + (1 * self.seperators),
                1000 - val,
                self.space - (2 * self.seperators),
                val,
            )
            if not self.done:
                if i == self.current_index or i == self.second_index:
                    pygame.draw.rect(screen, (255, 0, 0), rect)
                else:
                    pygame.draw.rect(screen, (255, 255, 255), rect)
            else:
                pygame.draw.rect(screen, (0, 255, 0), rect)

    def check(self):
        if self.to_sort == self.sorted:
            self.done = True

    def process(self, screen: pygame.Surface, speed: int, proc):
        if not self.done:
            for i in range(speed):
                proc()
        self.draw(screen)


class Selection(Sort):
    def __init__(self, elements, *, seperators=True) -> None:
        super().__init__(elements, seperators=seperators)
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
            self.check()
            self.swap()
            self.second_index += 1
            self.second_index %= len(self.to_sort)
            self.current_index = self.second_index
            self.smallest = inf

    def swap(self):
        temp = self.to_sort[self.second_index]
        self.to_sort[self.second_index] = self.smallest
        self.to_sort[self.smallest_index] = temp

    def run(self, screen, speed):
        self.process(screen, speed, self.step)


class Bozo(Sort):
    def __init__(self, elements, *, seperators=True) -> None:
        super().__init__(elements, seperators=seperators)

    def pick_random(self):
        return randint(0, len(self.to_sort) - 1), randint(0, len(self.to_sort) - 1)

    def select_indexes(self):
        self.current_index, self.second_index = self.pick_random()

    def swap(self):
        temp = self.to_sort[self.current_index]
        self.to_sort[self.current_index] = self.to_sort[self.second_index]
        self.to_sort[self.second_index] = temp

    def step(self):
        self.check()
        if not self.done:
            self.select_indexes()
            self.swap()

    def run(self, screen, speed):
        self.process(screen, speed, self.step)


class Bogo(Sort):
    def __init__(self, elements, *, seperators=True) -> None:
        super().__init__(elements, seperators=seperators)

    def swap(self):
        shuffle(self.to_sort)

    def step(self):
        if not self.done:
            self.swap()
            self.check()

    def run(self, screen, speed):
        self.process(screen, speed, self.step)


class Bubble(Sort):
    def __init__(self, elements, *, seperators=True) -> None:
        super().__init__(elements, seperators=seperators)
        self.second_index = 1

    def step(self):
        if self.to_sort[self.current_index] > self.to_sort[self.second_index]:
            temp = self.to_sort[self.current_index]
            self.to_sort[self.current_index] = self.to_sort[self.second_index]
            self.to_sort[self.second_index] = temp
        self.increment()

    def increment(self):
        self.current_index += 1
        self.current_index %= len(self.to_sort) - 1
        self.second_index = self.current_index + 1

    def proc(self):
        if not self.done:
            self.step()
            self.check()

    def run(self, screen, speed):
        self.process(screen, speed, self.proc)


class Merge(Sort):
    def __init__(self, elements, *, seperators=True) -> None:
        super().__init__(elements, seperators=seperators)


class Shell(Sort):
    def __init__(self, elements, *, seperators=True) -> None:
        super().__init__(elements, seperators=seperators)
        self.n = len(self.to_sort)
        self.gap = self.n // 2
        self.j = self.gap
        self.i = 0

    def interior(self):
        if self.i >= 0:
            self.second_index = self.i + self.gap
            self.current_index = self.i
            if self.to_sort[self.i + self.gap] > self.to_sort[self.i]:
                self.inc_mid()
                return
            else:
                self.to_sort[self.i], self.to_sort[self.i + self.gap] = (
                    self.to_sort[self.i + self.gap],
                    self.to_sort[self.i],
                )
            self.i -= self.gap
        else:
            self.inc_mid()

    def inc_mid(self):
        self.j += 1
        if self.j < self.n:
            self.i = self.j - self.gap
        else:
            self.inc_ext()

    def inc_ext(self):
        self.gap //= 2
        if self.gap > 0:
            self.j = self.gap
            self.i = 0

    def step(self):
        if not self.done:
            self.interior()
            self.check()

    def run(self, screen, speed):
        self.process(screen, speed, self.step)
