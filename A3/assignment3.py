import os
import random


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

      # Store all trial data
      with open(os.path.join(directory, trial), 'r') as file:
        for line in file:
          state, action = line.split(",")
          if action == "-\n":
            action = None
          else:
            action = int(action)

          state_action_pairs.append((state, action))

          # Initializes a nested dictionary with format (state, (action, q-value))
          if action is not None:
            # Initialize inner nested dictionary if key for current state does not exist
            if state not in self.qfunction:
              self.qfunction[state] = {}

            self.qfunction[state][action] = reward(state)

      # Add list of state-action pairs for a trial as a new element in the trials list, representing a single trial
      self.trials.append(state_action_pairs)

    # Train the Q-function use reward function
    for _ in range(500):
      for trial in self.trials:

        # Iterate through all state action pairs within a trial
        for i in range(len(trial) - 1):

          # Get state action values for the current "timestep" in a trial
          state, action = trial[i]
          current_reward_value = reward(state)

          # Terminal state reached, exit loop
          if action is None:
            continue
          
          # Get data for the next state
          next_state, next_action = trial[i+1]

          # If the next state is terminal, set q value to 0, else find max q value for an action associated with the next state
          if next_action is None:
            max_next_q = self.qvalue(next_state, None)
          else:
            max_next_q = max(self.qvalue(next_state, a) for a in self.qfunction[next_state])

          # Apply update equation for tmeporal difference Q - learning
          new_q = self.qvalue(state, action) + self.alpha * (current_reward_value + self.gamma * max_next_q - self.qvalue(state, action))

          # Store updated q value
          self.qfunction[state][action] = new_q


    # Return nothing

  def qvalue(self, state, action):
    # state is a string representation of a state
    # action is an integer representation of an action

    # Return the q-value for the state-action pair
    if state not in self.qfunction or action not in self.qfunction[state]:
      return reward(state)

    return self.qfunction[state][action]



  def policy(self, state):
    # state is a string representation of a state

    max_qvalue = float('-inf')
    best_action = None
    cbag, _, _, _ = interpret_state(state)
    if cbag == 0:
      return 0
    if state not in self.qfunction:
      # can pick any action
      max_action = min(3, cbag)
      
      return random.randint(1, max_action)

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
  






# test_td_learning() is used to test the td_qlearning class
def test_td_learning():
  example = 1
  td_learning = td_qlearning(f"Examples/Example{example}/Trials/")

  print("policy tests:")
  with open(os.path.join(f"Examples/Example{example}/policy_tests.csv"), 'r') as file:
    for line in file:
      state, expected = line.split(",")
      if td_learning.policy(state) == int(expected):
        print("PASS: {} == {}".format(td_learning.policy(state), int(expected)))
      else:
        print("FAIL: {} != {}".format(td_learning.policy(state), int(expected)))
  
  print("\nqvalue tests:")
  with open(os.path.join(f"Examples/Example{example}/qvalue_tests.csv"), 'r') as file:
    for line in file:
      state, action, expected = line.split(",")
      if abs(td_learning.qvalue(state, int(action)) - float(expected)) < 0.000001:
        print("PASS: {} == {}".format(td_learning.qvalue(state, int(action)), float(expected)))
      else:
        print("FAIL: {} != {}".format(td_learning.qvalue(state, int(action)), float(expected)))


# test_td_learning()