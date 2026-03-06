from injector import Injector

class CodeInjector(Injector):
    def __init__(self, process_name, shellcode):
        super().__init__(process_name, shellcode)