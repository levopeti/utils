import sys
import numpy as np
import matplotlib.pyplot as plt
import cv2
import threading, time


def load_params():
    pass


def inside_fn():
    pass


def press(event):
    global changed
    sys.stdout.flush()

    event_handler(event.key)
    changed = True


def increase(key, ind, d):
    if isinstance(ind, int):
        parameters_dict[key][ind] += d
    elif isinstance(ind, list):
        parameters_dict[key][ind[0], ind[1]] += d

    print("{} = {}".format(key, parameters_dict[key]))


def decrease(key, ind, d):
    if isinstance(ind, int):
        parameters_dict[key][ind] -= d
    elif isinstance(ind, list):
        parameters_dict[key][ind[0], ind[1]] -= d

    print("{} = {}".format(key, parameters_dict[key]))


def event_handler(event_key):
    global v_box_view_mult, inc, dec, parameters_dict, v_box_view_add
    df = 20
    dp = 0.2
    dxyz = 0.2
    dypr = 0.2
    dml = 0.1
    ddist = 0.5

    if event_key == 'left':
        try:
            dec()
        except Exception:
            print("Choose a value to change!")
    elif event_key == 'right':
        try:
            inc()
        except Exception:
            print("Choose a value to change!")
    ##### cam mat #####
    # f1
    elif event_key == '1':
        inc = lambda: increase("cam_mat", [0, 0], df)
        dec = lambda: decrease("cam_mat", [0, 0], df)
        print("f1")
    # f2
    elif event_key == '2':
        inc = lambda: increase("cam_mat", [1, 1], df)
        dec = lambda: decrease("cam_mat", [1, 1], df)
        print("f2")
    # p1
    elif event_key == '3':
        inc = lambda: increase("cam_mat", [2, 0], dp)
        dec = lambda: decrease("cam_mat", [2, 0], dp)
        print("p1")
    # p2
    elif event_key == '4':
        inc = lambda: increase("cam_mat", [2, 1], dp)
        dec = lambda: decrease("cam_mat", [2, 1], dp)
        print("p2")
    ##### pos meter #####
    # x
    elif event_key == '5':
        inc = lambda: increase("pos_meter", 0, dxyz)
        dec = lambda: decrease("pos_meter", 0, dxyz)
        print("x")
    # y
    elif event_key == '6':
        inc = lambda: increase("pos_meter", 1, dxyz)
        dec = lambda: decrease("pos_meter", 1, dxyz)
        print("y")
    # z
    elif event_key == '7':
        inc = lambda: increase("pos_meter", 2, dxyz)
        dec = lambda: decrease("pos_meter", 2, dxyz)
        print("z")
    ##### ypr deg #####
    # yaw
    elif event_key == '8':
        inc = lambda: increase("ypr_deg", 0, dypr)
        dec = lambda: decrease("ypr_deg", 0, dypr)
        print("yaw")
    # pitch
    elif event_key == '9':
        inc = lambda: increase("ypr_deg", 1, dypr)
        dec = lambda: decrease("ypr_deg", 1, dypr)
        print("pitch")
    # roll
    elif event_key == 'ö':
        inc = lambda: increase("ypr_deg", 2, dypr)
        dec = lambda: decrease("ypr_deg", 2, dypr)
        print("roll")
    ##### v_box_view_mult #####
    # vbm0
    elif event_key == 'y':
        inc = lambda: increase("v_box_view_mult", 0, dml)
        dec = lambda: decrease("v_box_view_mult", 0, dml)
        print("vbm0")
    # vbm1
    elif event_key == 'x':
        inc = lambda: increase("v_box_view_mult", 1, dml)
        dec = lambda: decrease("v_box_view_mult", 1, dml)
        print("vbm1")
    # vbm2
    elif event_key == 'c':
        inc = lambda: increase("v_box_view_mult", 2, dml)
        dec = lambda: decrease("v_box_view_mult", 2, dml)
        print("vbm2")
    ##### v_box_view_add #####
    # vba0
    elif event_key == 'v':
        inc = lambda: increase("v_box_view_add", 0, dml)
        dec = lambda: decrease("v_box_view_add", 0, dml)
        print("vba0")
    # vba1
    elif event_key == 'b':
        inc = lambda: increase("v_box_view_add", 1, dml)
        dec = lambda: decrease("v_box_view_add", 1, dml)
        print("vba1")
    # vba2
    elif event_key == 'n':
        inc = lambda: increase("v_box_view_add", 2, dml)
        dec = lambda: decrease("v_box_view_add", 2, dml)
        print("vba2")

    ##### distortion #####
    # d0
    elif event_key == 'm':
        inc = lambda: increase("dist", 0, ddist)
        dec = lambda: decrease("dist", 0, ddist)
        print("d0")
    # d1
    elif event_key == ',':
        inc = lambda: increase("dist", 1, ddist)
        dec = lambda: decrease("dist", 1, ddist)
        print("d1")
    # d2
    elif event_key == '.':
        inc = lambda: increase("dist", 2, ddist)
        dec = lambda: decrease("dist", 2, ddist)
        print("d2")
    # d3
    elif event_key == '-':
        inc = lambda: increase("dist", 3, ddist)
        dec = lambda: decrease("dist", 3, ddist)
        print("d3")

    elif event_key == 'p':
        print_parameters()
    elif event_key == 'r':
        print_parameters()
        load_camera_params()
        parameters_dict['v_box_view_mult'][::] = [1, 1, 1, 1]
        parameters_dict['v_box_view_add'][::] = [0, 0, 0, 0]
        print("reset parameters")


def print_parameters():
    print()


def draw_loop():
    global changed
    while True:
        if changed:
            changed = False
            inside_img = img.copy()
            image_to_imshow = indside_fn()
            try:
                ax.imshow(image_to_imshow[..., ::-1])
                fig.canvas.draw()
            except Exception as e:
                print(e)
                pass
        time.sleep(0.2)


def main():
    global fig, ax
    load_camera_params()

    plt.rcParams["figure.figsize"] = (20, 12)
    fig, ax = plt.subplots()

    fig.canvas.mpl_connect('key_press_event', press)
    inside_img = img.copy()
    image_to_imshow = render_image(inside_img, pos_meter, ypr_deg, data_dict, cam_mat, dist)
    ax.imshow(image_to_imshow[..., ::-1])

    threading.Thread(target=draw_loop).start()

    plt.show()


if __name__ == "__main__":
    main()
