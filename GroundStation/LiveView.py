import pygame

black = (0,0,0)
white = (255,255,255)

class LiveView:



    def __init__(self,Airplane = None,target_fps=10):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.test_frame = pygame.image.load('test.bmp')
        self.test_frame = pygame.transform.scale(self.test_frame, (1280, 720))
        self.airplane = Airplane


    def draw_test_frame(self):
        print(self)
        self.screen.blit(self.test_frame, (0, 0))

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

        self.screen.fill(white)
        self.draw_test_frame()
        pygame.display.update()
        self.clock.tick(60)

if __name__ == '__main__':
    L = LiveView()
    crashed = False
    while not crashed:
        L.update()