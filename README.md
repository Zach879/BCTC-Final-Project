Dataset Creation -> Dataset Creation Main.py: Generates a dataset incorporating real-world-like noise, text rotations, font variety and styles, and visual noise. The results were very robust for training the model and prevented overtraining at all stages.

Character Determiner -> main.py: Serves as the neural network model training center. Used to train the model on the command line and manually tune the parameters. Once good enough, the program allows for the savings of the weights for future access.

Senior Project Hub -> Contains the Visual Studio setup files. Within the "Senior Project Hub" subdirectory, there contains the "Character Determiner.cs" file, which acts as the frontend application before being compiled into an executable and placed within 
  the home directory. The frontend application is handled 100% locally once all necessary files are downloaded. 

Data -> OCR Scanner.py: Serves as the processing helper function for the frontend application. This file splits an image of computer text into multiple lines (if applicable), then using edge detection to generate boundary boxes, as well as
  various algorithms to refine the boundary boxes generated. Finally, each boundary box is fed to the trained model from "Character Determiner" and sent back to the frontend application.
