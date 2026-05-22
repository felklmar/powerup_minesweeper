"""
__Module that represents one tile of minefield__
Contains class Tile, which represents and control one tile of the minefield
"""
import pygame as pg
from powerup_minesweeper.src.utilities import TILES

class Tile:
    """Class representing one tile of minefield"""
    def __init__( self, coords : tuple , dim : tuple ):
        """
        Initializes class instance\n
        Args:
            coords (tuple): tile coordinates ( y, x )
            dim (tuple): tile dimension ( tile is usually a square, but doesn't have to be )
        """
        self.m_coords = coords  # cooordinates of topleft sprite surface
        self.m_dim  = dim       # dimensions of tile
        self.m_status = {       # tile status
            'open'  : False,
            'flag'  : False,
            'mine'  : False,
            'boom'  : False,
            'token' : False
        }
        self.m_min_arnd = 0     # number of mines around the tile

    def __eq__( self, other ) -> bool:
        """Operator ==, returns true if tile coordinates are equal"""
        return self.m_coords == other.m_coords

    def display( self, win : pg.Surface ):
        """
        Displays the tile to given pygame window/surface\n
        Args:
            win (pg.Surface): pygame window/surface on which tile should display
        """
        if not self.is_open():
            if self.is_flag():
                self.__sprite_display( win, TILES['flag'] )
            else:
                self.__sprite_display( win, TILES['closed'] )
        else:
            if self.is_mine():
                if self.is_boom():
                    self.__sprite_display( win, TILES['boom'] )
                else:
                    self.__sprite_display( win, TILES['mine'] )
            else:
                self.__sprite_display( win, TILES[str( self.m_min_arnd )] )

    def __sprite_display( self, win : pg.Surface, sprite : pg.Surface ):
        """
        Displays tile sprite onto the pygame window\n
        Args:
            win (pg.Surface): window/surface on which to display
            sprite (pg.Surface): tile sprite ( image )
        """
        win.blit( pg.transform.smoothscale( sprite, self.m_dim[::-1] ), self.m_coords[::-1] )

    def arr_coords( self, t_offset : tuple ) -> tuple:
        """Returns:\n tuple: the tile coordinates in minefield array"""
        col = ( self.m_coords[0] - t_offset[0] )//self.m_dim[0]
        row = ( self.m_coords[1] - t_offset[1] )//self.m_dim[1]
        return ( col, row )

    def dimensions( self ) -> tuple:
        """Returns: tuple: the dimensions of tile"""
        return self.m_dim

    def tile_rect( self, f_offset : tuple ) -> pg.Rect:
        """Returns: pg.Rect: rectangle created using tile dimensions and coordinates"""
        y_coord = self.m_coords[0] + f_offset[0]
        x_coord = self.m_coords[1] + f_offset[1]
        return pg.Rect( ( x_coord, y_coord ), self.m_dim[::-1] )

    def is_mine( self ) -> bool:
        """Returns: bool: True if tile contains mine"""
        return self.m_status['mine']

    def is_boom( self ) -> bool:
        """Returns: bool: True if tiles mine is the detonated one"""
        return self.m_status['boom']

    def is_token( self ) -> bool:
        """Returns: bool: True if tile contains powerup token"""
        return self.m_status['token']

    def is_open( self ) -> bool:
        """Returns: bool: True if tile has been open"""
        return self.m_status['open']

    def is_flag( self ) -> bool:
        """Returns: bool: True if tile is flaged"""
        return self.m_status['flag']

    def mines_around( self ) -> int:
        """Returns: int: number of mines around the tile ( 0 - 8 )"""
        return self.m_min_arnd

    def add_mine( self ):
        """Adds mine to the tile"""
        self.m_status['mine'] = True

    def add_token( self ):
        """Adds powerup token to the tile"""
        self.m_status['token'] = True

    def boom( self ):
        """Detonates the mine"""
        self.m_status['boom'] = True

    def open( self ) -> bool:
        """
        Opens the tile\n
        Returns:
            bool: True if tile contains token
        """
        if not self.is_open() and not self.is_flag():
            self.m_status['open'] = True
            return self.m_status['token']

        return False

    def flag( self ) -> bool:
        """
        Flags the tile\n
        Returns:
            bool: True if tile was flaged and False if tile was unflaged
        """
        if not self.is_open():
            self.m_status['flag'] = not self.m_status['flag']

        return self.is_flag()

    def new_mine_neighbor( self ):
        """Increases the number of mines around the tile"""
        self.m_min_arnd += 1
