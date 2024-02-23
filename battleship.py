import random

# Constants
grid_size = 10
ship_sizes = [5, 3, 2]
ship_quantities = [1, 2, 3]

def display_grid(grid):
    # Display the grid with letters for columns and numbers for lines
    print("\nPlayer's Grid:")
    print("  A  B  C  D  E  F  G  H  I  J")
    for i, row in enumerate(grid):
        print(f"{i} {' '.join(cell.ljust(2) for cell in row)}")

def display_empty_grid():
    # Display an empty grid with letters for columns and numbers for lines
    empty_grid = [['.' for _ in range(10)] for _ in range(10)]
    display_grid(empty_grid)

def display_moves_grid(player_moves):
    # Display the player's moves grid with letters for columns and numbers for lines
    print("\nPlayer's Moves Grid:")
    print("  A  B  C  D  E  F  G  H  I  J")
    for i, row in enumerate(player_moves):
        print(f"{i} {' '.join(cell.ljust(2) for cell in row)}")

def update_moves_grid(moves_grid, coords, result):
    # Update the moves grid with the result of the player's move
    x, y = coords
    moves_grid[x][y] = result

def player_ship_positions():
    # Starts an empty list to put player ships
    player_ships = []

    # Creates the player grid
    player_grid = [['.' for _ in range(10)] for _ in range(10)]

    # Display the empty grid
    display_empty_grid()

    # Get player ship positions
    for size, quantity in zip(ship_sizes, ship_quantities):
        for a in range(quantity):
            print(f"\nPlace a {size}-space ship:")
            placed_successfully = False

            while not placed_successfully:
                try:
                    y = input("\nEnter column for the ship starting position (A-J): ").upper()
                    x = int(input("\nEnter row for the ship starting position (0-9): "))
                    y = ord(y) - ord('A')  # Convert letter to corresponding index
                    orientation = input("\nEnter orientation (H for horizontal, V for vertical): ").upper()

                    # Verify if the ship placement is valid
                    positions = []
                    if orientation == 'H' and 0 <= x <= 9 and 0 <= y <= 9 and all(player_grid[x][y + i] == '.' for i in range(size)):
                        positions = [(x, y + i) for i in range(size)]
                    elif orientation == 'V' and 0 <= x <= 9 and 0 <= y <= 9 and all(player_grid[x + i][y] == '.' for i in range(size)):
                        positions = [(x + i, y) for i in range(size)]

                    if positions:
                        player_ships.extend(positions)
                        for x, y in positions:
                            player_grid[x][y] = 'X' + str(size)  # Mark the ship on the player's board
                        placed_successfully = True
                        display_grid(player_grid)  # Display the player's updated grid
                    else:
                        print("Invalid position or ship doesn't fit. Try again.")
                except (ValueError, IndexError):
                    print("Invalid input. Please enter valid values and try again.")

    return player_ships, player_grid

def pc_ship_positions(pc_grid):
    # Creates an empty list to put pc ships
    pc_ship_positions = []
    pc_ships = []

    # Randomly place pc ships on the grid
    for size, quantity in zip(ship_sizes, ship_quantities):
        for a in range(quantity):
            placed_successfully = False

            while not placed_successfully:
                x = random.randint(0, 9)
                y = random.randint(0, 9)
                orientation = random.choice(['H', 'V'])  # Randomly choose horizontal or vertical

                # Verify if the position is valid and not already taken
                if orientation == 'H' and x + size <= 10 and all(pc_grid[x + i][y] == '.' for i in range(size)):
                    positions = [(x + i, y) for i in range(size)]
                    pc_ship_positions.extend(positions)
                    pc_ships.append(positions)
                    for x, y in positions:
                        pc_grid[x][y] = 'X' + str(size)  # Mark the ship on the pc's board
                    placed_successfully = True
                elif orientation == 'V' and y + size <= 10 and all(pc_grid[x][y + i] == '.' for i in range(size)):
                    positions = [(x, y + i) for i in range(size)]
                    pc_ship_positions.extend(positions)
                    pc_ships.append(positions)
                    for x, y in positions:
                        pc_grid[x][y] = 'X' + str(size)  # Mark the ship on the pc's board
                    placed_successfully = True

    return pc_ship_positions, pc_grid, pc_ships

def player_attack(pc_ship_positions_list, pc_grid, moves_grid):
    eliminated_pc_ship_positions = []

    while True:
        # Player's turn
        try:
            attack_y = input("\nEnter column for the attack (A-J): ").upper()
            attack_x = int(input("\nEnter row for the attack (0-9): "))
            attack_y = ord(attack_y) - ord('A')  # Convert letter to corresponding index
            player_attack_coords = (attack_x, attack_y)

            # Validate input
            if 0 <= attack_x <= 9 and 0 <= attack_y <= 9:
                break
            else:
                print("Invalid input. Row should be between 0 and 9, and column should be between A and J. Try again.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter valid values and try again.")
    
    # Check if the attack hits a ship
    if player_attack_coords in pc_ship_positions_list:
        print("Player has hit a ship!")
        pc_ship_positions_list.remove(player_attack_coords)
        eliminated_pc_ship_positions.append(player_attack_coords)  # Mark as eliminated
        update_moves_grid(moves_grid, player_attack_coords, "H")  # Update moves grid with a hit
       
    else:
        print("Player Miss!")
        update_moves_grid(moves_grid, player_attack_coords, "M")  # Update moves grid with a miss

    return player_attack_coords, player_attack_coords in eliminated_pc_ship_positions

