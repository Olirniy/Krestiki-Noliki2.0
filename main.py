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

        # === Часть 1: Создание графического интерфейса ===

        def create_mode_selection(self):
            """Создает элементы выбора режима игры и символа игрока"""
            mode_frame = tk.Frame(self.window)
            mode_frame.pack(pady=5)

            tk.Label(mode_frame, text="Режим игры:").pack()

            self.mode_var = tk.StringVar(value="player")
            tk.Radiobutton(mode_frame, text="Два игрока", variable=self.mode_var,
                           value="player", command=self.set_game_mode).pack(anchor="w")
            tk.Radiobutton(mode_frame, text="Против компьютера", variable=self.mode_var,
                           value="computer", command=self.set_game_mode).pack(anchor="w")

            symbol_frame = tk.Frame(self.window)
            symbol_frame.pack(pady=5)

            tk.Label(symbol_frame, text="Играть за:").pack()

            self.symbol_var = tk.StringVar(value="X")
            tk.Radiobutton(symbol_frame, text="Крестики (X)", variable=self.symbol_var,
                           value="X", command=self.set_player_symbol).pack(anchor="w")
            tk.Radiobutton(symbol_frame, text="Нолики (0)", variable=self.symbol_var,
                           value="0", command=self.set_player_symbol).pack(anchor="w")

        def create_game_board(self):
            """Создает игровое поле 3x3"""
            board_frame = tk.Frame(self.window)
            board_frame.pack(pady=10)

            for i in range(3):
                row = []
                for j in range(3):
                    btn = tk.Button(
                        board_frame,
                        text="",
                        font=("Arial", 24),
                        width=3,
                        height=1,
                        bg=self.colors["bg"],
                        command=lambda r=i, c=j: self.on_click(r, c)
                    )
                    btn.grid(row=i, column=j, padx=5, pady=5)
                    row.append(btn)
                self.buttons.append(row)

        def create_scoreboard(self):
            """Создает панель счета"""
            self.score_frame = tk.Frame(self.window)
            self.score_frame.pack(pady=5)

            self.x_score_label = tk.Label(self.score_frame, text="X: 0", font=("Arial", 12))
            self.x_score_label.pack(side="left", padx=10)

            self.tie_score_label = tk.Label(self.score_frame, text="Ничьи: 0", font=("Arial", 12))
            self.tie_score_label.pack(side="left", padx=10)

            self.o_score_label = tk.Label(self.score_frame, text="0: 0", font=("Arial", 12))
            self.o_score_label.pack(side="left", padx=10)

        def create_reset_button(self):
            """Создает кнопку сброса игры"""
            reset_btn = tk.Button(
                self.window,
                text="Новая игра",
                font=("Arial", 12),
                bg=self.colors["reset"],
                command=self.reset_game
            )
            reset_btn.pack(pady=10)





# Запуск игры
if __name__ == "__main__":
    window = tk.Tk()
    game = TicTacToe(window)
    window.mainloop()
