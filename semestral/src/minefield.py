"""
__Module handling minefield__
Contains Minefield class itself with GameData class aswell
 - minefield class handles everything about minefield from creating
   the field to displaying the field and checking mouse button clicks
 - gamedata class just contains game data and runs game timer
"""
import time as t
import random as rd
import numpy as np
import pygame as pg
from src.tile import Tile
from src.utilities import OUT_OF_BOUNDS, FONT

class GameData:
    """Class representig game data and timer"""
    def __init__( self, mines : np.uint32, tokens : np.uint32 ):
        """
        Initializes class instance\n
        Args:
            mines (np.uint32): number of mines on the minefield
            tokens (np.uint32): number of powerup tokens on the minefield
        """
        self.m_cursor = OUT_OF_BOUNDS   # minefield cursor
        self.m_data = {                 # data regarding mines, flags and tokens
            'mines'  : mines,
            'flags'  : 0,
            'tokens' : tokens,
            'coll'   : 0
        }
        self.m_start_time = 0           # time of the game start
        self.m_time = 0                 # time
        self.m_t_running = False        # tells whether the timer is running

    def display( self, window : pg.Surface, offset : dict, colors : dict ):
        """
        Displays the number of mines left to flag, number of tokens and time\n
        Args:
            window (pg.Surface): pygame window/surface on which tile should display
            offset (dict): offset to display everything correctly
            colors (dict): colors
        """
        font = pg.font.Font( FONT, 17 )
        strings = []
        strings.append( f"FLAGS: { str( self.m_data['mines'] - self.m_data['flags'] ) }" )
        strings.append( f"TOKENS: { str( self.m_data['coll'] ) }" )
        strings.append( f"TIME: { str( self.m_time ) }" )

        height = offset['f'][0] + offset['t'][0]
        pg.draw.rect( window, colors['background'], pg.Rect( ( 45, height ), ( 130, 70 ) ) )
        for string in strings:
            text = font.render( string, True, colors['t_disabled'] )
            t_rect = text.get_rect()
            t_rect.topleft = ( 50, height )
            height += 20
            window.blit( text, t_rect )

    def start_timer( self ):
        """Starts the game timer"""
        self.m_t_running = True
        self.m_start_time = t.time()

    def stop_timer( self ):
        """Stops the game timer"""
        self.m_t_running = False
        self.m_start_time = t.time() - self.m_start_time

