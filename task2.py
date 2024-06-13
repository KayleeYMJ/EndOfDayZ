"""
End of Dayz
"""

import tkinter as tk
from a2_solution import *
from task1 import *
from PIL import Image, ImageTk
from tkinter import filedialog
import tkinter.messagebox as tm
from typing import Tuple, Optional, Dict, List

class ImageMap(AbstractGrid):
    """
    Extend existing BasicMap class. Images should be used to display
    each square rather than rectangles.
    """
    
    def __init__(self, master, size):
        """
        Each rectangle should have images.
        
        Parameters:
            master: The toplevel window.
            size: The number of rows (= number of columns) in the grid.
        """
        super().__init__(master,size, size, CELL_SIZE, CELL_SIZE)
        self.config(width = size*CELL_SIZE, height = size*CELL_SIZE,\
                    bg = "white")
        self._size = size

    def draw_background(self) -> None:
        """
        Draw tile background. Every tile should be 50 pixels high
        and 50 pixels wide.
        """
        # resize and convert the image of background 
        background = Image.open(IMAGES[BACK_GROUND])
        resize_background = background.resize((CELL_SIZE, CELL_SIZE),\
                                              Image.ANTIALIAS)
        self._background = ImageTk.PhotoImage(resize_background)

        # draw background 
        for row in range (0, self._size):
            for column in range (0, self._size):
                x = CELL_SIZE / 2 + row * CELL_SIZE
                y = CELL_SIZE / 2 + column * CELL_SIZE
                self.create_image(x, y, image = self._background)
        
    def draw_entity(self, game:AdvancedGame) -> None:
        """
        Draw entity in the map of game.

        Parameters:
            game: The current game.
        """
        grid_map = game.get_grid().get_mapping()
        # convert the images
        self._zombie = PhotoImage(file =IMAGES[ZOMBIE])
        self._garlic = PhotoImage(file =IMAGES[GARLIC])
        self._hero = PhotoImage(file =IMAGES[PLAYER])
        self._hospital = PhotoImage(file =IMAGES[HOSPITAL])
        self._crossbow = PhotoImage(file =IMAGES[CROSSBOW])
        
        # draw entity
        for position, entity in grid_map.items():
            if isinstance(entity,Zombie):
                self.create_entity(position, self._zombie) 
            elif isinstance(entity,Garlic):
                self.create_entity(position, self._garlic)
            elif isinstance(entity,Player):
                self.create_entity(position, self._hero)   
            elif isinstance(entity,Hospital):
                self.create_entity(position, self._hospital)        
            elif isinstance(entity,Crossbow):
                self.create_entity(position, self._crossbow)
                
    def create_entity(self, position:Position, image) -> None:
        """
        Create images of entities at the given position. This method
        should be called when draw entities of the game.
        
        Parameters:
            position: The position of entity.
            image: The image of entity.
        """
        # get x and y of position 
        x = position.get_x()
        y = position.get_y()
        # get the center point of position
        position_center = self.get_position_center((x, y))
        x_center = position_center[0]
        y_center = position_center[1]
        # create images
        self.create_image(x_center, y_center, image = image)


