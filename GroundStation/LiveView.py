import pygame
import threading
import os
from pygame.locals import *
from pygame.constants import MOUSEBUTTONUP

black = (0, 0, 0)
white = (255, 255, 255)


class LiveView(threading.Thread):

    def __init__(self, telemetry=None):
        super().__init__()
        pygame.init()
        self.game = pygame
        self.screen_width = 1200
        self.screen_height = 800
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        try:
            self.test_frame = pygame.image.load((os.path.abspath(os.getcwd()) + '\\GroundStation\\test.bmp'))
        except:
            self.test_frame = pygame.image.load((os.path.abspath(os.getcwd()) + '\\RcMain\\GroundStation\\test.bmp'))
        self.test_frame = pygame.transform.scale(self.test_frame, (self.screen_width, self.screen_height))
        self.telemetry = telemetry
        self.crashed = False
        self.test_string = None
        self.font = pygame.font.SysFont(pygame.font.get_fonts()[1], size=24)
        self.frame_skip = 1

    def run(self):
        while not self.crashed:
            if self.frame_skip != 0:
                pygame.display.update()
                self.clock.tick()
                self.frame_skip = 2
                self.clock.tick()
            # White background
            # self.screen.fill(white)
            # Filler frame for testing
            # self.draw_test_frame()
            self.set_blue_brown_horizon()
            # Horizon line, to be tied to roll of aircraft
            self.draw_horizon()
            # Draw received heading
            self.draw_heading()
            # Draw Altitude
            self.draw_altitude()
            # Draw Airspeed
            self.draw_airspeed()
            self.draw_fps()
            pygame.display.update()
            self.clock.tick()

    def set_blue_brown_horizon(self):
        middle_y = (self.screen_height / 2) - ((self.screen_height / 2) * (self.telemetry['pitch'] * .01))
        pygame.draw.rect(self.screen,
                         pygame.color.Color(77, 166, 255),  #BLUE
                         Rect(0, 0, self.screen_width, middle_y))
        pygame.draw.rect(self.screen,
                         pygame.color.Color(128, 64, 0),  #BROWN
                         Rect(0, middle_y, self.screen_width, self.screen_height))

    def set_telemetry(self, t):
        self.telemetry = t

    '''Draw functions, call these in run()'''

    def draw_test_frame(self):
        # print(self)
        self.screen.blit(self.test_frame, (0, 0))

    def draw_horizon(self):
        pygame.draw.line(surface=self.screen,
                         color=black,
                         start_pos=(0, self.screen_height / 2),
                         end_pos=(self.screen_width, self.screen_height / 2),
                         width=1)

    def draw_airspeed(self):
        txt = f'Speed   {str(self.telemetry["speed"])}kn'
        img = self.font.render(txt, True, pygame.color.Color('black'))
        # display heading on top of screen
        self.screen.blit(img, (20, self.screen_height / 2))

    def draw_altitude(self):
        txt = f'Alt   {str(self.telemetry["altitude"])}ft'
        img = self.font.render(txt, True, pygame.color.Color('black'))
        # display heading on top of screen
        self.screen.blit(img, (self.screen_width - img.get_width() * 1.5, self.screen_height / 2))

    def draw_heading(self):
        txt = f'Heading   {str(self.telemetry["heading"])}°'
        img = self.font.render(txt, True, pygame.color.Color('black'))
        # display heading on top of screen
        self.screen.blit(img, (((self.screen_width - img.get_width()) / 2), 20))

    def draw_test(self):
        txt = f'Test  {str(self.test_string)}'
        img = self.font.render(txt, True, pygame.color.Color('black'))
        # display heading on top of screen
        self.screen.blit(img, (((self.screen_width - img.get_width()) / 2), 200))

    def draw_fps(self):
        txt = f'FPS:  {str(int(self.clock.get_fps()))}'
        img = self.font.render(txt, True, pygame.color.Color('black'))
        # display heading on top of screen
        self.screen.blit(img, (0, 0))


if __name__ == '__main__':
    L = LiveView()
    L.start()
