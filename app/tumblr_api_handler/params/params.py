class Param:
    def __init__(self, name, required, data_type=object, default=None, getter_lambda=lambda x: x):
        self.name = name
        self._value = default
        self._required = required
        self._data_type = data_type
        self._default = default
        self._getter_lambda = getter_lambda

    @property
    def value(self):
        val = self._default
        if self._value:
            val = self._getter_lambda(self._value)
        elif self._required:
            raise KeyError("{} has no defualt value and is required".format(self.name))
        return val

    @value.setter
    def value(self, value):
        if isinstance(value, self._data_type):
            self._value = value
        elif value is None and not self._required:
            self._value = value
        else:
            raise TypeError


class BaseURLParam(Param):
    pass


class QueryStringParam(Param):
    pass


class POSTDataParam(Param):
    pass


class Params:

    def __setattr__(self, key, value):
        val = self.__dict__.get(key)
        if issubclass(val.__class__, Param):
            val.value = value
        else:
            super().__setattr__(key, value)

    def of_type(self, param_type):
        params = dict()
        for key, val in self.__dict__.items():
            if val.__class__ == param_type and (param_type == BaseURLParam or val.value):
                params[val.name] = val.value
        return params
