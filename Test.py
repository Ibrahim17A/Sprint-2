import unittest
from unittest.mock import MagicMock
from sos_game import SOSGame, SOSGameGUI  # Adjust the import according to your file structure

class TestSOSGame(unittest.TestCase):

    def setUp(self):
        self.game = SOSGame(board_size=3, game_mode="Simple")

    def test_initial_board(self):
        self.assertEqual(self.game.board, [['', '', ''], ['', '', ''], ['', '', '']])
        self.assertEqual(self.game.current_turn, 'blue')

    def test_make_move_valid(self):
        self.game.make_move(0, 0, 'S')
        self.assertEqual(self.game.board[0][0], 'S')
        self.assertEqual(self.game.current_turn, 'red')

    def test_make_move_invalid(self):
        self.game.make_move(0, 0, 'S')
        with self.assertRaises(ValueError):
            self.game.make_move(0, 0, 'O')

    def test_switch_turn(self):
        self.assertEqual(self.game.current_turn, 'blue')
        self.game.switch_turn()
        self.assertEqual(self.game.current_turn, 'red')
        self.game.switch_turn()
        self.assertEqual(self.game.current_turn, 'blue')

    def test_full_board(self):
        self.game.make_move(0, 0, 'S')
        self.game.make_move(0, 1, 'O')
        self.game.make_move(0, 2, 'S')
        self.game.make_move(1, 0, 'O')
        self.game.make_move(1, 1, 'S')
        self.game.make_move(1, 2, 'O')
        self.game.make_move(2, 0, 'S')
        self.game.make_move(2, 1, 'O')
        self.game.make_move(2, 2, 'S')
        with self.assertRaises(ValueError):
            self.game.make_move(2, 2, 'O')  # Attempting to move on a full board

class TestSOSGameGUI(unittest.TestCase):
    
    def setUp(self):
        self.gui = SOSGameGUI()
        self.gui.master = MagicMock()  # Mock the master window to avoid opening a window

    def test_widgets_created(self):
        self.assertIsNotNone(self.gui.title_label)
        self.assertEqual(self.gui.title_label.cget("text"), "SOS")
        self.assertIsNotNone(self.gui.mode_var)
        self.assertEqual(self.gui.mode_var.get(), "Simple")
        self.assertIsNotNone(self.gui.current_player_label)
        self.assertEqual(self.gui.current_player_label.cget("text"), "Current Player: BLUE")

    def test_new_game_button(self):
        self.gui.new_game()  # Start a new game
        self.assertEqual(self.gui.board_size, 3)  # Should reset to default size
        self.assertEqual(self.gui.current_player_label.cget("text"), "Current Player: BLUE")

    def test_on_cell_click(self):
        # Setup for testing cell click
        self.gui.new_game()  # Reset the game
        self.gui.on_cell_click(0, 0)  # Simulate clicking on the top left cell
        self.assertEqual(self.gui.board_buttons[0][0].cget("text"), 'S')  # Default letter is 'S'
        self.assertEqual(self.gui.board_buttons[0][0].cget("fg"), 'blue')  # Text color for blue player

        self.gui.move_var.set('O')  # Switch to 'O'
        self.gui.on_cell_click(1, 1)  # Simulate red player clicking
        self.assertEqual(self.gui.board_buttons[1][1].cget("text"), 'O')  # Now should show 'O'
        self.assertEqual(self.gui.board_buttons[1][1].cget("fg"), 'red')  # Text color for red player

if __name__ == "__main__":
    unittest.main()
