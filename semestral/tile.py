import pygame as pg

UNOPENED = pg.image.load( 'assets/unopened.svg' )
FLAG = pg.image.load( 'assets/flag.svg' )

class Tile:
    def __init__( self, x = 1, y = 1, size = 10 ):
        self.m_x, self.m_y = x, y
        self.m_size = size
        self.m_opened = False
        self.m_flaged = False
        self.m_mine   = False
        self.m_mines_around = 0

    def __str__( self ):
        return "tile"

    def display( self, window ):
        window.blit( pg.transform.scale( UNOPENED, ( self.m_size, self.m_size ) ), ( self.m_y, self.m_x ) )

    def contains_mine( self ) -> bool:
        return self.m_mine

    def is_opened( self ) -> bool:
        return self.m_opened