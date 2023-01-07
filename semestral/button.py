import pygame as pg
from utilities import COLORS

class Button:
    def __init__( self, coords : tuple, color : tuple, text : tuple ):
        self.m_coords = coords
        self.m_color, self.m_default_color = color, color
        text_render = text[0].render( text[2], True, (0,0,0) )
        self.m_rect = text_render.get_rect()
        self.m_rect.topleft = coords[::-1]
        #self.m_rect = pg.Rect( coords[::-1], dim[::-1] )
        #self.m_text = text['font'].render(text['text'], False, self.m_color )
        self.m_text = text

    def name( self ) -> str:
        return self.m_text[1]

    def text( self ) -> str:
        return self.m_text[2]

    def display( self, window : pg.Surface ):
        text = self.m_text[0].render( self.m_text[2], True, self.m_color )
        text_rect = text.get_rect()
        text_rect.center = self.m_rect.center
        #self.m_rect.size = ( text_rect.size[0] + 5, text_rect.size[1] + 5 )  
        pg.draw.rect( window, COLORS['background'], self.m_rect )
        window.blit( text, text_rect )

    def is_cursor_on( self ) -> bool:
        return self.m_rect.collidepoint( pg.mouse.get_pos() )
        #cursor_position = pg.mouse.get_pos()
        #return True if self.m_active and self.m_rect.collidepoint( cursor_position ) else False
    
    def change_color( self, color : tuple ):
        self.m_color = color
