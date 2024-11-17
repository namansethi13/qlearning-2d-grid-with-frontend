import numpy as np

class QLearningAgent:
    def __init__(self, discount_factor, learning_rate, grid_size, environment, start_state, goal_state):
        self.discount_factor = discount_factor
        self.learning_rate = learning_rate
        self.grid_size = grid_size
        self.environment = np.array(environment)
        self.start_state = start_state
        self.goal_state = goal_state
        print(tuple(goal_state))
        self.environment[tuple(goal_state)] = 1000  # Set high reward for the goal state
        self.q_table = np.random.rand(*grid_size, 4)  # Initialize Q-table for 4 actions: up, down, left, right

    def get_q_value(self, state, action):
        action_index = {'up': 0, 'down': 1, 'left': 2, 'right': 3}[action]
        return self.q_table[state[0]][state[1]][action_index]

    def set_q_value(self, state, action, value):
        action_index = {'up': 0, 'down': 1, 'left': 2, 'right': 3}[action]
        self.q_table[state[0]][state[1]][action_index] = value

    def max_q_value(self, state):
        actions = self.get_action_list(state)
        return max(self.get_q_value(state, action) for action in actions)

    def move_agent(self, state, action):
        new_state = state[:]
        if action == 'up' and state[0] > 0:
            new_state[0] -= 1
        elif action == 'down' and state[0] < self.grid_size[0] - 1:
            new_state[0] += 1
        elif action == 'left' and state[1] > 0:
            new_state[1] -= 1
        elif action == 'right' and state[1] < self.grid_size[1] - 1:
            new_state[1] += 1
        return new_state

    def get_reward(self, state):
        return self.environment[state[0]][state[1]]

    def get_action_list(self, state):
        actions = []
        if state[0] > 0:
            actions.append('up')
        if state[0] < self.grid_size[0] - 1:
            actions.append('down')
        if state[1] > 0:
            actions.append('left')
        if state[1] < self.grid_size[1] - 1:
            actions.append('right')
        return actions

    def create_behavior_policy(self, agent_location):
        old_state = agent_location[:]
        actions = self.get_action_list(old_state)
        chosen_action = np.random.choice(actions)
        new_state = self.move_agent(old_state, chosen_action)
        reward = self.get_reward(new_state)
        max_q = self.max_q_value(new_state)
        observed_q = reward + self.discount_factor * max_q
        td = observed_q - self.get_q_value(old_state, chosen_action)
        new_q = self.get_q_value(old_state, chosen_action) + self.learning_rate * td
        self.set_q_value(old_state, chosen_action, new_q)
        return new_state

    def get_optimal_policy(self):
        optimal_policy = []
        visited_states = set()
        current_location = self.start_state[:]
        
        while current_location != self.goal_state:
            if tuple(current_location) in visited_states:
                print("Loop detected in optimal policy!")
                break
            visited_states.add(tuple(current_location))

            actions = self.get_action_list(current_location)
            max_value = -float('inf')
            optimal_action = None

            for action in actions:
                value = self.get_q_value(current_location, action)
                if value > max_value:
                    max_value = value
                    optimal_action = action

            if optimal_action is None:
                print("No valid action found!")
                break

            optimal_policy.append(optimal_action)
            current_location = self.move_agent(current_location, optimal_action)

        return optimal_policy



    def train(self, episodes):
        for episode in range(episodes):
            agent_location = self.start_state[:]
            while agent_location != self.goal_state:
                agent_location = self.create_behavior_policy(agent_location)
            print(f"Episode {episode + 1} complete.")
        print("Training complete.")
        return self.q_table



if __name__ == "__main__":
    environment = [[-1, -1, -100, -100],
                   [-100, -1, -1, -1],
                   [-1, -100, -100, -1],
                   [-1, -1, -100, -1]]
    agent = QLearningAgent(discount_factor=0.9, learning_rate=0.1, grid_size=(4, 4), environment=environment, start_state=[0, 0], goal_state=[3, 3])
    q_table = agent.train(episodes=50)
    optimal_policy = agent.get_optimal_policy()
    print("Optimal policy:", optimal_policy)