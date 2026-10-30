import importlib, inspect, json, sys
mod = importlib.import_module('google.antigravity')
Agent = getattr(mod, 'Agent')
methods = [m for m in dir(Agent) if not m.startswith('_')]
print('Agent methods:', methods)
print('Docstring:', inspect.getdoc(Agent))

