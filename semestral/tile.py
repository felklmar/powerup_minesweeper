"""
Module that represents one tile of minefield
--------------------------------------------
Contains dictionary TILES, which is used for pictures of tiles
and class Tile, which contains all necessary information
"""
import pygame as pg

"""offsets"""
OFFSET = {
    'x'   : 200,
    'y'   : 10,
    't_x' : 5,
    't_y' : 5
}

"""Dictionary for tile sprites"""
TILES = {
    'unopened' : pg.image.load( 'assets/unopened.svg' ),
    'flag' : pg.image.load( 'assets/flag.svg' ),
    'mine' : pg.image.load( 'assets/mine.jpeg' ),
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
        self.m_rect = pg.Rect( ( coords[1] + OFFSET['x'], coords[0] + OFFSET['y'] ), dim[::-1] )
        self.m_status = {
            'open'  : False,
            'flag'  : False,
            'mine'  : False,
            'token' : False
        }
        self.m_min_arnd = 0

    def __str__( self ) -> str:
        return f'coords = { self.m_coords }, status = { ( self.m_open, self.m_flag, self.m_mine ) }'

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
        if not self.is_open():
            if self.is_flag():
                win.blit(
                    pg.transform.scale( TILES['flag'], self.m_dim[::-1] ), self.m_coords[::-1] )
            else:
                win.blit(
                    pg.transform.scale( TILES['unopened'], self.m_dim[::-1] ), self.m_coords[::-1] )
        else:
            if self.is_mine():
                win.blit(
                    pg.transform.scale( TILES['mine'], self.m_dim[::-1] ), self.m_coords[::-1] )
            else:
                win.blit(
                    pg.transform.scale( TILES[str( self.m_min_arnd )], self.m_dim[::-1] ), self.m_coords[::-1] )

    def arr_coords( self ) -> tuple:
        col = ( self.m_coords[0] - OFFSET['t_y'] )//self.m_dim[0]
        row = ( self.m_coords[1] - OFFSET['t_x'] )//self.m_dim[1]
        return ( col, row )

    def dimensions( self ) -> tuple:
        return self.m_dim

    def is_mine( self ) -> bool:
        return self.m_status['mine']

    def is_token( self ) -> bool:
        return self.m_status['token']

    def is_open( self ) -> bool:
        return self.m_status['open']

    def is_flag( self ) -> bool:
        return self.m_status['flag']

    def mines_around( self ) -> int:
        return self.m_min_arnd

    def add_mine( self ):
        self.m_status['mine'] = True

    def add_token( self ):
        self.m_status['token'] = True

    def open( self ) -> bool:
        if not self.is_open() and not self.is_flag():
            self.m_status['open'] = True
            return self.m_status['token']

        return False

    def flag( self ) -> bool:
        if not self.is_open():
            self.m_status['flag'] = not self.m_status['flag']

        return self.is_flag()

    def new_mine_neighbor( self ):
        self.m_min_arnd += 1