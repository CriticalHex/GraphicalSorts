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
        self.c1 = 0
        self.c2 = 0
        self.c3 = 0
        self.n = len(self.to_sort)
        self.gap = self.n // 2
        self.exterior()
        self.middle()
        self.internal()

    def exterior(self):
        self.c1 += 1
        self.j = self.gap

    def middle(self):
        self.c2 += 1
        self.i = self.j - self.gap
        self.current_index = self.i

    def internal(self):
        self.c3 += 1
        self.second_index = self.i + self.gap
        if self.to_sort[self.second_index] > self.to_sort[self.current_index]:
            self.inc_mid()
            return
        else:
            self.to_sort[self.current_index], self.to_sort[self.second_index] = (
                self.to_sort[self.second_index],
                self.to_sort[self.current_index],
            )
        self.i -= self.gap

    def inc_mid(self):
        self.j += 1

    def inc_ext(self):
        self.gap //= 2

    def step(self):
        if self.gap > 0:
            self.exterior()
            if self.j < self.n:
                self.middle()
                if self.i >= 0:
                    self.internal()
                else:
                    self.inc_mid()
            else:
                self.inc_ext()
        else:
            self.done = True

    def run(self, screen, speed):
        print(self.c1, self.c2, self.c3)
        self.process(screen, speed, self.step)
