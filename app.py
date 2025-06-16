import sys

grid = None
car_list = None

class Car:
    def __init__(self, name, init_pos, commands):
        self.name = name
        x, y, self.direction = init_pos.split()
        self.x = int(x)
        self.y = int(y)
        self.commands = commands
        self.current_step = None
        self.collision_step = None

    def display(self):
        #*: List down car_name, current_position, current_direction, last_commands/all_commands
        #SAMPLE: - A, (1,2) N, FFRFFFFRRL
        print(f"- {self.name}, ({self.x},{self.y}) {self.direction}, {self.commands}")


def input_validated(variable, workflow):
    # print(f"Validating the following input value: {variable} | type: {type(variable)} for {workflow} workflow")   # For debugging
    if workflow == "field_size":
        #* Validate field_size to only have 2 positive integers
        dimension = variable.split()

        if len(dimension) != 2:
            return False
        
        max_width_str, max_height_str = dimension
        
        if not (max_width_str.isdigit() and max_height_str.isdigit()):
            return False
        
        max_width = int(max_width_str)
        max_height = int(max_height_str)

        if not (0 <= max_width and 0 <= max_height):
            return False
        
        return True
    elif workflow == "car_name":
        #TODO: Check requirements - Are all alphanumeric, symbols, spaces and mixed caps allowed? (Assume only alphanumeric, any caps allowed for now, add more cleaning and/or validation check if not allowed)
        if variable.isalnum():
            return True
        return False
    elif workflow == "init_pos":
        #* Only 2 positive integer positive positions within the grid and a single direction of N, S, W, E
        parts = variable.split()

        if len(parts) != 3:
            return False

        x_str, y_str, direction = parts

        if not (x_str.isdigit() and y_str.isdigit()):
            return False

        x = int(x_str)
        y = int(y_str)

        max_x, max_y = grid
        if not (0 <= x < max_x and 0 <= y < max_y):
            return False

        if direction not in ("N", "S", "E", "W"):
            return False
        
        return True
    elif workflow == "menu":
        #* Validate to only options integer inputs of 1 or 2 
        if not variable.isdigit():
            return False
        if variable not in ("1", "2"):
            return False
        return True
    elif workflow =="commands":
        #* Validate series of input commands
        if not variable.isalpha():
            return False
        for each_command in variable:
            if each_command not in ("F", "R", "L"):
                return False
        return True
        

def start_menu():
    # Declare and clean up
    global grid
    global car_list
    grid = []
    car_list = []
    
    # Start of app
    print("Welcome to Auto Driving Car Simulation!")
    print("")
    while True:
        print("Please enter the width and height of the simulation field in x y format:")
        field_size = input()
        if not input_validated(field_size, "field_size"):
            continue
        break
    
    # Validate then split
    width_str, height_str = field_size.split()
    print(f"\nYou have created a field of {width_str} x {height_str}.")
    width = int(width_str)
    height = int(height_str)
    grid = [width, height]
    main_menu()


def main_menu():
    print("\nPlease choose from the following options:")
    print("[1] Add a car to field")
    print("[2] Run simulation")
    while True:
        choice = input()
        if not input_validated(choice, "menu"):
            continue
        break

    if choice == "1":
        add_car()
    else:
        if not car_list:
            print("You need to add at least one car before running the simulation.")
            main_menu()
        else:
            run_simulation()
    

def add_car():
    while True:
        car_name = input("\nPlease enter the name of the car:")
        #TODO: Check requirement - Assume auto strip but mixed caps and spaces allowed
        car_name = car_name.strip()
        if not input_validated(car_name, "car_name"):
            continue
        break
    
    while True:
        init_pos = input(f"Please enter initial position of car {car_name} in x y Direction format:")
        #TODO: Check requirement for initial position inputs - Assume allow small caps but auto change to big caps and auto strip
        init_pos = init_pos.strip().upper()
        if not input_validated(init_pos, "init_pos"):
            continue
        break
    
    while True:
        commands = input("Please enter the commands for car A:")
        if not input_validated(commands, "commands"):
            continue
        break
    
    new_car = Car(car_name, init_pos, commands)
    car_list.append(new_car)
    
    #* List car with position, direction and commands, then go back to main menu
    list_cars()
    main_menu()
    
    
