# Name this file to assignment1.py when you submit
from ast import mod
import pandas as pd
import heapq

MOVING_COST = 1
# The pathfinding function must implement A* search to find the goal state
def pathfinding(filepath):
  # Read csv file
  csv = pd.read_csv(filepath, header=None)  # header=None since there are no column headers
  graph = csv.values.tolist()  # Convert DataFrame to 2D list
  goals = []
  walls = []
  treasures = []
  start = None

  # Parse grid to find start, goals, walls, and treasures
  for x in range(len(graph)):
    for y in range(len(graph[x])):
      graph[x][y] = str(graph[x][y])
      cell_value = graph[x][y] 
      if cell_value == "S": 
        start = Node((x, y), type="S")
      elif cell_value == "G":
        goals.append(Node((x, y), type="G"))
      elif cell_value == "X":
        walls.append(Node((x, y), type="X"))
      elif str(cell_value).isdigit() and cell_value != "0":
        treasures.append(Node((x, y), type=cell_value))

  start.heuristic = heuristic(start.position, goals, treasures, 0)

  # if there is no start or no goals path cannot be found
  if (start == None or len(goals) <= 0):
    return False
  
  treasure_points = 0
  optimal_path = []
  optimal_path_cost = 0
  num_states_explored = 0
  leaf = start
  frontier = []
  # Continue until all goals reached or treasure limit hit
  while len(goals) > 0 or treasure_points < 5:
    if (len(frontier) > 0):
      leaf = heapq.heappop(frontier)  # Get node with lowest f-cost

    explored = []
    frontier = [leaf]  # Priority queue for A* search

    # A* search for next goal
    while True:
      for f in frontier:
        print(f.heuristic,f.path_cost, f.position, f.type, f.value, f.parent.position if f.parent else None)
      leaf = heapq.heappop(frontier)  # Get node with lowest f-cost
      print("popped: ", leaf.position)
      print("--------------------------------")
      
      if (len(goals) == 0):
        raise Exception("All goals reached but treasure points < 5")

      explored.append(leaf)
      num_states_explored += 1
      # Expand current node - check all valid neighbors
      for node in neighbourhood(graph, explored, leaf):
        curr_path_cost = leaf.path_cost + MOVING_COST + leaf.heuristic
        node.heuristic = heuristic(node.position, goals, treasures, treasure_points)
        # Add to frontier if new node or better path found
        if (not node in frontier and not node in explored or 
        node in frontier and curr_path_cost < node.path_cost + node.heuristic):
          node.parent = leaf
          node.path_cost = leaf.path_cost + MOVING_COST 
          if (node in frontier):
            frontier.remove(node)
          heapq.heappush(frontier, node)



      if leaf in goals:  # Goal reached
        goals.remove(leaf)
        break

      if (leaf in treasures):
        treasures.remove(leaf)
        treasure_points += leaf.value
        break      
  

  # Build optimal path from leaf to start
  while True:
    optimal_path.insert(0, leaf.position)
    if (leaf.parent == None):
      break
    leaf = leaf.parent

  # optimal_path is a list of coordinate of squares visited (in order)
  # optimal_path_cost is the cost of the optimal path
  # num_states_explored is the number of states explored during A* search
  return optimal_path, len(optimal_path)*MOVING_COST-1, num_states_explored


def neighbourhood(graph, explored, leaf):
  """Get valid adjacent cells (up, down, left, right) that aren't walls or explored"""
  x = leaf.position[0]
  y = leaf.position[1]
  neighbours = []
  
  # Check all 4 directions
  if (x > 0):  # Up
    if (graph[x-1][y] != "X" and Node((x-1, y)) not in explored):
      neighbours.append(Node((x-1, y), graph[x-1][y]))
  if (y > 0):  # Left
    if (graph[x][y-1] != "X" and Node((x, y-1)) not in explored):
      neighbours.append(Node((x, y-1), graph[x][y-1]))
  if (x < len(graph)-1):  # Down
    if (graph[x+1][y] != "X" and Node((x+1, y)) not in explored):
      neighbours.append(Node((x+1, y), graph[x+1][y]))
  if (y < len(graph[x])-1):  # Right
    if (graph[x][y+1] != "X" and Node((x, y+1)) not in explored):
      neighbours.append(Node((x, y+1), graph[x][y+1]))
  return neighbours


def heuristic(position, goals, treasures, points):
  # Manhattan distance
  # TODO: we can use the value of the treasure to calculate the heuristic somehow....

  min_distance = float('inf')
  for goal in goals:
    base_distance = abs(position[0] - goal.position[0]) + abs(position[1] - goal.position[1])
    if base_distance < min_distance:
      min_distance = base_distance

  if treasures is None or len(treasures) == 0 or points >= 5:
    return min_distance

  # Find nearest treasure
  nearest_value = 0
  for treasure in treasures:
    distance = abs(position[0] - treasure.position[0]) + abs(position[1] - treasure.position[1])
    # Closer treasures have more influence
    nearest_value = max(nearest_value, treasure.value/ (distance + 1))
  print(base_distance, nearest_value)
  
  if base_distance - nearest_value < 0:
    return base_distance
  return base_distance - nearest_value


class Node:
  """Node class for A* search with position, costs, and parent tracking"""
  def __init__(self, position, type="0", path_cost=0, heuristic=0, parent=None, value=0) -> None:
    self.position = position
    self.path_cost = path_cost
    self.heuristic = heuristic
    self.parent = parent
    self.type = type

    # Handle treasure cells (numeric values > 0)
    if (self.type.isdigit() and self.type != "0"):
      self.value = int(self.type)
      self.type = "T"
    else:
      self.type = type
      self.value = value

  def __eq__(self, other):
    if (other == None):
      return False
    return self.position == other.position
    
  def __lt__(self, other):
    """Define less-than for priority queue sorting by f-cost (g + h)"""
    return self.heuristic + self.path_cost < other.heuristic + other.path_cost










print(pathfinding("./Examples/Example0/grid.txt"))