import ctypes
from ctypes import wintypes
from structure.process_entry import PROCESSENTRY32
from constants.variable import *
from window_api.api import winapi_kernel32
import wmi

def get_process_id_ex(process_name):
    try:
        snapshot =\
        winapi_kernel32\
        .CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
        process_entry = PROCESSENTRY32()
        process_entry.dwSize = ctypes.sizeof(PROCESSENTRY32)

        if not winapi_kernel32\
            .Process32First(snapshot, ctypes.byref(process_entry)):
            print("[*] No have any process")
            return None

        while True:
            current_name =process_entry.szExeFile\
                .decode('utf-8', errors='ignore').lower()
            if current_name == process_name.lower():
                pid = int(process_entry.th32ProcessID)
                print(f"[*] {process_name} have process id: {pid}")
                return pid

            if not winapi_kernel32\
                .Process32Next(snapshot, ctypes.byref(process_entry)):
                break
    except Exception:
        error_code = ctypes.get_last_error()
        raise ctypes.WinError(error_code)
    finally:
        if snapshot != INVALID_HANDLE_VALUE:
            winapi_kernel32.CloseHandle(snapshot)

    return None

def get_process_id(process_name):
    processes = wmi.WMI().Win32_Process(name=process_name)
    if len(processes) == 0:
        return None

    pid = processes[0].ProcessId
    print(f"[*] {process_name} have process id: {pid}")

    return int(pid)

if __name__ == "__main__":
    pid_1 = get_process_id("mspaint.exe")
    pid_2 = get_process_id_ex("mspaint.exe")
    print(f"[*] mspaint.exe have PID: {pid_1} - {pid_2}")


