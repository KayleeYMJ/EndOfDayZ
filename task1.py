"""
End of Dayz
"""

import tkinter as tk
from constants import *
from tkinter import *
from a2_solution import *
import tkinter.messagebox as tm
from typing import Tuple, Optional, Dict, List


# Implement my classes here.
class AbstractGrid(tk.Canvas):
    """
    AbstractGrid is an abstract view class that provides base functionality
    for other view classes.
    """
    
    def __init__ (self, master, rows, cols, width, height,**kwargs):
        """
        A grid is constructed with the length and width of the grid in a
        root window. Also, there are some rows and columns in the grid.
        
        Parameters:
            master: The toplevel window.
            rows: The number of rows in the grid.
            cols: The number of columns in the grid.
            width: The width of the grid (in pixels).
            height: The height of the grid (in pixels).
            **kwargs: Any additional named arguments.
        """
        super().__init__(master)
        self._master = master
        self._rows = rows
        self._cols = cols
        self._width = width
        self._height = height
        
    def get_bbox(self, position: tuple) -> tuple:
        """
        Returns the bounding box for the (row, column) position; this is a tuple
        containing information about the pixel positions of the edges of the shape,
        in the form (x min, y min, x max, y max).

        Parameters:
            position: The position of top left corner of box.
        """
        x_min = position[0] * CELL_SIZE
        y_min = position[1] * CELL_SIZE
        x_max = x_min + self._width
        y_max = y_min + self._height
        return (x_min, y_min, x_max, y_max)
        
    def pixel_to_position(self, pixel: tuple) -> tuple:
        """
        Converts the (x, y) pixel position (in graphics units) to a
        (row, column) position.

        Parameters:
            pixel: (x, y) pixel position.
        """
        return (pixel[0] / CELL_SIZE, pixel[1] / CELL_SIZE)

    def get_position_center(self, position: tuple) -> tuple:
        """
        Gets the graphics coordinates for the center of
        the cell at the given (row, column) position.

        Parameters:
            position: The given (row, column) position.
        """
        x = (self.get_bbox(position)[0] + self.get_bbox(position)[2]) / 2
        y = (self.get_bbox(position)[1] + self.get_bbox(position)[3]) / 2
        return (x, y)

    def annotate_position(self, position: tuple, text: str) -> None:
        """
        Annotates the center of the cell at the given (row, column) position
        with the provided text.

        Parameters:
            position: The given (row, column) position.
            text: The provided text that should be Annotated.
        """
        row = self.get_position_center(position)[0]
        column = self.get_position_center(position)[1]
        
        # The color of fonts is white (player and hospital).
        if text == PLAYER or text == HOSPITAL:
            self.create_text(row, column, text = text, fill="White")
        else:
            self.create_text(row, column, text = text)


class BasicMap(AbstractGrid):
    """
    Entities are drawn on the map using coloured rectangles at different
    (row, column) positions.
    """
    
    def __init__(self, master, size):
        """
        Each rectangle should be 50 pixels high and 50 pixels wide.
        
        Parameters:
            master: The toplevel window.
            size: The number of rows (= number of columns) in the grid.  
        """
        super().__init__(master,size, size, CELL_SIZE,CELL_SIZE)
        self.config(width = size*CELL_SIZE, height = size*CELL_SIZE,\
                    bg = MAP_BACKGROUND_COLOUR)
        self._size = size
        
    def draw_entity(self, position: tuple, tile_type: str) -> None:
        """
        Draws the entity with tile type at the given position using a coloured
        rectangle with superimposed text identifying the entity.

        Parameters:
            position: the given position
            tile_type: the superimposed text
        """
        # get background color of entity
        for entity, color in ENTITY_COLOURS.items():
            if tile_type == entity:
                entity_color = color
                
        # create rectangle and add letter
        self.create_rectangle(self.get_bbox(position), fill = entity_color)
        self.annotate_position(position, tile_type)