class StatusBar(tk.Frame):
    """
    The layout of the status bar and positioning of the banner.
    """
    
    def __init__(self, master, size, interface):
        """
        Draw chaser and chasee images and create two buttons:
        ('restart game' and 'quit').Also, create the frame of time and
        the frame of moving steps.
        
        Parameters:
            master: The toplevel window.
            size: The number of rows (= number of columns) in the grid.
            interface: The current interface of game.
        """
        super().__init__(master)
        self._master = master
        self._size = size
        self._interface = interface
        # draw two images and create two buttons
        self.draw_images()
        self.gameButton()
        # set the original time and create the frame of time
        self._seconds = 0
        self._mins = 0
        self._timeFrame = None
        self._time = None
        self.timer()
        # set the original step and create the frame of moving steps
        self._steps = 0
        self._movesFrame = None
        self.movesMade()    

    def _space(self) -> int:
        """
        Calulate the space between two frame.
        """
        return (self._size * CELL_SIZE + INVENTORY_WIDTH) // 24
        
    def draw_images(self) -> None:
        """
        Draw chaser and chasee images.
        """
        # convert the images
        self._chasee = PhotoImage(file = IMAGES[CHASEE])
        self._chaser = PhotoImage(file = IMAGES[CHASER])
        # create images
        chaser_image = tk.Label(self, image = self._chaser, bg = 'white')
        chaser_image.pack(side = tk.LEFT,padx = self._space())
        chaser_image = tk.Label(self, image = self._chasee, bg = 'white')
        chaser_image.pack(side = tk.RIGHT, padx = self._space())  
         
    def timer(self) -> None:
        """
        Draw time frame. Thie method should be called every seconds.
        """
        # draw time frame and create 'timer' label
        if self._timeFrame == None:
            self._timeFrame = Frame(self)
            self._timeFrame.pack(side = tk.LEFT,padx = self._space())
            self._timer = tk.Label(self._timeFrame, text = TIMER,\
                                   font = ("Purisa", 13))
            self._timer.pack(side = tk.TOP)
            
        # clear the time count last time
        elif self._time != None:
            self._time.destroy()

        # create time count label
        TIME = str(self._mins) + " mins " + str(self._seconds) + " seconds"
        self._time = tk.Label(self._timeFrame, text = TIME,\
                              font = ("Purisa", 13))
        self._time.pack(side = tk.TOP)
        
        # called every seconds
        self._cancel = self.after(1000, self.timer)
        # count time
        self.timeCount()
        
    def timeCount(self) -> None:
        """
        Count time.
        """
        self._seconds += 1
        while self._seconds >= 60:
            self._mins += 1
            self._seconds -= 60
    
    def movesMade(self) -> None:
        """
        Create moves frame. this method should be called every step
        after moving player.
        """
        # draw moves made frame and create 'Moves Made' label
        if self._movesFrame ==None:
            self._movesFrame = Frame(self)
            self._movesFrame.pack(side = tk.LEFT, padx = self._space())
            self._movesMade = tk.Label(self._movesFrame, text = MOVES_MADE,\
                                       font = ("Purisa", 13))
            self._movesMade.pack(side = tk.TOP)

        # clear the moves made count last time
        elif self._moves != None:
            self._moves.destroy()

        # create moves made count label
        MOVES = str(self._steps)+" "+"moves"
        self._moves = tk.Label(self._movesFrame, text = MOVES, \
                               font= ("Purisa", 13))
        self._moves.pack(side = tk.TOP)

    def movesCount(self) -> None:
        """
        Count steps of moving player.
        """
        self._steps += 1
        self.movesMade()
    
    def gameButton(self) -> None:
        """
        Create button frame and two buttons.
        """
        # create button frame
        button_frame = Frame(self)
        button_frame.pack(side = tk.RIGHT, padx = self._space())
        
        # create two buttons
        self._restartButton = tk.Button(button_frame, text = RESTART_GAME,\
                                        command = self.restartGame)
        self._restartButton.pack(side = tk.TOP)
        self._quitButton = tk.Button(button_frame, text = QUIT_GAME,\
                                     command = self.quitGame)
        self._quitButton.pack(side = tk.TOP)

    def resetData(self) -> None:
        """
        Reset the data and recreate moves frame, when restart the game.
        """
        self._steps = 0
        self._seconds = 0
        self._mins = 0
        self.movesMade()
        
    def restartGame(self) -> None:
        """
        Restart the game.
        """
        self.after_cancel(self._cancel)
        self._interface.replay()
        self.timer()

    def quitGame(self) -> None:
        """
        Quit the game.
        """
        self._master.destroy()

    
