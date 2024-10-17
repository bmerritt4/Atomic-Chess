# Author: Brian Merritt
# GitHub username: bmerritt4
# Date: 6/9/2024
# Description: Defines a class 'ChessVar' that implements the game logic for Atomic Chess.
#              The class handles piece movements, turn management, and special rules. It
#              includes methods for validating moves, executing moves, and updating the
#              game state, including detecting when a king is captured and the game ends.
#              The board's state is managed and can be printed for visualization.

class ChessVar:
    """Class representing an Atomic Chess game.

    Responsibilities:
    - Initialize the game with the standard chess starting position.
    - Keep track of the current board state and turn order.
    - Handle moves, including validations and updating the board.
    - Manage special rules of Atomic Chess, including explosion effects.
    - Determine and update the game state.

    Communicates with:
    - Internal methods for move validation, explosion handling, and game state determination.
    """

    def __init__(self):
        """Initialize the board, turn order, and game state."""
        self._board = self._initialize_board()
        self._turn = 'WHITE'
        self._game_state = 'UNFINISHED'

    @staticmethod
    def _initialize_board():
        """Initialize the board with pieces in their starting positions."""
        return [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["R", "N", "B", "Q", "K", "B", "N", "R"]
        ]

    def get_game_state(self):
        """Return the current game state ('UNFINISHED', 'WHITE_WON', 'BLACK_WON')."""
        return self._game_state

    def make_move(self, start, end):
        """Attempt to make a move from 'start' to 'end'.

        Parameters:
        - start: A string representing the starting square (e.g., 'd2').
        - end: A string representing the ending square (e.g., 'd4').

        Returns:
        - True if the move is valid and made successfully.
        - False if the move is invalid or the game is already won.
        """
        if self._game_state != 'UNFINISHED':
            return False

        if not self._is_valid_move(start, end):
            return False

        start_row, start_col = self._convert_to_indices(start)
        end_row, end_col = self._convert_to_indices(end)
        piece = self._board[start_row][start_col]
        target = self._board[end_row][end_col]

        # Execute the move
        self._board[end_row][end_col] = piece
        self._board[start_row][start_col] = ' '

        # Handle explosion effects if a piece is captured
        if target != ' ':
            self._handle_explosion(end_row, end_col)

        # Switch turns
        self._turn = 'BLACK' if self._turn == 'WHITE' else 'WHITE'

        # Check for end of game
        if self._is_king_captured():
            self._game_state = 'BLACK_WON' if self._turn == 'WHITE' else 'WHITE_WON'

        return True

    def print_board(self):
        """Print the current state of the board."""
        for row in self._board:
            print(" ".join(row))
        print()

    def _is_valid_move(self, start, end):
        """Check if the move from 'start' to 'end' is valid.

        Parameters:
        - start: A string representing the starting square.
        - end: A string representing the ending square.

        Returns:
        - True if the move is valid.
        - False otherwise.

        Validates the following for each piece type:
        - Pawns: Can move one square forward or two squares from their initial position, capture diagonally, cannot
          capture directly forward.
        - Knights: Move in an L-shape (two squares in one direction and one square perpendicular).
        - Bishops: Move diagonally any number of squares.
        - Rooks: Move horizontally or vertically any number of squares.
        - Queens: Move horizontally, vertically, or diagonally any number of squares.
        - Kings: Move one square in any direction but cannot capture due to the special rule in Atomic Chess.
        """
        start_row, start_col = self._convert_to_indices(start)
        end_row, end_col = self._convert_to_indices(end)
        piece = self._board[start_row][start_col]
        target = self._board[end_row][end_col]

        # Ensure the piece belongs to the current player
        if (self._turn == 'WHITE' and piece.islower()) or (self._turn == 'BLACK' and piece.isupper()):
            return False

        # Ensure the move is within bounds and not the same square
        if start == end or not (0 <= start_row < 8 and 0 <= start_col < 8 and 0 <= end_row < 8 and 0 <= end_col < 8):
            return False

        # Special rule: King cannot make captures
        if piece.upper() == 'K' and target != ' ':
            return False

        # Handle pawn moves
        if piece.upper() == 'P':
            if piece.isupper():  # White pawn
                if start_row == 6 and end_row == 4 and start_col == end_col and self._board[5][start_col] == ' ' and \
                        self._board[4][start_col] == ' ':
                    return True  # Two-square move from starting position
                if end_row == start_row - 1 and start_col == end_col and self._board[end_row][end_col] == ' ':
                    return True  # One-square move forward
                if end_row == start_row - 1 and abs(start_col - end_col) == 1 and target != ' ':
                    return True  # Capture move
            else:  # Black pawn
                if start_row == 1 and end_row == 3 and start_col == end_col and self._board[2][start_col] == ' ' and \
                        self._board[3][start_col] == ' ':
                    return True  # Two-square move from starting position
                if end_row == start_row + 1 and start_col == end_col and self._board[end_row][end_col] == ' ':
                    return True  # One-square move forward
                if end_row == start_row + 1 and abs(start_col - end_col) == 1 and target != ' ':
                    return True  # Capture move
                return False  # Invalid move for black pawn

        # Handle knight moves
        if piece.upper() == 'N':
            row_diff = abs(end_row - start_row)
            col_diff = abs(end_col - start_col)
            if (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2):
                return True  # Valid knight move

        # Handle bishop, rook, and queen moves using a helper method
        if piece.upper() in ['B', 'R', 'Q']:
            return self._is_valid_bishop_rook_queen_move(piece, start_row, start_col, end_row, end_col)

        if piece.upper() == 'K':
            if abs(end_row - start_row) <= 1 and abs(end_col - start_col) <= 1:
                return True  # Valid king move

        return False

    def _is_valid_bishop_rook_queen_move(self, piece, start_row, start_col, end_row, end_col):
        """Check if the move for a bishop, rook, or queen is valid.

        Parameters:
        - piece: The piece being moved.
        - start_row: The starting row index.
        - start_col: The starting column index.
        - end_row: The ending row index.
        - end_col: The ending column index.

        Returns:
        - True if the move is valid.
        - False otherwise.
        """
        if piece.upper() == 'B' or piece.upper() == 'Q':
            # Diagonal move like a bishop
            if abs(end_row - start_row) == abs(end_col - start_col):
                row_step = 1 if end_row > start_row else -1
                col_step = 1 if end_col > start_col else -1
                current_row = start_row + row_step
                current_col = start_col + col_step
                while current_row != end_row and current_col != end_col:
                    if self._board[current_row][current_col] != ' ':
                        return False  # Path is blocked
                    current_row += row_step
                    current_col += col_step
                return True  # Valid bishop-like move

        if piece.upper() == 'R' or piece.upper() == 'Q':
            # Horizontal or vertical move like a rook
            if start_row == end_row or start_col == end_col:
                if start_row == end_row:
                    # Horizontal move
                    col_step = 1 if end_col > start_col else -1
                    current_col = start_col + col_step
                    while current_col != end_col:
                        if self._board[start_row][current_col] != ' ':
                            return False  # Path is blocked
                        current_col += col_step
                elif start_col == end_col:
                    # Vertical move
                    row_step = 1 if end_row > start_row else -1
                    current_row = start_row + row_step
                    while current_row != end_row:
                        if self._board[current_row][start_col] != ' ':
                            return False  # Path is blocked
                        current_row += row_step
                return True  # Valid rook-like move

        return False

    def _handle_explosion(self, row, col):
        """Handle the explosion effect when a piece is captured at (row, col).

        Parameters:
        - row: The row index of the captured piece.
        - col: The column index of the captured piece.
        """
        # Remove the capturing piece
        self._board[row][col] = ' '
        # Remove pieces in the surrounding 8 squares (except pawns)
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and self._board[r][c] not in 'Pp ':
                self._board[r][c] = ' '

        # Check if the king is in the explosion range
        for dr, dc in directions + [(0, 0)]:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                if self._board[r][c] == 'K':
                    self._game_state = 'BLACK_WON'
                if self._board[r][c] == 'k':
                    self._game_state = 'WHITE_WON'

    def _is_king_captured(self):
        """Check if either king has been captured.

        Returns:
        - True if a king has been captured.
        - False otherwise.
        """
        white_king = black_king = False
        for row in self._board:
            if 'K' in row:
                white_king = True
            if 'k' in row:
                black_king = True
        return not white_king or not black_king

    @staticmethod
    def _convert_to_indices(position):
        """Convert a board position from algebraic notation to indices.

        Parameters:
        - position: A string representing the board position (e.g., 'd2').

        Returns:
        - A tuple (row, col) representing the indices on the board.
        """
        col, row = position
        return 8 - int(row), ord(col) - ord('a')
