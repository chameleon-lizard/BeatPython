import pygame as pg
import tracking

if __name__ == "__main__":
    pg.init()

    screen = pg.display.set_mode([500, 500])
    # Run until the user asks to quit
    running = True
    line_color = (255, 0, 0)
    landmarks = tracking.Track(0)
    while running:
        # Did the user click the window close button?
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # Fill the background with white
        screen.fill((255, 255, 255))

        line_start = landmarks[14]
        line_end = landmarks[16]
        print(line_start)

        pg.draw.line(screen, line_color, line_start, line_end)
    
        # Flip the display
        pg.display.flip()

    # Done! Time to quit.
    pg.quit()
