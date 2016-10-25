from coordinate import Coordinate
class Prey:
    def __init__(self,info):
    	self.x_coord = info['prey'].x 
    	self.y_coord = info['prey'].y

    def move(self,info):
        resp['gameNum'] = info['gameNum']
        resp['tickNum'] = info['tickNum']

        resp['x'] = self.x_coord + info['hunter'].vx
        resp['y'] = self.y_coord + info['hunter'].vy

        return resp