import grpc
import missile_attack_pb2
import missile_attack_pb2_grpc
import random
from threading import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import logging
logging.basicConfig(filename='mylog.log', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


# 'T' is total time of the game and 't' is time of one iteration
print("Enter the following values : ")
N=int(input("Number of soldiers : "))
M=int(input("Size of grid : "))
T=int(input("Total time of game : "))
t=int(input("Duration of each attack : "))
t_initial =0

commander=None

#missile information
missile_x=None
missile_y=None
missile_radius=None

#Coordinates of commander and soldiers
used_coordinates=set()

#Objects alive in current iteration
current_iteration_obj=[]

#Class representing soldier info
class soldier:
    #initialising objects
    def __init__(self,id,x,y,speed,alive) -> None:
        self.id=id
        self.x=x
        self.y=y
        self.speed=speed
        self.alive=alive
    
#List of objects
list_obj=[]

logging.info('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$  STARTING THE GAME  $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$  STARTING THE GAME  $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
#function invoked by theard
def run_client():
    global M
    global N
    global T
    global t
    global t_initial
    global commander
    global used_coordinates
    global list_obj
    global current_iteration_obj
    for i in range(1,N+1):
        while(1):
            x=random.randint(0,M-1)
            y=random.randint(0,M-1)
            if(x,y) not in used_coordinates:
                used_coordinates.add((x,y))
                break
        speed=random.randint(0,4)
        alive=1
        obj=soldier(i,x,y,speed,alive)
        list_obj.append(obj)

    
    #printing values of objects
    for obj in list_obj:
        logging.info('Soldier '+str(obj.id)+',Position-('+str(obj.x)+','+str(obj.y)+'),speed:'+str(obj.speed)+',status:'+str(obj.alive))
        print('Soldier ID',obj.id, ':Position(',obj.x,',',obj.y,'),speed :',obj.speed,'status:',obj.alive )

    #printing grid with missile and soldiers
    def print_grid(list_obj):
        
        # Create a figure and axis
        fig, ax = plt.subplots()

        # Define the size of the grid, the number of rows, and columns
        rows = M
        columns = M

        # Define the size of each square (adjust these values as needed)
        square_size_x = 1.0 / columns  # Width of each square
        square_size_y = 1.0 / rows     # Height of each square

        # Set the axis limits to match the grid size
        ax.set_xlim(0, columns * square_size_x)
        ax.set_ylim(0, rows * square_size_y)

        # Set the background color to white
        ax.set_facecolor('white')

        # Define the row and column for the center of the missile
        global missile_x
        global missile_y
        global missile_radius
        missile_x_const=missile_x
        missile_y_const=missile_y
        missile_row = missile_y  
        missile_column = missile_x  

        # Define the width and height of the missile 
        missile_width = 2*missile_radius-1  
        missile_height = 2*missile_radius-1  

        # Calculate the corner coordinates of the missile
        missile_x = (missile_column - (missile_width - 1) / 2) * square_size_x
        missile_y = (missile_row - (missile_height - 1) / 2) * square_size_y

        # Draw the missile as a red rectangle covering the specified width and height
        missile = patches.Rectangle(
            (missile_x, missile_y),
            missile_width * square_size_x,
            missile_height * square_size_y,
            fill=True,
            color='red'
        )
        ax.add_patch(missile)

        # Create a 2D grid of coordinates for each square
        grid = []
        for row in range(rows):
            row_coords = []
            for col in range(columns):
                x = col * square_size_x
                y = row * square_size_y
                square = patches.Rectangle(
                    (x, y), square_size_x, square_size_y, fill=False, edgecolor='black', linewidth=1.0
                )
                ax.add_patch(square)
                row_coords.append((x, y))
            grid.append(row_coords)

        # Add numbering to rows and columns
        for i in range(rows):
            ax.text(-0.03, i * square_size_y + square_size_y / 2, str(i), va='center', ha='center', fontsize=12)

        for j in range(columns):
            ax.text(j * square_size_x + square_size_x / 2, -0.03, str(j), va='center', ha='center', fontsize=12)


        for item in list_obj:
                s1_x = item.x * square_size_x + square_size_x / 2
                s1_y = item.y * square_size_y + square_size_y / 2
                ax.text(s1_x, s1_y, f"s{item.id}", va='center', ha='center', fontsize=12, color='black')


        # Remove axis labels and ticks
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Show the grid
        plt.show()
        missile_x=missile_x_const
        missile_y=missile_y_const



    #function called by commander for giving info of missile to each thread and invoking soldier threads
    def missile_approaching(final_missile_coordinates):
        for obj in list_obj:
            if obj == commander:
                continue
            else:
                if obj.alive==1:
                    thread = Thread(target=run_soldier, args=(final_missile_coordinates,obj,))
                    list_thread.append(thread)
                    thread.start()


    #function for commander
    def run_commander():
        print("commander is s",commander.id)
        run_soldier(final_missile_coordinates,commander)
        missile_approaching(final_missile_coordinates)
        
    def status_all():
            for item in current_iteration_obj:
                status(item.id)
                

    def status(soldier_id):
        true_flag=0
        true_flag=was_hit(soldier_id,true_flag)
        if(true_flag==1):
            print("Soldier ",soldier_id,"is alive")
            logging.info("Soldier "+str(soldier_id)+ ':'+ "is alive")
        elif(soldier_id==commander.id):
            logging.info("Commander (soldier"+str(soldier_id)+") is dead")
            print("Commander (Sodier ",soldier_id,") is dead") 
        else:
            logging.info("Soldier "+str(soldier_id)+ ':'+ "is dead")
            print("Soldier ",soldier_id,"is dead")

    def was_hit(soldier_id,true_flag):
        for item in current_iteration_obj:
            if(item.id==soldier_id):
                if(item.alive==0):
                    true_flag=0
                else:
                    true_flag=1    
        return true_flag
    used_coordinates_lock = Lock()

    #function - taking shelter
    def run_soldier(final_missile_coordinates,obj):
        with used_coordinates_lock:
            print("soldier",obj.id,"coordinates:(",obj.x,obj.y,")")
            obj_coordinate=(obj.x,obj.y)
            #calculating possible soldier moves if he is in red zone
            if(obj_coordinate not in final_missile_coordinates):
                return
            else:
                k=2*obj.speed+1
                m=obj.x-(obj.speed)
                n=obj.y-(obj.speed)
                soldier_moves=[]
                o1=m+k-1
                o2=n+k-1
            while(m<=o1):
                n=obj.y-(obj.speed)
                while(n<=o2):
                    soldier_moves.append((m,n))
                    n=n+1
                
                m=m+1    
            #Discarding coordinates which are outside of grid
            final_soldier_moves=[]
            for item in soldier_moves:
                    if(item[0]<0 or item[0]>=M or item[1]<0 or item[1]>=M):
                        continue
                    final_soldier_moves.append(item)
    
            # Create a list of possible moves as strings
            possible_moves = [f"({item[0]}, {item[1]})" for item in final_soldier_moves]

            # Join the possible moves into a single string
            moves_str = ', '.join(possible_moves)

            # Print all the moves in a single line
            print(f"Soldier {obj.id} possible moves according to its speed: {moves_str}")


            #moving soldier to unoccupied coordinate
            for item in final_soldier_moves:
                if item not in final_missile_coordinates:
                    if (item) in used_coordinates:
                        continue
                    else:
                        used_coordinates.discard((obj.x,obj.y))
                        obj.x=item[0]
                        obj.y=item[1]
                        used_coordinates.add((obj.x,obj.y))
                        logging.info("Soldier"+str(obj.id)+"got saved and moved to new position:("+str(obj.x)+","+str(obj.y)+")")
                        print("Soldier ",obj.id,"finally moved to:(",obj.x,",",obj.y,") and is safe")
                        return
            #making soldier dead if not able to come out of red zone
            obj.alive=0
            for item in current_iteration_obj:
                if(item.id==obj.id):
                    item.alive=0
            id_delete=obj.id
            used_coordinates.discard((obj.x,obj.y))
            for item in list_obj:
                if item.id==id_delete:
                    list_obj.remove(item)

    #for each iteration getting info of missile through grpc from server
    #giving missile info to commander and invoking commander thread
    while(t_initial<=T):
        current_iteration_obj=list_obj.copy()
        if commander is None:
            commander=random.choice(list_obj)
            logging.info('Commander is soldier : '+str(commander.id))
        logging.info('**************Missile launching at time '+str(t_initial)+'*****************')
        print('*********************************Missile launching at time= ',t_initial,'******************************')
        channel = grpc.insecure_channel('172.17.84.82:50051') 
        stub = missile_attack_pb2_grpc.AttackStub(channel)
        response = stub.assign(missile_attack_pb2.Request(M=M))
        #Calculating missile coordinates
        global missile_x
        global missile_y
        global missile_radius
        missile_x = response.x
        missile_y = response.y
        missile_radius=response.radius
        print("missile position is : (",missile_x,",",missile_y,"), missile radius : ",missile_radius)
        logging.info("missile position is : "+str(missile_x)+","+str(missile_y)+" missile radius : "+str(missile_radius))

        k=2*missile_radius-1
        m=missile_x-(missile_radius-1)
        n=missile_y-(missile_radius-1)
        missile_coordinates=[]
        o1=m+k-1
        o2=n+k-1
        print("printing all coordinates covered by missile")
        while(m<=o1):
            n=missile_y-(missile_radius-1)
            while(n<=o2):
                missile_coordinates.append((m,n))
                n=n+1 
            m=m+1   
        #Discarding coordinates which are outside of grid 
        final_missile_coordinates=[]
        for item in missile_coordinates:
                if(item[0]<0 or item[0]>=M or item[1]<0 or item[1]>=M):
                    continue
                final_missile_coordinates.append(item)
       
        # Create a list of coordinates as strings
        coordinates_str = [f"({item[0]}, {item[1]})" for item in final_missile_coordinates]

        # Concatenate the coordinates into a single string
        coordinates_line = ', '.join(coordinates_str)

        # Print all the coordinates in a single line
        print(f"Missile coordinates: {coordinates_line}")

  
        #printing grid
        print_grid(list_obj)

        #invoking commander thread
        list_thread=[]
        for obj in list_obj:
            if obj == commander:
                thread=Thread(target=run_commander, args=())
                list_thread.append(thread)
                thread.start()


        for item in list_thread:
            item.join()

        if(commander.alive==0):
            commander=random.choice(list_obj)
            logging.info("Commander died so Newly elected commander is soldier" + str(commander.id))
            print("Commander died so Newly elected commander is soldier ",commander.id)
        print_grid(list_obj)
        print("Status of soldiers after current missile attack-------------")
        logging.info("Status of soldiers after current missile attack-------------")
        status_all()
        logging.info("Number of alive soldiers are : "+str(len(list_obj)))
        print("Number of alive soldiers are : ",len(list_obj))
        t_initial=t_initial+t

#starting the game
if __name__ == '__main__':
    run_client()

if len(list_obj)<=N/2:
    logging.info("###################  War lost  ##################")
    print("###################  War lost  ##################")
else:
    logging.info("###################  War won  ###################")
    print("###################  War won  ##################")






























