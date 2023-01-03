import pygame as pg

class Button:
    def __init__( self, coords : tuple, dim : tuple, color : tuple ):
        self.m_coords = coords
        self.m_dim    = dim 
        self.m_color, self.m_default_color = color, color
        self.m_active = True
        self.m_rect   = pg.Rect( coords[::-1], dim[::-1] )

    def display( self, window : pg.Surface ):
        pg.draw.rect( window, self.m_color, self.m_rect )

    def is_cursor_on( self ) -> bool:
        cursor_position = pg.mouse.get_pos()
        return True if self.m_active and self.m_rect.collidepoint( cursor_position ) else False
    
    def change_color( self, color : tuple ):
        self.m_color = color

    def deactivate( self ):
        self.m_active = False
        self.m_color  = ( 100, 100, 100 )

    def activate( self ):
        self.m_active = True
        self.m_color  = self.m_default_color
