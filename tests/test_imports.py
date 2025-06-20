import importlib
import pkgutil
import valon_ai

MODULES = [
    'smc',
    'order_block',
    'fair_value_gap',
    'break_of_structure',
    'risk_management',
    'trailing_stop',
    'mt5_integration',
    'strategy',
]

def test_modules_exist():
    for mod in MODULES:
        assert pkgutil.find_loader(f"valon_ai.{mod}") is not None, (
            f"Module {mod} should be importable"
        )
        importlib.import_module(f"valon_ai.{mod}")

