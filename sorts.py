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
        self.n = len(self.to_sort)
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

    def run(self):
        """OVERLOAD THIS"""
        pass


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
        if self.current_index % self.n == 0:
            self.check()
            self.swap()
            self.second_index += 1
            self.second_index %= self.n
            self.current_index = self.second_index
            self.smallest = inf

    def run(self, speed):
        self.process(speed, self.step)


class Bozo(Sort):
    def __init__(self, elements, *, seperators=True) -> None:
        super().__init__(elements, seperators=seperators)

    def pick_random_indexes(self):
        return randint(0, self.n - 1), randint(0, self.n - 1)

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
        self.current_index %= self.n - 1
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
        self.n = self.n
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
        self.current_index %= self.n - 1
        self.second_index = self.current_index + 1

    def increment(self):
        self.current_index += 1
        self.current_index %= self.n - 1
        self.second_index = self.current_index + 1

    def run(self, speed):
        self.process(speed, self.step)


class Comb(Sort):
    def __init__(self, elements, *, seperators=True) -> None:
        super().__init__(elements, seperators=seperators)
        self.n = self.n
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
        self.n = self.n
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
        self.second_index = self.current_index + 1
        self.reversing = False

    def step(self):
        if self.to_sort[self.current_index] > self.to_sort[self.second_index]:
            self.swap()
        self.increment()

    def increment(self):
        if self.reversing:
            self.current_index -= 1
            if self.current_index == 0:
                self.reversing = False
        else:
            self.current_index += 1
            if self.current_index == (self.n - 2):
                self.reversing = True
        self.second_index = self.current_index + 1

    def proc(self):
        if not self.done:
            self.step()
            self.check()

    def run(self, speed):
        self.process(speed, self.proc)


class Gnome(Sort):
    def __init__(self, elements, *, seperators=True) -> None:
        super().__init__(elements, seperators=seperators)

    def inc(self):
        if self.second_index < self.n:
            if self.second_index == 0:
                self.second_index += 1
            self.current_index = self.second_index - 1
            if self.to_sort[self.second_index] >= self.to_sort[self.current_index]:
                self.second_index += 1
            else:
                self.swap()
                self.second_index -= 1

    def step(self):
        if not self.done:
            self.inc()
            self.check()

    def run(self, speed):
        self.process(speed, self.step)


class Tim(Sort):
    def __init__(self, elements, *, seperators=True) -> None:
        super().__init__(elements, seperators=seperators)
        self.min_merge = self.n // 32
        self.switch = 0
        self.min = self.calc_min()

        self.start = 0

    def calc_min(self):
        n = self.n
        r = 0
        while n >= self.min_merge:
            r |= n & 1
            n >>= 1
        return n + r

    def full(self):
        match self.switch:
            case 0:
                # from 0 to n step by min
                if self.start < self.n:  # loop conditional
                    self.end = min(self.start + self.min - 1, self.n - 1)
                    self.i = self.start + 1  # start of insertion sort
                    self.switch = 2  # to insertion sort loop
                else:
                    self.size = self.min  # initialize external while
                    self.switch = 4
            case 1:
                self.start += self.min
                self.switch = 0
            case 2:
                # from start + 1 to end + 1
                if self.i < self.end + 1:  # loop conditional
                    self.j = self.i
                    self.switch = 3  # internal while
                else:  # loop ends
                    self.switch = 1  # increment for
            case 3:
                self.current_index = self.j  # for drawing
                self.second_index = self.j - 1
                if (
                    self.j > self.start
                    and self.to_sort[self.j] < self.to_sort[self.j - 1]
                ):  # loop conditional
                    self.swap()
                    self.j -= 1
                else:  # loop ends
                    self.i += 1  # iterate insertion for
                    self.switch = 2  # back to insertion for
            case 4:
                # external while
                if self.size < self.n:  # loop conditional
                    self.left = 0  # initialize internal for
                    self.switch = 6  # to internal for
            case 5:
                self.size *= 2  # iterate external while
                self.switch = 4  # to external while
            case 6:
                # from 0 to n step by 2size
                if self.left < self.n:
                    self.mid = min(self.n - 1, self.left + self.size - 1)
                    self.right = min(self.left + 2 * self.size - 1, self.n - 1)
                    if self.mid < self.right:
                        self.switch = 8  # to merge
                    else:
                        self.switch = 7
                else:
                    self.switch = 5  # iterate external while
            case 7:
                self.left += self.size * 2  # iterate internal for
                self.switch = 6  # to internal for
            case 8:
                # merge
                self.len1, self.len2 = self.mid - self.left + 1, self.right - self.mid
                self.left_array, self.right_array = [], []
                self.i = 0  # initialize for loop
                self.switch = 9
            case 9:
                if self.i < self.len1:
                    self.left_array.append(self.to_sort[self.left + self.i])
                    self.i += 1
                else:
                    self.i = 0
                    self.switch = 10
            case 10:
                if self.i < self.len2:
                    self.right_array.append(self.to_sort[self.mid + self.i + 1])
                    self.i += 1
                else:
                    self.i, self.j, self.k = 0, 0, self.left  # initialize merge while
                    self.switch = 11
            case 11:
                if self.i < self.len1 and self.j < self.len2:
                    if self.left_array[self.i] <= self.right_array[self.j]:
                        self.to_sort[self.k] = self.left_array[self.i]
                        self.i += 1
                    else:
                        self.to_sort[self.k] = self.right_array[self.j]
                        self.j += 1
                    self.k += 1
                else:
                    self.switch = 12
            case 12:
                if self.i < self.len1:
                    self.to_sort[self.k] = self.left_array[self.i]
                    self.k += 1
                    self.i += 1
                else:
                    self.switch = 13
            case 13:
                if self.j < self.len2:
                    self.to_sort[self.k] = self.right_array[self.j]
                    self.k += 1
                    self.j += 1
                else:
                    self.switch = 7  # iterate internal for

        if self.switch > 10:
            self.current_index = self.i
            self.second_index = self.j

    def step(self):
        if not self.done:
            self.full()
            self.check()

    def run(self, speed):
        self.process(speed, self.step)


