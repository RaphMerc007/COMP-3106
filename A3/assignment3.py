import os


class td_qlearning:

  WINNER = 'A'
  LOSER = 'O'
  alpha = 0.10
  gamma = 0.90
  trials = []
  qfunction = {}

  def __init__(self, directory):
    # directory is the path to a directory containing trials through state space
    trials = os.listdir(directory)
    for trial in trials:

      # Store all state-action pairs for a single trial in a list
      state_action_pairs = []

      with open(os.path.join(directory, trial), 'r') as file:
        for line in file:
          state, action = line.split(",")
          if action == "-\n":
            action = None
          else:
            action = int(action)

          state_action_pairs.append((state, action))

          
          if action is not None:
            if state not in self.qfunction:
              self.qfunction[state] = {}

            self.qfunction[state][action] = reward(state)

    

      # Add list of state-action pairs for a trial as a new element in the trials list, representing a single trial
      self.trials.append(state_action_pairs)

    # Train the Q-function use reward function
    for _ in range(50):
      for trial in self.trials:

        # Iterate through all state action pairs within a trial
        for i in range(len(trial) - 1):

          # Get state action values for the "timestep" in a trial
          state, action = trial[i]

          if action is None:
            continue
          
          next_state, next_action = trial[i+1]
          next_reward_value = reward(next_state)

          if next_action is None:
            max_next_q = reward(next_state)
          else:
            max_next_q = max(self.qvalue(next_state, a) for a in self.qfunction[next_state])

          # Apply update equation for tmeporal difference Q - learning
          new_q = self.qvalue(state, action) + self.alpha * (next_reward_value + self.gamma * max_next_q - self.qvalue(state, action))

          # Store updated q value
          self.qfunction[state][action] = new_q

    # Return nothing

  def qvalue(self, state, action):
    # state is a string representation of a state
    # action is an integer representation of an action

    # Return the q-value for the state-action pair
    return self.qfunction[state][action]



  def policy(self, state):
    # state is a string representation of a state

    max_qvalue = float('-inf')
    best_action = None

    for action in self.qfunction[state]:
      qvalue = self.qvalue(state, action)
      if qvalue > max_qvalue:
        max_qvalue = qvalue
        best_action = action

    # Return the optimal action (as an integer) under the learned policy
    return best_action




def reward(state):
  cbag, cagent, copponent, winner = interpret_state(state)

  # Currently hard coded winner or loser
  if winner == 'A':
    return cagent
  elif winner == 'O':
    return -cagent
  else:
    return 0

# returns cbag, cagent, copponent, winner
def interpret_state(state):
  cbag, cagent, copponent, winner = state.split("/")
  return int(cbag), int(cagent), int(copponent), winner
  






def test_td_learning():
  td_learning = td_qlearning("Examples/Example0/Trials/")

  with open(os.path.join("Examples/Example0/policy_tests.csv"), 'r') as file:
    for line in file:
      state, expected = line.split(",")
      if td_learning.policy(state) == int(expected):
        print("PASS: {} == {}".format(td_learning.policy(state), int(expected)))
      else:
        print("FAIL: {} != {}".format(td_learning.policy(state), int(expected)))
  
  with open(os.path.join("Examples/Example0/qvalue_tests.csv"), 'r') as file:
    for line in file:
      state, action, expected = line.split(",")
      if td_learning.qvalue(state, int(action)) == float(expected):
        print("PASS: {} == {}".format(td_learning.qvalue(state, int(action)), float(expected)))
      else:
        print("FAIL: {} != {}".format(td_learning.qvalue(state, int(action)), float(expected)))
        print(td_learning.qvalue(state, int(action))/2)


test_td_learning()