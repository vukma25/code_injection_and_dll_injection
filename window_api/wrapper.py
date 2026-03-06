import ctypes


def check_zero(result, func, args):
        if result == 0:
            error = ctypes.get_last_error()
            raise ctypes.WinError(error)
        return result

class WindowAPI:
    def __init__(self, dll_name):
        self.dll = ctypes.WinDLL(dll_name, use_last_error=True)

    def bind(self, func_name, argtypes, restype):
        func = getattr(self.dll, func_name)
        func.argtypes = argtypes
        func.restype = restype
        func.errcheck = check_zero

        setattr(self, func_name, func)