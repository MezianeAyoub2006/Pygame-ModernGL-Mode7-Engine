from src.app import App

# remove auto dpi (windows only)
import ctypes
try:
    ctypes.windll.user32.SetProcessDPIAware() 
except:
    pass 

if __name__ == "__main__":
    App().run()

