import decimal
import config, time
from pqdict import pqdict
from decimal import Decimal

# 3600 seconds
TIME_LIMIT = 60*60

class Node:

  def __init__(self, agent_location, dirty_squares, parent, action):
    state = dirty_squares.copy()
    state.insert(0, agent_location)
    self.state = tuple(
        state)  # A tuple, ( agent_location, dirty square, dirty_square, ... )
    self.parent = parent  # A Node, can be None if it is root
    self.action = action  # A string (left, right, up, down, suck), can be None if it is root
    self.path_cost = 0  # int
    if parent:
      self.path_cost = parent.path_cost + config.ACTION_COST[action][2]

  def __get_agent_location(self):
    return self.state[0]

  def __get_dirty_squares(self):
    return list(self.state[1:])

  def generate_solution(self):
    node = self
    solution = []  # [ str ] array of actions
    while node.parent is not None:
      # print(f'path cost: {node.path_cost}, parent cost: {node.parent.path_cost}, config: {config.ACTION_COST[node.action][2]}')
      solution.insert(0, node.action)
      node = node.parent
    return solution

  agent_location = property(__get_agent_location)
  dirty_squares = property(__get_dirty_squares)


def goal_check(node):
  return len(node.dirty_squares) == 0


def depth_limited_search(start_node, limit, result_record):
  """[summary]

    Args:
        start_node: Node.
        limit: int, limit of depth.
        result_record: Dict, dictionary of execution results.
    
    Returns:
        result_record: Dict, updated dictionary of execution results.
    """
  def recursive_dls(node, limit, result_record):

    # Stop the searching since it is time out (1 hrs).  
    if time.time() - result_record["execution_time"] > TIME_LIMIT:
      result_record["solution"] = None
      result_record["total_cost"] = None
      result_record["execution_time"] = time.time(
      ) - result_record["execution_time"]
      return result_record

    if goal_check(node):
      result_record["solution"] = node.generate_solution()
      result_record["total_cost"] = node.path_cost
      result_record["execution_time"] = time.time(
      ) - result_record["execution_time"]
      return result_record
    elif limit == 0:
      return 'NotFound'
    else:

      result_record["nodes_expanded"] += 1
      if result_record["nodes_expanded"] <= 5:
        result_record["first_five_nodes"].append({
            "agent_location": node.agent_location,
            "dirty_squares": node.dirty_squares
        })

      cutoff_occurred = False

      # exppand the ndoe.
      for (action, cost) in config.ACTION_COST.items():
        child_location = (node.agent_location[0] + cost[0],
                          node.agent_location[1] + cost[1])
        child_dirty_squares = node.dirty_squares
        if (child_location[0] > 0 and child_location[0] <= config.GRID_WIDTH and
            child_location[1] > 0 and child_location[1] <= config.GRID_HEIGH):
          # Generate the child if child is not out of the grid.
          if action == "suck" and child_location in child_dirty_squares:
            child_dirty_squares.remove(child_location)

          child = Node(child_location, child_dirty_squares, node, action)
          result_record["nodes_generated"] += 1
          result = recursive_dls(child, limit - 1, result_record)
          if result == 'NotFound':
            cutoff_occurred = True
          elif result is not None:
            return result
      return 'NotFound' if cutoff_occurred else None

  return recursive_dls(start_node, limit, result_record)


def iterative_deepening_tree_search(instance_id: int):
  """[summary]

    Args:
        instance_id: int, ID of instance. 

    Returns:
        Dict: dictionary of exection results.
  """
  # Solution tracking
  result_record = {
      "first_five_nodes": [],
      "nodes_expanded": 0,
      "nodes_generated": 0,
      "execution_time": time.time(),
      "solution": None,
      "total_cost": None
  }

  max_num_dept = 20
  for depth_limit in range(max_num_dept):
    dirty_squares = config.DIRTY_SQUARES[instance_id]
    start_node = Node(config.init_agent(instance_id), dirty_squares, None, None)
    result_record["nodes_generated"] += 1

    # print("[LOG] depth_limit: ", depth_limit)

    result = depth_limited_search(start_node, depth_limit, result_record)
    if result != 'NotFound':
      return result

  return 'NotFound'


def main():

  # Instance 1
  result = iterative_deepening_tree_search(1)
  if result != 'NotFound':
    print("Instance #1 results:")
    print(f'a. First 5 nodes: {result["first_five_nodes"]}')
    print(f'b. Nodes Expanded: {result["nodes_expanded"]}, Nodes Generated: {result["nodes_generated"]}, Execution Time: {result["execution_time"]}')
    print(f'c. Solution: {result["solution"]}, Number of Moves: {len(result["solution"])}, Total Cost: { Decimal(result["total_cost"])}')

  # Instance 2
  result = iterative_deepening_tree_search(2)
  if result != 'NotFound':
    print("Instance #2 results:")
    print(f'a. First 5 nodes: {result["first_five_nodes"]}')
    print(f'b. Nodes Expanded: {result["nodes_expanded"]}, Nodes Generated: {result["nodes_generated"]}, Execution Time: {result["execution_time"]}')
    print(f'c. Solution: {result["solution"]}, Number of Moves: {len(result["solution"])}, Total Cost: { Decimal(result["total_cost"])}')


if __name__ == "__main__":
  main()
