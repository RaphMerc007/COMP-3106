# Name this file to assignment1.py when you submit
import pandas as pd
import heapq

VERBOSE = True
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

  focus_treasures = get_closest_treasures_num(treasures, start.position)
  # if there is no start or no goals path cannot be found
  if (start == None or len(goals) <= 0):
    return False
  
  optimal_path = []
  optimal_path_cost = float('inf')
  num_states_explored = 0
  picked_up_treasures = set()

  # get closest treasures to check path from
  for focus_treasure in focus_treasures:
    while True:
      if VERBOSE:
        print("focused treasure:", focus_treasure.position)

      # copy treasures array because gets removed during search
      current_treasures = treasures.copy()
      breaking = False
      for t in picked_up_treasures:

        if t.ignoring:
          if focus_treasure == t:
            breaking = True
            break
          current_treasures.remove(t)
          if VERBOSE:
            print("Removing:", t.position)

      if breaking:
        break
      # determine focus
      focus_treasure.focused = True
      start.heuristic = heuristic(start.position, goals, current_treasures, 0)
      leaf = start
      goals_reached = False
      frontier = [leaf]
      treasure_points = 0

      # Continue until all goals reached or treasure limit hit
      while not goals_reached or treasure_points < 5:
        explored = []
        # A* search for next goal
        while True:

          if VERBOSE:
            print("treasure points: ", treasure_points)
            for f in frontier:
              print(f.heuristic,"+",f.path_cost, f.position, f.type, f.value)

          leaf = heapq.heappop(frontier)  # Get node with lowest f-cost

          if VERBOSE:
            print("popped: ", leaf.position)
            print("--------------------------------")
            input()
          if (len(goals) == 0):
            raise Exception("All goals reached but treasure points < 5")

          breaking = False
          explored.append(leaf)
          num_states_explored += 1

          if leaf in goals and treasure_points >= 5:  # Goal reached
            goals_reached = True
            explored = []
            frontier = []
            breaking = True
          else: # goal reached but not ready to end
            goals_reached = False

          # pickup treasure only if focus is already found or it is the focus
          if leaf in current_treasures and (not focus_treasure.focused or focus_treasure == leaf):
            current_treasures.remove(leaf)
            picked_up_treasures.add(leaf)
            treasure_points += leaf.value
            explored = []
            frontier = []
            breaking = True
            focus_treasure.focused = False

          # Expand current node - check all valid neighbors
          for node in neighbourhood(graph, explored, leaf):
            curr_path_cost = leaf.path_cost + MOVING_COST + leaf.heuristic
            node.heuristic = heuristic(node.position, goals, current_treasures, treasure_points)
            # Add to frontier if new node or better path found
            if ((not node in frontier and not node in explored) or 
            (node in frontier and curr_path_cost < node.path_cost + node.heuristic)):
              node.parent = leaf
              node.path_cost = leaf.path_cost + MOVING_COST 
              if (node in frontier):
                frontier.remove(node)
              heapq.heappush(frontier, node)

          if breaking:
            break

      retrying =  False
      
      # Sort picked_up_treasures from high to low value (so we remove high-value ones first to keep low-value ones)
      sorted_treasures = sorted(picked_up_treasures, key=lambda x: x.value, reverse=True)
      for t in sorted_treasures:        
        if treasure_points - t.value >= 5:
          treasure_points -= t.value
          t.ignoring = True
          retrying = True
          if VERBOSE:
            print(t.value, "is extra")
      
      if retrying:
        continue
      
      path = []
      path_cost = 0
      # Build optimal path from leaf to start
      while True:
        path.insert(0, leaf.position)
        if (leaf.parent == None):
          break
        leaf = leaf.parent

      path_cost = len(path)*MOVING_COST-1

      # get best path of the different attempts
      if path_cost < optimal_path_cost:
        optimal_path_cost = path_cost
        optimal_path = path
      
      focus_treasure.focused = False
      
      if VERBOSE:
        print(path, path_cost)
      
      break


  # optimal_path is a list of coordinate of squares visited (in order)
  # optimal_path_cost is the cost of the optimal path
  # num_states_explored is the number of states explored during A* search
  return optimal_path, optimal_path_cost, num_states_explored


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
  if points >= 5:
    min_distance = float('inf')
    for goal in goals:
      goal_distance = abs(position[0] - goal.position[0]) + abs(position[1] - goal.position[1])
      if goal_distance < min_distance:
        min_distance = goal_distance
    return min_distance
  else:
    min_heuristic = float('inf')
    for treasure in treasures:
      distance = abs(position[0] - treasure.position[0]) + abs(position[1] - treasure.position[1])
      treasure_heuristic = distance/treasure.value
      if treasure.focused:
        return treasure_heuristic
      if treasure_heuristic < min_heuristic:
        min_heuristic = treasure_heuristic

    return min_heuristic


# get closest treasures to focus on in start state
def get_closest_treasures_num(treasures, position):
  NUMBER_OF_TREASURES_CONSIDERED = 4

  treasures_pq = []
  for treasure in treasures:
    distance = abs(position[0] - treasure.position[0]) + abs(position[1] - treasure.position[1])
    treasure.path_cost = distance
    heapq.heappush(treasures_pq, treasure)

  result=[]
  for _ in range(min(NUMBER_OF_TREASURES_CONSIDERED, len(treasures))): 
    t = heapq.heappop(treasures_pq)
    result.append(t)

  return result


class Node:
  """Node class for A* search with position, costs, and parent tracking"""
  def __init__(self, position, type="0", path_cost=0, heuristic=0, parent=None, value=0, focused=False, ignoring=False) -> None:
    self.position = position
    self.path_cost = path_cost
    self.heuristic = heuristic
    self.parent = parent
    self.type = type
    self.focused = focused
    self.ignoring = ignoring

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
    
  def __hash__(self):
    """Make Node hashable so it can be used in sets"""
    return hash(self.position)
    
  def __lt__(self, other):
    """Define less-than for priority queue sorting by f-cost (g + h)"""
    return self.heuristic + self.path_cost < other.heuristic + other.path_cost









# for i in range(4):
#   print("Example", i,":")
#   print(pathfinding(f"./Examples/Example{i}/grid.txt"))

print(pathfinding(f"./Examples/Example3/grid.txt"))
