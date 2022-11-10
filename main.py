from selectionsort import SelectionSort
import pygame


def main():
    screen = pygame.display.set_mode((1000, 1000))
    sort = SelectionSort()
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LCTRL]:
                running = False
            if keys[pygame.K_LSHIFT]:
                sort = SelectionSort()
            if keys[pygame.K_SPACE]:
                pass

        screen.fill((0, 0, 0))

        sort.update(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
