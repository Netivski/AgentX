'''
BF-Search alhorithm implementation suggested by ChatGPT
'''

from collections import deque
from main import *

# Directions for moving in the grid: [left, right, up, down]
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def is_valid_move(matrix, x, y, visited):
    """Checks if a cell can be visited (within bounds and not an obstacle)."""
    rows, cols = len(matrix), len(matrix[0])
    return 0 <= x < rows and 0 <= y < cols and matrix[x][y] == 0 and not visited[x][y]


def bfs_shortest_path(matrix, start, end):
    """Finds the shortest path from start to end using BFS."""
    rows, cols = len(matrix), len(matrix[0])
    
    # Create a queue for BFS and a visited array
    queue = deque([(start[0], start[1], 0)])  # (x, y, distance)
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    visited[start[0]][start[1]] = True  # Mark the start as visited
    
    # Perform BFS
    while queue:
        x, y, distance = queue.popleft()
        
        # If we reached the destination, return the distance
        if (x, y) == end:
            return distance
        
        # Explore all 4 possible directions (up, down, left, right)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if is_valid_move(matrix, nx, ny, visited):
                visited[nx][ny] = True  # Mark the neighbor as visited
                queue.append((nx, ny, distance + 1))  # Enqueue the neighbor with updated distance
    
    # If no path is found, return -1
    return -1

# Example Usage
if __name__ == "__main__":
    # Example matrix: 0 represents free space, 1 represents an obstacle
    matrix = [
        [0, 0, 0, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0],
        [1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0]
    ]
    
    start = (0, 0)  # Starting position (row 0, column 0)
    end = (4, 4)    # End position (row 4, column 4)
    
    # Find the shortest path using BFS
    result = bfs_shortest_path(matrix, start, end)
    
    if result != -1:
        print(f"The shortest path length from {start} to {end} is: {result}")
    else:
        print(f"There is no path from {start} to {end}.")
