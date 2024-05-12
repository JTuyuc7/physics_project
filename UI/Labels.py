import tkinter as tk
from typing import Optional, Tuple


class LabelsUi:
    def __init__(self, text: str, font: Optional[Tuple] = None, grid: Tuple = ()):
        self.text = text
        self.font = font
        self.grid = grid
        self.label = None

    def pack_data(self):
        self.label = tk.Label(text=self.text, font=self.font)
        self.label.grid(**self.grid)

    def update_text(self, new_text):
        if self.label:
            self.label.config(text=new_text)
