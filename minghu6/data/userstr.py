from types import MethodType
import abc


class CustomStrBytesCommon(abc.ABC):

    @property
    @abc.abstractmethod
    def _custom_class(self):
        raise NotImplementedError

    def __init__(self, *args, **kwargs):
        self._s = self._custom_class(*args, **kwargs)
        allowed_magic_method = [
            "__str__",
            "__repr",
            "__add__",
            "__contains__",
            "__format__",
            "__iter__",
            "__len__",
        ]

        def _wrap_callable(self, method):

            def newmethod(self, *args, **kwargs):
                result = method(*args, **kwargs)
                if isinstance(result, str):
                    result = CustomStr(result)
                    setattr(result, "extra_attrs", self.extra_attrs)
                elif isinstance(result, bytes):
                    result = CustomBytes(result)
                    setattr(result, "extra_attrs", self.extra_attrs)

                return result

            return MethodType(newmethod, self)

        for attrname in dir(self._custom_class):
            if not attrname.startswith("__") or attrname in allowed_magic_method:
                attrvalue = getattr(self._s, attrname)
                if callable(attrvalue):
                    setattr(self, attrname, _wrap_callable(self, attrvalue))

        if len(args) == 0 or not hasattr(args[0], "extra_attrs"):
            self.extra_attrs = {}

    def __eq__(self, s):
        if self._s != s:
            return False

        if self.extra_attrs != getattr(s, "extra_attrs", {}):
            return False

        return True

    def __ne__(self, s):
        return not self.__eq__(s)

    # TODO
    # '__reduce__',
    # '__reduce_ex__',


class CustomBytes(CustomStrBytesCommon, bytes):
    @property
    def _custom_class(self):
        return bytes


class CustomStr(CustomStrBytesCommon, str):
    @property
    def _custom_class(self):
        return str
