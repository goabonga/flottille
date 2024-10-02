import importlib

def test_init_flottille():
    module = importlib.import_module("flottille")
    assert type(module).__name__ == "module"