def pc_attack(player_ships, player_grid, pc_ship_positions_list, moves_grid, last_hit_coords=None):
    eliminated_player_ship_positions = []

    print("\nPC's Turn!\n")

    if last_hit_coords is not None:
        # If the PC has a previous hit, try to attack in the vicinity
        pc_attack_x, pc_attack_y = get_next_attack_coords(player_grid, last_hit_coords)
    else:
        # Otherwise, make a random attack
        pc_attack_x = random.randint(0, 9)
        pc_attack_y = random.randint(0, 9)

    pc_attack = (pc_attack_x, pc_attack_y)

    display_pc_move_coordinates(pc_attack)

    # Check if the attack hits a player ship
    if pc_attack in player_ships:
        print("PC has hit a ship!")
        player_ships.remove(pc_attack)
        eliminated_player_ship_positions.append(pc_attack)  # Mark as eliminated
        player_grid[pc_attack_x][pc_attack_y] = "H"  # Mark the hit on the player's grid

       
    else:
        print("PC Miss!")
        player_grid[pc_attack_x][pc_attack_y] = "M"  # Mark the miss on the player's grid

        # If the PC has a previous hit, keep attacking in the same direction
        if last_hit_coords is not None:
            last_hit_coords = get_next_attack_coords(player_grid, last_hit_coords)

    return bool(eliminated_player_ship_positions), last_hit_coords

def display_pc_move_coordinates(pc_attack_coords):
    letter = chr(pc_attack_coords[1] + ord('A'))
    number = pc_attack_coords[0]
    print(f"PC's Move: Column {letter}, Row {number}")

def get_next_attack_coords(player_grid, last_hit_coords):
    # Returns the next attack coordinates based on the last hit
    x, y = last_hit_coords

    # Check surrounding coordinates (up, down, left, right) and choose randomly
    possible_coords = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    valid_coords = [(cx, cy) for cx, cy in possible_coords if 0 <= cx < 10 and 0 <= cy < 10 and player_grid[cx][cy] != "H" and player_grid[cx][cy] != "M"]

    if valid_coords:
        return random.choice(valid_coords)
    else:
        # If no valid surrounding coordinates, go back to random attacks
        return None
    
def check_player_ship_destroyed(pc_attack, player_ship_positions, player_grid):
    # Check if the attack hits a player ship
    if pc_attack in player_ship_positions:
        x, y = pc_attack
        print("PC has hit a ship!")
        player_ship_positions.remove((x, y))

    return False

def check_pc_ship_destroyed(player_attack, pc_ship_positions, pc_grid):
    # Check if the attack hits a player ship
    if player_attack in pc_ship_positions:
        x, y = player_attack
        print("Player has hit a ship!")
        pc_ship_positions.remove((x, y))

    return False

def display_pc_move_coordinates(pc_attack):
    print(f"PC's Move: Row {pc_attack[0]}, Column {pc_attack[1]}")

def main():
    # Start message
    print("\nThis is a game of Battleship. Enjoy!\n")

    # Creates the pc grid
    pc_grid = [['.' for _ in range(10)] for _ in range(10)]

    # Initialize pc_ship_positions
    pc_ship_positions_list = []

    # Get player ship positions and grid
    player_ships, player_grid = player_ship_positions()

    # Get pc ship positions, grid, and ships
    pc_ship_positions_list, pc_grid, pc_ships = pc_ship_positions(pc_grid)

    # Initialize moves grid
    moves_grid = [['.' for _ in range(10)] for _ in range(10)]  # Initialize moves grid
    
    # Initialize turn counter
    turn_counter = 0

    # Main game loop
    game_over = False
    while not game_over:
        # Increment turn counter
        turn_counter += 1
        print(f"\nTurn {turn_counter}")

        display_moves_grid(moves_grid)  # Display the initial moves grid

        # Player's turn
        player_attack_coords, player_result = player_attack(pc_ship_positions_list, pc_grid, moves_grid)
        update_moves_grid(moves_grid, player_attack_coords, "H" if player_result else "M")

        # Check if player has won
        if not pc_ship_positions_list:
            game_over = True
            break  # Exit the loop if the player has won

        # PC's turn
        pc_hit = pc_attack(player_ships, player_grid, pc_ship_positions_list, moves_grid)

        # Display the updated player's grid and moves grid after both turns
        display_grid(player_grid)
        display_moves_grid(moves_grid)

        # Check if PC has won
        if not player_ships:
            game_over = True

    # Display game result
    if not pc_ship_positions_list:
        print("Congratulations! You destroyed all PC ships.")
    else:
        print("PC destroyed all your ships. Game over.")

if __name__ == "__main__":
    main()