"""
Module that represents one tile of minefield
--------------------------------------------
Contains dictionary TILES, which is used for pictures of tiles
and class Tile, which contains all necessary information
"""
import pygame as pg

TILES = {
    'unopened' : pg.image.load( 'assets/unopened.svg' ),
    'flag' : pg.image.load( 'assets/flag.svg' ),
    'mine' : pg.image.load( 'assets/mine.svg' ),
    '0' : pg.image.load( 'assets/0.svg' ),
    '1' : pg.image.load( 'assets/1.svg' ),
    '2' : pg.image.load( 'assets/2.svg' ),
    '3' : pg.image.load( 'assets/3.svg' ),
    '4' : pg.image.load( 'assets/4.svg' ),
    '5' : pg.image.load( 'assets/5.svg' ),
    '6' : pg.image.load( 'assets/6.svg' ),
    '7' : pg.image.load( 'assets/7.svg' ),
    '8' : pg.image.load( 'assets/8.svg' )
}

class Tile:
    """Class representing one tile of minefield"""
    def __init__( self, coords : tuple , dim : tuple ):
        """
        Constructor for class instance
        ------------------------------

        Args:
            coords (tuple): tile coordinates ( y, x )
            dim (tuple): tile dimension ( tile is usually a square, but doesn't have to be )
        """
        self.m_coords = coords
        self.m_dim  = dim
        self.m_rect = pg.Rect( coords, dim )
        self.m_open = False
        self.m_flag = False
        self.m_mine = False
        self.m_min_arnd = 0

    def __eq__( self, other ) -> bool:
        """Operator ==, returns true if tile coordinates are equal"""
        return self.m_coords == other.m_coords

    def display( self, win : pg.Surface ):
        """
        Displays the tile to given pygame window/surface
        ------------------------------------------------
        - uses TILES dictionary to display right sprites/pictures

        Args:
            win (pg.Surface): pygame window/surface on which tile should display
        """
        if not self.m_open:
            if self.m_flag:
                win.blit(
                    pg.transform.scale( TILES['flag'], self.m_dim ), self.m_coords )
            else:
                win.blit(
                    pg.transform.scale( TILES['unopened'], self.m_dim ), self.m_coords )
        else:
            if self.m_mine:
                win.blit(
                    pg.transform.scale( TILES['mine'], self.m_dim ), self.m_coords )
            else:
                win.blit(
                    pg.transform.scale( TILES[str( self.m_min_arnd )], self.m_dim ), self.m_coords )

    def click( self ) -> tuple:
        cursor_position = pg.mouse.get_pos()
        print( self.m_rect, cursor_position )
        if self.m_rect.collidepoint( cursor_position ):
            return self.arr_coords()

        return ( -1, -1 )

    def arr_coords( self ) -> tuple:
        return ( self.m_coords[0]//self.m_dim[0], self.m_coords[1]//self.m_dim[1] )

    def is_mine( self ) -> bool:
        return self.m_mine

    def is_opened( self ) -> bool:
        return self.m_open

    def is_flaged( self ) -> bool:
        return self.m_flag

    def add_mine( self ):
        self.m_mine = True

    def open( self ) -> bool:
        if not self.m_open and not self.m_flag:
            self.m_open = True
            return True

        return False

    def flag( self ):
        self.m_flag = not self.m_flag
