import os
import time

# Define the maze
maze = [
    "█████████",
    "█S      █",
    "█ ███ █ █",
    "█   █ █ █",
    "███ █ ███",
    "█       █",
    "███ ███ █",
    "█     E █",
    "█████████"
]

# Convert maze into a 2D list for easier manipulation
maze = [list(row) for row in maze]

# Player's start and end positions
start = (1, 1)  # 'S'
end = (7, 7)  # 'E'

# Display the maze
def display_maze(maze):
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal
    for row in maze:
        print(''.join(row))

# Depth-First Search (DFS) algorithm for solving the maze
def solve_maze(maze, pos, visited):
    # Check if we have reached the end
    if pos == end:
        return True

    # Mark the current position as visited
    x, y = pos
    visited.add(pos)

    # Possible directions to move: Up, Down, Left, Right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Try all four directions
    for direction in directions:
        new_x, new_y = x + direction[0], y + direction[1]

        # Check if the new position is valid and not visited
        if (0 <= new_x < len(maze)) and (0 <= new_y < len(maze[0])) and maze[new_x][new_y] in (' ', 'E') and (new_x, new_y) not in visited:
            # Mark the current path with a dot (.)
            maze[new_x][new_y] = '.'

            # Display the maze with the current move
            display_maze(maze)
            time.sleep(0.2)  # Slow down for better visualization

            # Recursively solve from the new position
            if solve_maze(maze, (new_x, new_y), visited):
                return True

            # If not a valid path, backtrack (remove the dot)
            if maze[new_x][new_y] != 'E':
                maze[new_x][new_y] = ' '

    return False

# Start the maze solver game
def play_maze_solver_game():
    print("Starting Maze Solver...")
    display_maze(maze)

    # Solve the maze using DFS
    if solve_maze(maze, start, set()):
        print("Maze solved!")
    else:
        print("No solution found!")

# Start the game
play_maze_solver_game()
