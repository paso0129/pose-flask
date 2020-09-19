import math
from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class Parts(str, Enum):
    nose = 'nose'
    leftEye = 'leftEye'
    rightEye = 'rightEye'
    leftEar = 'leftEar'
    rightEar = 'rightEar'
    leftShoulder = 'leftShoulder'
    rightShoulder = 'rightShoulder'
    leftElbow = 'leftElbow'
    rightElbow = 'rightElbow'
    leftWrist = 'leftWrist'
    rightWrist = 'rightWrist'
    leftHip = 'leftHip'
    rightHip = 'rightHip'
    leftKnee = 'leftKnee'
    rightKnee = 'rightKnee'
    leftAnkle = 'leftAnkle'
    rightAnkle = 'rightAnkle'


class Vector2D(BaseModel):
    x: float
    y: float

    def __init__(self, x, y) -> None:
        super().__init__(x=x, y=y)

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, other) -> float:
        return self.x * other.x + self.y * other.y

    @property
    def magnitude(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def distance(self, other) -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)



class Pose(BaseModel):
    score: float
    part: Parts
    position: Vector2D


class PoseList(BaseModel):
    pose_list: List[Pose] = Field(..., alias="pose")

    def find(self, part: Parts) -> Pose:
        for pose in self.pose_list:
            if pose.part == part:
                return pose


class PoseDetector:
    def __init__(self, pose_list: PoseList):
        self.pose_list = pose_list

    @staticmethod
    def _compute_angle(a: Vector2D, b: Vector2D, c: Vector2D):
        """ab, bc의 사잇각 계산
        todo: 이거 맞는지 확인 좀..귀찮아서 안 함
        """
        a = a - b
        c = c - b
        return math.acos((a * c) / (a.magnitude * c.magnitude)) * 180 / math.pi

    def is_mountain(self) -> bool:
        conditions = []

        # 첫번째 조건
        left_wrist = self.pose_list.find(Parts.leftWrist).position
        right_wrist = self.pose_list.find(Parts.RightWrist).position
        conditions.append(left_wrist.distance(right_wrist) in range(20, 160))

        # 두번째 조건 fixme: neck 이 없음
        some_result = self._compute_angle(Vector2D(1, 0), Vector2D(0, 0), Vector2D(0, 1))
        conditions.append(some_result)

        # 세번째 조건 fixme: 손인지 어딘지 모르겠음..
        some_result3 = 1 in range(80, 145)
        conditions.append(some_result3)

        return all(conditions)
