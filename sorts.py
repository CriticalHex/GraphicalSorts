from random import shuffle, randint
import pygame
from math import inf
from numpy import interp


class Sort:
    def __init__(self, elements, *, seperators=True) -> None:
        self.screen = pygame.display.get_surface()
        self.space = self.screen.get_width() // elements
        self.to_sort: list[int] = [
            val for val in range(self.space, self.screen.get_width() + 1, self.space)
        ]
        self.sorted = self.to_sort.copy()
        shuffle(self.to_sort)
        self.current_index = 0
        self.second_index = 0
        self.done = False
        self.seperators = seperators

    def swap(self):
        self.to_sort[self.current_index], self.to_sort[self.second_index] = (
            self.to_sort[self.second_index],
            self.to_sort[self.current_index],
        )

    def draw(self):
        for i, val in enumerate(self.to_sort):
            rect = (
                (i * self.space) + (1 * self.seperators),
                self.screen.get_height()
                - interp(
                    val, [0, self.screen.get_width()], [0, self.screen.get_height()]
                ),
                self.space - (2 * self.seperators),
                interp(
                    val, [0, self.screen.get_width()], [0, self.screen.get_height()]
                ),
            )
            if not self.done:
                if i == self.current_index or i == self.second_index:
                    pygame.draw.rect(self.screen, (255, 0, 0), rect)
                else:
                    pygame.draw.rect(self.screen, (255, 255, 255), rect)
            else:
                pygame.draw.rect(self.screen, (0, 255, 0), rect)

    def check(self):
        if self.to_sort == self.sorted:
            self.done = True

    def process(self, speed: int, proc):
        if not self.done:
            for _ in range(speed):
                proc()
        self.draw()


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

    def swap(self):
        self.to_sort[self.second_index], self.to_sort[self.smallest_index] = (
            self.to_sort[self.smallest_index],
            self.to_sort[self.second_index],
        )

    def increment(self):
        self.current_index += 1
        if self.current_index % len(self.to_sort) == 0:
            self.check()
            self.swap()
            self.second_index += 1
            self.second_index %= len(self.to_sort)
            self.current_index = self.second_index
            self.smallest = inf

    def run(self, speed):
        self.process(speed, self.step)


class Bozo(Sort):
    def __init__(self, elements, *, seperators=True) -> None:
        super().__init__(elements, seperators=seperators)

    def pick_random_indexes(self):
        return randint(0, len(self.to_sort) - 1), randint(0, len(self.to_sort) - 1)

    def select_indexes(self):
        self.current_index, self.second_index = self.pick_random_indexes()

    def step(self):
        self.check()
        if not self.done:
            self.select_indexes()
            self.swap()

    def run(self, speed):
        self.process(speed, self.step)


class Bogo(Sort):
    def __init__(self, elements, *, seperators=True) -> None:
        super().__init__(elements, seperators=seperators)

    def swap(self):
        shuffle(self.to_sort)

    def step(self):
        if not self.done:
            self.swap()
            self.check()

    def run(self, speed):
        self.process(speed, self.step)


class Bubble(Sort):
    def __init__(self, elements, *, seperators=True) -> None:
        super().__init__(elements, seperators=seperators)
        self.second_index = 1

    def step(self):
        if self.to_sort[self.current_index] > self.to_sort[self.second_index]:
            self.swap()
        self.increment()

    def increment(self):
        self.current_index += 1
        self.current_index %= len(self.to_sort) - 1
        self.second_index = self.current_index + 1

    def proc(self):
        if not self.done:
            self.step()
            self.check()

    def run(self, speed):
        self.process(speed, self.proc)


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
                self.swap()
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

    def run(self, speed):
        self.process(speed, self.step)


class Insertion(Sort):
    def __init__(self, elements, *, seperators=True) -> None:
        super().__init__(elements, seperators=seperators)
        self.second_index = 1

    def step(self):
        if not self.done:
            if self.to_sort[self.current_index] > self.to_sort[self.second_index]:
                self.swap()
                self.decrement()
            else:
                self.increment()
            self.check()

    def decrement(self):
        if self.current_index > 0:
            self.current_index -= 1
        self.current_index %= len(self.to_sort) - 1
        self.second_index = self.current_index + 1

    def increment(self):
        self.current_index += 1
        self.current_index %= len(self.to_sort) - 1
        self.second_index = self.current_index + 1

    def run(self, speed):
        self.process(speed, self.step)


