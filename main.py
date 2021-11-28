import core
# import interface
#
# gui = interface.GUI()
# gui.Window_1()
# S_0 = []
# obs_area_0 = []
# obs_area_g = []
# t_a = 0
# t_b = 0




# if len(gui.rectangle) != 0:
#     x_rect = gui.rectangle[0]
#     y_rect = gui.rectangle[0]
#     S_0 = [[0, 0], [0, y_rect], [x_rect, y_rect], [x_rect, 0]]
#     x_subrect = gui.subrectangle[0]
#     y_subrect = gui.subrectangle[0]
#     obs_area_0 = [[0, 0], [0, y_subrect], [x_subrect, y_subrect], [x_subrect, 0]]
# else:
#     for i in range(0, len(gui.arrS0x2)):
#         S_0.append([gui.arrS0x2[i], gui.arrS0y2[i]])
#     for i in range(0, len(gui.subx2)):
#         obs_area_0.append([gui.subx2[i], gui.suby2[i]])
# for i in range(0, len(gui.contour_x)):
#     obs_area_g.append([gui.contour_x[i], gui.contour_y[i]])
# t_a = gui.t1
# t_b = gui.t2












tmp = core.core()


tmp.set_T(10)
tmp.set_m0_size(1)

s_0 = [[0, 0],[0, 2], [1, 3], [2, 2],[2, -3], [1, -2]]
tmp.set_S_0(s_0)


f_tmp = lambda x, y, t:  (x * (2.0 - x) + y * (2.0 - y) + 0.1 * t) * 0.01
tmp.set_observation_function(f_tmp)

tmp.push_observation_area([s_0, [0.0, 0.0]])
tmp.push_observation_area([s_0, [1.0, 2.0]])

# print(tmp.get_all_observation_areas())

tmp.push_modeling_point([1.0, 1.5, -1.2])
tmp.push_modeling_point([1.0, -1.0, 0.3])

tmp.solve()

tmp.print_py_plot(0)
# tmp.print_py_plot(1)
tmp.print_py_plot(1.5)
# tmp.print_py_plot(2.0)



