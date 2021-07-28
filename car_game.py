import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame, sys
import cv2
from math import *
from pygame.locals import *
from enum import Enum
from detect_drowsiness import detect_drowsy

# game code modified from
# https://www.pygame.org/project/5051

# 
WHITE = (255, 255, 255)
BLUE = (135,206,250)

class state(Enum):
    DRIVE = 1
    PULL_OVER = 2
    STOP = 3
    MERGE_BACK = 4

class CarGame:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.w = 640
        self.h = 480
        self.screen = pygame.display.set_mode(
                            (self.w, self.h),
                        )
        pygame.display.set_caption("QAware")
        self.plane_center_x = self.w / 2

        self.stripe = pygame.image.load("game_asset/stripes.png").convert()
        self.stripe = pygame.transform.scale(self.stripe, (self.w, self.stripe.get_height()))

        self.road = pygame.image.load("game_asset/road.png").convert()
        self.road_width = self.road.get_width()
        self.road_height = self.road.get_height()

        self.player_car = pygame.image.load("game_asset/car.png").convert_alpha()
        self.player_car = pygame.transform.scale(self.player_car, (160, 82))

        self.q_cloud = pygame.image.load("game_asset/qcloud.png").convert_alpha()
        self.q_cloud.set_colorkey(WHITE)
        self.q_cloud = pygame.transform.scale(self.q_cloud, (100, 100))
        self.q_cloud.set_alpha(200)

        self.team_cloud = pygame.image.load("game_asset/team.png").convert_alpha()
        self.team_cloud.set_colorkey(WHITE)
        self.team_cloud = pygame.transform.scale(self.team_cloud, (100, 100))
        self.team_cloud.set_alpha(200)


        self.player_pos = [0, 0]

        self.plane_center_y = self.h // 2

        self.x_move = 15
        self.y_move = -15
        self.car_x = 240
        self.car_y = 320
        self.state = state.DRIVE

        self.eye_detector = detect_drowsy()
        self.threshold = 3


    def run(self):
        while True:
            self.clock.tick(30)

            # # set states:
            if self.state == state.DRIVE and self.eye_detector.is_drowsy():
                self.state = state.PULL_OVER

            if self.state == state.STOP and not self.eye_detector.is_drowsy():
                self.state = state.MERGE_BACK

            if self.state == state.DRIVE:
                self.player_pos[1] += self.y_move
                keys=pygame.key.get_pressed()
                if keys[K_LEFT] and self.car_x > 100:
                    self.car_x -= 10
                if keys[K_RIGHT] and self.car_x < 400:
                    self.car_x += 10
                    # self.car_x = 240
                    # self.car_y = 320
            
            elif self.state == state.PULL_OVER:
                self.player_pos[1] += self.y_move / 4
                if self.car_x != 500:
                    self.car_x += 5
                if self.car_y != 270:
                    self.car_y -= 5
                if self.car_x == 500 and self.car_y == 270:
                    self.state = state.STOP
            
            elif self.state == state.STOP:
                pass

            elif self.state == state.MERGE_BACK:
                self.player_pos[1] += self.y_move / 2
                if self.car_x != 240:
                    self.car_x -= 1
                if self.car_y != 320:
                    self.car_y += 1
                if self.car_x == 240 and self.car_y == 320:
                    self.state = state.DRIVE

            wall_bottom = self.h
            while wall_bottom > self.plane_center_y + 10:
                wall_bottom -= 1
                row = wall_bottom - self.plane_center_y
                straight_p_dist = 32 / row * self.w
                to_floor_dist = straight_p_dist
                ray_y = int(self.player_pos[1] - to_floor_dist)
                floor_y = ray_y % self.road_height
                slice_width = int(self.road_width / to_floor_dist * self.w)
                slice_x = (self.plane_center_x) - (slice_width // 2)
                row_slice = self.road.subsurface(0, floor_y, self.road_width, 1)
                row_slice = pygame.transform.scale(row_slice, (slice_width, 1))
                self.screen.blit(self.stripe, (0, wall_bottom), (0, floor_y, self.w, 1))
                self.screen.blit(row_slice, (slice_x, wall_bottom))
                self.screen.blit(self.player_car, (self.car_x, self.car_y))

            self.screen.blit(self.q_cloud, (20,20))
            self.screen.blit(self.team_cloud, (500,40))
            


            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.flip()
            self.screen.fill(BLUE)
                    