class Minefield:
    """Class representing the minefield"""
    def __init__( self, init_data : dict, offset : dict, colors : dict ):
        """
        Initializes class instance\n
        Args:
            init_data (dict): initial game settings
        """
        self.m_offset = offset
        self.m_colors = colors
        # numpy ndarray of Tile class instances
        self.m_field = self.__init_field( init_data['dim'], init_data['tile_dim'], offset['t'] )

        # surface under the field, to which tiles are displayed
        self.m_surface = self.__init_surface( init_data['dim'], init_data['tile_dim'], offset['t'] )
        self.m_mines = []   # list of mine coordinates

        # game data ( class GameData instance )
        self.m_game_data = GameData( init_data['mines'], init_data['tokens'] )

    @staticmethod
    def __init_field( dim : tuple, tile_dim : tuple, offset : tuple ) -> np.ndarray:
        """
        Creates 2D array of minefield tiles\n
        Args:
            dim (tuple): dimensions of minefield
            tile_dim (tuple): dimensions of one minefield tile
            offset (tuple): offset of tiles
        Returns:
            np.ndarray: 2D array of initialized class Tile instances
        """
        field = np.ndarray( dim, dtype = Tile )
        for t_idx, _ in np.ndenumerate( field ):
            tile_y = t_idx[0]*tile_dim[0] + offset[0]
            tile_x = t_idx[1]*tile_dim[1] + offset[1]
            field[t_idx] = Tile( ( tile_y, tile_x ), tile_dim )

        return field

    @staticmethod
    def __init_surface( dim : tuple, tile_dim : tuple, offset : tuple ) -> pg.Surface:
        """
        Creates pygame surface to which minefield tile will be displayed\n
        Args:
            dim (tuple): dimensions of minefield
            tile_dim (tuple): dimensions of one minefield tile
            offset (tuple): offset of tiles
        Returns:
            pg.Surface: pygame surface "under" the field
        """
        surf_y = dim[0]*tile_dim[0] + 2*offset[0]
        surf_x = dim[1]*tile_dim[1] + 2*offset[1]
        return pg.Surface( ( surf_x, surf_y ), pg.SRCALPHA )

    def height( self ) -> np.uint32:
        """Returns: np.uint32: height of field"""
        return self.m_field.shape[0]

    def width( self ) -> np.uint32:
        """Returns: np.uint32: width of field"""
        return self.m_field.shape[1]

    def dimensions( self ) -> tuple:
        """Returns: tuple: dimensions of field"""
        return self.m_field.shape

    def t_dimensions( self ) -> tuple:
        """Returns: tuple: dimensions of one field tile"""
        return self.m_field[0, 0].dimensions()

    def tokens( self ) -> np.uint32:
        """Returns: np.uint32: number of collected tokens"""
        return self.m_game_data.m_data['coll']

    def __hide_mines_and_tokens( self, c_start_click : tuple ):
        """
        Randomly scatters m mines and t tokens across the minefield\n
        ( m, t ... values given when creating instance )\n
        Args:
            c_start_click (tuple):  array coordinations of clicked tile
        """
        # first randomly generate m mine coordinates
        for _ in range( self.m_game_data.m_data['mines'] ):
            # making sure that tile on random coordinates doesn't already contains mine
            while True:
                c_mine = ( rd.randint( 0, self.height() - 1 ), rd.randint( 0, self.width() - 1 ) )
                if not self.m_field[c_mine].is_mine() and c_mine != c_start_click:
                    break

            self.m_field[c_mine].add_mine()
            for neighbor in self.__get_neighbors( c_mine ):
                neighbor.new_mine_neighbor()

            # adding coordinates to list of mines coords for better handling in other methods
            self.m_mines.append( c_mine )

        # then randomly generate t powerup tokens
        for _ in range( self.m_game_data.m_data['tokens'] ):
            # again making sure that tile on random coords doesn't already contains mine or token
            while True:
                c_token = ( rd.randint( 0, self.height() - 1 ), rd.randint( 0, self.width() - 1 ) )
                if not self.m_field[c_token].is_token() and not self.m_field[c_token].is_mine():
                    break

            self.m_field[c_token].add_token()

    def show_cursor( self, window : pg.Surface, color : tuple ):
        """
        Displays array cursor\n
        Args:
            window (pg.Surface): pygame window/surface to which display
            color (tuple): cursor color
        """
        # from mouse get field coordinates and create pygame
        # transparent surface on top of the window
        c_cursor = self.mouse_pos_to_coords( pg.mouse.get_pos() )
        surface = pg.Surface( window.get_size(), pg.SRCALPHA )

        # display field tile on last cursor position and then displays cursor on new position
        # if new cursor coords aren't the same as last or out of bounds
        if c_cursor not in ( OUT_OF_BOUNDS, self.m_game_data.m_cursor ):
            self.display_field( window, self.m_game_data.m_cursor )
            rect = self.m_field[c_cursor].tile_rect( self.m_offset['f'] )
            pg.draw.rect( surface, color, rect )
            window.blit( surface, ( 0, 0 ) )
            self.m_game_data.m_cursor = c_cursor

        # if cursor is out of bounds display field without it
        if c_cursor == OUT_OF_BOUNDS:
            self.display_field( window, self.m_game_data.m_cursor )
            window.blit( surface, ( 0, 0 ) )

    def display_game_data( self, window : pg.Surface, display: bool = False ):
        """
        Displays game data onto pygame window and updates time\n
        Args:
            window (pg.Surface): pygame window/surface to display on
            display (bool, optional): states whether to display even if the time is not running
                                      Defaults to False.
        """
        if self.m_game_data.m_t_running:
            self.m_game_data.display( window, self.m_offset, self.m_colors )
            self.m_game_data.m_time = int( t.time() - self.m_game_data.m_start_time )

        if display:
            self.m_game_data.display( window, self.m_offset, self.m_colors )

    def display_field( self, window : pg.Surface, c_tile : tuple = OUT_OF_BOUNDS ):
        """
        Displays minefield itself or just one tile ( used in show_cursor ) on the pygame window\n
        Args:
            window (pg.Surface): pygame window/surface to display on
            c_tile (tuple, optional): tile coordinates to display only that tile
                                      Defaults to OUT_OF_BOUNDS.
        """
        # if not given coordinates in method call display the whole minefield
        if c_tile == OUT_OF_BOUNDS:
            self.m_surface.fill( self.m_colors['t_disabled'] )
            for row in self.m_field:
                for tile in row:
                    tile.display( self.m_surface )
        else:
            # display only tile on given coordinates
            self.m_field[c_tile].display( self.m_surface )

        window.blit( self.m_surface, self.m_offset['f'][::-1] )
        #window.blit( self.m_surface, ( OFFSET['x'], OFFSET['y'] ) )
        self.display_game_data( window, True )

    def handle_click( self, button : np.uint32, mouse_pos : tuple ) -> bool:
        """
        Handles the mous click on tile ( left click - open tile, right click - flag tile ).
        If opened tile has mine, ends game with loss else checks if all safe tiles are open and
        ends game with win
        Args:
            button (np.uint32): mouse button
            mouse_pos (tuple): position of mouse
        Returns:
            bool: False if game ends no matter if won or lost
        """
        c_click = self.mouse_pos_to_coords( mouse_pos )

        if c_click != OUT_OF_BOUNDS:
            if button == 1 and not self.m_field[c_click].is_flag():
                if len( self.m_mines ) == 0:
                    self.m_game_data.start_timer()
                    self.__hide_mines_and_tokens( c_click )
                if not self.open( c_click ):
                    self.m_game_data.stop_timer()
                    self.m_field[c_click].boom()
                    self.open_mines()
                    return False
                if not self.open( c_click ) or self.__are_safe_tiles_open():
                    self.m_game_data.stop_timer()
                    self.open_mines()
                    return False
            if button == 3:
                if self.m_field[c_click].flag():
                    self.m_game_data.m_data['flags'] += 1
                else:
                    self.m_game_data.m_data['flags'] -= 1

        return True

    def __get_neighbors( self, c_tile : tuple ) -> np.array:
        """
        Creates and returns array of tile neighbors\n
        Args:
            c_tile (tuple): coordinates of tile, which neighbors we want
        Returns:
            np.array: 1D array of tile neighbors with itself
        """
        neighbors = self.m_field[
            max( c_tile[0] - 1, 0 ) : min( c_tile[0] + 2, self.height() ),
            max( c_tile[1] - 1, 0 ) : min( c_tile[1] + 2, self.width() ) ].flatten()

        return neighbors

    def __check_neighbors( self, c_tile : tuple ) -> str:
        """
        Checks if all neighbor tile mines are flaged correctly
        ( used to open neigbors, when clicked on already opened tile )\n
        Args:
            c_tile (tuple): coordinates of tile, which neighbors we checking
        Returns:
            str: 'open' if all neighbor mines are correctly flaged;
                 'boom' if number of flaged neighbors is same as number of mines,
                        but not all mines are correctly flaged;
                 'ok' if either opening or explosion doesn't take place
        """
        flaged, mines, flaged_mines = 0, 0, 0
        for neighbor in self.__get_neighbors( c_tile ):
            if neighbor.is_mine():
                mines += 1
            if neighbor.is_flag():
                flaged += 1
            if neighbor.is_mine() and neighbor.is_flag():
                flaged_mines += 1

        if flaged == mines:
            return 'open' if flaged_mines == mines else 'boom'

        return 'ok'

    def open( self, c_tile ) -> bool:
        """
        Opens the minefield tile. If tile has zero mines around, opens all connected
        "zero" tiles and their neighbors. If tile is already open, checks wheter all neigbor
        mines are correctly flaged and opens them or detonates mines\n
        Args:
            c_tile (_type_): coordinates of tile to open
        Returns:
            bool: False if mine was detonated
        """
        if self.m_field[c_tile].is_mine():
            return False

        if not self.m_field[c_tile].is_open():
            self.__flood_fill( c_tile )
        else:
            n_check = self.__check_neighbors( c_tile )
            if n_check == 'open':
                for neighbor in self.__get_neighbors( c_tile ):
                    if not neighbor.is_mine():
                        self.__flood_fill( neighbor.arr_coords( self.m_offset['t'] ) )
            elif n_check == 'boom':
                for neighbor in self.__get_neighbors( c_tile ):
                    if neighbor.is_mine():
                        neighbor.boom()

                return False

        return True

    def __flood_fill( self, c_tile : tuple ):
        """
        Opens all connected "zero" tiles and their neighbors by flood fill
        algorithm which is implemented iteratively as modified bfs\n
        Args:
            c_tile (tuple): coordinates of tile to start flood fill from
        """
        queue, visited = [], []
        queue.append( c_tile )
        visited.append( c_tile )

        if self.m_field[c_tile].is_open():
            return

        self.add_powerup_token( self.m_field[c_tile].open() )

        if self.m_field[c_tile].mines_around() != 0:
            for neighbor in self.__get_neighbors( c_tile ):
                if not neighbor.is_mine() and neighbor.mines_around() == 0:
                    queue.append( neighbor.arr_coords( self.m_offset['t'] ) )
                    visited.append( neighbor.arr_coords( self.m_offset['t'] ) )

        while queue:
            c_exam_tile = queue.pop( 0 )
            if self.m_field[c_exam_tile].mines_around() == 0:
                self.add_powerup_token( self.m_field[c_exam_tile].open() )
            else:
                continue

            for neighbor in self.__get_neighbors( c_exam_tile ):
                if not neighbor.arr_coords( self.m_offset['t'] ) in visited:
                    if self.__has_nomine_neighbor( neighbor.arr_coords( self.m_offset['t'] ) ):
                        self.add_powerup_token( neighbor.open() )
                    queue.append( neighbor.arr_coords( self.m_offset['t'] ) )
                    visited.append( neighbor.arr_coords( self.m_offset['t'] ) )

    def open_mines( self ):
        """Opens all tiles with mine"""
        for c_mine in self.m_mines:
            if self.m_field[c_mine].is_flag():
                self.m_field[c_mine].flag()
            self.m_field[c_mine].open()

    def __has_nomine_neighbor( self, c_tile : tuple ) -> bool:
        """
        Checks whether the tile has neighbor with zero mines around\n
        Args:
            c_tile (tuple): coordinates of tile to check
        Returns:
            bool: True if tile actually has neighbor with no mines around
        """
        for neighbor in self.__get_neighbors( c_tile ):
            if neighbor.mines_around() == 0:
                return True
        return False

    def __are_safe_tiles_open( self ) -> bool:
        """Returns: bool: True if all safe tiles are open"""
        for row in self.m_field:
            for tile in row:
                if not tile.is_open() and not tile.is_mine():
                    return False

        return True

    def mouse_pos_to_coords( self, mouse_pos : tuple ) -> tuple:
        """
        Transforms mouse cursor position into the array coordinates\n
        Args:
            mouse_pos (tuple): coordinates of mouse cursor
        Returns:
            tuple: array coordinates or OUT_OF_BOUNDS constant
        """
        mouse_pos = mouse_pos[::-1]
        f_offset = self.m_offset['f']
        t_offset = self.m_offset['t']
        col = ( mouse_pos[0] - f_offset[0] - t_offset[0] )//self.t_dimensions()[0]
        row = ( mouse_pos[1] - f_offset[1] - t_offset[1] )//self.t_dimensions()[1]
        if 0 <= col < self.height() and 0 <= row < self.width():
            return ( col, row )

        return OUT_OF_BOUNDS

    def no_bubbles( self ) -> bool:
        """Returns: bool: True if there is no bubble ( unopened zero tile ) in the field"""
        for row in self.m_field:
            for tile in row:
                if not tile.is_open() and not tile.is_mine() and tile.mines_around() == 0:
                    return False

        return True

    def add_powerup_token( self, how_much : int ):
        """
        Adds or subtracts powerup tokens\n
        Args:
            how_much (int): how much tokens to add/sub
        """
        self.m_game_data.m_data['coll'] += how_much
