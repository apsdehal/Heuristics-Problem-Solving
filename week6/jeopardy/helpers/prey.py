from coordinate import Coordinate
class Prey:
    def __init__(self,info):
    	self.x_coord = info['prey'].x
    	self.y_coord = info['prey'].y

    def move(self,info):
        resp = {}
        resp['gameNum'] = info['gameNum']
        resp['tickNum'] = info['tickNum']

        if int(resp['tickNum']) % 2 == 0:
            resp['x'] = self.x_coord
            resp['y'] = self.y_coord
        else:
            resp['x'] = self.x_coord + info['hunter'].vx
            resp['y'] = self.y_coord + info['hunter'].vy

        return resp
