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
    sort: sorts.Sort

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    elements = screen.get_width()
    seperators = False
    menu = True
    sorting = False
    running = True
    speed = 10000

    menu_buttons: list[Button] = []
    menu_buttons.append(
        Button(rec(1, 1, 198, 50), (255, 0, 0), "Selection", lambda: sorts.Selection)
    )
    menu_buttons.append(
        Button(rec(201, 1, 198, 50), (255, 0, 0), "Bozo", lambda: sorts.Bozo)
    )
    menu_buttons.append(
        Button(rec(401, 1, 198, 50), (255, 0, 0), "Bogo", lambda: sorts.Bogo)
    )
    menu_buttons.append(
        Button(rec(601, 1, 198, 50), (255, 0, 0), "Bubble", lambda: sorts.Bubble)
    )
    menu_buttons.append(
        Button(rec(801, 1, 198, 50), (255, 0, 0), "Shell", lambda: sorts.Shell)
    )
    menu_buttons.append(
        Button(rec(1, 52, 198, 50), (255, 0, 0), "Comb", lambda: sorts.Comb)
    )
    menu_buttons.append(
        Button(rec(201, 52, 198, 50), (255, 0, 0), "Insertion", lambda: sorts.Insertion)
    )
    menu_buttons.append(
        Button(rec(401, 52, 198, 50), (255, 0, 0), "Cycle", lambda: sorts.Cycle)
    )
    menu_buttons.append(
        Button(rec(601, 52, 198, 50), (255, 0, 0), "Cocktail", lambda: sorts.Cocktail)
    )
    menu_buttons.append(
        Button(rec(801, 52, 198, 50), (255, 0, 0), "Gnome", lambda: sorts.Gnome)
    )
    menu_buttons.append(
        Button(rec(1, 103, 198, 50), (255, 0, 0), "Tim", lambda: sorts.Tim)
    )
    menu_buttons.append(
        Button(rec(201, 103, 198, 50), (255, 0, 0), "Radix", lambda: sorts.Radix)
    )
    menu_buttons.append(
        Button(rec(401, 103, 198, 50), (255, 0, 0), "Pancake", lambda: sorts.Pancake)
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
                        break

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

                if keys[pygame.K_ESCAPE]:
                    sorting = False
                    menu = True
                    break

                if keys[pygame.K_SPACE]:
                    pass

            screen.fill((0, 0, 0))

            sort.run(speed)

            pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
