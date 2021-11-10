
class Process:

    def __init__(self):
        self._name = ""
        self._green = ""
        self._oper = ""             #protected
        self._dimension = 1
        self._func = ""
        self._T = 0
        self._const = None

    @property
    def T(self):
        return self._T

    @T.setter
    def T(self, newT):
        self._T = newT

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newname):
        self._name = newname

    @property
    def func(self):
        return self._func

    @func.setter
    def func(self, newfunc):
        self._func = newfunc

    @property
    def green(self):
        return self._green

    @green.setter
    def green(self, newgreen):
        self._green = newgreen

    @property
    def oper(self):
        return self._oper

    @oper.setter
    def oper(self, newoper):
        self._oper = newoper

    @property
    def dimension(self):
        return self._dimension

    @dimension.setter
    def dimension(self, newdimenson):
        self._dimension = newdimenson

    @property
    def const(self):
        return self._const

    @const.setter
    def const(self, newconst):
        self._const = newconst


        


