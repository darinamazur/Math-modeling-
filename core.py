class core:
    def __init__(self):
        return 1

# ============================================================
#            Setters of formulations of the problems
# ============================================================

    def set_T(self, T):
        return 1

    def set_S_0(self, S_0):
        return 1

    def set_observation_function(self, func):
        return 1

# ============================================================
#                 Editing of observation areas
# ============================================================

    def push_observation_area(self, area):
        return 1

    def pop_observation_area(self):
        return 1

    def remove_observation_area(self, id):
        return 1

    def get_all_observation_areas(self):
        return 1

# ============================================================
#                 Editing of modeling points
# ============================================================

    def push_modeling_point(self, point):
        return 1

    def pop_modeling_point(self):
        return 1

    def remove_modeling_point(self, id):
        return 1

    def get_all_modeling_points(self):
        return 1

# ============================================================
#                     Solution and results
# ============================================================

    def solve(self):
        return 1

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
