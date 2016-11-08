from coordinate import Coordinate
from wall import Wall
import math
class Prey:
    def __init__(self,info):
        self.x_coord = info['prey'].x
        self.y_coord = info['prey'].y
        self.hunter_x = info['hunter'].x
        self.hunter_y = info['hunter'].y
        self.hunter_vx = info['hunter'].vx
        self.hunter_vy = info['hunter'].vy


    def move(self,info):
    	self.x_coord = info['prey'].x
        self.y_coord = info['prey'].y
        self.hunter_x = info['hunter'].x
        self.hunter_y = info['hunter'].y
        self.hunter_vx = info['hunter'].vx
        self.hunter_vy = info['hunter'].vy
        resp = {}
        resp['gameNum'] = info['gameNum']
        resp['tickNum'] = info['tickNum']
        if int(resp['tickNum']) % 2 == 0:
            resp['x'] = 0
            resp['y'] = 0
            return resp
        dist = math.pow(self.x_coord - self.hunter_x,2) + math.pow(self.y_coord -self.hunter_y ,2)
        if(dist>225):
            #225 because I am not taking sqaure root
            if(self.hunter_x > self.x_coord):
                resp['x'] = 1
            else:
                resp['x'] = -1
            if(self.hunter_y > self.y_coord):
                resp['y'] = 1
            else:
                resp['y'] = -1
            return resp
        else:
            x_dist = abs(self.hunter_x-self.x_coord)
            y_dist = abs(self.hunter_y-self.y_coord)
            x_dist_future = abs(self.hunter_x + self.hunter_vx -self.x_coord)
            y_dist_future = abs(self.hunter_y + self.hunter_vy -self.y_coord)
            if(x_dist_future < x_dist and y_dist_future<y_dist):
                if(x_dist<y_dist):
                    resp['x'] = 0-self.hunter_vx
                    resp['y'] = self.hunter_vy
                else:
                    resp['x'] = self.hunter_vx
                    resp['y'] = 0-self.hunter_vy
            elif(x_dist_future < x_dist):
                resp['x'] = self.hunter_vx
                resp['y'] = 0-self.hunter_vy
            elif(y_dist_future<y_dist):
                resp['x'] = 0-self.hunter_vx
                resp['y'] = self.hunter_vy
            else:
                resp['x'] = 0
                resp['y'] = 0
            print dist, " vx:", self.hunter_vx, " vy:", self.hunter_vy, " resp:", resp['x'], ",", resp['y']
            return resp

