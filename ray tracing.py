from settings import *
from classes import *
from PIL import Image
import numpy as np
import time


def throw_ray(ray, iteration=0):
    # find nearest figure
    if iteration >= 10:
        return [0] * 3
    dots = []
    fig = []
    for figure in scene:
        if figure.is_intersect(ray):
            dots += figure.is_intersect(ray)
            for i in range(len(figure.is_intersect(ray))):
                fig.append(figure)
    len_of_vec = []
    if len(dots) == 0:
        return [0] * 3
    for dot in dots:
        v = Vector(dot - person)
        len_of_vec.append(v.length())
    dist = float("inf")
    index = -1
    for i in range(len(len_of_vec)):
        length = len_of_vec[i]
        if length < MAX_DIST and length < dist:
            dist = length
            index = i
    if is_in_shadow(dots[index]):
        return [0] * 3
    elif fig[index].name == "sun":
        return [255] * 3
    else:
        # Fong's formula
        k_a = fig[index].k_a
        k_d = fig[index].k_d
        k_s = fig[index].k_s
        p = fig[index].p
        I = sun.color
        v = Vector(dots[index] - person)
        v /= v.length()
        l = Vector(sun.center - dots[index])
        l /= l.length()
        n = fig[index].normal(dots[index])
        n /= n.length()
        r = l - n / 0.5 / (1 / (l * n))
        r /= r.length()
        color = fig[index].color
        angle_n_l = math.cos(find_angle_between_vectors(n, l))
        if angle_n_l <= 0:
            angle_n_l = -angle_n_l
        angle_v_r = 1 - math.cos(find_angle_between_vectors(n, v) - find_angle_between_vectors(l, n))
        if angle_v_r <= 0:
            angle_v_r = -angle_v_r
        red = color[0] * (k_a + k_d * angle_n_l) + I[0] * k_s * angle_v_r ** p
        green = color[1] * (k_a + k_d * angle_n_l) + I[1] * k_s * angle_v_r ** p
        blue = color[2] * (k_a + k_d * angle_n_l) + I[2] * k_s * angle_v_r ** p
        second_ray = calculate_second_ray(ray, dots[index], fig[index], iteration)
        red = min(red + second_ray[0], 255)
        green = min(green + second_ray[1], 255)
        blue = min(blue + second_ray[2], 255)
        return [red, green, blue]


def is_in_shadow(dot):
    global sun, scene
    v = Ray(sun.center - dot, dot, [0] * 3)
    v /= v.length()
    dot = Dot(dot.x + 2 * v.x, dot.y + 2 * v.y, dot.z + 2 * v.z)
    v = Ray(v, dot, [0] * 3)
    for figure in scene:
        if figure.is_intersect(v) and figure.name != "sun":
            return figure
    return False


def calculate_second_ray(ray, dot, figure, iteration):
    n = figure.normal(dot)
    n /= n.length()
    r = ray - n / 0.5 / (1 / (ray * n))
    r /= r.length()
    r = Ray(Dot(r.x, r.y, r.z), dot, [0] * 3)
    out = throw_ray(r, iteration + 1)
    out = [figure.reflection * i for i in out]
    return out


def find_angle_between_vectors(a, b):
    alpha = (a.x * b.x + a.y * b.y + a.z * b.z) /\
            ((a.x ** 2 + a.y ** 2 + a.z ** 2) ** 0.5 + (b.x ** 2 + b.y ** 2 + b.z ** 2) ** 0.5)
    return math.acos(alpha)


def render_gif(start_x=0, start_y=-600, start_z=0):
    global sun
    t0 = time.time()
    frames = []
    k = 360
    l = 1000
    angle = 360 / k * math.pi / 180
    for i in range(k):
        screen = [[(0, 0, 0) for j in range(WIDTH)] for i in range(HEIGHT)]
        sun = Sphere(Dot(start_x + l * math.sin(angle * i), start_y, start_z + l * math.cos(angle * i)), 10,
                     [255] * 3, name="sun")
        print(sun.center.x, sun.center.y, sun.center.z)
        del(scene[-1])
        scene.append(sun)
        #print(scene)
        screen = [[(0, 0, 0) for j in range(WIDTH)] for i in range(HEIGHT)]
        for x in range(WIDTH):
            for y in range(HEIGHT):
                screen[y][x] = throw_ray(
                        Ray(Vector(Dot(x - WIDTH // 2 - person.x, y - HEIGHT // 2 - person.y, -person.z)),
                        person, [0, 0, 0]))
        screen = np.asarray(screen)
        image = screen.copy()
        image = Image.fromarray(image.astype('uint8'), "RGB")
        frames.append(image)
    frames[0].save("ray-tracing.gif", save_all=True, append_images=frames[1:], duration=100, loop=0, optimize=True)
    print(time.time() - t0)


def render_png():
    t0 = time.time()
    screen = [[(0, 0, 0) for j in range(WIDTH)] for i in range(HEIGHT)]
    for x in range(WIDTH):
        for y in range(HEIGHT):
            screen[y][x] = throw_ray(Ray(Vector(Dot(x - WIDTH // 2 - person.x, y - HEIGHT // 2 - person.y, -person.z)),
                                         person, [0, 0, 0]))
    screen = np.asarray(screen)
    image = Image.fromarray(screen.astype('uint8'), "RGB")
    image.save("screen.png")
    print(time.time() - t0)


if __name__ == "__main__":
    render_png()
