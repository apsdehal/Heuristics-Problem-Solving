from coordinate import Coordinate
class Prey:
    def __init__(self,info):
        self.x_coord = info['prey'].x
        self.y_coord = info['prey'].y
        hunter_x = info['hunter'].x
        hunter_y = info['hunter'].y


    def move(self,info):
        resp = {}
        resp['gameNum'] = info['gameNum']
        resp['tickNum'] = info['tickNum']

        if int(resp['tickNum']) % 2 == 0:
            resp['x'] = self.x_coord
            resp['y'] = self.y_coord
        else:
            if(self.x_coord >= hunter_x ):
                resp['x'] = self.x_coord + 1
            else:
                resp['x'] = self.x_coord - 1
            if(self.y_coord >= hunter_y):
                resp['y'] = self.y_coord + 1
            else:
                resp['y'] = self.y_coord - 1

        return resp
