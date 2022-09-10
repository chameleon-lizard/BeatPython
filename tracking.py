from typing import List

import mediapipe as mp
import numpy as np
import cv2 as cv

class Track:
    def __init__(self, sink: int) -> None:
        self._cap = cv.VideoCapture(sink)
        self._pose = mp.solutions.pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def __get_frame(self) -> np.array:
        ret, frame = self._cap.read()
        return cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    def get_keypoints(self) -> List:
        return self._pose.process(self.__get_frame()).pose_landmarks

    def __del__(self) -> None:
        self._cap.release()
