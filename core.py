import math
import numpy
import polygon
import matplotlib.pyplot as plt
from matplotlib import cm
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

    # def get_up_border(self, j_arg, x):
    #     pts_x = []
    #     pts_y = []
    #     for i in range(0, self.get_obs_area_i_size(j_arg)):
    #         pts_x.append(self.get_obs_area_i_j_x(j_arg, i))
    #         pts_y.append(self.get_obs_area_i_j_y(j_arg, i))
    #
    #     ind = []
    #     for i in range(0, len(pts_x) - 1):
    #         if x > pts_x[i] and x > pts_x[i + 1]:
    #             ind.append(i)
    #     if x > pts_x[len(pts_x) - 1] and x > pts_x[0]:
    #         ind.append(i)
    #     val = []
    #     for i in range(0, len(ind)):
    #         ind_cur = ind[i]
    #         ind_next = ind[i] + 1
    #         if ind_next > len(pts_x):
    #             ind_next = 0
    #         if pts_x[ind_cur] != pts_x[ind_next]:
    #             val.append(pts_y[ind_cur] + (x - pts_x[ind_cur]) * (pts_y[ind_next] - pts_y[ind_cur]) / (pts_x[ind_next] - pts_x[ind_cur]))
    #         else:
    #             val.append(max(pts_y[ind_cur], pts_y[ind_next]))
    #
    #     return max(val)
    #
    # def get_down_border(self, j_arg, x):
    #     pts_x = []
    #     pts_y = []
    #     for i in range(0, self.get_obs_area_i_size(j_arg)):
    #         pts_x.append(self.get_obs_area_i_j_x(j_arg, i))
    #         pts_y.append(self.get_obs_area_i_j_y(j_arg, i))
    #
    #     ind = []
    #     for i in range(0, len(pts_x) - 1):
    #         if x > pts_x[i] and x > pts_x[i + 1]:
    #             ind.append(i)
    #     if x > pts_x[len(pts_x) - 1] and x > pts_x[0]:
    #         ind.append(i)
    #     val = []
    #     for i in range(0, len(ind)):
    #         ind_cur = ind[i]
    #         ind_next = ind[i] + 1
    #         if ind_next > len(pts_x):
    #             ind_next = 0
    #         if pts_x[ind_cur] != pts_x[ind_next]:
    #             val.append(pts_y[ind_cur] + (x - pts_x[ind_cur]) * (pts_y[ind_next] - pts_y[ind_cur]) / (pts_x[ind_next] - pts_x[ind_cur]))
    #         else:
    #             val.append(min(pts_y[ind_cur], pts_y[ind_next]))
    #     return min(val)

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




        # for i in range(0, n):
        #     cur_t = t_a + h_t * (i + 0.5)
        #     res_2 = 0
        #
        #     # 1 - (0;0) -> (x1;0)
        #     cur_y = 0
        #     res_3 = 0
        #     for j in range(0, n):
        #         cur_x = x_a + h_x * (i + 0.5)
        #
        #         res_3 += res_4 * h_x
        #     res_2 += res_3
        #
        #     # 2 - (x1;0) -> (x1;x2)
        #     cur_x = core.x1
        #     res_3 = 0
        #     for j in range(0, n):
        #         cur_y = y_a + h_y * (i + 0.5)
        #         res_4 = self.get_B_i_j(k, i_arg, cur_x, cur_y, cur_t) * self.get_B_i_j(k, j_arg, cur_x, cur_y, cur_t)
        #         res_3 += res_4 * h_y
        #     res_2 += res_3
        #
        #     # 3 - (x1;x2) -> (0;x2)
        #     cur_y = core.x2
        #     res_3 = 0
        #     for j in range(0, n):
        #         cur_x = core.x1 - h_x * (i + 0.5)
        #         res_4 = self.get_B_i_j(k, i_arg, cur_x, cur_y, cur_t) * self.get_B_i_j(k, j_arg, cur_x, cur_y, cur_t)
        #         res_3 += res_4 * h_x
        #     res_2 += res_3
        #
        #     # 4 - (0;x2) -> (0;0)
        #     cur_x = 0
        #     res_3 = 0
        #     for j in range(0, n):
        #         cur_y = core.x2 - h_y * (i + 0.5)
        #         res_4 = self.get_B_i_j(k, i_arg, cur_x, cur_y, cur_t) * self.get_B_i_j(k, j_arg, cur_x, cur_y, cur_t)
        #         res_3 += res_4 * h_y
        #     res_2 += res_3
        #
        #     res_1 += res_2 * h_t
        #
        # return res_1

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


        # return 0
        # # print("i: " + str(i_arg) + " k: " + str(k))
        # t = 0
        # n = 20
        # x_a = 0
        # y_a = 0
        # h_x = (core.x1 - x_a) / n
        # h_y = (core.x2 - y_a) / n
        # res_1 = 0
        # for i in range(0, n):
        #     cur_x = x_a + h_x * (i + 0.5)
        #     res_2 = 0
        #     for j in range(0, n):
        #         cur_y = y_a + h_y * (j + 0.5)
        #         # B_k_i * b_k
        #         res_3 = self.get_B_i_j(k, i_arg, cur_x, cur_y, t) * self.get_b_i(k, cur_x, cur_y, t)
        #         res_2 += res_3 * h_y
        #     res_1 += res_2 * h_x
        #
        # return res_1

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

        # return 0
        # n = 20
        # t_a = 0
        # h_t = (core.T - t_a) / n
        # x_a = 0
        # y_a = 0
        # h_x = (core.x1 - x_a) / n
        # h_y = (core.x2 - y_a) / n
        # res_1 = 0
        #
        # for i in range(0, n):
        #     cur_t = t_a + h_t * (i + 0.5)
        #     res_2 = 0
        #
        #     # 1 - (0;0) -> (x1;0)
        #     cur_y = 0
        #     res_3 = 0
        #     for j in range(0, n):
        #         cur_x = x_a + h_x * (i + 0.5)
        #
        #         res_3 += res_4 * h_x
        #     res_2 += res_3
        #
        #     # 2 - (x1;0) -> (x1;x2)
        #     cur_x = core.x1
        #     res_3 = 0
        #     for j in range(0, n):
        #         cur_y = y_a + h_y * (i + 0.5)
        #         res_4 = self.get_B_i_j(k, i_arg, cur_x, cur_y, cur_t) * self.get_b_i(k, cur_x, cur_y, cur_t)
        #         res_3 += res_4 * h_y
        #     res_2 += res_3
        #
        #     # 3 - (x1;x2) -> (0;x2)
        #     cur_y = core.x2
        #     res_3 = 0
        #     for j in range(0, n):
        #         cur_x = core.x1 - h_x * (i + 0.5)
        #         res_4 = self.get_B_i_j(k, i_arg, cur_x, cur_y, cur_t) * self.get_b_i(k, cur_x, cur_y, cur_t)
        #         res_3 += res_4 * h_x
        #     res_2 += res_3
        #
        #     # 4 - (0;x2) -> (0;0)
        #     cur_x = 0
        #     res_3 = 0
        #     for j in range(0, n):
        #         cur_y = core.x2 - h_y * (i + 0.5)
        #         res_4 = self.get_B_i_j(k, i_arg, cur_x, cur_y, cur_t) * self.get_b_i(k, cur_x, cur_y, cur_t)
        #         res_3 += res_4 * h_y
        #
        #     res_2 += res_3
        #
        #     res_1 += res_2 * h_t
        #
        #     # if debug:
        #     #     print("gran")
        #     #     print("i: " + str(i_arg) + " k: " + str(k) + " x: " + str(cur_x) + " y: " + str(cur_y) + " t: " + str(cur_t) + " res: " + str(
        #     #         res_3))
        #     #     print("part1: " + str(self.get_B_i_j(k, i_arg, cur_x, cur_y, cur_t)))
        #     #     print("part2: " + str(self.get_b_i(k, cur_x, cur_y, cur_t)))
        #
        # return res_1
        #
        # t = 0
        # n = 20
        # x_a = 0
        # y_a = 0
        # h_x = (core.x1 - x_a) / n
        # h_y = (core.x2 - y_a) / n
        # res_1 = 0
        # for i in range(0, n):
        #     cur_x = x_a + h_x * (i + 0.5)
        #     res_2 = 0
        #     for j in range(0, n):
        #         cur_y = y_a + h_y * (j + 0.5)
        #         # B_k_i * B_k_j
        #         res_3 = self.get_B_i_j(k, i_arg, cur_x, cur_y, t) * self.get_b_i(k, cur_x, cur_y, t)
        #         res_2 += res_3 * h_y
        #
        #     res_1 += res_2 * h_x
        #
        # return res_1

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

    # def getUZero_sum(self, x, y, t):
    #     sum = 0
    #     for i in range(0, self.m0):
    #         sum += calc.G(x, y, t, self.m0Pts[i, 0], self.m0Pts[i, 1], self.m0Pts[i, 2]) * self.vecF[i]
    #     return sum
    #
    # def getUGran_sum(self, x, y, t):
    #     sum = 0
    #     for i in range(0, self.mg):
    #         sum += calc.G(x, y, t, self.mgPts[i, 0], self.mgPts[i, 1], self.mgPts[i, 2]) * self.vecF[calc.m0 + i]
    #     return sum

    def get_f_modeled(self, x, y, t):
        sum = 0
        if self.S_0_poly.contains_point(x, y):
            for i in range(0, len(self.m_pts)):
                sum += self.G(x - self.__get_m_pnt_x__(i), y - self.__get_m_pnt_x__(i), t - self.__get_m_pnt_x__(i)) * self.vecF[i]
        return sum

    def get_f_modeled_meshgrid(self, X_arr, Y_arr, t):
        res = numpy.zeros(X_arr.shape)
        for i in range(X_arr.shape[0]):
            for j in range(X_arr.shape[1]):
                res[i][j] = self.get_f_modeled(X_arr[i][j], Y_arr[i][j], t)
        return res

    # def getUFull(self, x, y, t):
    #     # print("getFullU",x,y,t)
    #     return self.getUZero_sum(x, y, t) + self.getUGran_sum(x, y, t)

    def print_py_plot(self, time, points = 30):
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        x = numpy.linspace(self.S_0_poly.get_x_min(), self.S_0_poly.get_x_max(), points)
        y = numpy.linspace(self.S_0_poly.get_y_min(), self.S_0_poly.get_y_max(), points)
        t = time

        X, Y = numpy.meshgrid(x, y)
        Z = self.get_f_modeled_meshgrid(X, Y, t)
        Z_2 = self.f_obs(X, Y, t)

        surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)
        ax.plot_wireframe(X, Y, Z_2, rstride=3, cstride=3)

        plt.title(f't = {t}')
        plt.xlabel('x')
        plt.ylabel('y')

        fig.colorbar(surf, shrink=0.5, aspect=5)
        plt.show()





