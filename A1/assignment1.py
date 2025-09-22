# Name this file to assignment1.py when you submit
import pandas as pd
import heapq

MOVING_COST = 1
# The pathfinding function must implement A* search to find the goal state
def pathfinding(filepath):
  csv = pd.read_csv(filepath, header=None)  # header=None since there are no column headers
  graph = csv.values.tolist()  # Convert DataFrame to 2D list
  goals = []
  walls = []
  treasures = []
  start = None

  # get all important nodes
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

  explored = []
  # TODO: turn frontier into a priority queue
  frontier = [start]
  optimal_path = []
  optimal_path_cost = 0

  # A* implementation
  # TODO: we need to somehow consider how to gather at least 5 treasure points before finishing
  while True:
    leaf = heapq.heappop(frontier)

    if leaf in goals:
      break
    explored.append(leaf)
    for node in neighbourhood(graph, explored, leaf):
      curr_path_cost = leaf.path_cost + MOVING_COST + leaf.heuristic
      node = priority_queue_contains(frontier, node)
      frontier_contains_node = node != None
      explored_contains_node = priority_queue_contains(explored, node) != None
      
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
  x = leaf.position[0]
  y = leaf.position[1]
  neighbours = []
  if (x > 0):
    if (graph[x-1][y] != "X" and Node((x-1, y)) not in explored):
      neighbours.append(Node((x-1, y), graph[x-1][y]))
  if (y > 0):
    if (graph[x][y-1] != "X" and Node((x, y-1)) not in explored):
      neighbours.append(Node((x, y-1), graph[x][y-1]))
  if (x < len(graph)-1):
    if (graph[x+1][y] != "X" and Node((x+1, y)) not in explored):
      neighbours.append(Node((x+1, y), graph[x+1][y]))
  if (y < len(graph[x])-1):
    if (graph[x][y+1] != "X" and Node((x, y+1)) not in explored):
      neighbours.append(Node((x, y+1), graph[x][y+1]))
  return neighbours


def heuristic(position, goal):
  # Manhattan distance
  return abs(position[0] - goal[0]) + abs(position[1] - goal[1])


def priority_queue_contains(frontier, node):
  for i in frontier:
    if (i.position == node.position):
      return i
  return None


class Node :
  def __init__(self, position, type="0", path_cost=0, heuristic=0 ,parent=None, value=0, explored=False) -> None:
    self.position = position
    self.path_cost = path_cost
    self.heuristic = heuristic
    self.parent = parent
    self.explored = explored

    # special case for treasures
    if (self.type.isdigit() and self.type != "0"):
      self.value = int(self.type)
      self.type = "T"
    else:
      self.type = type
      self.value = value

  def __eq__(self, other):
    return self.position == other.position
    
  def __lt__(self, other):
    # Define less-than for priority queue sorting
    return self.heuristic + self.path_cost < other.heuristic + other.path_cost










pathfinding("/Users/raphaelmercier/Documents/COMP 3106/COMP-3106/A1/Examples/Example0/grid.txt")