import pygame

from ball import Ball

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)

DIRECTIONS = {
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0),
}


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Moving Ball")
    timer = pygame.time.Clock()
    ball = Ball(WIDTH // 2, HEIGHT // 2)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in DIRECTIONS:
                    dx, dy = DIRECTIONS[event.key]
                    ball.move(dx, dy, WIDTH, HEIGHT)
                elif event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill(WHITE)
        ball.draw(screen)
        pygame.display.flip()
        timer.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
