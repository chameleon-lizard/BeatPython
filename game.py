from typing import Tuple

import pygame as pg
import tracking

def landmark_to_game(landmark, imsize) -> Tuple[int, int, int]:
    # According to mediapipe's documentation, the coordinates are normalized
    # to a range of [0, 1] relative to the image size.
    return (
                int(landmark.x * imsize[0]), 
                int(landmark.y * imsize[1]), 
                int(landmark.z * imsize[0])
            )

if __name__ == "__main__":
    pg.init()
    imsize = (500, 500)
    screen = pg.display.set_mode(imsize)
    # Run until the user asks to quit
    running = True
    rhand_color = (255, 0, 0)
    lhand_color = (0, 0, 255)
    landmarks = tracking.Track(0, imsize)
    while running:
        # Did the user click the window close button?
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # Fill the background with white
        screen.fill((255, 255, 255))

        pose = landmarks.get_keypoints().pose_landmarks.landmark

        rhand_start = landmark_to_game(pose[14], imsize)
        rhand_end = landmark_to_game(pose[16], imsize)

        lhand_start = landmark_to_game(pose[13], imsize)
        lhand_end = landmark_to_game(pose[15], imsize)

        pg.draw.line(screen, rhand_color, (rhand_start[0], rhand_start[1]), (rhand_end[0], rhand_end[1]))
        pg.draw.line(screen, lhand_color, (lhand_start[0], lhand_start[1]), (lhand_end[0], lhand_end[1]))

        # Flip the display
        pg.display.flip()

    # Done! Time to quit.
    pg.quit()
