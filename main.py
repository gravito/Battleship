import pandas as pd
import random
import os

class battleship:
    grid = 10 #custom grid side
    computer_flag = True #if you want to play with player 2, change this to False

    def __init__(self):
        self.grid1 = [[0 for i in range(self.grid)] for j in range(self.grid)]
        self.grid2 = [[0 for i in range(self.grid)] for j in range(self.grid)]
        self.carrier = 5
        self.bs = 4
        self.cruiser = 3
        self.sub = 3
        self.des = 2
        self.total = self.carrier + self.bs + self.cruiser + self.sub + self.des 
        self.counter = 0 #counter to track minimum number of attempts

    def cls(self):
        os.system('cls' if os.name=='nt' else 'clear')

#validation function to check whether ship can be placed in the coordinate range
    def validate(self,a,b,ships,choice):
        if choice == "v":
            dist = a + self.shipping(ships)
        elif choice == "h":
            dist = b + self.shipping(ships)
        else:
            print("Please only enter v or h \n")
            return False
        if dist <= self.grid:
            return True
        else:
            print("Ship going out of range \n. Enter starting coordinates again \n")
            return False

    
    def shipping(self,ship):
        if ship == "carrier":
            return self.carrier
        elif ship == "battleship":
            return self.bs
        elif ship == "cruiser":
            return self.cruiser
        elif ship == "submarine":
            return self.sub
        elif ship == "destroyer":
            return self.des

#This function checks whether ships are already placed in the grid while placing.

    def collision(self,player,ship,choice,s1,t1):
        if choice == "v":
            for i in range(s1,s1+self.shipping(ship)):
                if player == 1:
                    if self.grid1[i][t1] == 0:
                        continue
                    else:
                        return False
                elif player == 2:
                    if self.grid2[i][t1] == 0:
                        continue
                    else:
                        return False
        if choice == "h":
            for i in range(t1,t1+self.shipping(ship)):
                if player == 1:
                    if self.grid1[s1][i] == 0:
                        continue
                    else:
                        return False
                elif player == 2:
                    if self.grid2[s1][i] == 0:
                        continue
                    else:
                        return False
        return True

#used dataframe from panda library to put beautiful coordinate system for the 2D array    
    def print_grid(self,player):
        if player == 1:
            print(pd.DataFrame(self.grid1))
        else:
            print(pd.DataFrame(self.grid2))

#simple for loop to place ships
    def place_board(self,player,ship,n,s1,t1):
        if n == "v":
            for i in range(s1,s1+self.shipping(ship)):
                if player == 1: 
                    self.grid1[i][t1] = 1
                elif player == 2: 
                    self.grid2[i][t1] = 1
        elif n == "h":
            for i in range(t1,t1+self.shipping(ship)):
                if player == 1: 
                    self.grid1[s1][i] = 1
                elif player == 2: 
                    self.grid2[s1][i] = 1

#random input for the computer
    def input_computer(self):
        coor = [0,0]
        coor[0] = random.randint(0,self.grid-1)
        coor[1] = random.randint(0,self.grid-1)
        return coor

#guilty for copying, but was too tired to create those pesky input test cases :(
    def input_user(self):
        while True:
            user_input = input("Please enter coordinates (row,col) ? ")
            try:
                coor = user_input.split(",")
                if len(coor) != 2:
                    raise Exception("Invalid entry, too few/many coordinates.")
                coor[0] = int(coor[0])
                coor[1] = int(coor[1])
                if coor[0] >= self.grid or coor[0] < 0 or coor[1] >= self.grid or coor[1] < 0:
                    raise Exception("Invalid entry. Please use values between 0 to {0} only.".format(self.grid - 1))
                return coor
            except ValueError:
                print ("Invalid entry. Please enter only numeric values for coordinates")
            except Exception as e:
                print (e)          

#this function places the ships after validating input and collision cases
    def place(self,ship,player):
        print ("Enter starting coordinates to place your %s \n" % ship)
        while True:
            if self.computer_flag == True and player == 2:
                s1,t1 = (self.input_computer())
                n = random.choice("vh")
            else:
                s1,t1 = (self.input_user())
                print ("Do you want to place your %s horizontally or row wise (h) or vertically or column wise (v) \n" % ship)
                n = input()

            if (self.validate(s1,t1,ship,n) == True):
                if (self.collision(player,ship,n,s1,t1) == True):                
                    self.place_board(player,ship,n,s1,t1)
                    if self.computer_flag == True:
                        self.print_grid(1)
                    else:
                        self.print_grid(player)    
                else:
                    print("Your ships are already placed there. Enter starting coodinates again \n")
                    continue
            else:
                continue
            break

#a little helper function to place all ships
    def place_ships(self,player):
        print ("Player {0} place your ship \n".format(player))
        self.place("carrier",player)
        self.place("battleship",player)
        self.place("cruiser",player)
        self.place("submarine",player)
        self.place("destroyer",player)
        self.print_grid(player)

#this function cehcks the grid status. Doing it the crude way, of checking whether any ship is alive (1)
    def check_grid(self,player):
        for i in range(self.grid):
            for j in range(self.grid):
                if player == 1:
                    if self.grid2[i][j] == 1:
                        return False
                else:
                    if self.grid1[i][j] == 1:
                        return False
        return True

#Reports hit or miss. If hit, changes the grid to -1. Input from computer random

    def attack(self,player):
        print ("Player {0} enter your coordinate".format(player))
        if self.computer_flag == True and player == 2:
            x,y = self.input_computer()
        else:
            x,y = self.input_user()
            self.counter += 1

        if player == 2:
            if self.grid1[x][y] == 1:
                print ("HIT HIT HIIIIIIIT \n")
                self.grid1[x][y] = -1
            elif self.grid1[x][y] == -1:
                print ("You already hit this \n")
            else:
                print ("MISS MISS MIIIIIIS \n")
        else:
            if self.grid2[x][y] == 1:
                print ("HIT HIT HIIIIIIIT \n")
                self.grid2[x][y] = -1
            elif self.grid2[x][y] == -1:
                print ("You already hit this \n")
            else:
                print ("MISS MISS MIIIIIIS \n")

        #a nifty little add on, taking the minimum time to sink all ships is total number of ships, so won't check grid before that. Applied to computer logic too
        if self.counter >= self.total and self.check_grid(player) == True:
            return True
        else:
            return False

    def get_player_turn(self,counter):
        if (counter)%2 == 0:
            return 2
        else:
            return 1
    def print_rules(self):
        print ("Objective of the game is to sink opponents battleship \n")
        print ("You will get unlimited chances, unless all battleships are sunk \n")
        print ("When placing battleship, remember, they are of following lengths: \n")
        print ("Carrier is of length %d \n" % self.carrier)
        print ("Battleship is of length %d \n" % self.bs)
        print ("Cruiser is of length %d \n" % self.cruiser)
        print ("Submarine is of length %d \n" % self.sub)
        print ("Destryoer is of length %d \n" % self.des)
        print ("All the best comrade \n")

if __name__ == "__main__":
    a = battleship()
    a.print_rules()
    a.print_grid(1) 
    a.place_ships(1)
    a.print_grid(2) 
    a.place_ships(2)
    a.cls()
    print ("Begin battle \n") 
    counter = 1
    while True:
        counter = a.get_player_turn(counter)
        result = a.attack(counter)
        if result == True:
            print("Player {0} has won the match \n".format(counter))
            break
        else:
            counter += 1
            continue
