import ctypes
print("attempting to open dll")

lib = ctypes.windll.LoadLibrary("example_dll.dll")