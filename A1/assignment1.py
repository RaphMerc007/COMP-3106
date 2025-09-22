# Name this file to assignment1.py when you submit
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
      cell_value = graph[x][y] 
      if cell_value == "S": 
        start = Node((x, y), "S", heuristic=heuristic((x, y), goals[0].position))
      elif cell_value == "G":
        goals.append(Node((x, y), "G"))
      elif cell_value == "X":
        walls.append(Node((x, y), "X"))
      elif str(cell_value).isdigit() and cell_value != "0":
        treasures.append(Node((x, y), cell_value))

  # if there is no start or no goals path cannot be found
  if (start == None or len(goals) <= 0):
    return False
  
  treasure_points = 0
  frontier = [start]  # Priority queue for A* search
  optimal_path = []
  optimal_path_cost = 0

  # Continue until all goals reached or treasure limit hit
  while len(goals) > 0 and treasure_points < 5:
    explored = []

    # A* search for next goal
    while True:
      leaf = heapq.heappop(frontier)  # Get node with lowest f-cost

      if leaf in goals:  # Goal reached
        goals.remove(leaf)
        break

      explored.append(leaf)
      optimal_path_cost += leaf.path_cost
      
      # Expand current node - check all valid neighbors
      for node in neighbourhood(graph, explored, leaf):
        curr_path_cost = leaf.path_cost + MOVING_COST + leaf.heuristic
        node = priority_queue_contains(frontier, node)
        frontier_contains_node = node != None
        explored_contains_node = priority_queue_contains(explored, node) != None
        
        # Add to frontier if new node or better path found
        if (not frontier_contains_node and not explored_contains_node or 
        frontier_contains_node and curr_path_cost < node.path_cost + node.heuristic):
          node.parent = leaf
          node.path_cost = leaf.path_cost + MOVING_COST 
          node.heuristic = heuristic(node.position, goals[0].position)
          if (frontier_contains_node):
            frontier.remove(node)
          heapq.heappush(frontier, node)


  # optimal_path is a list of coordinate of squares visited (in order)
  # optimal_path_cost is the cost of the optimal path
  # num_states_explored is the number of states explored during A* search
  return optimal_path, optimal_path_cost, len(explored)


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


def heuristic(position, goal):
  # Manhattan distance
  # TODO: we can use the value of the treasure to calculate the heuristic somehow....
  return abs(position[0] - goal[0]) + abs(position[1] - goal[1])


def priority_queue_contains(frontier, node):
  """Check if frontier already contains a node at the same position"""
  for i in frontier:
    if (i.position == node.position):
      return i
  return None


class Node:
  """Node class for A* search with position, costs, and parent tracking"""
  def __init__(self, position, type="0", path_cost=0, heuristic=0, parent=None, value=0, explored=False) -> None:
    self.position = position
    self.path_cost = path_cost
    self.heuristic = heuristic
    self.parent = parent
    self.explored = explored

    # Handle treasure cells (numeric values > 0)
    if (self.type.isdigit() and self.type != "0"):
      self.value = int(self.type)
      self.type = "T"
    else:
      self.type = type
      self.value = value

  def __eq__(self, other):
    return self.position == other.position
    
  def __lt__(self, other):
    """Define less-than for priority queue sorting by f-cost (g + h)"""
    return self.heuristic + self.path_cost < other.heuristic + other.path_cost










pathfinding("./Examples/Example0/grid.txt")