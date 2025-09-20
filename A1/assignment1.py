# Name this file to assignment1.py when you submit
import pandas as pd

# The pathfinding function must implement A* search to find the goal state
def pathfinding(filepath):
  csv = pd.read_csv(filepath, header=None)  # header=None since there are no column headers
  graph = csv.values.tolist()  # Convert DataFrame to 2D list
  goals = []
  walls = []
  treasures = []
  start = None

  for x in range(len(graph)):
    for y in range(len(graph[x])):
      cell_value = graph[x][y] 
      if cell_value == "S": 
        start = (x, y)
      elif cell_value == "G":
        goals.append((x, y))
      elif cell_value == "X":
        walls.append((x, y))
      elif str(cell_value).isdigit() and cell_value != "0":
        treasures.append((x, y, int(cell_value)))


  # TODO: Implement A* search algorithm here
  # For now, return placeholder values
  optimal_path = []  # Will contain the path from start to goal
  optimal_path_cost = 0  # Will contain the total cost of the path
  num_states_explored = 0  # Will contain number of states explored during search

  # optimal_path is a list of coordinate of squares visited (in order)
  # optimal_path_cost is the cost of the optimal path
  # num_states_explored is the number of states explored during A* search
  return optimal_path, optimal_path_cost, num_states_explored






pathfinding("/Users/raphaelmercier/Documents/COMP 3106/COMP-3106/A1/Examples/Example0/grid.txt")


# uniform cost search pseudo
def graph_search(graph, start_states, goal_states):
  frontier = start_states
  explored = []
  while True:
    if frontier == []:
      return False

    leaf = frontier.pop()

    if leaf in goal_states:
      return path

    explored.append (leaf)
    for node in neighbourhood (graph, leaf):
      curr_path_cost = leaf.path_cost + edge_weight(leaf, node) 
      if (node not in frontier and node not in explored or node in frontier and curr_path_cost < node.path_cost):
        node.parent = leaf
        node.path_cost = curr_path_cost 
        frontier.append (node)
