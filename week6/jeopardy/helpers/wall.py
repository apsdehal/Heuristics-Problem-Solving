class Wall:
    HORIZONTAL = 0
    VERTICAL = 1
    def __init__(self, wallType, coord, start, end):
        # 0 for horizontal, 1 for vertical
        self.type = wallType
        self.coord = coord
        self.start = start
        self.end = end

    def occupies(self, coord):
        if self.type == self.HORIZONTAL:
            return coord.y == self.coord and self.start <= coord.x and self.end >= coord.x
        elif self.type == self.VERTICAL:
            return coord.x == self.coord and self.start <= coord.y and self.end >= coord.y

        # We should not be here technically, just in case
        return 0
