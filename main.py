from tictactoe import TicTacToe
from ai import AI
from human_player import HumanPlayer

def play_human_vs_ai(env, agent, human_starts=False, learn=True):
    state = env.reset()
    done = False
    human = HumanPlayer()
    last_ai_state = None
    last_ai_action = None
    print("Initial board:")
    env.print_board()
    while not done:
        actions = env.get_possible_actions()
        if not actions:
            break
        current_player = env.current_player
        if current_player == -1:  # Human plays as O
            action = human.choose_action(env)
        else:  # AI plays as X
            action = agent.choose_action(state, actions, epsilon=0.1 if learn else 0.0)
            block_action = env.check_potential_win(-1)
            reward_adjust = 0.8 if block_action and action == block_action else 0
            last_ai_state = state
            last_ai_action = action
        if action is None:
            break
        next_state, reward, done = env.step(action)
        if current_player == 1 and learn:  # Update Q-table for AI's moves
            adjusted_reward = reward + reward_adjust
            agent.update_q_value(state, action, adjusted_reward, next_state, done, env)
        elif current_player == -1 and learn and last_ai_state is not None:  # Update Q-table after human's move
            agent.update_q_value(last_ai_state, last_ai_action, reward, next_state, done, env)
        state = next_state
        print(f"Player {current_player} moves to {action}:")
        env.print_board()
    print(f"Game over. Winner: {env.winner}, Reward: {reward}")
    if learn:
        agent.save_q_table()  # Save updated Q-table
        #print('Learnt')

if __name__ == "__main__":
    env = TicTacToe()
    agent = AI()
    #agent.train(env)
    #agent.save_q_table()
    #agent.play_game(env)
    agent.load_q_table()
    play_human_vs_ai(env, agent, learn=True)