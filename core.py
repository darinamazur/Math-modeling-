import math
import numpy
import polygon
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib
from matplotlib.ticker import LinearLocator

class core:
    def __init__(self):
        self.T = 0
        self.S_0 = []
        # self.obs_0 = []
        # self.obs_g = []
        self.obs = []
        self.obs_poly = []
        self.m_pts = []
        self.m0_size = 0
        self.green_is_setted = False

        # return 1

    def set_m0_size(self, val):
        self.m0_size = val

    def get_m0_size(self):
        return self.m0_size

# ============================================================
#     Setters and getters of formulations of the problems
# ============================================================

    def set_T(self, T):
        self.T = T

    def set_S_0(self, S_0_array):
        self.S_0 = S_0_array
        self.S_0_poly = polygon.polygon(self.S_0)

    def set_observation_function(self, func):
        self.func = func

    def set_green_function(self, func):
        self.G_func = func
        self.green_is_setted = True

    def get_T(self):
        return self.T

    def get_S_0(self):
        return self.S_0_array

    def get_observation_function(self):
        return self.func

# ============================================================
#                 Editing of observation areas
# ============================================================

    def push_observation_area(self, area):
        self.obs.append(area)
        self.obs_poly.append(polygon.polygon(area[0]))
        return True


    def pop_observation_area(self):
        return 1

    def remove_observation_area(self, id):
        return 1

    # def get_0_observation_areas(self):
        # return self.obs_0

    # def get_g_observation_areas(self):
    #     return self.obs_g

    def get_all_observation_areas(self):
        return self.obs



# ============================================================
#                 Editing of modeling points
# ============================================================

    def push_modeling_point(self, point):
        self.m_pts.append(point)
        return 1

    def pop_modeling_point(self):
        return 1

    def remove_modeling_point(self, id):
        return 1

    def get_all_modeling_points(self):
        return self.m_pts

# ============================================================
#                     Solution and results
# ============================================================

    # def solve(self):
    #     return 1

    def get_solution(self):
        # returns the solution function
        # Guaranteed that result is same as after solve()
        # Required to use solve() before using of this functions
        # It just gives already solved result to you, but did not solves a problem
        return self.vecF

