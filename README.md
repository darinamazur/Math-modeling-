# Math-modeling

## Class core
### Formulation of the problem
`set_m0_size(self, val)`
-- sets how much first observations will is at `t = 0` moment.\
`def get_m0_size(self)`
-- getter.\
`set_T(self, T)`
-- sets T -- last moment of the range `[0, T]`.\
`get_T(self)`
-- getter.\
`set_S_0(self, S_0_array)`
-- sets area `S_0`, as list, like `[[x0, y0], [x1, y1], ... [xn, yn]]`, where points `(x0, y0), (x1, y1) ... (xn, yn)` forms a polynom.\
`get_S_0(self)`
-- getter.\
Example of setting this value:

    import core
    foo = core.core()
    s_0 = [[0, 0],[0, 2], [1, 3], [2, 2],[2, -3]]
    foo.set_S_0(s_0)

`set_observation_function(self, func)`
-- sets the function of observations, where func is lambda (x, y, t).\
`get_observation_function(self)`
-- getter.\
Example:

    func_foo = lambda x, y, t:  (x * (2.0 - x) + y * (2.0 - y) + 0.1 * t) * 0.01
    foo.set_observation_function(func_foo)
    
`set_green_function(self, func)`
-- sets the Green function, where func is lambda (x, y, t). If not setted, class will use Green function for Laplass equation by default.\

### Editing areas
General form of observation areas:

    [[[x0, y0], [x1, y1], ... [xn, yn]], [t_a, t_b]]

where `(x0, y0), (x1, y1) ... (xn, yn)` is a contour of area,\
`t_a`, `t_b` - start and final moments of observations, as time range `[t_a, t_b]`

**Warning!** Observations at zero moment should be pushed before all others.\
Possible absense of areas of one of types.

`push_observation_area(self, area)`
-- adds new observation area to the end of list.\
`get_all_observation_areas(self)`
-- returns list with all observation areas.

`push_modeling_point(self, arr)`
-- adds a points to the list of modeling points. `arr` have form of `[x, y, t]`, where `x, y, t` -- coordinates of the point.

### Solution and visualisation
`solve(self)`
-- solve the problem, returns vector `u`.\
`get_solution(self)`
-- returns vector `u`, use only after using `solve(self)`.\
`get_f_modeled(self, x, y, t)`
-- get a value of modeled function in the point `(x, y, t)`. Use only after using `solve(self)`.
`print_py_plot(self, time, points = 30)`.]\
-- print a plot of modelled function and observation function. Use only after using `solve(self)`.
`time` -- a moment of time, when plot should be builded.\
`points = 30` -- number of points for each axis to build a plot.

### Example of the program

    import core
    foo = core.core()
    foo.set_T(10) 
    # sets [0, T] range as [0, 10]
    s_0 = [[0, 0],[0, 2], [1, 3], [2, 2],[2, -3]]
    foo.set_S_0(s_0) 
    # sets a polygon for S_0 area
    
    f_tmp = lambda x, y, t:  (x * (2.0 - x) + y * (2.0 - y) + 0.1 * t) * 0.01
    foo.set_observation_function(f_tmp) 
    # sets observation function
    
    foo.push_observation_area([s_0, [0.0, 0.0]])
    # adds observation area, with the contour, same as S_0, at the moment t = 0
    foo.set_m0_size(1)
    # we sets that only first one observation will be "zero-moment" observation
    foo.push_observation_area([s_0, [1.0, 2.0]])
    # adds observation area, with the contour, same as S_0, at the time range t in [1.0, 2.0]
    
    foo.push_modeling_point([1.0, 1.5, -1.2])
    foo.push_modeling_point([1.0, -1.0, 0.3])
    # adds modeling points
    
    foo.solve()
    # solving
    
    foo.print_py_plot(0.0, 50)
    foo.print_py_plot(1.0)
    # printing plots
