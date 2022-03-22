Begin by making sure pygame is within your libraries on your computer. This is essential in getting the graph to display.

Next make sure you download and save the master code file (.ipynb file) and open it with Jupyter in order to run it.

You will execute the task by running the “runFunction” function, this will call all the functions in the file (be sure to run the other functions first so their respective actions are defined). You will then be prompted to enter the required values, follow the prompts and once they are all entered the code should execute.

This code works by first drawing the obstacle board, then getting the user inputs (or defining random start inputs if that is what the user specifies), then then gathering node information (position, cost), next executing the a star search method (assesses movement based on cost) and finally it backtraces and displays the final path from start node to goal node, all the while avoiding obstacles.
