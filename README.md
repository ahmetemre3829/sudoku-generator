# Sudoku Generator
This Python program generates random Sudoku puzzles and saves their solutions. Sudoku puzzles are also created visually and saved in a specified folder.

## Requirements
The following Python libraries are required for the program to run:

* Pillow (for ImageFont, ImageDraw, and Image modules)
* colorama (for Fore)
* concurrent.futures and multiprocessing (They are part of the Python standard library, so no need to install them separately.)

You can install these libraries by running the following command:

`pip install pillow colorama`

Note: These requirements are for the latest version. It may vary in older versions.

## Usage
1- Start the program by running the following command in the terminal or command prompt:

`python sudoku-generator.py`

2- Enter how many Sudoku puzzles you want to generate.

3- Set the difficulty level (a value between 17 and 64).
* This value determines how many numbers will be removed from a fully filled Sudoku board.

4- The program will save the generated Sudoku puzzles in the "Sudokular" folder and their solutions in the "Sudoku Solutions" folder.

## Program Features
The program ensures that each generated Sudoku has only one solution.
It repeatedly tries to remove the desired number of numbers from the board without breaking the solution.

## License
This project is licensed under the GNU GENERAL PUBLIC LICENSE.
