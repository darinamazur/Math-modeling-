#import database

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

f_tmp = lambda x, y, t: x + y + 0.1 * t
tmp.set_observation_function(f_tmp)

tmp.push_observation_area([s_0, [0, 0]])
# tmp.push_observation_area([s_0, [1, 2]])

# print(tmp.get_all_observation_areas())

tmp.push_modeling_point([1, 1, -1])
# tmp.push_modeling_point([1, -1, 0.3])

# print(tmp.get_obs_area_i_j(0))
print(tmp.__get_m_size__())



tmp.solve()
