from injector import Injector
from constants.variable import *
from window_api.api import winapi_kernel32

def get_procedure_address():
    try:
        h_kernel32 = winapi_kernel32.GetModuleHandleA(b'kernel32.dll')
        procedure_address = winapi_kernel32.GetProcAddress(h_kernel32, b'LoadLibraryA')
        return procedure_address
    except Exception as e:
        raise TypeError(f"[*] Error here: {e}")

class DllInjector(Injector):
    def __init__(self, process_name, path):
        source = path.encode("ascii") + b"\x00"
        super().__init__(process_name, source)

    def execute(self):
        try:
            print("Injecting...")

            self.open_process()
            self.virtual_alloc_ex()
            self.write_process_memory()

            procedure_address = get_procedure_address()

            injection = winapi_kernel32.CreateRemoteThread(
                self.handle,
                None,
                0,
                procedure_address,
                self.memory,
                EXECUTE_IMMEDIATELY,
                None
            )

            if not injection:
                raise ctypes.WinError(ctypes.get_last_error())

            print("kernel32 LoadLibraryA:", hex(procedure_address))
            print("remote memory:", hex(self.memory))
            print("dll path:", self.source)

            winapi_kernel32.WaitForSingleObject(injection, 0xFFFFFFFF)

            print('[*] Injected the source into the process')

            winapi_kernel32.CloseHandle(injection)
            winapi_kernel32.CloseHandle(self.handle)

        except Exception as error:
            print(f"[*] Error: {error}")

    

    