import config
from pqdict import pqdict

class Node:
  def __init__(self, agent_location, dirty_squares, parent, action):
    state = dirty_squares.copy()
    state.insert(0, agent_location)
    self.state = tuple(state)               # A tuple, ( agent_location, dirty square, dirty_square, ... )
    self.parent = parent                    # A Node, can be None if it is root
    self.action = action                    # A string (left, right, up, down, suck), can be None if it is root
    self.path_cost = 0                      # int
    if parent:
      self.path_cost = parent.path_cost + config.ACTION_COST[action][2]

  def __get_agent_location(self):
    return self.state[0]

  def __get_dirty_squares(self):
    return list(self.state[1:])

  def generate_solution(self):
    node = self
    solution = [] # [ str ] array of actions
    while node.parent is not None:
      solution.insert(0, node.action)
      node = node.parent
    return solution
  
  agent_location = property(__get_agent_location)
  dirty_squares = property(__get_dirty_squares)

def uniform_cost_graph_search(instance_id):
  """
    Return:
      Array of locations representing the squence of actions, [ str ]
        return None if no solution is found
  """
  dirty_squares = config.DIRTY_SQUARES[instance_id]
  node = Node(config.init_agent(instance_id), dirty_squares, None, None)
  frontier = pqdict({node.state: node}, key=lambda x: x.path_cost)
  explored = set()

  # Solution tracking

  while len(frontier) > 0:
    node = frontier.popitem()[1]
    if goal_check(node):
      # The solution is found
      return node.generate_solution()
    explored.add(node.state)

    for (action,cost) in config.ACTION_COST.items():
      child_location = (node.agent_location[0]+cost[0], node.agent_location[1]+cost[1])
      child_dirty_squares = node.dirty_squares
      
      if (child_location[0] > 0 and child_location[0] <= config.GRID_WIDTH 
        and child_location[1] > 0 and child_location[1] <= config.GRID_HEIGH):
        # Generate the child
        if action == "suck" and child_location in child_dirty_squares:
          child_dirty_squares.remove(child_location)
        child = Node(child_location, child_dirty_squares, node, action)

        # print(f'frontier: {list(frontier.keys())}')
        # print(f'child: {child.state}')

        if child.state not in explored and child.state not in frontier:
          frontier[child.state] = child
        elif child.state in frontier and frontier[child.state].path_cost > child.path_cost:
          frontier[child.state] = child

  return None

def goal_check(node):
  return len(node.dirty_squares) == 0

print(uniform_cost_graph_search(2))