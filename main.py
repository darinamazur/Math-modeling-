#import database

import numpy
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator

# import matplotlib

# db = database.DataBase()
# db.ShowTables()
# db.SelectAllTable('PROCESS')
# db.ShowTable('PROCESS')
# res = db.SelectGreenFunction('Хвильове рівняння', 2)
# print(res)
# res = db.SelectDiffOperator('Хвильове рівняння', 2)
# print(res)


import core

tmp = core.core()
tmp.set_T(10)
tmp.set_m0_size(1)

s_0 = [[0, 0],[0, 2],[2, 2],[2, 0]]
tmp.set_S_0(s_0)

f_tmp = lambda x, y, t:  x ** 2 + y ** 2 + 0.1 * t
tmp.set_observation_function(f_tmp)

tmp.push_observation_area([s_0, [0, 0]])
# tmp.push_observation_area([s_0, [1, 2]])

# print(tmp.get_all_observation_areas())

tmp.push_modeling_point([1, 1.5, -5])
# tmp.push_modeling_point([1, -1, 0.3])


# print(tmp.get_obs_area_i_j(0))
print(tmp.__get_m_size__())
tmp.solve()

print(tmp.get_f_modeled(1, 1, 2))
print(tmp.get_f_modeled(1, 1.5, 2))


fig, ax = plt.subplots(subplot_kw={"projection": "3d"})


x = numpy.linspace(0, 2, 30)
y = numpy.linspace(0, 2, 30)
t = 0.7
z = []


# for i in range(0, len(x)):
#     z.append(tmp.get_f_modeled(x[i], y[i], t))
X, Y = numpy.meshgrid(x, y)
Z = tmp.get_f_modeled_meshgrid(X, Y, t)

# t2 = X + Y
#
# print(t2.shape)
# print(t2)

print(X[1])
print(Y[1])

# ax.set_xlim([0, 2])
# ax.set_ylim([0, 2])

surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)
# surf = ax.plot_wireframe(X, Y, Z)


fig.colorbar(surf, shrink=0.5, aspect=5)
plt.show()


