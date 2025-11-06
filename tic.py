import tkinter as tk
from itertools import cycle
from tkinter import font
from typing import NamedTuple

# Data structures for players and moves
class Player(NamedTuple):
    label: str
    color: str

class Move(NamedTuple):
    row: int
    col: int
    label: str = ""

# Constants
BOARD_SIZE = 3
DEFAULT_PLAYERS = (
    Player(label="X", color="#1E90FF"),  # Dodger Blue
    Player(label="O", color="#32CD32"),  # Lime Green
)

# Game logic class
class TicTacToeGame:
    def __init__(self, players=DEFAULT_PLAYERS, board_size=BOARD_SIZE):
        self._players = cycle(players)
        self.board_size = board_size
        self.current_player = next(self._players)
        self.winner_combo = []
        self._current_moves = []
        self._has_winner = False
        self._winning_combos = []
        self._setup_board()

    def _setup_board(self):
        self._current_moves = [
            [Move(row, col) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]
        self._winning_combos = self._get_winning_combos()

    def _get_winning_combos(self):
        rows = [[(move.row, move.col) for move in row] for row in self._current_moves]
        columns = [list(col) for col in zip(*rows)]
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]
        return rows + columns + [first_diagonal, second_diagonal]

    def toggle_player(self):
        self.current_player = next(self._players)

    def is_valid_move(self, move):
        row, col = move.row, move.col
        return self._current_moves[row][col].label == "" and not self._has_winner

    def process_move(self, move):
        row, col = move.row, move.col
        self._current_moves[row][col] = move
        for combo in self._winning_combos:
            results = set(self._current_moves[n][m].label for n, m in combo)
            if len(results) == 1 and "" not in results:
                self._has_winner = True
                self.winner_combo = combo
                break

    def has_winner(self):
        return self._has_winner

    def is_tied(self):
        return not self._has_winner and all(move.label for row in self._current_moves for move in row)

    def reset_game(self):
        for row, row_content in enumerate(self._current_moves):
            for col, _ in enumerate(row_content):
                row_content[col] = Move(row, col)
        self._has_winner = False
        self.winner_combo = []

# UI Class
class TicTacToeBoard(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title("🎮 Colorful Tic-Tac-Toe 🎮")
        self.configure(bg="#222831")  # Dark background
        self._cells = {}
        self._game = game
        self._create_menu()
        self._create_board_display()
        self._create_board_grid()

    def _create_menu(self):
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(master=menu_bar, tearoff=0)
        file_menu.add_command(label="🔄 Play Again", command=self.reset_board)
        file_menu.add_separator()
        file_menu.add_command(label="❌ Exit", command=self.destroy)
        menu_bar.add_cascade(label="", menu=file_menu)

    def _create_board_display(self):
        display_frame = tk.Frame(master=self, bg="#393E46")
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text="Ready to Play!",
            font=font.Font(size=28, weight="bold"),
            bg="#393E46",
            fg="#FFD369",  # Yellow
            pady=15
        )
        self.display.pack()

    def _create_board_grid(self):
        grid_frame = tk.Frame(master=self, bg="#222831")
        grid_frame.pack(pady=10)
        for row in range(self._game.board_size):
            self.rowconfigure(row, weight=1)
            self.columnconfigure(row, weight=1)
            for col in range(self._game.board_size):
                button = tk.Button(
                    master=grid_frame,
                    text="",
                    font=font.Font(size=36, weight="bold"),
                    fg="#EEEEEE",
                    bg="#00ADB5",  # Teal
                    activebackground="#393E46",
                    width=4,
                    height=2,
                    relief="raised",
                    bd=4
                )
                self._cells[button] = (row, col)
                button.bind("<ButtonPress-1>", self.play)
                button.grid(row=row, column=col, padx=5, pady=5)

    def play(self, event):
        if self._game.has_winner():
            return
        clicked_btn = event.widget
        row, col = self._cells[clicked_btn]
        move = Move(row, col, self._game.current_player.label)
        if self._game.is_valid_move(move):
            self._update_button(clicked_btn)
            self._game.process_move(move)
            if self._game.is_tied():
                self._update_display("🤝 Tied game!", "#FFD369")
            elif self._game.has_winner():
                self._highlight_cells()
                msg = f'🎉 Player "{self._game.current_player.label}" wins!'
                color = self._game.current_player.color
                self._update_display(msg, color)
            else:
                self._game.toggle_player()
                msg = f"🎯 {self._game.current_player.label}'s Turn"
                self._update_display(msg, self._game.current_player.color)

    def _update_button(self, clicked_btn):
        clicked_btn.config(
            text=self._game.current_player.label,
            fg=self._game.current_player.color,
            state="disabled"
        )

    def _update_display(self, msg, color="#FFD369"):
        self.display.config(text=msg, fg=color)

    def _highlight_cells(self):
        for button, coordinates in self._cells.items():
            if coordinates in self._game.winner_combo:
                button.config(bg="#FF2E63")  # Vibrant Red

    def reset_board(self):
        self._game.reset_game()
        self._update_display("Ready to Play!", "#FFD369")
        for button in self._cells:
            button.config(text="", fg="#EEEEEE", bg="#00ADB5", state="normal")

# Main execution
def main():
    game = TicTacToeGame()
    board = TicTacToeBoard(game)
    board.mainloop()

# Entry point
if __name__ == "__main__":
    main()

