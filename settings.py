from classes import *

WIDTH = 720
HEIGHT = 540
MAX_DIST = 1e15
FOV = 90  # in degrees
distance_to_screen = (WIDTH / 2) / math.tan(FOV / 2 * math.pi / 180)
person = Dot(1, 1, -distance_to_screen)  # x=1 and y=1 made because of artifacts
# place sun
sun = Sphere(Dot(0, -600, -500), 0.01, [255] * 3, name="sun")
# here place your figures
scene = [
    Sphere(Dot(100, 100, 500), 100, [0, 255, 0], k_s=40, p=6, reflection=0),
    Sphere(Dot(-300, -200, 500), 200, [255, 255, 0], k_s=40, p=6, reflection=0.8),
    Surface(Dot(0, 500, 0), Dot(0, 500, 1), Dot(1, 500, 0), [255, 0, 255]),
    sun
]