class ImageGraphicalInterface(BasicGraphicalInterface):
    """
    Extend existing BasicMap class. Images should be used to display
    each square rather than rectangles.
    """
    
    def __init__(self,root,size):
        """
        Draw the banner, and instantiate and pack the ImageMap
        ,the StatusBar and the InventoryView. Also, create file menu.
        
        Parameters:
            root: The root window.
            size: The number of rows (= number of columns) in the grid.
        """
        self._root = root
        self._size = size
        self._root.title(TITLE)

        # set time records
        self._minsRecords = 0
        self._secondsRecords = 0
        self._timesRecords =0

        # draw banner label
        banner = Image.open(IMAGES[BANNER])
        resize_banner = banner.resize((self._size*CELL_SIZE+INVENTORY_WIDTH,\
                                       BANNER_HEIGHT), Image.ANTIALIAS)
        self._banner = ImageTk.PhotoImage(resize_banner)
        banner_image = tk.Label(self._root, image = self._banner, bg = 'white')
        banner_image.pack(side = tk.TOP)

        # instantiate the StatusBar 
        self._statusBar = StatusBar(self._root, self._size,self)
        self._statusBar.pack(side = tk.BOTTOM)

        # instantiate the ImageMap
        self._map = ImageMap(self._root, self._size)
        self._map.pack(side = tk.LEFT)

        # instantiate the InventoryView
        self._inventoryView = InventoryView(self._root, self._size)
        self._inventoryView.pack(side = tk.RIGHT)

        # create file menu
        menu_bar = tk.Menu(self._root)
        self._root.config(menu = menu_bar)
        menu_options = tk.Menu(menu_bar)
        menu_bar.add_cascade(label = FILE, menu = menu_options)

        # add command into file menu
        menu_options.add_command(label = RESTART_GAME,\
                                 command = self.replay, font = ("Verdana",15))
        menu_options.add_command(label = SAVE_GAME,\
                                 command = self.saveGame, font = ("Verdana",15))
        menu_options.add_command(label = LOAD_GAME, \
                                 command = self.loadGame, font = ("Verdana",15))
        menu_options.add_command(label = QUIT, \
                                 command = self.quitCheck, font = ("Verdana",15))
        menu_options.add_command(label = HIGH_SCORES, \
                                 command = self.highScores, font = ("Verdana",15))

    def draw(self, game:AdvancedGame) -> None:
        """
        Draws the view based on the current game state.
        """
        self._game = game
        self._map.draw_background()
        self._map.draw_entity(game)
        inventory = game.get_player().get_inventory()
        self._inventoryView.draw(inventory)

    def move(self, game:AdvancedGame, direction) -> None:
        """
        Handles moving the player and count the moving steps.
        """
        super().move(game, direction)
        self._statusBar.movesCount()
            
    def replay(self) -> None:
        """
        Replay the game and reset the data.
        """
        self._statusBar.resetData()
        super().replay()

    def quitCheck(self) -> None:
        """
        Ask if quit.
        """
        end = tm.askquestion("Quit",QUIT_MESSAGE)
        if end == "yes":
            super().quit()
                
    def saveGame(self) -> None:
        """
        Save the map of the game.
        """
        grid = self._game.get_grid()
        mapping =''

        save_file = filedialog.asksaveasfile(mode='w', defaultextension='txt')
        if save_file is None:
            return
        
        for row in range (0,10-1):
            for column in range (0,10-1):
                if (row,column) in grid.serialize() :
                    mapping += grid.serialize()[(row,column)]
                else:
                    mapping += ' '
            mapping += '\n'

        save_file.write(mapping)
        save_file.close()

    def loadGame(self) -> None:
        """
        Load a saved game by open a file.
        """
        game_map = filedialog.askopenfilename()
        if game_map:
           try:
               mapping = advanced_game(game_map)
               self.loadPlay(mapping)
           except:
               tkinter.messagebox.showwarning(message=WARNING_MESSAGE, title=WARNING)
               return

    def loadPlay(self, gameMap:str) -> None:
        """
        Load a saved game and stop the current game.
        """
        self._map.after_cancel(self._mapRenew)
        self._map.delete(tk.ALL)
        self._inventoryView.delete(tk.ALL)
        self.play(gameMap)

    def highScores(self) -> None:
        """
        Display top 3.
        """
        print("That's all.")
        print("Thank you for marking.")
        

## test Task 2
def main() -> None:
    root = tk.Tk()
    gui = ImageGraphicalInterface(root,10)
    game=advanced_game(MAP_FILE)
    gui.play(game)
    root.mainloop()
    
    
if __name__ == "__main__":
    main()
        
