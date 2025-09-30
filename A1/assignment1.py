# Name this file to assignment1.py when you submit
from time import sleep
import pandas as pd
import heapq

from pandas.core.ops import invalid

# printing frontier step by step
VERBOSE = False
# cool visualization
VISUAL = True

# cost of moving from one node to the other
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
      # add cells to graph, will be useful to check neighbours
      graph[x][y] = str(graph[x][y])
      
      cell_value = graph[x][y] 

      if cell_value == "S": # start
        start = Node((x, y), type="S")
      elif cell_value == "G": # goals
        goals.append(Node((x, y), type="G"))
      elif cell_value == "X": # walls
        walls.append(Node((x, y), type="X"))
      elif str(cell_value).isdigit() and cell_value != "0": # treasures (handled further inside node class)
        treasures.append(Node((x, y), type=cell_value))

  # define subset of treasures that will be attempted to grab first
  focus_treasures = get_closest_treasures_num(treasures, start.position)


  # if there is no start or no goals path cannot be found
  if (start == None or len(goals) <= 0):
    return False
  
  optimal_path = []
  optimal_path_cost = float('inf')
  num_states_explored = 0
  picked_up_treasures = set()

  # considers multiple different branches by selecting which treasure to go to first
  for focus_treasure in focus_treasures:

    while True:
      if VERBOSE:
        print("focused treasure:", focus_treasure.position)

      # copy treasures array because gets removed during search
      current_treasures = treasures.copy()

      # determine which treasures will be ignored
      # treasures are ignored if they are not needed to reach 5 points
      breaking = False
      for t in picked_up_treasures:
        if t.ignoring:
          # the focused treasure is being ignored
          if focus_treasure == t:
            breaking = True
            break
          # do not consider this treasure
          current_treasures.remove(t)
          
          if VERBOSE:
            print("Removing:", t.position, t.value)

      # do not continue: focus_treasure == t
      if breaking:
        break

      focus_treasure.focused = True
      start.heuristic = heuristic(start.position, goals, current_treasures, 0)
      leaf = start
      goals_reached = False
      frontier = [leaf]
      treasure_points = 0
      invalid_path = False
      # Continue until all goals reached or treasure limit hit
      while not goals_reached or treasure_points < 5:
        # reset explored nodes after a goal or treasure is reached
        explored = []

        # do not continue
        if len(frontier) == 0:
          invalid_path = True
          break

        # A* search for next goal or treasure
        while True:
          # do not continue
          if len(frontier) == 0:
            break

          if VERBOSE:
            print("treasure points: ", treasure_points)
            for f in frontier:
              print(f.heuristic,"+",f.path_cost, f.position, f.type, f.value)
          
          # Get node with lowest f-cost
          leaf = heapq.heappop(frontier)  
          
          if VISUAL:
            print_map(0.1, graph, leaf, frontier, explored, walls, current_treasures, start, goals)


            if VERBOSE:
              for t in current_treasures:
                print (t.value, t.position)

          if VERBOSE:
            print("popped: ", leaf.position)
            print("--------------------------------")
            input()

          breaking = False

          # add to explored list
          explored.append(leaf)
          num_states_explored += 1

          # Goal reached, we can end this itteration
          if leaf in goals and treasure_points >= 5:  
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
            if treasure_points < 5:
              explored = []
              frontier = []
              breaking = True
              focus_treasure.focused = False

            treasure_points += leaf.value

          # check all valid neighbors
          for node in neighbourhood(graph, explored, leaf):
            curr_path_cost = leaf.path_cost + MOVING_COST
            node.heuristic = heuristic(node.position, goals, current_treasures, treasure_points)

            leaf_fcost = curr_path_cost + leaf.heuristic
            node_fcost = node.path_cost + node.heuristic
            
            # Add to frontier if its a new node or better a path was found
            if (not node in frontier and not node in explored) or (node in frontier and leaf_fcost < node_fcost):
              node.parent = leaf
              node.path_cost = curr_path_cost 

              # if the node is already in the frontier remove and add it again
              if node in frontier:
                frontier.remove(node)

              # add to frontier
              heapq.heappush(frontier, node)

          if breaking:
            break

      if invalid_path:
        break

      # last node path cost is always the total path cost
      total_path_cost = leaf.path_cost
      if VERBOSE or VISUAL:
        path = get_path(leaf)
        print(path)
        if VISUAL:
          print_map(3, graph, leaf, frontier, explored, walls, current_treasures, start, goals, path)

      # if the path cost == the distance from the closest goal to the start, you have found the fastest possible route
      if leaf.path_cost == get_closest_goal(start.position, goals):
        return get_path(leaf), total_path_cost, num_states_explored

      retrying =  False

      # Sort picked_up_treasures from high to low value
      sorted_treasures = sorted(picked_up_treasures, key=lambda x: x.value, reverse=True)

      # if we have treasures that were picked up but are not necessary to achieve 5 treasure points, 
      # we should try again with the same original path but without considering the extra treasures
      for t in sorted_treasures:        
        if treasure_points - t.value >= 5 and not t.ignoring:
          treasure_points -= t.value
          t.ignoring = True
          retrying = True
          if VERBOSE:
            print(t.value, t.position, "is extra")
      
      if retrying:
        continue
      
      
      # get best path of the different attempts
      if total_path_cost < optimal_path_cost:
        optimal_path_cost = total_path_cost
        optimal_path = get_path(leaf)
      
      focus_treasure.focused = False
      
      break


  # optimal_path is a list of coordinate of squares visited (in order)
  # optimal_path_cost is the cost of the optimal path
  # num_states_explored is the number of states explored during A* search
  return optimal_path, optimal_path_cost, num_states_explored

