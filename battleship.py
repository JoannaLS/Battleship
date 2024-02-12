import random

def create_grid(ships):
    # Creates the map
    map = [['.' for _ in range(10)] for _ in range(10)]
  
    # Place ships on the map
    for ship in ships:
        x, y = ship
        map[x][y] = "X"
    
    # Prints the map without spaces
    for row in map:
        print(' '.join(row))

def display_grid(grid):
    for row in grid:
        print(' '.join(row))

def select_ship_positions(player_grid):
    # Initialize an empty list to store ship positions
    player_ship_positions = []

    # Maximum number of ships
    max_ships = 5

    # Get ship positions from the user
    for _ in range(max_ships):
        while True:
            try:
                display_grid(player_grid)  # Display the current player's board
                x = int(input("Enter x-coordinate for the ship (0-9): "))
                y = int(input("Enter y-coordinate for the ship (0-9): "))

                # Verify if the position is valid
                if 0 <= x <= 9 and 0 <= y <= 9 and (x, y) not in player_ship_positions:
                    player_ship_positions.append((x, y))
                    player_grid[y][x] = 'X'  # Mark the ship on the player's board
                    break
                else:
                    print("Invalid position. Try again.")
            except ValueError:
                print("Invalid input. Please enter integers.")

    return player_ship_positions

# Create an empty player grid
player_grid = [['.' for _ in range(10)] for _ in range(10)]

# Get and display player ship positions
user_ship_positions = select_ship_positions(player_grid)

# Print the final player's board
display_grid(player_grid)

def pc_ships_position():
    # Creates an empty list to put pc ships
    pc_ship_positions = []

    # Maximum number of pc ships
    max_pc_ships = 5

    # Randomly place pc ships on the grid
    for a in range(max_pc_ships):
        x = random.randint(0, 9)
        y = random.randint(0, 9)

        # Verify if the position is valid and not already taken
        while (x, y) in pc_ship_positions:
            x = random.randint(0, 9)
            y = random.randint(0, 9)

        pc_ship_positions.append((x, y))

    return pc_ship_positions

# Get pc ship positions
pc_ship_positions = pc_ships_position()

    


