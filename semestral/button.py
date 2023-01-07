"""
__Module handling button__
Contains class Button, which represents and controls one button
"""
import pygame as pg
from utilities import COLORS

class Button:
    """Class representing one onscreen button/choice"""
    def __init__( self, coords : tuple, color : tuple, text : tuple ):
        """
        Initializes Button class instance\n
        Args:
            coords (tuple): button coordinates
            color (tuple): button text color
            text (tuple): name and text on the button
        """
        self.m_coords = coords  # coordinates of button
        self.m_color = color    # button text color
        self.m_text = text      # button text and name

        # initialization of text rectangle ( pg.Rect )
        self.m_rect = text[0].render( text[2], True, (0,0,0) ).get_rect()
        self.m_rect.topleft = coords[::-1]

    def name( self ) -> str:
        """Returns: str: button name"""
        return self.m_text[1]

    def text( self ) -> str:
        """Returns: str: text on button"""
        return self.m_text[2]

    def display( self, window : pg.Surface ):
        """
        Displays button on given pygame window/surface\n
        Args:
            window (pg.Surface): pygame window/surface on which to display
        """
        text = self.m_text[0].render( self.m_text[2], True, self.m_color )
        text_rect = text.get_rect()
        text_rect.center = self.m_rect.center
        pg.draw.rect( window, COLORS['background'], self.m_rect )
        window.blit( text, text_rect )

    def is_cursor_on( self ) -> bool:
        """Returns: bool: True if mouse cursor is on the button"""
        return self.m_rect.collidepoint( pg.mouse.get_pos() )

    def change_color( self, color : tuple ):
        """
        Changes color of button text\n
        Args:
            color (tuple): color
        """
        self.m_color = color
