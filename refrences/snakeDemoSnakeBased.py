from __future__ import annotations
from typing import Any
import ctypes
import math

global BOARD


def createBoard(size: int = 8) -> None:
    global BOARD
    BOARD: list[list[bytes | None]] = [[None for _ in range(size)] for _ in range(size)]


class int2:
    def __init__(self: int2, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y

    def __len__(self: int2) -> int:
        return 2

    def length(self: int2) -> float:
        return math.sqrt([val**2.0 for val in [self.x, self.y]])

    def __getitem__(self: int2, key: str | int):
        if type(key) is int:
            return [self.x, self.y][key % 2]
        return self.to_dict().get(key, 0)

    def to_dict(self: int2) -> dict[str, int]:
        return {"x": self.x, "y": self.y}


class Snake:
    def __init__(self: Snake, starting: int2, length: int = 3) -> None:
        self.length: int = length
        self.children: list[int2] = [starting]


class Apple:
    def __init__(self: Apple) -> None:
        pass


def gameWon(snakeAddress: bytes) -> bool:
    for row in BOARD:
        for address in row:
            if address != snakeAddress:
                return False
    return True


def main() -> None:
    global BOARD

    size: int = 10

    snake: Snake = Snake()
    snakeAddress: bytes = id(snake)

    while True:
        createBoard(size)
        while not gameWon(snakeAddress):
            pass
        else:
            print("You Won")
            continue
        print("You Lost")


def ramMain() -> None:
    my_list: list[int] = [10, 20, 30]
    mem_address: bytes = id(my_list)
    print(f"Memory Address (Decimal): {mem_address}")
    print(f"Memory Address (Hex): {hex(mem_address)}")
    retrieved_obj: Any = ctypes.cast(mem_address, ctypes.py_object).value
    print(f"Retrieved Object: {retrieved_obj}")
    print(f"Are they the exact same object? {retrieved_obj is my_list}")


if __name__ == "__main__":
    main()
