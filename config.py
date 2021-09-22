import numpy as np
import enum

# The world is a 2-D grid with 4x5 = 20 rooms.
GRID_WIDTH, rooms_HEIGH = 4, 5

# Instance 1: Dirty squares: (1,2), (2,4), (3,5).
# Instance 2: Dirty squares: (1,2), (2,1), (2,4), (3,3), (4,4).
DIRTY_SQUARES = {
    1: [(1, 2), (2, 4), (3, 5)],
    2: [(1, 2), (2, 1), (2, 4), (3, 3), (4, 4)]
}

# A dictionary of ation and cost.
# The key is actin. The valus is (move_in_row, move_in_column, cost)
ACTION_COST = {
  "left": (0, -1, 1), 
  'right': (0, 1, 0.9), 
  "up": (-1, 0, 0.8), 
  "down": (1, 0, 0.7), 
  "suck": (0, 0, 0.2), 
}


def init_rooms(instance_id: int) -> np.array:
  """Initializing the rooms.

  Usage: 
    init_rooms(1) for Instance 1.
    init_rooms(2) for Instance 2.

  Args:
      instance_id: int, instance ID to initialize the dirt distribution.

  Return:
      np.array: A 2D array (adjacency matrix) representing 2D 20-room 
        vacuum-cleaner world. The 2D array is consisted of elements 0 or 1 which
        representing the rooms is clean or dirty respectively. 
  """
  rooms_np = np.zeros((GRID_WIDTH, rooms_HEIGH))
  candidate_dirty_squares = DIRTY_SQUARES[instance_id]
  for i, j in candidate_dirty_squares:
    rooms_np[i - 1][j - 1] = 1
  return rooms_np


def goal_test(rooms_np: np.array) -> bool:
  """Check whether all rooms are clean.

  Args: 
      rooms_np: np.array, A 2D array representing 2D 20-room.

  Return:
      bool: `True` indicates all rooms are clean. `Flase` indicates some rooms 
        are dirty.
  """
  return np.sum(rooms_np) == 0