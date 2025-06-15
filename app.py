import os
import sys
import argparse

grid = []
car_list = []

class Car:
    def __init__(self, name, x, y, direction, commands):
        self.name = name
        self.x = x
        self.y = y
        self.direction = direction
        self.commands = commands

    def display(self):
        print(f"- {self.name}, ({self.x},{self.y}) {self.direction}, {self.commands}")

def input_validated(variable, workflow):
    print(f"Validating the following input value: {variable} | type: {type(variable)} for {workflow} workflow")
    if workflow == "new_car":
        #TODO: Only 2 positive integer positive positions within the grid and a single direction of N, S, W, E (maybe allow small caps? and auto change to big caps)
        return False
    elif workflow == "field_size":
        #TODO: Validate field_size to only have 2 positive integers, else ask again and/or raise error
        print(f"input value: {variable} | type: {type(variable)}")
        return False
    elif workflow == "menu":
        #TODO: Validate to only options integer inputs of 1 or 2 | action options: ignore / ask this question again / prompt valid choices
        return False
    elif workflow =="commands":
        #TODO: Validate series of input with the position and direction of car"
        return False
        

def start_menu():
    print("Welcome to Auto Driving Car Simulation!")
    print("")
    while True:
        field_size = input("Please enter the width and height of the simulation field in x y format:")
        if not input_validated(field_size, "field_size"):
            continue
        break
    
    width, height = field_size.split()
    print(f"You have created a field of {width} x {height}.")
    global grid
    grid = [width,height]
    main_menu()

def main_menu():
    print("Please choose from the following options:")
    print("[1] Add a car to field")
    print("[2] Run simulation")
    while True:
        choice = input()
        if not input_validated(choice, "menu"):
            continue
        break

    if choice == 1:
        add_car()
    

def add_car():
    car_name = input("Please enter the name of the car:")
    #TODO: Are all alphanumeric and symbols allowed? (Assume allowed for now, add validation check if not allowed)
    while True:
        init_pos = input(f"Please enter initial position of car {car_name} in x y Direction format:")
        if not input_validated(init_pos,"new_car"):
            continue
        break
        
    x, y, dir = init_pos.split()
    while True:
        commands = input("Please enter the commands for car A:")
        if not input_validated(commands, "commands"):
            continue
        break
    
    new_car = Car(car_name, x, y, dir, commands)
    car_list.append(new_car)
    for each_car in car_list:
        each_car.display()
    #TODO: Before going back to main menu, a listing of all cars add will be printed
    main_menu()
    

def app():
    start_menu()
    
    
    if menu_choice == 1:
        
        
        print("Your current list of cars are:")
        #TODO: list down car_name, current_position, current_direction, last_commands/all_commands
        #- A, (1,2) N, FFRFFFFRRL
        
        #TODO: back to menu again
        print("""Please choose from the following options:
        [1] Add a car to field
        [2] Run simulation""")
        
        #TODO: if 2, result should be this, which is after running the commands
        #TODO: commands should check for wall collision and other car collision, the rest of the commands will negate, position will be car-car collision is after collision.
        
        print("After simulation, the result is:")
        # - A, (5,4) S
        
        lines = ["Please choose from the following options:",
        "[1] Start over",
        "[2] Exit"]
        print("\n".join(lines))
        end_choice = input()
        #TODO: Validate choices
        
        if end_choice == 2:
            print("Thank you for running the simulation. Goodbye!")
            sys.exit()
        
        
    
    
    
    #bottom left 0,0
    #top right width,height (e.g. 9,9 for 10x10)
    pass


if __name__ == "__main__":
    #possible inputs: width,height,car_name,start_pos,direction
    #ongoing inputs can be given to each car
    #limit within the grid
    app()