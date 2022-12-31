import pygame as pg

TILES = {
    "unopened" : pg.image.load( 'assets/unopened.svg' ),
    "flag"     : pg.image.load( 'assets/flag.svg'     ),
}

class Tile:
    def __init__( self, x = 1, y = 1, size = 10 ):
        self.m_x, self.m_y = x, y
        self.m_size = size
        self.m_rect = pg.Rect( ( y, x ), ( size, size ) )
        self.m_opened = False
        self.m_flaged = False
        self.m_mine   = False
        self.m_mines_around = 0

    def __eq__( self, other ) -> bool:
        return self.m_x == other.m_x and self.m_y == other.m_y

    def display( self, window ):
        if not self.m_opened:
            if self.m_flaged:
                window.blit(
                    pg.transform.scale( TILES['flag'], ( self.m_size, self.m_size ) ),
                    ( self.m_y, self.m_x ) )
            else:
                window.blit(
                    pg.transform.scale( TILES['unopened'], ( self.m_size, self.m_size ) ),
                    ( self.m_y, self.m_x ) )        
    
    def click( self, button ) -> tuple:
        cursor_position = pg.mouse.get_pos() 
        if self.m_rect.collidepoint( cursor_position ):
            return self.arr_coords()

        return ( -1, -1 )
    
    def arr_coords( self ) -> tuple:
        return ( self.m_x//self.m_size, self.m_y//self.m_size )

    def contains_mine( self ) -> bool:
        return self.m_mine

    def is_opened( self ) -> bool:
        return self.m_opened

    def is_mine( self ):
        self.m_mine = True

    def open( self ) -> bool:
        if not self.m_opened:
            self.m_opened = True
            return True

        return False
