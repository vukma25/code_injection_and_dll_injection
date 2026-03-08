import ctypes
from ctypes import wintypes
from structure.process_entry import PROCESSENTRY32
from .wrapper import WindowAPI

winapi_kernel32 = WindowAPI("kernel32")

winapi_kernel32.bind(
    "OpenProcess",
    [wintypes.DWORD,wintypes.BOOL,wintypes.DWORD],
    wintypes.HANDLE
)

winapi_kernel32.bind(
    "VirtualAllocEx",
    [wintypes.HANDLE, wintypes.LPVOID, ctypes.c_size_t, wintypes.DWORD,wintypes.DWORD],
    wintypes.LPVOID
)

winapi_kernel32.bind(
    "WriteProcessMemory",
    [wintypes.HANDLE, wintypes.LPVOID, wintypes.LPCVOID, ctypes.c_size_t, wintypes.LPVOID],
    wintypes.BOOL
)

winapi_kernel32.bind(
    "CreateRemoteThread",
    [wintypes.HANDLE, wintypes.LPVOID, ctypes.c_size_t, wintypes.LPVOID, wintypes.LPVOID, wintypes.DWORD, wintypes.LPDWORD],
    wintypes.HANDLE
)

winapi_kernel32.bind(
    "CloseHandle",
    [wintypes.HANDLE],
    wintypes.BOOL
)

winapi_kernel32.bind(
    "LoadLibraryA",
    [wintypes.LPCSTR],
    wintypes.HMODULE
)

winapi_kernel32.bind(
    "GetModuleHandleA",
    [wintypes.LPCSTR],
    wintypes.HMODULE
)

winapi_kernel32.bind(
    "GetProcAddress",
    [wintypes.HMODULE, wintypes.LPCSTR],
    ctypes.c_void_p
)

winapi_kernel32.bind(
    "FreeLibrary",
    [wintypes.HMODULE],
    ctypes.c_bool
)

winapi_kernel32.bind(
    "CreateToolhelp32Snapshot",
    [wintypes.DWORD, wintypes.DWORD],
    wintypes.HANDLE
)

winapi_kernel32.bind(
    "Process32First",
    [wintypes.HANDLE, ctypes.POINTER(PROCESSENTRY32)],
    wintypes.BOOL
)

winapi_kernel32.bind(
    "Process32Next",
    [wintypes.HANDLE, ctypes.POINTER(PROCESSENTRY32)],
    wintypes.BOOL
)

winapi_kernel32.bind(
    "CloseHandle",
    [wintypes.HANDLE],
    wintypes.BOOL
)

winapi_kernel32.bind(
    "VirtualFreeEx",
    [wintypes.HANDLE, wintypes.LPVOID, ctypes.c_size_t, wintypes.DWORD],
    wintypes.BOOL
)