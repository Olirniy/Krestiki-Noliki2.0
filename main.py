
import tkinter as tk
from tkinter import messagebox
import random
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='tictactoe.log',
    filemode='w'
)
logger = logging.getLogger(__name__)

# Добавляем вывод логов в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


class TicTacToe:
    def __init__(self, window):
        logger.info("Инициализация игры")
        print("Инициализация игры")

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
        self.game_active = True
        self.waiting_for_computer = False

        # Цвета
        self.colors = {
            "X": "cornflower blue",
            "0": "turquoise",
            "win": "SpringGreen",
            "lose": "brown1",
            "bg": "AntiqueWhite4",
            "reset": "grey1"
        }

        # Создание интерфейса
        self.create_mode_selection()
        self.create_game_board()
        self.create_scoreboard()
        self.create_reset_button()

        logger.info(f"Игра инициализирована. Режим: {self.game_mode}, Игрок: {self.player_symbol}")
        print(f"Игра инициализирована. Режим: {self.game_mode}, Игрок: {self.player_symbol}")

    def make_move(self, row, col, symbol):
        """Выполняет ход на указанной клетке"""
        self.buttons[row][col]['text'] = symbol
        self.buttons[row][col]['bg'] = self.colors[symbol]
        logger.info(f"Ход {symbol} на клетку ({row}, {col})")
        print(f"Ход {symbol} на клетку ({row}, {col})")

    def set_game_mode(self):
        """Устанавливает режим игры"""
        self.game_mode = self.mode_var.get()
        logger.info(f"Установлен режим игры: {self.game_mode}")
        print(f"Установлен режим игры: {self.game_mode}")
        self.reset_game()

    def set_player_symbol(self):
        """Устанавливает символ, которым играет игрок"""
        self.player_symbol = self.symbol_var.get()
        self.computer_symbol = "0" if self.player_symbol == "X" else "X"
        logger.info(f"Игрок выбрал символ: {self.player_symbol}, Компьютер: {self.computer_symbol}")
        print(f"Игрок выбрал символ: {self.player_symbol}, Компьютер: {self.computer_symbol}")
        self.reset_game()  # Вся логика теперь в reset_game

    def reset_game(self):
        """Сбрасывает текущую игру, но сохраняет счет"""
        # Сначала сбрасываем состояние игры
        self.game_active = True
        self.waiting_for_computer = False

        # Очищаем поле
        for row in self.buttons:
            for btn in row:
                btn['text'] = ""
                btn['bg'] = self.colors["bg"]

        # Всегда начинаем с X
        self.current_player = "X"

        # Если игра с компьютером и игрок выбрал "0"
        if self.game_mode == "computer" and self.player_symbol == "0":
            logger.info("Компьютер ходит первым (игрок выбрал нолики)")
            print("Компьютер ходит первым (игрок выбрал нолики)")
            self.current_player = self.computer_symbol
            self.game_active = True  # Явно активируем игру
            self.computer_move()  # Непосредственный вызов хода компьютера
        else:
            logger.info("Сброс игры. Первый ход за X")
            print("Сброс игры. Первый ход за X")

    def reset_match(self):
        """Сбрасывает весь матч"""
        self.x_wins = 0
        self.o_wins = 0
        self.ties = 0
        self.x_score_label.config(text="X: 0")
        self.o_score_label.config(text="0: 0")
        self.tie_score_label.config(text="Ничьи: 0")
        logger.info("Сброс матча")
        print("Сброс матча")
        self.reset_game()

    def create_mode_selection(self):
        """Создает элементы выбора режима"""
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
        """Создает игровое поле"""
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
        logger.info("Игровое поле создано")
        print("Игровое поле создано")

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
        logger.info("Панель счета создана")
        print("Панель счета создана")

    def create_reset_button(self):
        """Создает кнопку сброса"""
        reset_btn = tk.Button(
            self.window,
            text="Новая игра",
            font=("Arial", 12),
            bg=self.colors["reset"],
            command=self.reset_game
        )
        reset_btn.pack(pady=10)
        logger.info("Кнопка сброса создана")
        print("Кнопка сброса создана")

    def on_click(self, row, col):
        """Обрабатывает клик по клетке"""
        if not self.game_active or self.waiting_for_computer or self.buttons[row][col]['text'] != "":
            logger.debug(f"Клик по клетке ({row}, {col}) проигнорирован")
            print(f"Клик по клетке ({row}, {col}) проигнорирован")
            return

        if self.game_mode == "computer" and self.current_player != self.player_symbol:
            logger.debug("Игрок пытается сделать ход за компьютер")
            print("Игрок пытается сделать ход за компьютер")
            return

        logger.info(f"Игрок кликнул на клетку ({row}, {col})")
        print(f"Игрок кликнул на клетку ({row}, {col})")

        self.make_move(row, col, self.current_player)

        if self.check_winner():
            self.handle_win()
        elif self.is_board_full():
            self.handle_tie()
        else:
            self.switch_player()
            if self.game_mode == "computer" and self.current_player == self.computer_symbol:
                logger.info("Запланирован ход компьютера")
                print("Запланирован ход компьютера")
                self.waiting_for_computer = True
                self.window.after(500, self.computer_move)

    def computer_move(self):
        """Обрабатывает ход компьютера"""
        if not self.game_active:
            logger.debug("Попытка хода компьютера в неактивной игре")
            print("Попытка хода компьютера в неактивной игре")
            return

        logger.info("Компьютер делает ход")
        print("Компьютер делает ход")

        # Сначала проверяем, может ли компьютер выиграть
        for i in range(3):
            for j in range(3):
                if self.buttons[i][j]['text'] == "":
                    self.buttons[i][j]['text'] = self.computer_symbol
                    if self.check_winner():
                        self.make_move(i, j, self.computer_symbol)
                        self.handle_win()
                        self.waiting_for_computer = False
                        return
                    self.buttons[i][j]['text'] = ""

        # Затем проверяем, может ли игрок выиграть следующим ходом (блокировка игрока)
        for i in range(3):
            for j in range(3):
                if self.buttons[i][j]['text'] == "":
                    self.buttons[i][j]['text'] = self.player_symbol
                    if self.check_winner():
                        self.buttons[i][j]['text'] = ""
                        self.make_move(i, j, self.computer_symbol)
                        if self.check_winner():
                            self.handle_win()
                        else:
                            self.switch_player()
                        self.waiting_for_computer = False
                        return
                    self.buttons[i][j]['text'] = ""

        # Если центр свободен, занимаем его
        if self.buttons[1][1]['text'] == "":
            self.make_move(1, 1, self.computer_symbol)
        else:
            # Иначе выбираем случайную свободную клетку
            empty_cells = []
            for i in range(3):
                for j in range(3):
                    if self.buttons[i][j]['text'] == "":
                        empty_cells.append((i, j))

            if empty_cells:
                row, col = random.choice(empty_cells)
                self.make_move(row, col, self.computer_symbol)

        if self.check_winner():
            self.handle_win()
        elif self.is_board_full():
            self.handle_tie()
        else:
            self.switch_player()

        self.waiting_for_computer = False

    def check_winner(self):
        """Проверяет наличие победителя"""
        # Проверка строк и столбцов
        for i in range(3):
            if self.buttons[i][0]['text'] == self.buttons[i][1]['text'] == self.buttons[i][2]['text'] != "":
                logger.info(f"Победа по строке {i}")
                print(f"Победа по строке {i}")
                return True
            if self.buttons[0][i]['text'] == self.buttons[1][i]['text'] == self.buttons[2][i]['text'] != "":
                logger.info(f"Победа по столбцу {i}")
                print(f"Победа по столбцу {i}")
                return True

        # Проверка диагоналей
        if self.buttons[0][0]['text'] == self.buttons[1][1]['text'] == self.buttons[2][2]['text'] != "":
            logger.info("Победа по главной диагонали")
            print("Победа по главной диагонали")
            return True
        if self.buttons[0][2]['text'] == self.buttons[1][1]['text'] == self.buttons[2][0]['text'] != "":
            logger.info("Победа по побочной диагонали")
            print("Победа по побочной диагонали")
            return True

        return False

    def is_board_full(self):
        """Проверяет, заполнено ли поле"""
        for row in self.buttons:
            for btn in row:
                if btn['text'] == "":
                    return False
        logger.info("Ничья - поле заполнено")
        print("Ничья - поле заполнено")
        return True

    def handle_win(self):
        """Обрабатывает победу"""
        self.game_active = False
        self.waiting_for_computer = False
        winner = self.current_player
        logger.info(f"Игрок {winner} победил")
        print(f"Игрок {winner} победил")

        if winner == "X":
            self.x_wins += 1
            self.x_score_label.config(text=f"X: {self.x_wins}")
        else:
            self.o_wins += 1
            self.o_score_label.config(text=f"0: {self.o_wins}")

        self.highlight_winning_cells()

        if self.x_wins >= 3 or self.o_wins >= 3:
            message = f"Игрок {winner} выиграл матч со счетом {max(self.x_wins, self.o_wins)}-{min(self.x_wins, self.o_wins)}!"
            logger.info(f"Матч окончен. {message}")
            print(f"Матч окончен. {message}")
            messagebox.showinfo("Матч окончен", message)
            self.reset_match()
        else:
            messagebox.showinfo("Игра окончена", f"Игрок {winner} победил!")
            self.reset_game()

    def highlight_winning_cells(self):
        """Подсвечивает выигрышные клетки"""
        winner = self.current_player
        loser = "0" if winner == "X" else "X"
        logger.info(f"Подсветка клеток: победитель {winner}, проигравший {loser}")
        print(f"Подсветка клеток: победитель {winner}, проигравший {loser}")

        for row in self.buttons:
            for btn in row:
                if btn['text'] == winner:
                    btn['bg'] = self.colors["win"]
                elif btn['text'] == loser:
                    btn['bg'] = self.colors["lose"]

    def handle_tie(self):
        """Обрабатывает ничью"""
        self.game_active = False
        self.waiting_for_computer = False
        self.ties += 1
        self.tie_score_label.config(text=f"Ничьи: {self.ties}")
        logger.info("Ничья")
        print("Ничья")
        messagebox.showinfo("Игра окончена", "Ничья!")
        self.reset_game()

    def switch_player(self):
        """Меняет текущего игрока"""
        self.current_player = "0" if self.current_player == "X" else "X"
        logger.info(f"Смена игрока. Теперь ходит: {self.current_player}")
        print(f"Смена игрока. Теперь ходит: {self.current_player}")


# Запуск игры
if __name__ == "__main__":
    window = tk.Tk()
    game = TicTacToe(window)
    window.mainloop()