def list_cars():
    print("\nYour current list of cars are:")
    for each_car in car_list:
        each_car.display()


def turn_car(current, cmd):
    #TODO: Maybe have better way to write this, but this is most easy to understand
    if cmd == "R":
        if current == "N":
            return "E"
        elif current == "E":
            return "S"
        elif current == "S":
            return "W"
        elif current == "W":
            return "N"
    elif cmd == "L":
        if current == "N":
            return "W"
        elif current == "W":
            return "S"
        elif current == "S":
            return "E"
        elif current == "E":
            return "N"


def run_simulation():
    list_cars()
    print("\nAfter simulation, the result is:")
    
    # Get grid's max
    max_x, max_y = grid
    
    # Track cars that ended their commands or due to collision
    car_results = {}
    
    # Get biggest number of steps among all the cars
    max_steps = max(len(car.commands) for car in car_list)
    
    for step in range(max_steps):
        # Use a set for car-car collision tracking
        position_set = {}
        for car_obj in car_list:
            # Ignore if no steps for the specific car
            if len(car_obj.commands) < step:
                continue
            
            # Ignore if collided and end prematurely
            if car_obj.name in car_results:
                continue
            
            # Get car's x and y position
            car_x, car_y = car_obj.x, car_obj.y
            
            # Get car's current direction
            facing = car_obj.direction
            
            # Get specific step
            cmd = car_obj.commands[step]
            step_str = str(step+1)
            
            #* Move each car one step at a time, within the grid - ignore if beyond the boundary
            if cmd in ("L", "R"):
                car_obj.direction = turn_car(facing, cmd)
            else:
                #* cmd is "F" means move forward one step in the direction it's facing
                if car_obj.direction == "E":
                    if (car_x + 1) < max_x:
                        car_obj.x = car_x + 1
                    else:
                        continue
                elif car_obj.direction == "W":
                    if (car_x - 1) > 0:
                        car_obj.x = car_x - 1
                    else:
                        continue
                elif car_obj.direction == "N":
                    if (car_y + 1) < max_y:
                        car_obj.y = car_y + 1
                    else:
                        continue
                elif car_obj.direction == "S":
                    if (car_y - 1) > 0:
                        car_obj.y = car_y - 1
                    else:
                        continue
            
            # Car-Car collision check
            new_pos = (car_obj.x, car_obj.y)
            
            if new_pos not in position_set:
                position_set[new_pos] = car_obj.name
            else:
                #* Collision detected -> affected cars stop moving, show position and step number
                collided_car = position_set[new_pos]
                
                # Save both cars' results
                car_results[car_obj.name] = f"- {car_obj.name}, collides with {collided_car} at ({car_obj.x},{car_obj.y}) at step {step_str}"
                car_results[collided_car] = f"- {collided_car}, collides with {car_obj.name} at ({car_obj.x},{car_obj.y}) at step {step_str}"
    
            # Check for end of commands
            if step == len(car_obj.commands) - 1 and car_obj.name not in car_results:
                car_results[car_obj.name] =  f"- {car_obj.name}, {new_pos} {car_obj.direction}"
    
    # After for-loop over car_list at the current step:
    for car_obj in car_list:
        # If car has stored result (e.g. from collision), print it
        # Otherwise, print current position/direction as fallback
        print(car_results.get(car_obj.name, f"- {car_obj.name}, ({car_obj.x},{car_obj.y}) {car_obj.direction}"))
                
    end_menu()


def end_menu():
    lines = ["\nPlease choose from the following options:",
    "[1] Start over",
    "[2] Exit"]
    print("\n".join(lines))
    while True:
        end_choice = input()
        if not input_validated(end_choice, "menu"):
            continue
        break
    
    if end_choice == "2":
        print("\nThank you for running the simulation. Goodbye!")
        input()
        sys.exit()
    start_menu()


if __name__ == "__main__":
    start_menu()