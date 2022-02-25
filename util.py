import os

def clear():
    os.system('cls' if os.name == "nt" else "clear")

class ProgressBar:
    def __init__(self, max_value):
        self.max_value = max_value
        self.value = 0

    def add(self):
        if( self.value != self.max_value ):
            self.value += 1

    def show(self):
        percentage = self.value * 100 / self.max_value
        return f"[{'=' * (int(percentage) - 1)}{'>' if percentage else ''}{'-' * (100 - int(percentage))}] {int(percentage)}%"