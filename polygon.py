




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

