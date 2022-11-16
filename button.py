import pygame

pygame.init()

FONT = pygame.font.SysFont(None, 48)


class Button:
    def __init__(
        self,
        rect: pygame.Rect,
        color: tuple[int, int, int],
        text: str,
        func,
    ) -> None:
        self.screen = pygame.display.get_surface()
        self.rect = rect
        self.color = color
        self.text = FONT.render(text, True, (0, 0, 0))
        self.func = func

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        self.screen.blit(self.text, self.text.get_rect(center=self.rect.center).topleft)
