import sorts
import pygame


def main():
    screen = pygame.display.set_mode((1000, 1000))
    elements = 1000
    seperators = False
    using = sorts.Shell
    sort = using(elements, seperators=seperators)
    clock = pygame.time.Clock()
    running = True
    while running:
        # clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LCTRL]:
                running = False
            if keys[pygame.K_LSHIFT]:
                sort = using(elements, seperators=seperators)
            if keys[pygame.K_SPACE]:
                pass

        screen.fill((0, 0, 0))

        sort.run(screen, 100)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
