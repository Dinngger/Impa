
class Pos:
    x: int
    y: int
    def __init__(self, x: int, y: int):
        ...

class Node:
    valid: bool
    type: int
    size: int
    color: int
    next_color: int
    another_pos: Pos

class Map:
    h: int
    w: int
    def get(self, pos: Pos) -> Node:
        ...
    def success(self) -> bool:
        ...
    def click(self, pos: Pos):
        ...
    def load(self, src: str):
        ...
