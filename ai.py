import numpy as np
import random

class AI:
    def __init__(self, alpha=0.1, gamma=0.95, epsilon=0.2, episodes=150000):
        self.q_table = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.999
        self.episodes = episodes
        
    def choose_action(self, state, possible_actions, epsilon=None):
        if epsilon is None:
            epsilon = self.epsilon
        if random.random() < self.epsilon and possible_actions:
            return random.choice(possible_actions)
        
        q_values = []
        for action in possible_actions:
            q_value = self.q_table.get((state, action), 0.0)
            q_values.append((action, q_value))
        
        return max(q_values, key=lambda x : x[1])[0] if q_values else None
        
    
    def update_q_value(self, state, action, reward, next_state, done, env):
        if (state, action) not in self.q_table:
            self.q_table[state, action] = 0.0
            
        next_max = max([self.q_table.get((next_state, a), 0.0) for a in env.get_possible_actions()], default=0) if not done else 0
        
        old_value = self.q_table[state, action]
        
        self.q_table[(state, action)] = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
        
    def _opponent_winning_move(self, env, player):
        # Check for winning move for the given player
        for action in env.get_possible_actions():
            temp_board = env.board.copy()
            row, col = action
            temp_board[row, col] = player
            for i in range(3):
                if all(temp_board[i, :] == player) or all(temp_board[:, i] == player):
                    return action
            if all(np.diag(temp_board) == player) or all(np.diag(np.fliplr(temp_board)) == player):
                return action
        return None
    
    def train(self, env):
        for _ in range(self.episodes):
            state = env.reset()
            done = False
            
            while not done:
                actions = env.get_possible_actions()
                if not actions:
                    break
                
                current_player = env.current_player
                # AI plays as player 1 (X)
                if env.current_player == 1:
                    action = self.choose_action(state, actions)
                    # Check if AI blocks opponent's win
                    block_action = env.check_potential_win(-1)
                    reward_adjust = 0.8 if block_action and action == block_action else 0
                else:
                    # Smarter opponent: 90% chance to make a winning/blocking move
                    if random.random() < 0.9:
                        # Check for winning move (player -1)
                        action = self._opponent_winning_move(env, -1)
                        if action is None:
                            # Check for blocking AI's win (player 1)
                            action = self._opponent_winning_move(env, 1)
                        if action is None:
                            action = random.choice(actions) if actions else None
                    else:
                        action = random.choice(actions) if actions else None
                    reward_adjust = 0
                if action is None:
                    break
                next_state, reward, done = env.step(action)
                if env.current_player == -1:  # Update Q-table only for AI's actions (player 1)
                    adjusted_reward = reward + reward_adjust
                    self.update_q_value(state, action, adjusted_reward, next_state, done, env)
                    
                state = next_state
            # Decay epsilon
            self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
    
    def save_q_table(self, filename='q_table_tictactoe.npy'):
        np.save(filename, self.q_table)
        
    def load_q_table(self, filename='q_table_tictactoe.npy'):
        self.q_table = np.load(filename, allow_pickle=True).item()
    
    def play_game(self, env):
        state = env.reset()
        done = False
        print("Initial board:")
        env.print_board()
        while not done:
            actions = env.get_possible_actions()
            if not actions:
                break
            # Store current player before step
            current_player = env.current_player
            if current_player == 1:
                action = self.choose_action(state, actions, epsilon=0.0)  # AI plays as player 1
            else:
                action = random.choice(actions) if actions else None  # Random opponent as player -1
            if action is None:
                break
            state, reward, done = env.step(action)
            print(f"Player {current_player} moves to {action}:")
            env.print_board()
        print(f"Game over. Winner: {env.winner}, Reward: {reward}")