from typing import Tuple

import pygame as pg
import tracking

class Game:
    def __init__(self):
        # Initializing pygame
        pg.init()
        self._imsize = (500, 500)
        self._screen = pg.display.set_mode(self._imsize)

        # Creating an object for tracking the pose
        self._landmarks = tracking.Track(0, self._imsize)

        # Defining the colors
        self._background_color = (255, 255, 255)
        self._lhand_color = (0, 0, 255)
        self._rhand_color = (255, 0, 0)

    def run(self):
        running = True
        while running:
            # Checking if the game is not quit by the user
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            
            # Acquiring keypoints from the camera stream
            lhand, rhand = self.__get_point_data()

            # Draw background
            self._screen.fill(self._background_color)
        
            # Right and left hands
            pg.draw.line(self._screen, self._rhand_color, (rhand[0][0], rhand[0][1]), (rhand[1][0], rhand[1][1]))
            pg.draw.line(self._screen, self._lhand_color, (lhand[0][0], lhand[0][1]), (lhand[1][0], lhand[1][1]))

            # Flip the display
            pg.display.flip()

    def __landmark_to_game(self, landmark) -> Tuple[int, int, int]:
        # According to mediapipe's documentation, the coordinates are normalized
        # to a range of [0, 1] relative to the image size.
        return (
                    int(landmark.x * self._imsize[0]), 
                    int(landmark.y * self._imsize[1]), 
                    int(landmark.z * self._imsize[0])
            )

    def __get_point_data(self):
        pose = self._landmarks.get_keypoints().pose_landmarks.landmark
        
        return (
                    self.__landmark_to_game(pose[14]), 
                    self.__landmark_to_game(pose[16])
                ), \
                (
                    self.__landmark_to_game(pose[13]), 
                    self.__landmark_to_game(pose[15])
                )

    def __del__(self):
        pg.quit()

if __name__ == "__main__":
    game = Game()
    game.run()