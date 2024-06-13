"""
A GUI-based zombie survival game wherein the player has to reach
the hospital whilst evading zombies.
"""
import tkinter as tk
from a2_solution import advanced_game
from constants import TASK, MAP_FILE
from task1 import BasicGraphicalInterface
from task2 import ImageGraphicalInterface
    

def main() -> None:
    """Entry point to gameplay."""
    game = advanced_game(MAP_FILE)
    root = tk.Tk()
    root.title('EndOfDayz')
    
    if TASK == 1:
    	gui = BasicGraphicalInterface
    else:
    	gui = ImageGraphicalInterface
    app = gui(root, game.get_grid().get_size())    
    app.play(game)


if __name__ == '__main__':
    main()

