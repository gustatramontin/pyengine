import pygame as pg
from math import sin,cos, pi,sqrt
from sys import exit
from copy import deepcopy

h = 500
w = 500

screen = pg.display.set_mode((h,w))
clock = pg.time.Clock()

class Model:
    def __init__(self, obj):
        self.vertices = []
        self.faces = []
        f = open(obj, "r")
        for l in f:
            x = l.split()
            if x[0] == "v":
                self.vertices.append((float(x[1]), float(x[2]),float(x[3])))
            if x[0] == "f":
                f1,f2,f3 = tuple(map(lambda x: x.split("/"), x[1:]))

                v1 = int(f1[0])-1
                v2 = int(f2[0])-1
                v3 = int(f3[0])-1
                self.faces.append((v1,v2,v3))


    def transform(self, trans):
        new_points = []
        for p in self.vertices:
            new_points.append(trans(p))

        self.vertices = new_points


    def vrotate_y(self, theta, coord):
        x,y,z = coord
        return (x*cos(theta) + z*sin(theta), y, x*(- sin(theta)) + z*cos(theta))

    def vtranslate(self, trans, coord):
        x,y,z = coord
        tx,ty,tz = trans
        return (x+tx, y+ty, z+tz)

    def rotate_y(self, theta):
        self.transform(lambda x: self.vrotate_y(theta, x))
    def translate(self, trans):
        self.transform(lambda x: self.vtranslate(trans, x))

def project(x,y,z):
    z_near = 1
    xp = x/(z_near*z)
    yp = y/(z_near*z)
    return (xp, yp)


puppy = Model("french_bulldog.obj")
def render_model(model):
    global w,h,screen

    points = model.vertices

    projected_points = []
    pp = []
    for p in points:
        x,y,z = p
        xp,yp = project(x,y,z)
        xp,yp = (xp+1)*(w/2), ((yp)+1)*(h/2)
        pp.append((xp,yp))
        pg.draw.circle(screen, (255,0,0), (xp,yp), 1)
    for f in model.faces:
        
        pg.draw.line(screen, (0,0,0), pp[f[0]], pp[f[1]])
        pg.draw.line(screen, (0,0,0), pp[f[0]], pp[f[2]])
        pg.draw.line(screen, (0,0,0), pp[f[1]], pp[f[2]])

angle = 0
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
    screen.fill((255,255,255))
    new_model = deepcopy(puppy)
    new_model.rotate_y(angle)
    new_model.translate((0,-5,-15))
    render_model(new_model)
    angle += 0.01
    pg.display.flip()

    clock.tick(60)


