# axm/signals.py

class Signal(Exception):
    pass

class ReturnSignal(Signal):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"ReturnSignal({self.value})"

class BreakSignal(Signal):
    def __repr__(self):
        return "BreakSignal"