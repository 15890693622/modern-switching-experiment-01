import sys,importlib

def check():
    if sys.version_info<(3,10):raise RuntimeError('Python 3.10+ required')
    for name in ('numpy','matplotlib','pytest'):importlib.import_module(name)
    print('环境配置正确')

if __name__=='__main__':check()
