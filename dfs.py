
#region ################ Depth-First Search Algorithm ################

def is_valid_move(matrix, x, y, visited):
    """Checks if a cell can be visited."""
    rows, cols = len(matrix), len(matrix[0])
    # Check if the move is within bounds, not an obstacle, and not visited
    #return 0 <= x < rows and 0 <= y < cols and matrix[x][y] == 0 and not visited[x][y]
    if (0 <= x < rows and 0 <= y < cols):
        if not visited[x][y]:
            if matrix[x][y] == 0:
                return True
    return False


def isValidMove(w:World, x, y, initialAlt, visited):
    """Checks if a cell can be visited."""
    rows, cols = w.ground.height, w.ground.width
    if (0 <= x < rows and 0 <= y < cols):
        if not visited[x][y]:
            if (checkAltDiff(w, Location(x, y), initialAlt) > (len(ag.objects))):
                return True
    return False


def dfs(w:World, x, y, visited, path):
    """Performs DFS to visit valid cells starting from (x, y)."""
    # Mark the current cell as visited
    visited[x][y] = True
    path.append((x, y))  # Add current position to the path
    
    # Directions for moving in the grid: [up, down, left, right]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Explore all 4 possible directions
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if isValidMove(w, nx, ny, visited):
            dfs(w, nx, ny, visited, path)  # Recursively visit the neighboring cell

def navigate_grid(w:World, ag:Agent):
    """Navigates the grid starting from where the Agent is"""
    rows, cols = w.ground.height, w.ground.width
    
    # Initialize visited matrix to track visited cells
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    
    # Path to store the order of visited cells
    path = []
    
    # Perform DFS from the starting position
    if w.ground.space[ag.where.xpos][ag.where.ypos] == 0:  # Ensure the starting cell is passable
        dfs(w, ag.where.xpos, ag.where.ypos, visited, path)
    
    return path
#endregion

