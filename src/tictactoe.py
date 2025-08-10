import numpy as np

class TicTacToe:
    
    def __init__(self):
        self.board = np.zeros((3, 3), dtype = int)
        self.current_player = 1
        self.game_over = False
        self.winner = None

    
    def reset(self):
        self.board = np.zeros((3, 3), dtype = int)
        self.current_player = 1
        self.game_over = False
        self.winner = None
        return self.get_state()

    
    def get_state(self):
        """Return the current state of the gameboard.

        Returns:
            tuple: A tuple representation of the gameboard, where each
                inner tuple corresponds to a row in the board.
        """
        return tuple(map(tuple, self.board))

    def get_possible_actions(self):
        """Return a list of empty cells on the gameboard.

        Returns:
            list of tuples: A list containing tuples (row, col) for each
                            empty cell, indicating where a player can
                            make a move.
        """       
        rows, cols = self.board.shape
        possible_actions = []
    
        for i in range(rows):
            for j in range(cols):
                if self.board[i][j] == 0:
                    possible_actions.append((i, j))
        
        return possible_actions

    def step(self, action):
        """Execute a player's move on the gameboard and update the game state.

        Args:
            action (tuple): A tuple (row, col) representing the position 
                            on the gameboard where the current player wishes 
                            to make their move.

        Returns:
            - The current state of the gameboard as a tuple of tuples. 
            - The reward associated with the move (float).
            - A boolean indicating if the game is over (True) or not (False).
        """        
        row, col = action
        if self.board[row, col] != 0 or self.game_over:
            return self.get_state(), -10, True
        
        self.board[row, col] = self.current_player
        reward = 0
        
        if self.check_win(self.current_player):
            self.game_over = True
            self.winner = self.current_player
            if self.current_player == 1:
                reward = 1
            else:
                reward = -2
        elif len(self.get_possible_actions()) == 0:
            return self.get_state(), 0.5, True
        else:
            self.current_player = -self.current_player
            
        return self.get_state(), reward, self.game_over

    def check_win(self, player):
        for i in range(3):
            if all(self.board[i, :] == player) or all(self.board[:, i] == player):
                return True
        if all(np.diag(self.board) == player) or all(np.diag(np.fliplr(self.board)) == player):
            return True
        return False
    
    def check_potential_win(self, player):
        # Check if player has a potential win (two in a row/column/diagonal with empty spot)
        for action in self.get_possible_actions():
            temp_board = self.board.copy()
            row, col = action
            temp_board[row, col] = player
            if self.check_win(player):
                return action
        return None
    
    def print_board(self):
        symbols = {0: '.', 1: 'X', -1: 'O'}
        for row in self.board:
            print(' '.join(symbols[val] for val in row))