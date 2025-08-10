# Tic-Tac-Toe Q-Learning
A Q-learning implementation for tic-tac-toe.

## Setup
1. Create a virtual environment:
   ```bash
   conda create -n TicTacToe python=3.8
   conda activate TicTacToe

2. Install dependencies:
   ```bash
   pip install numpy

3. Run:
   ```bash
   python3 main.py

What is Tic Tac Toe?
Tic-tac-toe is a simple two-player game, also known as Noughts and Crosses or Xs and Os. It's played on a 3x3 grid where players take turns marking spaces with their symbol (either "X" or "O"). The goal is to get three of your symbols in a row—horizontally, vertically, or diagonally—before your opponent does. If neither player achieves this and all spaces are filled, the game ends in a draw. (Definition from Grok)
https://medium.com/@ardra4/tic-tac-toe-using-q-learning-a-reinforcement-learning-approach-d606cfdd64a3


Setup for a Tic Tac Toe model training
Environment
-	3x3 grid
-	Winning condition: if three of the symbols line up in a row (horizontally, vertically, diagonally)
State
-	Board state of each grid
Action
-	Occupation of each grid
Reward
-	Win: 1
-	Lose: -1
-	Tie: 0.5
-	Invalid: -10

CRC (Class responsibility collaboration) card for objects
TicTacToe (Environment)
-	board (3x3)
-	current_player
-	game_over
-	winner
initialize: initialize the board
reset: reset the board
get_state: return the board information
get_possible_actions: return list of empty cells
get_reward: return reward value
step: update board based on action, get reward, check game status
check_win: check if symbols are connected as three in a row
check_draw: check if board is full but not in winning/losing state (can be done by get_possible_actions)

AI (Agent)
-	alpha (learning rate)
-	gamma (discount factor)
-	epsilon (epsilon-greedy policy)
-	episodes
-	Q-table
choose_action: randomly choose action
update_q_value: update Q-value based on action and state
train: train AI model over episodes number of times, performing action and updating Q table, moving to next state
save_q_table: save trained q table to file
play_game: Testing the result of the trained AI model


Feedback:
Version 1.0.0: 
From the AI training result, found bug where winning/losing on the last possible action will lead to draw
Found that AI model will not perform the "best" action, choosing action other than winning, or lead to losing
Increased train episodes from 10000 to 100000, added epsilon decay for more accurate q table values

Version 1.0.1:
AI model sometimes still not perform "best" action due to training method (opponent player will randomly choose possible action)
Added logic for a smart opponent player, will randomly pick the action to stop AI winning

Version 1.1.0:
User can play with the trained AI model by entering row and col number

Version 1.1.1:
AI will train itself if losing to user (receivng a negative reward)