class Radix(Sort):
    def __init__(self, elements, *, seperators=True) -> None:
        super().__init__(elements, seperators=seperators)
        self.switch = 0
        self.max = max(self.to_sort)
        self.exp = 1
        self.i = 0
        self.index = 0

    def full(self):
        self.current_index = self.i
        self.second_index = self.index
        match self.switch:
            case 0:
                if self.max / self.exp >= 1:
                    self.switch = 2
            case 1:
                self.exp *= 10
                self.switch = 0
            case 2:
                #counting sort
                self.output = [0] * self.n
                self.count = [0] * 10
                self.i = 0
                self.switch = 3
            case 3:
                if self.i < self.n:
                    self.index = self.to_sort[self.i] // self.exp
                    self.count[self.index % 10] += 1
                    self.i += 1
                else:
                    self.i = 1
                    self.switch = 4
            case 4:
                if self.i < 10:
                    self.count[self.i] += self.count[self.i - 1]
                    self.i += 1
                else:
                    self.i = self.n - 1
                    self.switch = 5
            case 5:
                if self.i >= 0:
                    self.index = self.to_sort[self.i] // self.exp
                    self.output[self.count[self.index % 10] - 1] = self.to_sort[self.i]
                    self.count[self.index % 10] -= 1
                    self.i -= 1
                else:
                    self.i = 0
                    self.switch = 6
            case 6:
                if self.i < self.n:
                    self.to_sort[self.i] = self.output[self.i]
                    self.i += 1
                else:
                    self.switch = 1

    def step(self):
        if not self.done:
            self.full()
            self.check()

    def run(self, speed):
        self.process(speed, self.step)


class Pancake(Sort):
    def __init__(self, elements, *, seperators=True) -> None:
        super().__init__(elements, seperators=seperators)
        self.switch = 0
        self.reversing = False
        self.reverse_init = True
        self.current_size = self.n

    def work(self):
        if self.reversing:
            self.reverse()
        else:
            self.full()

    def reverse(self):
        if self.reverse_init == True:
            self.start = 0
            self.reverse_init = False
        else:
            self.current_index = self.start
            self.second_index = self.i
            if self.start < self.i:
                self.swap()
                self.start += 1
                self.i -= 1
            else:
                self.reverse_init = True
                self.reversing = False

    def findMax(self):
        mi = 0
        for i in range(0,self.current_size):
            if self.to_sort[i] > self.to_sort[mi]:
                mi = i
        return mi



    def full(self):
        match self.switch:
            case 0:
                if self.current_size > 1:
                    self.i = self.findMax()
                    self.switch = 2
            case 1:
                self.current_size -= 1
                self.switch = 0
            case 2:    
                if self.i != self.current_size - 1:
                    self.reversing = True
                    self.switch = 3
                else:
                    self.switch = 1
            case 3:
                self.i = self.current_size - 1
                self.reversing = True
                self.switch = 1

    def step(self):
        if not self.done:
            self.work()
            self.check()

    def run(self, speed):
        self.process(speed, self.step)