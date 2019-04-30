## Dots_And_Boxes_QLearning
Implementing a Q_Learning agent to play Dots and Boxes. Evaluating the performance of Q-Tables compared to Functional Approximations of the Q Table

The following is a brief description of how to use the scripts contained in this repository.

# Scripts
## QTable_vs_Approx_Test.py
  This script compares the performance of a Q Learning agent using a functional approximation playing against an agent using a Q-Table.
  There are two configurable switches within the script: tDrawNow and boardSize. tDrawNow controls whether or not a visualization of
  the game is provided along with a score printed to output. The board size is self explanitory. Nothing else should need to be
  modified within the script.
  To use this script the "QComp_Table_Seeded.h5" file must be present in your directory and correspond to the board size variable
  set within the script. For exmaple, When boardSize = 2. Overwrite "QComp_Table_Seeded.h5" with a copy of "QComp_Table_Seeded2x2.h5".
  Running the script will play 1000 games and output the performance of each agent in a plot. Close the plot to terminate the script.
  Run the script by typing the following in the terminal:
  
    python3 QTable_vs_Approx_Test.py
    
## QvQ_Training.py
  This script uses two Q learning agents to play against one another using the same Q-Table or functional approximation model. The
  following are configurable switches within the script:
  
    numEpisodes = 10000  # Number of Games Played  
    tDrawNow = False # Display Game and Print Game scores while they are played
    boardSize = 3 # Control the gameboard size
    useFcnApprox = True #Use this control whether the Q Agents are usinga functional approximation or a Q Table
    numGamesPerUpdate = 1000 # How often training is paused to sample performance against a random player.
    numGamesPerRetrain = 10000 # How often the functional approximation is retrained given data learned while playing.
    epsilon = .1 # How often the Q-Agents will explore "non-optimal" moves
    MasterQTable = {} # This means that the Q-Agents will start from scratch in their learning. Placing a tCompDict will allow
                      # the the Q agents to be seeded or non-empty.
                      
  In order to run this script with useFcnApprox set to True the correct model must be saved in "QComp_Table_Seeded.h5" Similarly to the
  instructions provided above. 
  To use this script the "QComp_Table_Seeded.h5" file must be present in your directory and correspond to the board size variable
  set within the script. For exmaple, When boardSize = 2. Overwrite "QComp_Table_Seeded.h5" with a copy of "QComp_Table_Seeded2x2.h5".
  Note a copy of a 2x2 functional approximation and a 3x3 functional approximation are provided in  this repository. Upon completion 
  the script will generate a plot of its performance while training. Close this plot to terminate the script.
  Run the script by typing the following in the terminal:
  
    python3 QvQ_Training.py
  
## NN_Regression_Fcn_Approx.py
  This script takes a training size and boardsize and creates a NN Functional approximation for the parameters provided.
  These are the configurable parameters:
  
    trainingSet = 10000 # Refers to the number of games played during QvQ training. This number is used to load the Q Table that will be
                        # used as training data for the functional approximation.
    boardSize = 2       # Refers to the board size. Also used to determine which file to load when obtaining a dictionary for training
                        # data.
                        
  This file also acts as a helper providing some functions to extract data from a Q-Table to convert them for training. As well as a
  function to convert state action pairs into a format suitable for the model to make a prediction.
  Run the script by typing the following in the terminal:
  
    python3 NN_Regression_Fcn_Approx.py
    
## Dots_Game_Driver.py
  This script allows a Human to play against a Q agent. The configurable switches are as follows:
  
    tDrawNow = False # Display Game and Print Game scores while they are played
    useFcnApprox = True #Use this control whether the Q Agents are usinga functional approximation or a Q Table
    trainingSet = 10000 # Refers to the number of games played during QvQ training. This number is used to load the Q Table that will be
                        # used as training data for the functional approximation.
                        
  This script is expecting that player 1 is a human and player 2 is a Q agent. So prompted while running the script. Use the proper
  enumerations to obtain that game configuration. (If both players are humans this should not matter and it should still work). Again
  when using a Functional approximation or training set the proper files must be available in the directory to properly load the
  Q-agent. Disclaimer that the performance improved against random moves is not guaranteed performance against human players.
  Run the script by typing the following in the terminal:
  
    python3 NN_Regression_Fcn_Approx.py
    
## Conv2x2To3x3.py
  This script takes a 2x2 Q-Table and changes it into a format that will be useable for a Q-Agent learning on a 3x3 board. 
  This scripts requires that the Dictionary corresponding to the configurable parameters is present in the directory.
  Configurable parameters include:
  
    trainingSet = 10000 # Refers to the number of games played during QvQ training. This number is used to load the Q Table that will be
                        # used as training data for the functional approximation.
    boardSize = 2       # Refers to the board size. Also used to determine which file to load when obtaining a dictionary for training
                        # data.
                        
  Run the script by typing the following in the terminal:
  
    python3 Conv2x2To3x3.py
    
## State_Reduction_Script.py
  This script takes a given board size and computes all possible states and actions possible for that board. It then saves that result
  to StateSet2x2.py. (I eventually learned that there was a much more efficient way to save variables but this was for early on
  exploratory measures.)

# Supporting Source Code
Q_Learning_Comp_Alt.py # Contains functions for the Q-Learning Agent to operate properly
Dots_RandMove_Comp.py # Contains functions to generate legal random moves
Dots.py # Contains the instructions of how to build a game and generate rewards.
StateSet2x2.py # Saved collection of states from State_Reduction_Script.py

