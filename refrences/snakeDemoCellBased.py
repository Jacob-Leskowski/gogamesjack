from __future__ import annotations
from typing import Generator
import math


def expendAxis(number: int | float | Vector, axis: int = 2) -> Vector:
    if type(number) is Vector:
        curAxis: int = len(number)
        if curAxis == axis:
            return number
        elif curAxis < axis:
            currentVals: list[int] = 0
            for idx, val in enumerate(number.values):
                currentVals[idx] = val
            return Vector(*currentVals)
        else:
            return Vector(*currentVals[:axis])
    line: Vector = Vector(1)
    line[0] = int(number)
    return expendAxis(line, axis)


class Vector:
    def init(self: Vector, dimentions: int = 2) -> None:
        self.values: list[int] = [0 for _ in range(min(max(dimentions, 0), 4))]

    def __iter__(self: Vector) -> Generator:
        return self

    def __getitem__(self: Vector, key: int):
        return self.values[key % len(self)]

    def __setitem__(self: Vector, key: int, value: int | float):
        self.values[key % len(self)] = int(value)

    def __next__(self: Vector) -> int:
        pass

    def __len__(self: Vector) -> int:
        return len(self.values)

    def __total__(self: Vector) -> int:
        return sum(self.values)

    def length(self: Vector) -> float:
        return math.sqrt(sum([val**2 for val in self.values]))

    def opper(
        self: Vector, other: int | float | Vector, opp: lambda x, y: x + y
    ) -> Vector:
        other: Vector = expendAxis(other, len(self))
        return Vector(*[opp(self[index], other[index]) for index in range(len(self))])
