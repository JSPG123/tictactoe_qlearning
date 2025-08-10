from tictactoe import TicTacToe
from ai import AI

if __name__ == "__main__":
    env = TicTacToe()
    agent = AI()
    agent.train(env)
    agent.save_q_table()
    agent.play_game(env)