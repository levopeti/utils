import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import ray
import multiprocessing

ray.init(num_cpus=multiprocessing.cpu_count())

delta = 0.05
m = 1
k = 1
l_0 = 1
a = 0.4
omega = 1
phi = np.pi * 0


def dU_dx(U, x):
    # Here U is a vector such that y=U[0] and z=U[1]. This function should return [y', z']
    return [U[1], -1000 * U[1] - 2 * U[0] + 1 * np.cos(2 * x)]


def quad_dU_dx(U, t):
    # Here U is a vector such that y=U[0] and z=U[1]. This function should return [y', z']
    y = U[0]
    z = U[1]
    l = l_0 + a * np.cos(omega * t + phi)
    return [z, - k / m * (1 - (1 / (np.sqrt(1 + ((y * y) / (l * l)))))) * y - delta * z]


# y_0 = 1
# z_0 = 1
# U0 = [y_0, z_0]
# xs = np.linspace(0, 500, 10000)
# Us = odeint(quad_dU_dx, U0, xs)
# ys = Us[:, 0]
# phase_map = Us[:, 1]
#
# plt.xlabel("x")
# plt.ylabel("y")
# plt.title("Damped harmonic oscillator")
# plt.plot(xs, ys)
# plt.grid()
# plt.show()
#
# plt.plot(Us[:, 1], ys)
# plt.grid()
# plt.show()

limit = 0.2
indicate = False


@ray.remote
def func(y_0):
    inner_result = []

    for z_0 in np.linspace(-2, 2, 1000):
        U0 = [y_0, z_0]
        ts = np.linspace(0, 1000, 50)
        Us = odeint(quad_dU_dx, U0, ts)
        xs = Us[:, 0]
        vs = Us[:, 1]
        l_2 = np.sqrt(np.multiply(xs, xs) + np.multiply(vs, vs))

        if indicate:
            indicate_list = np.where(l_2 < limit, 1, 0)
            indicator = indicate_list.sum()

            if indicator:
                # no oscillation
                inner_result.append([y_0, z_0, 0])
            else:
                # oscillation
                inner_result.append([y_0, z_0, 1])
        else:
            minimum = l_2.min()
            inner_result.append([y_0, z_0, minimum])

    return inner_result


result = []

for y_0 in np.linspace(-2, 2, 1000):
    result.append(func.remote(y_0))

result = ray.get(result)

result = np.array(result)
result = result.reshape((result.shape[0] * result.shape[1], -1))

plt.scatter(result[:, 0], result[:, 1], c=result[:, 2], s=1)
plt.colorbar()
plt.show()

