from helpers.hunter import Hunter
from helpers.bounce import hunterNextMove
from helpers.coordinate import Coordinate
from helpers.wall import Wall

if __name__ == '__main__':

    info = {}
    info['maxWalls'] = 1
    info['wallPlacementDelay'] = 1
    info['boardSizeX'] = 300
    info['boardSizeY'] = 300

    info['walls'] = []
    info['walls'].append(Wall(0, 94, 0, 299))
    info['walls'].append(Wall(0, 127, 0, 299))
    info['currentWallTimer'] = 0

    info['hunter'] = Coordinate(299, 135, 1 , 1)

    # Should be 299, 136
    print hunterNextMove(info)
