import tkinter as tk
from tkinter import messagebox
import random


class TicTacToe:
    def __init__(self, window):
        # Настройка основного окна
        self.window = window
        self.window.title("Крестики-нолики")
        self.window.geometry("300x400")
        self.window.resizable(False, False)

        # Переменные игры
        self.current_player = "X"
        self.player_symbol = "X"
        self.computer_symbol = "0"
        self.game_mode = "player"  # "player" или "computer"
        self.buttons = []
        self.x_wins = 0
        self.o_wins = 0
        self.ties = 0

        # Цвета
        self.colors = {
            "X": "lightblue",
            "0": "lightyellow",
            "win": "lightgreen",
            "lose": "lightcoral",
            "bg": "white",
            "reset": "lightgray"
        }

        # Создание интерфейса
        self.create_mode_selection()
        self.create_game_board()
        self.create_scoreboard()
        self.create_reset_button()

        # Если игра с компьютером и компьютер ходит первым
        if self.game_mode == "computer" and self.player_symbol == "0":
            self.computer_move()





# Запуск игры
if __name__ == "__main__":
    window = tk.Tk()
    game = TicTacToe(window)
    window.mainloop()