# Build optimal path from leaf to start
def get_path(leaf):
  path = []
  while True:
    path.insert(0, leaf.position)
    if (leaf.parent == None):
      break
    leaf = leaf.parent

  return path


# Get valid adjacent cells (up, down, left, right) that aren't walls or explored
def neighbourhood(graph, explored, leaf):
  x = leaf.position[0]
  y = leaf.position[1]
  neighbours = []
  
  # Check all 4 directions
  # if node is not a wall and it is not explored append it to neighbourhood
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

# get the closest goal from a given position
def get_closest_goal(position, goals):
  min_distance = float('inf')
  
  for goal in goals:
    goal_distance = abs(position[0] - goal.position[0]) + abs(position[1] - goal.position[1])
    
    if goal_distance < min_distance:
      min_distance = goal_distance
  
  return min_distance


# determine heuristic of a given position
def heuristic(position, goals, treasures, points):
  # if grabbed all treasure points, 
  # heuristic = distance from closest goal
  if points >= 5:
    return get_closest_goal(position, goals)

  # if still looking for treasures ignore, 
  # heuristic = (distance from closest treasure) / (value of closest treasure)
  else:
    min_heuristic = float('inf')
    for treasure in treasures:
      distance = abs(position[0] - treasure.position[0]) + abs(position[1] - treasure.position[1])
      treasure_heuristic = distance/treasure.value
     
      # if there exist a treasure which is our focus, 
      # let the heuristic depend on this treasure
      if treasure.focused:
        return treasure_heuristic

      if treasure_heuristic < min_heuristic:
        min_heuristic = treasure_heuristic

    return min_heuristic


# get set of closest treasures to focus on in start state
def get_closest_treasures_num(treasures, position):
  treasures_pq = []
  # get the treasures distances from a given positions
  for treasure in treasures:
    distance = abs(position[0] - treasure.position[0]) + abs(position[1] - treasure.position[1])
    treasure.path_cost = distance
    heapq.heappush(treasures_pq, treasure)

  # return a subset of all treasures determined by the lowest f costs
  result=[]
  for _ in range(len(treasures)): 
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

    # Handle treasure cells
    if (self.type.isdigit() and self.type != "0"):
      self.value = int(self.type)
      self.type = "T"
    else:
      self.type = type
      self.value = value

  # determine equality using position
  def __eq__(self, other):
    if (other == None):
      return False
    return self.position == other.position
    
  # Make Node hashable so it can be used in sets
  def __hash__(self):
    return hash(self.position)
  
  # Define less-than for priority queue sorting by f-cost (g + h)
  def __lt__(self, other):
    return self.heuristic + self.path_cost < other.heuristic + other.path_cost




def print_map(time, graph, leaf, frontier, explored, walls, current_treasures, start, goals, path=[]):
  # Clear screen and move cursor to top-left
  print("\033[2J\033[H", end="", flush=True)
  for x in range(len(graph)):
    for y in range(len(graph[x])):
      if (x,y) in path:
        print("🟥",end="")
      
      elif Node((x,y))==leaf:
        print("* ",end="")
      elif Node((x,y)) in frontier:
        print(". ",end="")
      elif Node((x,y)) in explored:
        print("⊡ ",end="")
      elif Node((x,y)) in walls:
        print("◻️ ",end="")
      elif Node((x,y)) in current_treasures:
        for t in current_treasures:
          if t == Node((x,y)):
            print(f"{t.value} ",end="")
      elif Node((x,y)) == start:
        print("S ",end="")
      elif Node((x,y)) in goals:
        print("G ",end="")
      else:
        print("  ",end="")
    print()
  sleep(time)







# show all examples
if VERBOSE or VISUAL:
  print(pathfinding(f"./Examples/Example0/grid.txt"))
else:
  for i in range(4):
    print("Example", i,":")
    print(pathfinding(f"./Examples/Example{i}/grid.txt"))

