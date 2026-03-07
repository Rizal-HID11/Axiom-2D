# axm/signals.py

class Signal(Exception):
    pass

class ReturnSignal(Signal):
    def __init__(self, value):
        self.value = value

class BreakSignal(Signal):
    pass