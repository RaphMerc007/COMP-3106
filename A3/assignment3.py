import os


class td_qlearning:

  WINNER = 'A'
  LOSER = 'O'
  alpha = 0.10
  gamma = 0.90
  qfunction = {}
  state_action_pairs = []

  def __init__(self, directory):
    # directory is the path to a directory containing trials through state space
    trials = os.listdir(directory)
    for trial in trials:
      with open(os.path.join(directory, trial), 'r') as file:
        for line in file:
          state, action = line.split(",")
          if action == "-\n":
            action = None
          else:
            action = int(action)

          self.state_action_pairs.append((state, action))



    # TODO: Train the Q-function use reward function



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



  def reward(self, state):
    cbag, cagent, copponent, winner = self.interpret_state(state)

    if winner == self.WINNER:
      return cagent
    elif winner == self.LOSER:
      return -cagent
    else:
      return 0


  # returns cbag, cagent, copponent, winner
  def interpret_state(self, state):
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