class Comb(Sort):
    def __init__(self, elements, *, seperators=True) -> None:
        super().__init__(elements, seperators=seperators)
        self.n = len(self.to_sort)
        self.gap = self.n
        self.swapped = True

    def next_gap(self):
        gap = (self.gap * 10) // 13
        if gap < 1:
            self.gap = 1
        else:
            self.gap = gap

    def iterate(self):
        self.second_index = self.current_index + self.gap
        if self.to_sort[self.current_index] > self.to_sort[self.second_index]:
            self.swap()
            self.swapped = True
        self.current_index += 1
        self.current_index %= self.n - self.gap

    def exterior(self):
        if self.gap != 1 or self.swapped:
            self.next_gap()
            self.swapped = False

    def step(self):
        if not self.done:
            if self.current_index == 0:
                self.exterior()
            self.iterate()
            self.check()

    def run(self, speed):
        self.process(speed, self.step)


class Cycle(Sort):
    def __init__(self, elements, *, seperators=True) -> None:
        super().__init__(elements, seperators=seperators)
        self.switch = 0
        self.n = len(self.to_sort)
        self.cycle_start = 0

    def swap(self):
        self.to_sort[self.pos], self.item = self.item, self.to_sort[self.pos]

    def full(self):
        if not self.done:
            match self.switch:

                case 0:
                    self.item = self.to_sort[self.cycle_start]
                    self.pos = self.cycle_start
                    self.i = self.cycle_start + 1
                    self.switch = 1

                case 1:
                    if self.to_sort[self.i] < self.item:
                        self.pos += 1
                    self.i += 1
                    self.i %= self.n
                    if self.i == 0:
                        self.switch = 2

                case 2:
                    if self.pos == self.cycle_start:
                        self.cycle_start += 1
                        self.cycle_start %= self.n - 1
                        self.switch = 0
                    else:
                        self.switch = 3

                case 3:
                    if self.item == self.to_sort[self.pos]:
                        self.pos += 1
                    else:
                        self.swap()
                        self.switch = 4

                case 4:
                    if self.pos != self.cycle_start:
                        self.pos = self.cycle_start
                        self.i = self.cycle_start + 1
                        self.switch = 5
                    else:
                        self.cycle_start += 1
                        self.cycle_start %= self.n - 1
                        self.switch = 0

                case 5:
                    if self.to_sort[self.i] < self.item:
                        self.pos += 1
                    self.i += 1
                    self.i %= self.n
                    if self.i == 0:
                        self.switch = 6

                case 6:
                    if self.item == self.to_sort[self.pos]:
                        self.pos += 1
                    else:
                        self.swap()
                        self.switch = 4

            self.current_index = self.cycle_start
            self.second_index = self.pos

            self.check()

    def run(self, speed):
        self.process(speed, self.full)


class Cocktail(Sort):
    def __init__(self, elements, *, seperators=True) -> None:
        super().__init__(elements, seperators=seperators)
        self.second_index = 1
        self.reversing = False

    def step(self):
        if self.to_sort[self.current_index] > self.to_sort[self.second_index]:
            self.swap()
        self.increment()

    def increment(self):
        if not self.reversing:
            self.current_index += 1
            self.current_index %= len(self.to_sort) - 1
            if self.current_index == 0:
                self.reversing = True
        else:
            self.current_index -= 1
            if self.current_index == 0:
                self.reversing = False
        self.second_index = self.current_index + 1

    def proc(self):
        if not self.done:
            self.step()
            self.check()

    def run(self, speed):
        self.process(speed, self.proc)


class Quick(Sort):
    def __init__(self, elements, *, seperators=True) -> None:
        super().__init__(elements, seperators=seperators)
        self.low = 0
        self.high = len(self.to_sort) - 1

    # def partition(self):
    #     self.pivot = self.to_sort[self.high]

    #     self.i = self.low - 1

    #     for self.j in range(self.low, self.high - 1):
    #         if self.to_sort[self.j] < self.pivot:
    #             self.i += 1
    #             self.current_index = self.i
    #             self.second_index = self.j
    #             self.swap()
    #     self.current_index = self.i + 1
    #     self.second_index = self.high
    #     self.swap()
    #     return self.i + 1

    # def quicksort(self):
    #     if self.low < self.high:
    #         self.pi = self.partition()
    #         self.high = self.pi - 1
    #         self.quicksort()

    def partition(self, low, high):
        pivot = self.to_sort[high]

        i = low - 1

        for j in range(low, high):
            if self.to_sort[j] <= pivot:
                i += 1
                self.current_index = i
                self.second_index = j
                self.swap()
        self.current_index = i + 1
        self.second_index = high
        self.swap()
        return i + 1

    def quicksort(self, low, high):
        if low < high:
            pi = self.partition(low, high)
            self.quicksort(low, pi - 1)
            self.quicksort(pi + 1, high)


class Merge(Sort):
    def __init__(self, elements, *, seperators=True) -> None:
        super().__init__(elements, seperators=seperators)
