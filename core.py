import math
import numpy

class core:
    ZERO_OBS_AREA = 0
    GRAN_OBS_AREA = 1

    def __init__(self):
        self.T = 0
        self.S_0 = []
        # self.obs_0 = []
        # self.obs_g = []
        self.obs = []
        self.m_pts = []
        self.m0_size = 0


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

    def set_observation_function(self, func):
        self.func = func

    def get_T(self):
        return self.T

    def get_S_0(self):
        return self.S_0_array

    def get_observation_function(self):
        return self.func

# ============================================================
#                 Editing of observation areas
# ============================================================

    def push_observation_area(self, area, type=0):
        # if type == core.ZERO_OBS_AREA:
        #     self.obs_0.append(area)
        #     return True
        # elif type == core.GRAN_OBS_AREA:
        #     self.obs_g.append(area)
        #     return True
        self.obs.append(area)
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
        return 1

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
        moddiff = math.sqrt((x)**2 + (y)**2) + t
        return moddiff

    def f_obs(self, x, y, t):
        return self.func(x, y, t)

    def get_B_i_j(self, i, j, x, y, t):
        return self.G(x - self.__get_m_pnt_x__(i), y - self.__get_m_pnt_y__(i), t - self.__get_m_pnt_t__(i))

    def get_b_i(self, i_arg, x, y, t):
        return self.f_obs(x, y, t)

    def get_obs_area_t_from(self, i):
        return self.obs[i][1][0]

    def get_obs_area_t_to(self, i):
        return self.obs[i][1][1]

    def get_obs_area_i_size(self, i):
        return len(self.obs[i][0])

    def get_obs_area_i_j(self, i, j):
        return self.obs[i][0][j]

    def get_obs_area_i_j_x(self, i, j):
        return self.get_obs_area_i_j(i, j)[0]

    def get_obs_area_i_j_y(self, i, j):
        return self.get_obs_area_i_j(i, j)[1]

    def get_up_border(self, j_arg, x):
        pts_x = []
        pts_y = []
        for i in range(0, self.get_obs_area_i_size(j_arg)):
            pts_x.append(self.get_obs_area_i_j_x(j_arg, i))
            pts_y.append(self.get_obs_area_i_j_y(j_arg, i))

        ind = []
        for i in range(0, len(pts_x) - 1):
            if x > pts_x[i] and x > pts_x[i + 1]:
                ind.append(i)
        if x > pts_x[len(pts_x) - 1] and x > pts_x[0]:
            ind.append(i)
        val = []
        for i in range(0, len(ind)):
            ind_cur = ind[i]
            ind_next = ind[i] + 1
            if ind_next > len(pts_x):
                ind_next = 0
            if pts_x[ind_cur] != pts_x[ind_next]:
                val.append(pts_y[ind_cur] + (x - pts_x[ind_cur]) * (pts_y[ind_next] - pts_y[ind_cur]) / (pts_x[ind_next] - pts_x[ind_cur]))
            else:
                val.append(max(pts_y[ind_cur], pts_y[ind_next]))

        return max(val)

    def get_down_border(self, j_arg, x):
        pts_x = []
        pts_y = []
        for i in range(0, self.get_obs_area_i_size(j_arg)):
            pts_x.append(self.get_obs_area_i_j_x(j_arg, i))
            pts_y.append(self.get_obs_area_i_j_y(j_arg, i))

        ind = []
        for i in range(0, len(pts_x) - 1):
            if x > pts_x[i] and x > pts_x[i + 1]:
                ind.append(i)
        if x > pts_x[len(pts_x) - 1] and x > pts_x[0]:
            ind.append(i)
        val = []
        for i in range(0, len(ind)):
            ind_cur = ind[i]
            ind_next = ind[i] + 1
            if ind_next > len(pts_x):
                ind_next = 0
            if pts_x[ind_cur] != pts_x[ind_next]:
                val.append(pts_y[ind_cur] + (x - pts_x[ind_cur]) * (pts_y[ind_next] - pts_y[ind_cur]) / (pts_x[ind_next] - pts_x[ind_cur]))
            else:
                val.append(min(pts_y[ind_cur], pts_y[ind_next]))
        return min(val)

    def get_zero_integral_of_mult(self, i_arg, j_arg, k):
        t = 0
        n = 50
        pts_x = []
        # pts_y = []
        #
        for i in range(0, self.get_obs_area_i_size(j_arg)):
            pts_x.append(self.get_obs_area_i_j_x(j_arg, i))
        #     pts_y.append(self.get_obs_area_i_j_y(j_arg, i))
        #
        # x_minimal = min(pts_x)
        # tmp = 0
        # for i in range(0, len(pts_x)):
        #     if pts_x[i] == x_minimal:
        #         tmp = i
        #         break
        # if tmp != 0:
        #     new_x = []
        #     new_y = []
        #     for i in range(tmp, len(pts_x)):
        #         new_x.append(pts_x[i])
        #         new_y.append(pts_y[i])
        #     for i in range(0, tmp):
        #         new_x.append(pts_x[i])
        #         new_y.append(pts_y[i])
        #     pts_x = new_x
        #     pts_y = new_y
        # min_ind = 0
        # max_ind = 0
        # x_maximal = max(pts_x)
        # for i in range(0, len(pts_x)):
        #     if pts_x[i] == x_maximal:
        #         max_ind = i
        #         break

        x_a = min(pts_x)
        x_b = max(pts_x)

        delta_x = (x_b - x_a) / n

        res_1 = 0
        for i in range(0, n):
            cur_x = x_a + delta_x * (i + 0.5)
            res_2 = 0
            y_a = self.get_down_border(j_arg, cur_x)
            y_b = self.get_up_border(j_arg, cur_x)
            delta_y = (y_b - y_a) / n
            for j in range(0, n):
                cur_y = y_a + delta_y * (j + 0.5)
                # B_k_i * B_k_j
                res_3 = self.get_B_i_j(k, i_arg, cur_x, cur_y, t) * self.get_B_i_j(k, j_arg, cur_x, cur_y, t)
                res_2 += res_3 * delta_y
            res_1 += res_2 * delta_x

        return res_1

    def get_gran_integral_of_mult(self, i_arg, j_arg, k):
        return 0
        # t = 0
        n = 20
        t_a = 0
        h_t = (core.T - t_a) / n
        x_a = 0
        y_a = 0
        h_x = (core.x1 - x_a) / n
        h_y = (core.x2 - y_a) / n
        res_1 = 0

        for i in range(0, n):
            cur_t = t_a + h_t * (i + 0.5)
            res_2 = 0

            # 1 - (0;0) -> (x1;0)
            cur_y = 0
            res_3 = 0
            for j in range(0, n):
                cur_x = x_a + h_x * (i + 0.5)
                res_4 = self.get_B_i_j(k, i_arg, cur_x, cur_y, cur_t) * self.get_B_i_j(k, j_arg, cur_x, cur_y, cur_t)
                res_3 += res_4 * h_x
            res_2 += res_3

            # 2 - (x1;0) -> (x1;x2)
            cur_x = core.x1
            res_3 = 0
            for j in range(0, n):
                cur_y = y_a + h_y * (i + 0.5)
                res_4 = self.get_B_i_j(k, i_arg, cur_x, cur_y, cur_t) * self.get_B_i_j(k, j_arg, cur_x, cur_y, cur_t)
                res_3 += res_4 * h_y
            res_2 += res_3

            # 3 - (x1;x2) -> (0;x2)
            cur_y = core.x2
            res_3 = 0
            for j in range(0, n):
                cur_x = core.x1 - h_x * (i + 0.5)
                res_4 = self.get_B_i_j(k, i_arg, cur_x, cur_y, cur_t) * self.get_B_i_j(k, j_arg, cur_x, cur_y, cur_t)
                res_3 += res_4 * h_x
            res_2 += res_3

            # 4 - (0;x2) -> (0;0)
            cur_x = 0
            res_3 = 0
            for j in range(0, n):
                cur_y = core.x2 - h_y * (i + 0.5)
                res_4 = self.get_B_i_j(k, i_arg, cur_x, cur_y, cur_t) * self.get_B_i_j(k, j_arg, cur_x, cur_y, cur_t)
                res_3 += res_4 * h_y
            res_2 += res_3

            res_1 += res_2 * h_t

        return res_1

    def get_c_i_j(self, i_arg, j_arg):
        res = 0
        for k in range(0, self.get_m0_size()):
            res += self.get_zero_integral_of_mult(i_arg, j_arg, k)
        for k in range(self.get_m0_size(), self.__get_m_size__()):
            res += self.get_gran_integral_of_mult(i_arg, j_arg, k)
        return res

    def get_matrix_c(self):
        res = numpy.zeros((self.__get_m_size__(), self.__get_m_size__()))
        for i in range(0, res.shape[0]):
            for j in range(0, res.shape[1]):
                res[i, j] = self.get_c_i_j(i, j)
        return res

    def get_zero_integral_of_mult_2(self, i_arg, k):
        return 0
        # print("i: " + str(i_arg) + " k: " + str(k))
        t = 0
        n = 20
        x_a = 0
        y_a = 0
        h_x = (core.x1 - x_a) / n
        h_y = (core.x2 - y_a) / n
        res_1 = 0
        for i in range(0, n):
            cur_x = x_a + h_x * (i + 0.5)
            res_2 = 0
            for j in range(0, n):
                cur_y = y_a + h_y * (j + 0.5)
                # B_k_i * b_k
                res_3 = self.get_B_i_j(k, i_arg, cur_x, cur_y, t) * self.get_b_i(k, cur_x, cur_y, t)
                # if debug:
                #     print("zero")
                #     print("i: " + str(i_arg) + " k: " + str(k) + " x: " + str(cur_x) + " y: " + str(cur_y) + " res: " + str(res_3))
                #     print("part1: " + str(self.get_B_i_j(k, i_arg, cur_x, cur_y, t)))
                #     print("part2: " + str(self.get_b_i(k, cur_x, cur_y, t)))

                res_2 += res_3 * h_y
            res_1 += res_2 * h_x

        return res_1

    def get_gran_integral_of_mult_2(self, i_arg, k):
        return 0
        n = 20
        t_a = 0
        h_t = (core.T - t_a) / n
        x_a = 0
        y_a = 0
        h_x = (core.x1 - x_a) / n
        h_y = (core.x2 - y_a) / n
        res_1 = 0

        for i in range(0, n):
            cur_t = t_a + h_t * (i + 0.5)
            res_2 = 0

            # 1 - (0;0) -> (x1;0)
            cur_y = 0
            res_3 = 0
            for j in range(0, n):
                cur_x = x_a + h_x * (i + 0.5)
                res_4 = self.get_B_i_j(k, i_arg, cur_x, cur_y, cur_t) * self.get_b_i(k, cur_x, cur_y, cur_t)
                res_3 += res_4 * h_x
            res_2 += res_3

            # 2 - (x1;0) -> (x1;x2)
            cur_x = core.x1
            res_3 = 0
            for j in range(0, n):
                cur_y = y_a + h_y * (i + 0.5)
                res_4 = self.get_B_i_j(k, i_arg, cur_x, cur_y, cur_t) * self.get_b_i(k, cur_x, cur_y, cur_t)
                res_3 += res_4 * h_y
            res_2 += res_3

            # 3 - (x1;x2) -> (0;x2)
            cur_y = core.x2
            res_3 = 0
            for j in range(0, n):
                cur_x = core.x1 - h_x * (i + 0.5)
                res_4 = self.get_B_i_j(k, i_arg, cur_x, cur_y, cur_t) * self.get_b_i(k, cur_x, cur_y, cur_t)
                res_3 += res_4 * h_x
            res_2 += res_3

            # 4 - (0;x2) -> (0;0)
            cur_x = 0
            res_3 = 0
            for j in range(0, n):
                cur_y = core.x2 - h_y * (i + 0.5)
                res_4 = self.get_B_i_j(k, i_arg, cur_x, cur_y, cur_t) * self.get_b_i(k, cur_x, cur_y, cur_t)
                res_3 += res_4 * h_y

            res_2 += res_3

            res_1 += res_2 * h_t

            # if debug:
            #     print("gran")
            #     print("i: " + str(i_arg) + " k: " + str(k) + " x: " + str(cur_x) + " y: " + str(cur_y) + " t: " + str(cur_t) + " res: " + str(
            #         res_3))
            #     print("part1: " + str(self.get_B_i_j(k, i_arg, cur_x, cur_y, cur_t)))
            #     print("part2: " + str(self.get_b_i(k, cur_x, cur_y, cur_t)))

        return res_1

        t = 0
        n = 20
        x_a = 0
        y_a = 0
        h_x = (core.x1 - x_a) / n
        h_y = (core.x2 - y_a) / n
        res_1 = 0
        for i in range(0, n):
            cur_x = x_a + h_x * (i + 0.5)
            res_2 = 0
            for j in range(0, n):
                cur_y = y_a + h_y * (j + 0.5)
                # B_k_i * B_k_j
                res_3 = self.get_B_i_j(k, i_arg, cur_x, cur_y, t) * self.get_b_i(k, cur_x, cur_y, t)
                res_2 += res_3 * h_y

            res_1 += res_2 * h_x

        return res_1

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
        core.vecF = x_res
        print(x_res)








