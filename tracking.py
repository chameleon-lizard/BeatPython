from typing import Tuple

import mediapipe as mp
import numpy as np
import cv2 as cv

class Track:
    def __init__(self, sink: int, imsize: Tuple[int, int]) -> None:
        self._imsize = imsize
        self._cap = cv.VideoCapture(sink)
        self._pose = mp.solutions.pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def __get_frame(self) -> np.array:
        _, frame = self._cap.read()
        frame = cv.resize(frame, self._imsize)
        frame = cv.flip(frame, 1)
        return cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    def get_keypoints(self):
        return self._pose.process(self.__get_frame())

    def __del__(self) -> None:
        self._cap.release()
