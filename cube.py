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
            if l == "\n":
                continue
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
    def vrotate_z(self, theta, coord):
        x,y,z = coord
        return (x, y*cos(theta) + z*-sin(theta), y*sin(theta) + z*cos(theta))

    def vtranslate(self, trans, coord):
        x,y,z = coord
        tx,ty,tz = trans
        return (x+tx, y+ty, z+tz)

    def rotate_y(self, theta):
        self.transform(lambda x: self.vrotate_y(theta, x))
    def rotate_z(self, theta):
        self.transform(lambda x: self.vrotate_z(theta, x))
    def translate(self, trans):
        self.transform(lambda x: self.vtranslate(trans, x))

def project(x,y,z):
    z_near = 1
    xp = x/(z_near*z)
    yp = y/(z_near*z)
    return (xp, yp)
def crossp(v1,v2):
    x,y,z = v1
    x2,y2,z2 = v2
    return (y*z2 - z*y2, z*x2 - x*z2, x*y2 - y*x2)
def dotp(v1,v2):
    x,y,z = v1
    x2,y2,z2 = v2
    return (x*x + y*y2 + z*z2)
    
def length(v):
    return sqrt(v[0]**2 + v[1]**2 + v[2]**2 )

def versor(v):
    return tuple(map(lambda x: x/(length(v)), v))

puppy = Model("Ram_Skull_Scan.obj")
def render_model(model):
    global w,h,screen

    points = model.vertices

    projected_points = []
    pp = []
    for p in points:
        x,y,z = p
        xp,yp = project(x,y,z)
        xp,yp = (xp+1)*(w/2), ((-yp)+1)*(h/2)
        pp.append((xp,yp))
        #pg.draw.circle(screen, (255,0,0), (xp,yp), 1)

    faces = sorted(model.faces, key=lambda x: points[x[0]][2], reverse=False)
    for f in faces:
        x,y,z = points[f[0]]
        x1,y1,z1 = points[f[1]]
        x2,y2,z2 = points[f[2]]
        v1 =  versor(( x1 - x, y1 - y, z1- z))
        v2 =  versor(( x2 - x, y2 - y, z2- z))
        
        v3 = crossp(v2,v1)
        color = dotp((0.,0.0,-1), v3)*255
        color = color if color > 0 else 0

        pg.draw.polygon(screen, (color,0,0), [pp[f[0]], pp[f[1]],pp[f[2]]])       
        #pg.draw.line(screen, (0,0,0), pp[f[0]], pp[f[1]])
        #pg.draw.line(screen, (0,0,0), pp[f[0]], pp[f[2]])
        #pg.draw.line(screen, (0,0,0), pp[f[1]], pp[f[2]])

angle = 0
posx,posy,posz = 0,0,0
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                posy += 1
            if event.key == pg.K_s:
                posy -= 1
            if event.key == pg.K_a:
                posx -= 1
            if event.key == pg.K_d:
                posx += 1
            if event.key == pg.K_e:
                posz += 1
            if event.key == pg.K_q:
                posz -= 1
    screen.fill((255,255,255))
    new_model = deepcopy(puppy)
    new_model.rotate_z(pi)
    new_model.rotate_y(angle)
    new_model.translate((0,0,2))

    new_model.translate((posx, posy, posz))
    render_model(new_model)
    angle += 0.01
    pg.display.flip()

    clock.tick(60)


