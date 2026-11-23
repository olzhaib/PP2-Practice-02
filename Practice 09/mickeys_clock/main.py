import pygame

from clock import MickeyClock


def main():
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Mickey's Clock")
    clock = MickeyClock()
    timer = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        screen.fill((255, 255, 255))
        clock.draw(screen)
        pygame.display.flip()
        timer.tick(30) 

    pygame.quit()


if __name__ == "__main__":
    main()
