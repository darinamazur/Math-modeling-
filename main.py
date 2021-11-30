import core
import interface
import numpy





exit(0)




tmp = core.core()


tmp.set_T(10)
tmp.set_m0_size(1)
s_0 = [[0, 0],[0, 2], [1, 3], [2, 2],[2, -3], [1, -2]]
tmp.set_S_0(s_0)
f_tmp = lambda x, y, t:  (x * (2.0 - x) + y * (2.0 - y) + 0.1 * t) * 0.01
tmp.set_observation_function(f_tmp)
tmp.push_observation_area([s_0, [0.0, 0.0]])
tmp.push_observation_area([s_0, [1.0, 2.0]])
tmp.push_modeling_point([1.0, 1.5, -1.2])
tmp.push_modeling_point([1.0, -1.0, 0.3])

tmp.solve()

tmp.print_py_plot(0)
tmp.print_py_plot(1.0)
tmp.print_py_plot(1.5)
tmp.print_py_plot(2.0)



