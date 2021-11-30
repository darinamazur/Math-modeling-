import core
import interface
import numpy

gui = interface.GUI()
gui.Window_1()
S_0 = []
obs_area_0 = []
obs_area_g = []
t_a = 0
t_b = 0
m_0_points = []
m_g_points = []

if len(gui.rectangle) != 0:
    x_rect = gui.rectangle[0]
    y_rect = gui.rectangle[0]
    S_0 = [[0, 0], [0, y_rect], [x_rect, y_rect], [x_rect, 0]]
    x_subrect = gui.subrectangle[0]
    y_subrect = gui.subrectangle[0]
    obs_area_0 = [[0, 0], [0, y_subrect], [x_subrect, y_subrect], [x_subrect, 0]]
else:
    for i in range(0, len(gui.arrS0x2)):
        S_0.append([gui.arrS0x2[i], gui.arrS0y2[i]])
    for i in range(0, len(gui.subx2)):
        obs_area_0.append([gui.subx2[i], gui.suby2[i]])
for i in range(0, len(gui.contour_x)):
    obs_area_g.append([gui.contour_x[i], gui.contour_y[i]])
t_a = gui.t1
t_b = gui.t2

for i in range(0, len(gui.M0x2)):
    m_0_points.append([gui.M0x2[i], gui.M0y2[i], gui.M0z2[i]])
for i in range(0, len(gui.Mgx2)):
    m_g_points.append([gui.Mgx2[i], gui.Mgy2[i], gui.Mgz2[i]])

c = core.core()
c.set_T(gui.process.T)
c.set_S_0(S_0)
if gui.process.func == "x+y+t":
    func_tmp = lambda x, y, t: x + y + t
    c.set_observation_function(func_tmp)
elif gui.process.func == "t*(sin(x)+cos(y))":
    func_tmp = lambda x, y, t: t*(math.sin(x)+math.cos(y))
    c.set_observation_function(func_tmp)
else:
    func_tmp = lambda x, y, t: 0
    c.set_observation_function(func_tmp)

if gui.process.func == "1/(2*pi)*ln(1/r)":
    func_tmp = lambda x, y, t: 1 / (2 * math.pi) * math.log(1 / math.sqrt(x**2 + y**2))
    c.set_green_function(func_tmp)
elif gui.process.func == "H(t-r/c)/(2*pi*c*sqrt(c^2*t^2-r^2))":
    cons = gui.process.const
    func_tmp = lambda x, y, t: numpy.heaviside(t - math.sqrt(x**2 + y**2) / cons, 1)/(2 * math.pi * cons * math.sqrt(cons ** 2* t ** 2- (x**2 + y**2) ** 2))
    c.set_green_function(func_tmp)
else:
    func_tmp = lambda x, y, t: 0
    c.set_green_function(func_tmp)



с.push_observation_area([obs_area_0, [0.0, 0.0]])
с.push_observation_area([obs_area_п, [t_a, t_b]])
c.set_m0_size(len(m_0_points))
for i in range(0, len(m_0_points)):
    c.push_modeling_point(m_0_points[i])
for i in range(0, len(m_g_points)):
    c.push_modeling_point(m_g_points[i])

c.solve()
c.print_py_plot(0)
c.print_py_plot(t_a)
c.print_py_plot((t_a + t_b) * 0.5)
c.print_py_plot(t_b)



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



