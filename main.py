# import polygon
#
# tmp = polygon.polygon([[2, 1], [3, -1], [3, -2], [2, -3], [-1, -3], [-2, 0], [1, 2]])
# print(tmp.sorted_arr)
# x = -2.0
# print(f' x = {x} min = {tmp.get_bottom_border(x)} max = {tmp.get_top_border(x)}')
#
#
# exit(0)







#import database

import numpy


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

f_tmp = lambda x, y, t:  (x * (2.0 - x) + y * (2.0 - y) + 0.1 * t) * 0.01
tmp.set_observation_function(f_tmp)

tmp.push_observation_area([s_0, [0.0, 0.0]])
tmp.push_observation_area([s_0, [1.0, 2.0]])

# print(tmp.get_all_observation_areas())

tmp.push_modeling_point([1.0, 1.5, -1.2])
tmp.push_modeling_point([1.0, -1.0, 0.3])


# print(tmp.get_obs_area_i_j(0))
print(tmp.__get_m_size__())
tmp.solve()

print(tmp.get_f_modeled(1, 1, 2))
print(tmp.get_f_modeled(1, 1.5, 2))

tmp.print_py_plot(0)
tmp.print_py_plot(1)
tmp.print_py_plot(1.5)
tmp.print_py_plot(2.0)



