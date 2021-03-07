import numba as nb
import numpy as np

from .. import Shape, logic, utility


class Cube(Shape):
    def __init__(self, min_box, max_box):
        super().__init__()
        if type(min_box) == list or type(max_box) == list:
            min_box = np.array(min_box, dtype=np.float64)
            max_box = np.array(max_box, dtype=np.float64)
        self.min: np.ndarray = min_box
        self.max: np.ndarray = max_box
        self.box: logic.Box = logic.Box(self.min, self.max)

    def compile(self):
        pass

    def bounding_box(self) -> logic.Box:
        return self.box

    def contains(self, v: np.ndarray, f: float) -> bool:
        for i in range(3):
            if (v[i] < (self.min[i] - f)) or (v[i] > (self.max[i] + f)):
                return False
        return True

    def intersect(
        self, ray_origin: np.ndarray, ray_direction: np.ndarray
    ) -> logic.Hit:
        ok, root = Cube._intersect(
            self.min, self.max, ray_origin, ray_direction
        )
        if ok:
            return logic.Hit(self, root)
        else:
            return logic.NoHit

    @staticmethod
    @nb.njit(cache=True)
    def _intersect(
        min_box: np.ndarray,
        max_box: np.ndarray,
        ray_origin: np.ndarray,
        ray_direction: np.ndarray,
    ) -> (bool, float):
        n = (min_box - ray_origin) / ray_direction
        f = (max_box - ray_origin) / ray_direction
        n, f = np.minimum(n, f), np.maximum(n, f)
        t0, t1 = np.amax(n), np.amin(f)
        if t0 < 1e-3 < t1:
            return True, t1
        if 1e-3 <= t0 < t1:
            return True, t0
        return False, 0

    def paths(self) -> logic.Paths:
        x1, y1, z1 = self.min[0], self.min[1], self.min[2]
        x2, y2, z2 = self.max[0], self.max[1], self.max[2]
        paths = [
            [[x1, y1, z1], [x1, y1, z2]],
            [[x1, y1, z1], [x1, y2, z1]],
            [[x1, y1, z1], [x2, y1, z1]],
            [[x1, y1, z2], [x1, y2, z2]],
            [[x1, y1, z2], [x2, y1, z2]],
            [[x1, y2, z1], [x1, y2, z2]],
            [[x1, y2, z1], [x2, y2, z1]],
            [[x1, y2, z2], [x2, y2, z2]],
            [[x2, y1, z1], [x2, y1, z2]],
            [[x2, y1, z1], [x2, y2, z1]],
            [[x2, y1, z2], [x2, y2, z2]],
            [[x2, y2, z1], [x2, y2, z2]],
        ]
        return logic.Paths(paths)