class InventoryView(AbstractGrid):
    """
    Displays the items the player has in their inventory.
    """
    
    def __init__ (self, master, rows):
        """
        The rows should be set to the number of rows in the game map.

        Parameters:
            master: The toplevel window.
            rows: The size of game.
        """
        super().__init__(master, MAX_ITEMS, INVENTORY_COLS, \
                         INVENTORY_WIDTH, CELL_SIZE)
        self.config(width = INVENTORY_WIDTH, height = rows*CELL_SIZE,\
                    bg = LIGHT_PURPLE)
        self._master = master
        self._rows = rows
  
    def draw(self, inventory:Inventory) -> None:
        """
        Draw the inventory label and current items with their remaining
        lifetimes.

        Parameters:
            inventory: The inventory of holding player.
        """
        text_name=""  # the name of items in the inventory
        row = 0  # the row of items in the inventory view

        # delete the inventory view before 
        self.delete(tk.ALL)
        # create title of the inventory view
        self.create_text(105,20, text = INVENTORY_TITLE, \
                         width = INVENTORY_WIDTH, font = ("Purisa", 25))

        # get the name of items in the inventory
        for item in inventory.get_items():
            if isinstance(item,Crossbow):
                text_name="Crossbow"
            else:
                text_name="Garlic"
                
            # draw an 'Activated' item
            if item.is_active():
                # create rectangle with dark purple
                self.create_rectangle(0, 45+50*row, INVENTORY_WIDTH, \
                                      45+50*(row+1), fill = ACCENT_COLOUR )
                # draw the name of items
                self.create_text(70, 70+50*row, text = text_name, \
                                 width = INVENTORY_WIDTH, font = ("Purisa",15),\
                                 fill = "White")
                # draw the liftime of items
                self.create_text(165, 70+50*row, text = item.get_lifetime(),\
                                 width = INVENTORY_WIDTH, font = ("Purisa",15),\
                                 fill = "White")
                
            # draw 'Deactivated' items
            else:
                # draw the name of items
                self.create_text(70, 70+50*row, text = text_name, \
                                 width = INVENTORY_WIDTH, font = ("Purisa",15))
                # draw the liftime of items
                self.create_text(165, 70+50*row, text = item.get_lifetime(),\
                                 width = INVENTORY_WIDTH, font = ("Purisa",15))
            row += 1
            
    def toggle_item_activation(self, pixel:tuple, inventory:Inventory) -> None:
        """
        Activates or deactivates the item (if one exists) in the row containing
        the pixel.
        
        Parameters:
            pixel: the pixel of click.
            inventory: the inventory of holding player.
        """
        clicked_item = None  # a item that is clicked
        y = pixel[1]  # the y-position of click
        inventory_num = 0  # the position of a item in the inventory dictionary
        
        # get max y_position, according to the numbers of items in the inventory
        y_max = 35 + CELL_SIZE * (len(inventory.get_items()))  
        # get the position of clicked item in the inventory dictionary
        if y >=45 and y < y_max:
            while y-45 > 0:
                y -= CELL_SIZE
                inventory_num += 1
                
            # get a item that is clicked
            clicked_item = inventory.get_items()[inventory_num-1]
            # check if it's active
            if inventory.any_active() == False:
                clicked_item.toggle_active()
            else:
                if clicked_item.is_active():
                    clicked_item.toggle_active()

            
