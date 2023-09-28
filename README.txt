*************************************************************************
Missile Defense Game
*************************************************************************

Group Members:
Aditi Bhardwaj (2023H1030084P)
Mahima Sharma (2023H1030081P)

*************************************************************************
Instructions for Running the Code
*************************************************************************

1. Environment Setup:
   - Ensure that you have Python installed on your system. 


2. Install Required Libraries:
   - This code relies on several Python libraries, including 'grpc', 'matplotlib'. You can install them using pip by running the following commands:
    
     python -m pip install grpcio
     python -m pip install grpcio-tools
     pip install matplotlib 
    

3. Protocol Buffers Compilation:
   - The code uses Protocol Buffers for gRPC communication. You need to compile the `missile_attack.proto` file to generate the necessary Python code.      	Navigate to the directory containing the `missile_attack.proto` file and run the following command:
     
      python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. missile_attack.proto
    
   - This will generate 2 files :

      missile_attack_pb2_grpc.py 
      missile_attack_pb2.py 

4. Running the Game:
   - To start the Missile Defense Game : 
    
     First at one computer, run the server using the following command (Make sure to enter server's system IP in the missile_attack_server.py at line 23):
     python missile_attack_server.py

     Now, at second computer, run the client using the following command (Make sure to enter server's system IP in the missile_attack_client.py at line               
     242):
     python missile_attack_client.py
     After running above command it will ask for inputs on terminal, give all the inputs.
 
    Note: Make sure first to run server then client.
    5.4.1. Ensure you have the required libraries installed, including grpc, matplotlib, and others.
    5.4.2. Make sure both the computers are connected to same wifi.
    5.4.3. Make sure the remote server and client have same ip address(of the server) in their code. 
    5.4.4. Monitor the game progress in the console.At each iteration, when the grid appears it will first show the pre missile attack snapshot of missile and 		soldiers and after closing the grid window it will show post missile attack snapshot.
    5.4.5. Game events are logged to a file named `mylog.log`.
   

5. Game Execution:
   - The game will start, and you will see the game grid with soldiers and a missile.
   - The game will continue for a specified duration T.
   - The game's progress and events will be logged to a file named 'mylog.log'.

6. Game Outcome:
   - After the game concludes, the log file will indicate whether the war was won or lost based on the number of remaining soldiers.
   - The log file will also contain detailed information about soldier movements and events during the game.
