from typing import Tuple

import pygame as pg
import tracking
import random
import math

class Game:
    def __init__(self, gamespeed) -> None:
        '''
        The init function for the game.
        '''
        # Initializing
        pg.init()
        pg.font.init()
        random.seed(None)
        self._font = pg.font.SysFont('Noto Sans', 30)

        # Set screen size
        self._imsize = (1280, 720)
        self._screen = pg.display.set_mode(self._imsize)

        # Creating an object for tracking the pose
        self._landmarks = tracking.Track(0, self._imsize)

        # Defining the colors
        self._background_color = (255, 255, 255)
        self._lhand_color = (0, 0, 255)
        self._rhand_color = (255, 0, 0)

        # Creating a list for boxes
        self._blue_boxes = []
        self._red_boxes = []

        # Creating a score counter
        self._score = 0

        # Creating variables
        self._gamespeed = gamespeed
        self._box_size = self._imsize[0] // 10

        # Hand position tracking
        self._track_status = True
        self._lhand = self._rhand = (0, 0), (0, 0)
        
    def run(self) -> None:
        '''
        Function with the main game loop.
        '''
        running = True
        fcount = 0
        while running:
            # Checking if the game is not quit by the user
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            
            # Acquiring keypoints from the camera stream

            try:
                self._lhand, self._rhand = self.__get_point_data()
                self._track_status = True
            except AttributeError:
                self._track_status = False

            # Generating boxes
            if fcount % self._gamespeed == 0 or (self._blue_boxes == [] and self._red_boxes == []):
                self._blue_boxes = [i for i in self._blue_boxes if abs(i[1] - fcount) <= self._gamespeed]
                self._red_boxes = [i for i in self._red_boxes if abs(i[1] - fcount) <= self._gamespeed]
                self.__create_boxes(fcount)

            self.__check_lhand_hit(self._lhand)
            self.__check_rhand_hit(self._rhand)

            # Draw stuff
            self.__draw(self._lhand, self._rhand, self._track_status)

            # Flip the display
            pg.display.flip()
            
            # Increasing the frame counter
            fcount += 1
    
    def __draw(self, lhand, rhand, track_status) -> None:
        '''
        Draw the graphics for the playing field.
        '''
        # Draw background
        self._screen.fill(self._background_color)
        
        # Right and left hands
        pg.draw.line(self._screen, self._rhand_color, (rhand[0][0], rhand[0][1]), (rhand[1][0], rhand[1][1]), 5)
        pg.draw.line(self._screen, self._lhand_color, (lhand[0][0], lhand[0][1]), (lhand[1][0], lhand[1][1]), 5)
        
        # Draw boxes
        for box in self._blue_boxes:
            pg.draw.rect(self._screen, 
                self._lhand_color, 
                box[0]
                )
        
        for box in self._red_boxes:
            pg.draw.rect(
                self._screen, 
                self._rhand_color, 
                box[0]
                )

        score = self._font.render(f'{self._score}', False, (0, 0, 0))
        self._screen.blit(score, (50, 50))

        if not track_status:
            tracking_error = self._font.render(f'No hands detected', False, (255, 0, 0))
            self._screen.blit(tracking_error, (50, 75))

    def __check_lhand_hit(self, lhand) -> None:
        '''
        Deleting any boxes if they were hit
        '''
        for box in self._blue_boxes:
            if len(box[0].clipline(lhand[0][0], lhand[0][1], lhand[1][0], lhand[1][1])) != 0:
                self._score += self._gamespeed - box[1] % self._gamespeed
                self._blue_boxes.remove(box)
            
        for box in self._red_boxes:
            if len(box[0].clipline(lhand[0][0], lhand[0][1], lhand[1][0], lhand[1][1])) != 0:
                self._score -= self._gamespeed
                self._red_boxes.remove(box)


    def __check_rhand_hit(self, rhand) -> None:
        '''
        Deleting any boxes if they were hit
        '''
        for box in self._red_boxes:
            if len(box[0].clipline(rhand[0][0], rhand[0][1], rhand[1][0], rhand[1][1])) != 0:
                self._score += self._gamespeed - box[1] % self._gamespeed
                self._red_boxes.remove(box)

        for box in self._blue_boxes:
            if len(box[0].clipline(rhand[0][0], rhand[0][1], rhand[1][0], rhand[1][1])) != 0:
                self._score -= self._gamespeed
                self._blue_boxes.remove(box)

    def __dist_points(self, p1: Tuple[int, int], p2: Tuple[int, int]) -> float:
        '''
        Calculates distance between two points.
        '''
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


    def __create_boxes(self, fcount) -> None:
        '''
        Populates the array with target boxes.
        '''
        redx = random.randint(self._imsize[0] // 10, self._imsize[0] - self._box_size)
        redy = random.randint(self._imsize[1] // 10, self._imsize[1] - self._box_size)

        bluex = random.randint(self._imsize[0] // 10, self._imsize[0] - self._box_size)
        bluey = random.randint(self._imsize[1] // 10, self._imsize[1] - self._box_size)
        while self.__dist_points((redx, redy), (bluex, bluey)) < self._box_size:
            bluex = random.randint(self._imsize[0] // 10, self._imsize[0] - self._box_size)
            bluey = random.randint(self._imsize[1] // 10, self._imsize[1] - self._box_size)
        
        self._red_boxes.append((pg.Rect(redx, redy, self._box_size, self._box_size), fcount))
        self._blue_boxes.append((pg.Rect(bluex, bluey, self._box_size, self._box_size), fcount))

    def __landmark_to_game(self, landmark) -> Tuple[int, int, int]:
        '''
        Function that converts landmark coordinates to the game coordinates.
        '''
        # According to mediapipe's documentation, the coordinates are normalized
        # to a range of [0, 1] relative to the image size.
        return (
                    int(landmark.x * self._imsize[0]), 
                    int(landmark.y * self._imsize[1]), 
                    int(landmark.z * self._imsize[0])
            )

    def __get_point_data(self) -> Tuple[Tuple[Tuple[int, int, int], Tuple[int, int, int]], Tuple[Tuple[int, int, int], Tuple[int, int, int]]]:
        '''
        Functions that gets the point data of both hands.
        '''
        pose = self._landmarks.get_keypoints().pose_landmarks.landmark
        
        return (
                    self.__landmark_to_game(pose[14]), 
                    self.__landmark_to_game(pose[16])
                ), \
                (
                    self.__landmark_to_game(pose[13]), 
                    self.__landmark_to_game(pose[15])
                )

    def __del__(self) -> None:
        '''
        Destructor.
        '''
        pg.quit()

if __name__ == "__main__":
    game = Game(100)
    game.run()
