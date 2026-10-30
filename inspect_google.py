import importlib, pkgutil, sys
import google
print('google package path:', google.__path__)
submods = [m.name for m in pkgutil.iter_modules(google.__path__)]
print('submodules:', submods)
# try importing antigravity
antigrav = importlib.import_module('google.antigravity')
print('antigravity attributes:', dir(antigrav)[:20])

