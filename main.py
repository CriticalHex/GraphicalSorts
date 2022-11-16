import sorts
import pygame
from button import Button

vec = pygame.Vector2
rec = pygame.Rect


def click(mouse: vec, buttons: list[Button]):
    for b in buttons:
        if b.rect.collidepoint(mouse):
            return b.func
    return None


def main():

    screen = pygame.display.set_mode((1000, 1000))

    elements = 1000
    seperators = False

    using = sorts.Shell
    sort = using(elements, seperators=seperators)

    menu = True
    sorting = False
    running = True

    menu_buttons: list[Button] = []
    menu_buttons.append(
        Button(rec(1, 1, 50, 20), (255, 0, 0), "Selection", lambda: sorts.Selection)
    )
    menu_buttons.append(
        Button(rec(51, 1, 50, 20), (255, 0, 0), "Bozo", lambda: sorts.Bozo)
    )
    menu_buttons.append(
        Button(rec(101, 1, 50, 20), (255, 0, 0), "Bogo", lambda: sorts.Bogo)
    )
    menu_buttons.append(
        Button(rec(151, 1, 50, 20), (255, 0, 0), "Bubble", lambda: sorts.Bubble)
    )
    menu_buttons.append(
        Button(rec(201, 1, 50, 20), (255, 0, 0), "Shell", lambda: sorts.Shell)
    )

    while running:

        while menu:
            for event in pygame.event.get():
                mouse = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if func := click(mouse, menu_buttons):
                        using = func()
                        sort = using(elements, seperators=seperators)
                        menu = False
                        sorting = True

                if event.type == pygame.QUIT:
                    running = False
                    sorting = False
                    menu = False

                keys = pygame.key.get_pressed()

                if keys[pygame.K_LCTRL]:
                    running = False
                    sorting = False
                    menu = False

            screen.fill((0, 0, 0))

            for b in menu_buttons:
                b.draw()

            pygame.display.flip()

        while sorting:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False
                    sorting = False
                    menu = False

                keys = pygame.key.get_pressed()

                if keys[pygame.K_LCTRL]:
                    running = False
                    sorting = False
                    menu = False

                if keys[pygame.K_LSHIFT]:
                    sort = using(elements, seperators=seperators)

                if keys[pygame.K_SPACE]:
                    pass

            screen.fill((0, 0, 0))

            sort.run(100)

            pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
