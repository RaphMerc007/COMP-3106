import os


class td_qlearning:

  WINNER = 'A'
  LOSER = 'O'
  alpha = 0.10
  gamma = 0.90
  qfunction = {}
  trials = []

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

      # Add list of state-action pairs for a trial as a new element in the trials list, representing a single trial
      self.trials.append(state_action_pairs)


    # Initialize Q - values as rewards Q(s,a) = r(s) in the qfunction dictionary (may not need this?)
    for trial in self.trials:
      for (state, action) in trial:
        if action is not None:
          self.qfunction[(state, action)] = reward(state)

    # TODO: Train the Q-function use reward function

    # store all the different trials in a list, we need to do Q laerning for every trial in the list
    # for every tirla, we will do Q learning on each state within the list until convergence

    # Iterate through each trial, updating Q - values
    for trial in self.trials:

      # Iterate through all state action pairs within a trial
      for i in range(len(trial) - 1):

        # Get state action values for the "timestep" in a trial
        state, action = trial[i]
        next_state, _ = trial[i+1]
        reward_value = reward(next_state)

        # Get current Q value, default to reward of the state if it hasn't been initialize (it should be)
        q = self.qfunction.get((state, action), reward(state))

        # Get the max Q value for the next state over all actions


        # Apply update equation for tmeporal difference Q - learning
        new_q = q + self.alpha * (reward_value + self.gamma * max_next_q_action - q)

        # Store updated q value
        self.qfunction[(state, action)] = new_q



    # Return nothing

  def qvalue(self, state, action):
    # state is a string representation of a state
    # action is an integer representation of an action

    # Return the q-value for the state-action pair
    return self.qfunction.get((state, action), 0)



  def policy(self, state):
    # state is a string representation of a state

    max_qvalue = float('-inf')
    best_action = None

    for (s, action), qvalue in self.qfunction.items():
      if s == state:
        if qvalue > max_qvalue:
          max_qvalue = qvalue
          best_action = action
          # TODO: migh need to check if action is valid

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
        print("PASS")
      else:
        print("FAIL: {} != {}".format(td_learning.policy(state), int(expected)))
  
  with open(os.path.join("Examples/Example0/qvalue_tests.csv"), 'r') as file:
    for line in file:
      state, action, expected = line.split(",")
      if td_learning.qvalue(state, int(action)) == float(expected):
        print("PASS")
      else:
        print("FAIL: {} != {}".format(td_learning.qvalue(state, int(action)), float(expected)))


test_td_learning()