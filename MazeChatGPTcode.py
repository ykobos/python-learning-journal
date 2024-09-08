# implement a recursive algorithm to solve a maze. The maze is represented as a 2D array where 1 represents walls and 0 represents valid paths. 
# The goal is to find a path from the starting point to the exit, if one exists, using recursion
# above prompt was used in ChatGPT, it is the lab's instructions, and this is the generated code:

def solve_maze(maze, start_x, start_y, exit_x, exit_y, path=[]):
    # Base case: if the current position is the exit, return the path
    if (start_x, start_y) == (exit_x, exit_y):
        path.append((start_x, start_y))
        return True
    
    # Check if the current position is out of bounds or is a wall
    if start_x < 0 or start_x >= len(maze) or start_y < 0 or start_y >= len(maze[0]) or maze[start_x][start_y] == 1:
        return False
    
    # If the position is already visited, return False
    if (start_x, start_y) in path:
        return False
    
    # Add the current position to the path
    path.append((start_x, start_y))
    
    # Explore the neighbors: up, down, left, right
    if (solve_maze(maze, start_x + 1, start_y, exit_x, exit_y, path) or  # Move down
        solve_maze(maze, start_x - 1, start_y, exit_x, exit_y, path) or  # Move up
        solve_maze(maze, start_x, start_y + 1, exit_x, exit_y, path) or  # Move right
        solve_maze(maze, start_x, start_y - 1, exit_x, exit_y, path)):   # Move left
        return True
    
    # If none of the moves work, backtrack (remove the current position from the path)
    path.pop()
    return False

# Function to print the solution path
def print_solution(path):
    if path:
        print("Path to exit:", path)
    else:
        print("No path found.")

# Example usage:
maze = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0]
]

start_x, start_y = 0, 0  # Starting point
exit_x, exit_y = 4, 4    # Exit point
path = []

if solve_maze(maze, start_x, start_y, exit_x, exit_y, path):
    print_solution(path)
else:
    print("No solution exists.")