# ============================================================
#                       Error handling
# ============================================================

    def get_last_error(self):
        return False

    def __get_m_pts_size__(self):
        return len(self.m_pts)

    def __get_m_pnt_x__(self, i):
        return self.m_pts[i][0]

    def __get_m_pnt_y__(self, i):
        return self.m_pts[i][1]

    def __get_m_pnt_t__(self, i):
        return self.m_pts[i][2]

    def __get_m_size__(self):
        return len(self.m_pts)

    def G(self, x, y, t):
        if self.green_is_setted:
            return self.G_func(x, y, t)
        else:
            moddiff = math.sqrt((y)**2 + (x)**2 + 0.000001)
            return - 1.0 / (2.0 * math.pi) * math.log(1.0 / moddiff)
            # return numpy.heaviside(t - moddiff / -1, 1) / moddiff
            c = -0.02
            # print(f't = {t} moddif = {moddiff}')
            # print(t - moddiff / c)
            # print(numpy.heaviside(t - moddiff / c, 1))
            # print((c**2) * (t**2) - moddiff**2)
            # print((2 * math.pi * c * math.sqrt((c**2) * (t**2) - moddiff**2)))
            # print(numpy.heaviside(t - moddiff / c, 1) / (2 * math.pi * c * math.sqrt((c**2) * (t**2) - moddiff**2)))
            tmp1 = t - moddiff / c
            tmp2 = (c**2) * (t**2) - moddiff**2
            tmp3 = 2.0 * math.pi * c * math.sqrt(abs(tmp2))
            tmp4 = numpy.heaviside(tmp1, 1.0)
            return  tmp4 / tmp3

    def f_obs(self, x, y, t):
        return self.func(x, y, t)

    def get_B_i_j(self, i, j, x, y, t):
        return self.G(x - self.__get_m_pnt_x__(i), y - self.__get_m_pnt_y__(i), t - self.__get_m_pnt_t__(i))

    def get_b_i(self, i_arg, x, y, t):
        # print(f'x: {x} y: {y} t: {t} f: {self.f_obs(x, y, t)}')
        return self.f_obs(x, y, t)

    def get_obs_area_t_from(self, i):
        return self.obs[i][1][0]

    def get_obs_area_t_to(self, i):
        return self.obs[i][1][1]

    def get_obs_area_i_size(self, i):
        return len(self.obs[i][0])

    def get_obs_area_i_j(self, i, j):
        return self.obs[i][0][j]

    def get_obs_area_i(self, i):
        return self.obs[i]

    def get_obs_area_i_j_x(self, i, j):
        return self.get_obs_area_i_j(i, j)[0]

    def get_obs_area_i_j_y(self, i, j):
        return self.get_obs_area_i_j(i, j)[1]

    def get_zero_integral_of_mult(self, i_arg, j_arg, k):
        t = 0
        n = 50
        cur_poly = self.obs_poly[j_arg]
        # print(cur_poly)

        x_a = cur_poly.get_x_min()
        x_b = cur_poly.get_x_max()
        delta_x = (x_b - x_a) / n

        res_1 = 0
        for i in range(0, n):
            cur_x = x_a + delta_x * (i + 0.5)
            res_2 = 0
            y_a = cur_poly.get_bottom_border(cur_x)
            y_b = cur_poly.get_top_border(cur_x)
            delta_y = (y_b - y_a) / n
            for j in range(0, n):
                cur_y = y_a + delta_y * (j + 0.5)
                # B_k_i * B_k_j
                res_3 = self.get_B_i_j(k, i_arg, cur_x, cur_y, t) * self.get_B_i_j(k, j_arg, cur_x, cur_y, t)
                res_2 += res_3 * delta_y
            res_1 += res_2 * delta_x
        return res_1

    def get_gran_integral_of_mult(self, i_arg, j_arg, k):
        cur_poly = self.obs_poly[k]
        cur_obs = self.get_obs_area_i(k)
        n = 20
        # print(cur_obs)
        t_a = cur_obs[1][0]
        t_b = cur_obs[1][1]
        step_t = (t_b - t_a) / n

        pnt_seq = cur_poly.get_contour_sequence()
        # print(pnt_seq)

        res_full = 0
        for j in range(0, n):
            cur_t = t_a + step_t * (j + 0.5)
            res_part = 0
            for i in range(0, len(pnt_seq)):
                cur_x = pnt_seq[i][0]
                cur_y = pnt_seq[i][1]
                # print(f'k = {k} i_arg = {i_arg} j_arg = {j_arg} cur_x = {cur_x} cur_y = {cur_y} cur_t = {cur_t}')
                res_cur = self.get_B_i_j(k, i_arg, cur_x, cur_y, cur_t) * self.get_B_i_j(k, j_arg, cur_x, cur_y, cur_t)
                res_part += pnt_seq[i][2] * res_cur
            res_full += res_part * step_t
        return res_full

    def get_c_i_j(self, i_arg, j_arg):
        res = 0
        for k in range(0, self.get_m0_size()):
            res += self.get_zero_integral_of_mult(i_arg, j_arg, k)
        for k in range(self.get_m0_size(), self.__get_m_size__()):
            # print(f'k = {k} m0 = {self.get_m0_size()} m = {self.__get_m_size__()}')
            res += self.get_gran_integral_of_mult(i_arg, j_arg, k)
        return res

    def get_matrix_c(self):
        res = numpy.zeros((self.__get_m_size__(), self.__get_m_size__()))
        for i in range(0, res.shape[0]):
            for j in range(0, res.shape[1]):
                res[i, j] = self.get_c_i_j(i, j)
        return res

    def get_zero_integral_of_mult_2(self, i_arg, k):
        t = 0
        n = 50
        cur_poly = self.obs_poly[i_arg]

        x_a = cur_poly.get_x_min()
        x_b = cur_poly.get_x_max()

        delta_x = (x_b - x_a) / n
        res_1 = 0
        for i in range(0, n):
            cur_x = x_a + delta_x * (i + 0.5)
            res_2 = 0
            y_a = cur_poly.get_bottom_border(cur_x)
            y_b = cur_poly.get_top_border(cur_x)
            delta_y = (y_b - y_a) / n
            for j in range(0, n):
                cur_y = y_a + delta_y * (j + 0.5)
                # B_k_i * b_k
                res_3 = self.get_B_i_j(k, i_arg, cur_x, cur_y, t) * self.get_b_i(k, cur_x, cur_y, t)
                res_2 += res_3 * delta_y
            res_1 += res_2 * delta_x

        return res_1

    def get_gran_integral_of_mult_2(self, i_arg, k):
        cur_poly = self.obs_poly[k]
        cur_obs = self.get_obs_area_i(k)
        n = 20
        # print(cur_obs)
        t_a = cur_obs[1][0]
        t_b = cur_obs[1][1]
        step_t = (t_b - t_a) / n

        pnt_seq = cur_poly.get_contour_sequence()
        # print(pnt_seq)

        res_full = 0
        for j in range(0, n):
            cur_t = t_a + step_t * (j + 0.5)
            res_part = 0
            for i in range(0, len(pnt_seq)):
                cur_x = pnt_seq[i][0]
                cur_y = pnt_seq[i][1]
                res_cur = self.get_B_i_j(k, i_arg, cur_x, cur_y, cur_t) * self.get_b_i(k, cur_x, cur_y, cur_t)
                res_part += pnt_seq[i][2] * res_cur
            res_full += res_part * step_t
        return res_full

    def get_B_b_i(self, i_arg):
        res = 0
        for k in range(0, self.get_m0_size()):
            res += self.get_zero_integral_of_mult_2(i_arg, k)
        for k in range(self.get_m0_size(), self.__get_m_size__()):
            res += self.get_gran_integral_of_mult_2(i_arg, k)
        return res

    def get_vec_B_b(self):
        res = numpy.zeros((self.__get_m_size__(), 1))
        for i in range(0, res.shape[0]):
            res[i, 0] = self.get_B_b_i(i)
        return res

    def solve(self):
        P_2 = self.get_matrix_c()
        B_b = self.get_vec_B_b()
        P_2_inv = numpy.linalg.pinv(P_2)
        x_res = numpy.matmul(P_2_inv, B_b)
        self.vecF = x_res
        print(x_res)
        return self.vecF

    def get_f_modeled(self, x, y, t):
        sum = 0
        if self.S_0_poly.contains_point(x, y):
            for i in range(0, len(self.m_pts)):
                sum += self.G(x - self.__get_m_pnt_x__(i), y - self.__get_m_pnt_x__(i), t - self.__get_m_pnt_x__(i)) * self.vecF[i]
        return sum

    def get_f_modeled_meshgrid(self, X_arr, Y_arr, t):
        if isinstance(X_arr, numpy.ndarray) and isinstance(Y_arr, numpy.ndarray):
            if len(X_arr.shape) == 1:
                res = numpy.zeros(X_arr.shape)
                for i in range(X_arr.shape[0]):
                    res[i] = self.get_f_modeled(X_arr[i], Y_arr[i], t)
                return res
            elif len(X_arr.shape) == 2:
                res = numpy.zeros(X_arr.shape)
                for i in range(X_arr.shape[0]):
                    for j in range(X_arr.shape[1]):
                        res[i][j] = self.get_f_modeled(X_arr[i][j], Y_arr[i][j], t)
                return res
            return 1

    # def get_f_modeled_meshgrid(self, X_arr, Y_arr, t):
    #     if isinstance(X_arr, numpy.ndarray) and isinstance(Y_arr, numpy.ndarray):
    #         res = numpy.zeros(X_arr.shape)
    #         for i in range(X_arr.shape[0]):
    #             for j in range(X_arr.shape[1]):
    #                 res[i][j] = self.get_f_modeled(X_arr[i][j], Y_arr[i][j], t)
    #         return res
    #     else:
    #         return 1

    def get_s_0_meshgrid(self, dpi = 30.0):
        x_a = self.S_0_poly.get_x_min()
        x_b = self.S_0_poly.get_x_max()
        y_min = self.S_0_poly.get_y_min()
        y_max = self.S_0_poly.get_y_max()
        x_size = max(round((x_b - x_a) * dpi), 1)
        y_size = max(round((y_max - y_min) * dpi), 1)

        res_x = numpy.zeros((x_size, y_size))
        res_y = numpy.zeros((x_size, y_size))
        x_step = (x_b - x_a) / x_size
        for i in range(0, x_size):
            x_cur = x_a + x_step * i
            y_a = self.S_0_poly.get_bottom_border(x_cur)
            y_b = self.S_0_poly.get_top_border(x_cur)
            y_step = (y_b - y_a) / y_size
            for j in range(0, y_size):
                y_cur = y_a + y_step * j
                res_x[i][j] = x_cur
                res_y[i][j] = y_cur

        return res_x, res_y

    def get_contour_nodes_seq(self):
        res_x = numpy.zeros(len(self.S_0) + 1)
        res_y = numpy.zeros(len(self.S_0) + 1)
        for i in range(0, len(self.S_0)):
            res_x[i] = self.S_0[i][0]
            res_y[i] = self.S_0[i][1]
        res_x[-1] = self.S_0[0][0]
        res_y[-1] = self.S_0[0][1]

        return res_x, res_y

    def get_contour_meshgrid(self, dpi=30.0):
        pnt_seq = self.S_0_poly.get_contour_sequence(dpi)
        res_x = numpy.zeros(len(pnt_seq))
        res_y = numpy.zeros(len(pnt_seq))
        for i in range(0, len(pnt_seq)):
            res_x[i] = pnt_seq[i][0]
            res_y[i] = pnt_seq[i][1]
        return res_x, res_y

    def print_py_plot(self, time, dpi = 30):
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(12, 7))
        t = time

        x_count, y_count = self.get_contour_nodes_seq()
        S_0_cont = ax.plot(x_count, y_count, color='red', linewidth=1.5, zorder=10, label='Контур S_0', alpha=0.7)

        if(abs (t) < 1E-3):
            X, Y = self.get_s_0_meshgrid(dpi)
            Z = self.get_f_modeled_meshgrid(X, Y, t)
            Z_2 = self.f_obs(X, Y, t)

            surf_modeled = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False, zorder=0, label ='Змодельовано',  alpha=0.7)
            surf_observ = ax.plot_surface(X, Y, Z_2, cmap=cm.PuOr, linewidth=0, antialiased=False, zorder=0, label ='Спостереження',  alpha=0.7)

            fig.colorbar(surf_modeled, shrink=0.5, aspect=5)
            fig.colorbar(surf_observ, shrink=0.5, aspect=5)

            fake_0 = matplotlib.lines.Line2D([0], [0], linestyle="none", c='blue', marker='o')
            fake_1 = matplotlib.lines.Line2D([0], [0], linestyle="none", c='purple', marker='o')
            fake_2 = matplotlib.lines.Line2D([0], [0], linestyle="none", c='red', marker=1)
            ax.legend([fake_0, fake_1, fake_2], ['Змодельовано', 'Спостереження', 'Контур S_0'], numpoints=1)
        else:
            X, Y = self.get_contour_meshgrid(dpi)
            Z = self.get_f_modeled_meshgrid(X, Y, t)
            Z_2 = self.f_obs(X, Y, t)
            surf_modeled = ax.plot(X, Y, Z, color='blue', zorder=0, label='Змодельовано')
            surf_observ = ax.plot(X, Y, Z_2, color='green', zorder=0, label='Спостереження')
            ax.legend()

        plt.title(f't = {t} mistake = {self.get_mistake()}')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.show()

    def get_mistake(self, dpi=20):
        res = 0
        for m in range(0, self.m0_size):
            t = 0
            cur_poly = self.obs_poly[m]
            x_a = cur_poly.get_x_min()
            x_b = cur_poly.get_x_max()
            delta_x = (x_b - x_a) / dpi
            res_1 = 0
            for i in range(0, dpi):
                cur_x = x_a + delta_x * (i + 0.5)
                res_2 = 0
                y_a = cur_poly.get_bottom_border(cur_x)
                y_b = cur_poly.get_top_border(cur_x)
                delta_y = (y_b - y_a) / dpi
                for j in range(0, dpi):
                    cur_y = y_a + delta_y * (j + 0.5)
                    res_3 = abs(self.get_f_modeled(cur_x, cur_y, t) - self.f_obs(cur_x, cur_y, t))
                    res_2 += res_3 * delta_y
                res_1 += res_2 * delta_x

            res += res_1
        for m in range(self.m0_size, len(self.m_pts)):
            cur_poly = self.obs_poly[m]
            cur_obs = self.get_obs_area_i(m)
            t_a = cur_obs[1][0]
            t_b = cur_obs[1][1]
            n_size = round((t_b - t_a) * dpi)
            step_t = (t_b - t_a) / n_size
            pnt_seq = cur_poly.get_contour_sequence(dpi)
            res_full = 0
            for j in range(0, n_size):
                cur_t = t_a + step_t * (j + 0.5)
                res_part = 0
                for i in range(0, len(pnt_seq)):
                    cur_x = pnt_seq[i][0]
                    cur_y = pnt_seq[i][1]
                    res_cur = abs(self.get_f_modeled(cur_x, cur_y, t) - self.f_obs(cur_x, cur_y, t))
                    res_part += pnt_seq[i][2] * res_cur
                res_full += res_part * step_t
            res += res_full

        return float(res)







