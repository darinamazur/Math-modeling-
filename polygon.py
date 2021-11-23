import math
class polygon:

    def __init__(self, arr):
        self.original_arr = arr

        self.size = len(self.original_arr)
        self.__set_min_max_by_original__()
        self.__refactor_original_seq__()
        self.sorted_arr.append(self.sorted_arr[0])
        self.size += 1

    def __set_min_max_by_original__(self):
        self.x_min_ind = 0
        self.x_max_ind = 0
        self.y_min_ind = 0
        self.y_max_ind = 0
        for i in range(1, self.size):
            if self.original_arr[i][0] > self.original_arr[self.x_max_ind][0]:
                self.x_max_ind = i
            if self.original_arr[i][0] < self.original_arr[self.x_min_ind][0]:
                self.x_min_ind = i
            if self.original_arr[i][1] > self.original_arr[self.y_max_ind][1]:
                self.y_max_ind = i
            if self.original_arr[i][1] < self.original_arr[self.y_min_ind][1]:
                self.y_min_ind = i

    def __refactor_original_seq__(self):
        self.sorted_arr = []
        for i in range(self.x_min_ind, self.size):
            self.sorted_arr.append(self.original_arr[i])
        for i in range(0, self.x_min_ind):
            self.sorted_arr.append(self.original_arr[i])
        self.x_max_ind = (self.x_max_ind - self.x_min_ind) % self.size
        self.y_max_ind = (self.y_max_ind - self.x_min_ind) % self.size
        self.y_min_ind = (self.y_min_ind - self.x_min_ind) % self.size
        self.x_min_ind = 0

    def __equal__(x1, x2):
        return abs(x1 - x2) < 1E-4

    def get_top_border(self, x):
        if polygon.__equal__(x, self.sorted_arr[self.x_max_ind][0]):
            if polygon.__equal__(self.sorted_arr[self.x_max_ind][0], self.sorted_arr[self.x_max_ind + 1][0]):
                return max(self.sorted_arr[self.x_max_ind][1], self.sorted_arr[self.x_max_ind + 1][1])
            else:
                return self.sorted_arr[self.x_max_ind][1]
        if polygon.__equal__(x, self.sorted_arr[self.x_min_ind][0]):
            if polygon.__equal__(self.sorted_arr[self.x_min_ind][0], self.sorted_arr[self.x_min_ind + 1][0]):
                return max(self.sorted_arr[self.x_min_ind][1], self.sorted_arr[self.x_min_ind + 1][1])
            else:
                return self.sorted_arr[self.x_min_ind][1]
        for i in range(self.x_min_ind, self.x_max_ind):
            if x >= self.sorted_arr[i][0] and x < self.sorted_arr[i + 1][0]:
                if self.sorted_arr[i][0] != self.sorted_arr[i + 1][0]:
                    x1 = self.sorted_arr[i][0]
                    x2 = self.sorted_arr[i + 1][0]
                    y1 = self.sorted_arr[i][1]
                    y2 = self.sorted_arr[i + 1][1]
                    return y1 + (x - x1) * (y2 - y1) / (x2 - x1)
                else:
                    return max(self.sorted_arr[i][1], self.sorted_arr[i + 1][1])
        exit(3)

    def get_bottom_border(self, x):
        if polygon.__equal__(x, self.sorted_arr[self.x_max_ind][0]):
            if polygon.__equal__(self.sorted_arr[self.x_max_ind][0], self.sorted_arr[self.x_max_ind + 1][0]):
                return min(self.sorted_arr[self.x_max_ind][1], self.sorted_arr[self.x_max_ind + 1][1])
            else:
                return self.sorted_arr[self.x_max_ind][1]
        if polygon.__equal__(x, self.sorted_arr[self.x_min_ind][0]):
            if polygon.__equal__(self.sorted_arr[self.x_min_ind][0], self.sorted_arr[self.x_min_ind + 1][0]):
                return min(self.sorted_arr[self.x_min_ind][1], self.sorted_arr[self.x_min_ind + 1][1])
            else:
                return self.sorted_arr[self.x_min_ind][1]
        for i in range(self.x_max_ind, self.size - 1):
            if x < self.sorted_arr[i][0] and x >= self.sorted_arr[i + 1][0]:
                if self.sorted_arr[i][0] != self.sorted_arr[i + 1][0]:
                    x1 = self.sorted_arr[i][0]
                    x2 = self.sorted_arr[i + 1][0]
                    y1 = self.sorted_arr[i][1]
                    y2 = self.sorted_arr[i + 1][1]
                    return y1 + (x - x1) * (y2 - y1) / (x2 - x1)
                else:
                    return min(self.sorted_arr[i][1], self.sorted_arr[i + 1][1])
        exit(3)

    def get_x_min(self):
        return self.sorted_arr[self.x_min_ind][0]
    def get_x_max(self):
        return self.sorted_arr[self.x_max_ind][0]

    def get_y_min(self):
        return self.sorted_arr[self.y_min_ind][1]
    def get_y_max(self):
        return self.sorted_arr[self.y_max_ind][1]

    def get_contour_length(self):
        res = 0
        for i in range(0, self.size - 1):
            res += math.sqrt((self.sorted_arr[i][0] - self.sorted_arr[i + 1][0]) ** 2 + (self.sorted_arr[i][1] - self.sorted_arr[i + 1][1]) ** 2)
        return res

    def get_contour_sequence(self, dpi=10):
        # returns 2d-array with 1-dimension length same as points in array,
        # second dimension have length 3, contains x, y, multiplier constant
        n = math.ceil(self.get_contour_length() * dpi)
        res_arr = []
        for i in range(0, self.size - 1):
            x_cur = self.sorted_arr[i][0]
            x_next = self.sorted_arr[i + 1][0]
            y_cur = self.sorted_arr[i][1]
            y_next = self.sorted_arr[i + 1][1]
            if not polygon.__equal__(x_cur, x_next):
                y_x = lambda x: y_cur + (x - x_cur) * (y_next - y_cur) / (x_next - x_cur)
                section_length = math.sqrt((x_next - x_cur) ** 2 + (y_next - y_cur) ** 2)
                n = math.ceil(section_length * dpi)
                if n != 0:
                    step_x = (x_next - x_cur) / float(n)
                    step_len = section_length / float(n)
                    for i in range(0, n):
                        tmp_x = x_cur + step_x * (i + 0.5)
                        tmp_y = y_x(tmp_x)
                        res_arr.insert(0, [tmp_x, tmp_y, step_len])
            else:
                section_length = math.sqrt((x_next - x_cur) ** 2 + (y_next - y_cur) ** 2)
                n = math.ceil(section_length * dpi)
                if n != 0:
                    step_p = (y_next - y_cur) / float(n)
                    step_len = section_length / float(n)
                    for i in range(0, n):
                        tmp_y = y_cur + step_p * (i + 0.5)
                        res_arr.insert(0, [x_cur, tmp_y, step_len])
        return res_arr

    def contains_point(self, x, y):
        if x > self.get_x_max() or x < self.get_x_min():
            return False
        return self.get_top_border(x) >= y and self.get_bottom_border(x) <= y

