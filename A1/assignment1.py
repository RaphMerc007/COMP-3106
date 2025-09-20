# Name this file to assignment1.py when you submit
import pandas as pd
MOVING_COST = 1
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

  if (start == None or len(goals) <= 0):
    return False

  explored = []
  frontier = [start]
  optimal_path = []
  optimal_path_cost = 0

  while True:
    leaf = frontier.pop()

    if leaf in goals:
      break

    explored.append (leaf)
    for node in neighbourhood(graph, leaf):
      curr_path_cost = leaf.path_cost + MOVING_COST + leaf.heuristic
      if (node not in frontier and node not in explored or node in frontier and curr_path_cost < node.path_cost + node.heuristic):
        node.parent = leaf
        node.path_cost = leaf.path_cost + MOVING_COST 
        frontier.append(node)

  # TODO: We will probably need to have a class: node, 
  # members should be: path cost, heuristic, parent, type(start, goal, wall, treasure(should also have treasure value here))

  # optimal_path is a list of coordinate of squares visited (in order)
  # optimal_path_cost is the cost of the optimal path
  # num_states_explored is the number of states explored during A* search
  return optimal_path, optimal_path_cost, len(explored)


# TODO: implement the neighbourhood function, 
# it should determine which nodes you can travel to
def neighbourhood(graph, leaf):
  return []


pathfinding("/Users/raphaelmercier/Documents/COMP 3106/COMP-3106/A1/Examples/Example0/grid.txt")