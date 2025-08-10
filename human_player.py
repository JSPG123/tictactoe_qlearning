class HumanPlayer:
    def choose_action(self, env):
        while True:
            try:
                row = int(input("Enter row (0-2): "))
                col = int(input("Enter col (0-2): "))
                action = (row, col)
                if action in env.get_possible_actions():
                    return action
                else:
                    print("Invalid move! Position is already taken or out of bounds. Try again.")
            except ValueError:
                print("Invalid input! Please enter numbers between 0 and 2.")