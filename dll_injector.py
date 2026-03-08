from injector import Injector, WaitForSingleObject
from constants.variable import *
from window_api.api import winapi_kernel32

def get_procedure_address():
    h_kernel32 = winapi_kernel32.GetModuleHandleA(b'kernel32.dll')
    procedure_address = winapi_kernel32.GetProcAddress(h_kernel32, b'LoadLibraryA')
    return procedure_address

class DllInjector(Injector):
    def __init__(self, process_name, path):
        source = path.encode("ascii") + b"\x00"
        print(source)
        super().__init__(process_name, source)
    def create_remote_thread(self):
        try:
            procedure_address = get_procedure_address()
        except Exception as e:
            raise TypeError(f"[*] Catched an error-2: {e}")
        else:
            self.thread = winapi_kernel32.CreateRemoteThread(
                    self.handle,
                    None,
                    0,
                    procedure_address,
                    self.memory,
                    EXECUTE_IMMEDIATELY,
                    None
                )

            WaitForSingleObject(self.thread, 0xFFFFFFFF)
            print("[*] Created a remote thread in target process")

    

    