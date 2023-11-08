import pkgutil
import importlib

# Extend __path__ to include core submodules
__path__ = __path__ + [f"{__path__[0]}/core"]

# Dynamically import submodules
for _, name, _ in pkgutil.iter_modules(__path__):
    globals()[name] = importlib.import_module(f"{__name__}.{name}")