class BasicGraphicalInterface(object):
    """
    Manage the overall view (i.e. constructing the three major widgets)
    and event handling.
    """

    def __init__(self,root,size):
        """
        Draw the title label, and instantiate and pack the BasicMap
        and InventoryView.

        Parameters:
            root: the root window
            size: the number of rows (= number of columns) in the game map.
        """
        self._size = size
        self._root = root
        self._root.title(TITLE)
        
        # draw the title label
        self._title = tk.Label(self._root, text = TITLE, bg = DARK_PURPLE,\
                               fg = "white", font = ("Purisa", 35))
        self._title.pack(side = tk.TOP, expand = True, fill = tk.X)
        
        # instantiate and pack the BasicMap
        self._map = BasicMap(self._root, self._size)
        self._map.pack(side = tk.LEFT)
        
        # instantiate and pack InventoryView
        self._inventoryView = InventoryView(self._root, self._size)
        self._inventoryView.pack(side = tk.RIGHT)
       
    def active_inventory(self, game:AdvancedGame) -> None :
        """
        Bind left clicks and InventoryView together.

        Parameters:
            game: The current game.
        """
        inventory = game.get_player().get_inventory()
        self._inventoryView.bind("<Button-1>", lambda \
                                 event: self.inventory_click(event, inventory))           

    def inventory_click(self, event, inventory:Inventory) -> None:
        """
        Handle activating or deactivating the clicked item (if one exists)
        and update both the model and the view accordingly.

        Parameters:
            event: The (x, y) pixel position when left clicks.
            inventory: The current invntory in the game.
        """
        self._inventoryView.toggle_item_activation((event.x, event.y), inventory)
        self._inventoryView.draw(inventory)
    
    def draw(self, game:AdvancedGame) -> None:
        """
        Draw the view based on the current game state.

        Parameters:
            game: The current game.
        """
        grid = game.get_grid()
        # draw BasicMap
        for position,entity in grid.serialize().items():
            self._map.draw_entity(position, entity)
            
        # draw Inventoryview
        inventory = game.get_player().get_inventory()
        self._inventoryView.draw(inventory)

    def keyPress(self, game:AdvancedGame) -> None:
        """
        Bind keyboard, player moving and the direction of fire together.

        Parameters:
            game: The current game.
        """
        # bind keyboard and player moving together
        self._root.bind("w",lambda event:self.direction("w",game))
        self._root.bind("s",lambda event:self.direction("s",game))
        self._root.bind("a",lambda event:self.direction("a",game))
        self._root.bind("d",lambda event:self.direction("d",game))
        
        # bind keyboard and the direction of fire together
        self._root.bind('<Up>', lambda event: self.fire('<Up>', game))
        self._root.bind('<Down>', lambda event: self.fire('<Down>', game))
        self._root.bind('<Left>', lambda event: self.fire('<Left>', game))
        self._root.bind('<Right>', lambda event: self.fire('<Right>', game))
        
    def direction(self, event, game:AdvancedGame) -> None:
        """
        This method should be called when press 'w', 's', 'a', 'd'.
        And move player according to the direction.

        Parameters:
            event: 'w' or 's' or 'a' or 'd' pressed.
            game: The current game.
        """
        press_direction = ['w', 's', 'a', 'd']
        if event in press_direction:
            self.move(game, event)
 
    def move(self, game:AdvancedGame, direction:str) -> None:
        """
        Handles moving the player and redrawing the game.

        Parameters:
            direction: The direction of moving player.('w' or 's' or 'a' or 'd')
            game: The current game.
        """
        # clear the BasicMap before
        self._map.delete(tk.ALL)

        # get offest of direction
        x = 0
        y = 0
        if direction =="w":
            x = 0
            y = -1
        elif direction =="s":
            x = 0
            y = 1
        elif direction =="a":
            x = -1
            y = 0
        elif direction =="d":
            x = 1
            y = 0
            
        # move player
        game.move_player(Position(x,y))
        # redraw the BasicMap
        self.draw(game)
        
    def fire(self, event, game:AdvancedGame) -> None:
        """
        Instantiate the AdvancedTextInterface and handle the fire action
        according to the direction event.

        Parameters:
            event: '<Down>' or '<Up>' or '<Left>' or '<Right>' pressed.
            game: The current game.
        """
        # instantiate the AdvancedTextInterface
        text_interface = AdvancedTextInterface(game.get_grid())
        # handle the fire action
        if event=='<Up>': 
            text_interface.handle_action(game,UP)
        elif event=='<Down>':
            text_interface.handle_action(game,DOWN)
        elif event=='<Left>':
            text_interface.handle_action(game,LEFT)
        else :
            text_interface.handle_action(game,RIGHT)

    def step(self, game:AdvancedGame) -> None:
        """
        The step method is called every second. This method triggers the step
        method for the game and updates the view accordingly.

        Parameters:
            game: The current game.
        """
        play_again =''  # 'yes' or 'no'
        player_position = game.get_grid().find_player()
        game_mapping = game.get_grid().get_mapping()
        
        # call the step of player
        game.get_player().step(player_position,game)
        
        # call the step of zombies
        for position,entity in game_mapping.items():
            if isinstance(entity,Zombie):
                entity.step(position, game)

        # clear and redraw the BasicMap and InventoryView
        self._map.delete(tk.ALL)
        self._inventoryView.delete(tk.ALL)
        self.draw(game)
        # update every second
        self._mapRenew = self._map.after(1000, lambda: self.step(game))

        # win or lost   
        if game.has_won():
            play_again = tm.askquestion("play again",\
                                        WIN_MESSAGE+"\n play again?")
        elif game.has_lost():
            play_again = tm.askquestion("play again",\
                                        LOSE_MESSAGE+'\n'+"play again?")
        # play again or not
        if play_again =="yes":
            self.replay()   
        elif play_again =="no":
            self.quit()
            
    def replay(self) -> None:
        """
        Play a new game and end the last game.
        """
        # end the last game
        self._map.after_cancel(self._mapRenew)
        self._map.delete(tk.ALL)
        self._inventoryView.delete(tk.ALL)
        # play a new game
        new_game = advanced_game(MAP_FILE)
        self.play(new_game)

    def quit(self) -> None:
        """
        If not play again, quit the window.
        """
        self._root.destroy()
        
    def play(self, game:AdvancedGame) -> None:
        """
        Binds events and initialises gameplay.This method will need to be
        called on the instantiated BasicGraphicalInterface in main to
        commence gameplay.

        Parameters:
            game: The current game.
        """
        self.draw(game)
        self.active_inventory(game)
        self.keyPress(game)
        self.step(game)


# test Task 1 
def main() -> None:
    root = tk.Tk()
    gui = BasicGraphicalInterface(root,10)
    game = advanced_game(MAP_FILE)
    gui.play(game)
    root.mainloop()
    
    
if __name__ == "__main__":
    main()
        
