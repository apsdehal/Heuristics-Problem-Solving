class Wall:
    HORIZONTAL = 0
    VERTICAL = 1
    def __init__(self, type, coord, start, end):
        # 0 for horizontal, 1 for vertical
        self.type = wallType
        self.coord = coord
        self.start = start
        self.end = end

    def occupies(self, coord):
        if self.type == HORIZONTAL:
            return coord.y == self.coord.y and self.coord.start <= coord.x and self.coord.end >= coord.x
        elif self.type == VERTICAL:
            return coord.x == self.coord.x and self.coord.start <= coord.y and self.coord.end >= coord.y

        # We should not be here technically, just in case
        return 0
