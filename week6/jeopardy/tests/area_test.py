from helpers.hunter import Hunter
from helpers.coordinate import Coordinate
from helpers.wall import Wall

if __name__ == '__main__':

    info = {}
    info['maxWalls'] = 1
    info['wallPlacementDelay'] = 1
    info['boardSizeX'] = 300
    info['boardSizeY'] = 300

    info['walls'] = []
    info['walls'].append(Wall(0, 4, 0, 299))
    info['walls'].append(Wall(0, 5, 0, 299))
    info['walls'].append(Wall(0, 6, 0, 299))
    info['walls'].append(Wall(0, 7, 0, 299))
    info['currentWallTimer'] = 0

    hunter = Hunter(info)
    hunter.walls = info['walls']
    hunter.preyCoord = Coordinate(230, 200)

    print hunter.preyArea(hunter.walls)
