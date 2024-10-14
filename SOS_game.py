import tkinter as tk
from tkinter import messagebox

# Game Logic Class
class SOSGame:
    def __init__(self, board_size, game_mode):
        # Initialize the game with a board size and game mode
        self.board_size = board_size
        self.game_mode = game_mode
        # Create a 2D board representation initialized with empty strings
        self.board = [['' for _ in range(board_size)] for _ in range(board_size)]
        # Set the starting player to 'blue'
        self.current_turn = 'blue'
    
    def make_move(self, row, col, letter):
        # Check if the selected cell is empty
        if self.board[row][col] == '':
            # Place the letter in the cell
            self.board[row][col] = letter
            # Switch to the other player's turn
            self.switch_turn()
        else:
            # Raise an error if the cell is already occupied
            raise ValueError("Cell is already occupied.")

    def switch_turn(self):
        # Toggle the current turn between 'blue' and 'red'
        self.current_turn = 'red' if self.current_turn == 'blue' else 'blue'

# GUI Class for SOS Game
class SOSGameGUI:
    def __init__(self):
        # Initialize the main window
        self.master = tk.Tk()
        self.master.title("SOS Game")
        # Set default values for board size and game mode
        self.board_size = 3
        self.game_mode = "Simple"
        # Set the default letter for moves
        self.current_letter = 'S'
        # List to hold buttons for the game board
        self.board_buttons = []
        # Create the GUI widgets
        self.create_widgets()
        # Start a new game
        self.new_game()

    def run(self):
        self.master.mainloop()

    def create_widgets(self):
        # Create and place the title label for the game
        self.title_label = tk.Label(self.master, text="SOS", font=("Arial", 24))
        self.title_label.grid(row=0, column=0, pady=10)

        # Create and place the game mode selection label
        self.mode_label = tk.Label(self.master, text="Game Mode:")
        self.mode_label.grid(row=0, column=1)
        # Create a variable to hold the selected game mode
        self.mode_var = tk.StringVar(value="Simple")
        # Create radio buttons for game mode selection
        tk.Radiobutton(self.master, text="Simple", variable=self.mode_var, value="Simple").grid(row=0, column=2)
        tk.Radiobutton(self.master, text="General", variable=self.mode_var, value="General").grid(row=0, column=3)

        # Create and place the board size selection label
        self.board_size_label = tk.Label(self.master, text="Board Size:")
        self.board_size_label.grid(row=0, column=4)
        # Create an entry box for users to input the board size
        self.board_size_entry = tk.Entry(self.master, width=5, font="bold")
        self.board_size_entry.grid(row=0, column=5)
        self.board_size_entry.insert(0, str(self.board_size))  # Set the default size in the entry

        # Create a frame to hold the game board buttons
        self.board_frame = tk.Frame(self.master)
        self.board_frame.grid(row=1, column=1, columnspan=6, pady=10)

        # Create and place the label for the current letter selection
        self.move_label = tk.Label(self.master, text="Current Letter:")
        self.move_label.grid(row=2, column=0, columnspan=2)
        # Variable to hold the currently selected letter
        self.move_var = tk.StringVar(value='S')
        # Create radio buttons for letter selection
        tk.Radiobutton(self.master, text="S", variable=self.move_var, value='S').grid(row=2, column=2)
        tk.Radiobutton(self.master, text="O", variable=self.move_var, value='O').grid(row=2, column=3)

        # Create and place the label to display the current player's turn
        self.current_player_label = tk.Label(self.master, text="Current Player: Blue", font=("Arial", 16, 'bold'), fg='blue')
        self.current_player_label.grid(row=3, column=0, columnspan=6, pady=10)

        # Create a button to start a new game
        self.new_game_button = tk.Button(self.master, text="New Game", command=self.new_game, width=20, height=3)
        self.new_game_button.grid(row=4, column=5, pady=10)

    def create_board(self):
        # Clear the existing board buttons from the UI
        for row in self.board_buttons:
            for btn in row:
                btn.grid_forget()  # Remove the old buttons from the grid
        self.board_buttons = []  # Reset the list

        # Create the board buttons dynamically based on the current board size
        for i in range(self.board_size):
            row_buttons = []
            for j in range(self.board_size):
                # Create a button for each cell with specified font
                btn = tk.Button(self.board_frame, text="", width=6, height=2, font=("Arial", 12, "bold"),
                                command=lambda i=i, j=j: self.on_cell_click(i, j), padx=0, pady=0)
                btn.grid(row=i, column=j)  # Place the button in the grid
                row_buttons.append(btn)  # Add the button to the row list
            self.board_buttons.append(row_buttons)  # Add the row to the board buttons list

    def new_game(self):
        # Validate the board size input
        try:
            board_size_input = self.board_size_entry.get()
            if board_size_input == "":
                self.board_size = 3  # Default size
            else:
                self.board_size = int(board_size_input)
            if self.board_size < 3:
                raise ValueError("Board size must be 3 or greater.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer for the board size (3 or greater).")
            return

        # Reset the game state based on the new board size and game mode
        self.game_mode = self.mode_var.get()  # Get the selected game mode
        self.game = SOSGame(self.board_size, self.game_mode)  # Initialize the game with the new size
        self.set_current_player_label()  # Update the current player label
        self.create_board()  # Create a new game board

    def set_current_player_label(self):
        # Determine the current player's name and color for display
        current_player_name = "Blue" if self.game.current_turn == 'blue' else "Red"
        if self.game.current_turn == 'blue':
            self.current_player_label.config(text=f"Current Player: {current_player_name.upper()}", fg="blue")
        else:
            self.current_player_label.config(text=f"Current Player: {current_player_name.upper()}", fg="red")

    def on_cell_click(self, row, col):
        current_letter = self.move_var.get()  # Get the selected letter (S or O)
        try:
            self.game.make_move(row, col, current_letter)  # Attempt to make the move
            self.board_buttons[row][col].config(text=current_letter)  # Update the button text
            # Update the button color based on the current player
            if self.game.current_turn == 'blue':
                self.board_buttons[row][col].config(fg='red')  # Blue moves
            else:
                self.board_buttons[row][col].config(fg='blue')  # Red moves

            self.set_current_player_label()  # Update the current player label
        except ValueError as e:
            messagebox.showerror("Error", str(e))  # Show error message if the move is invalid

def main():
    sos_game_gui = SOSGameGUI()  # Create an instance of the game GUI
    sos_game_gui.run()

if __name__ == "__main__":
    main()  # Run the main function
