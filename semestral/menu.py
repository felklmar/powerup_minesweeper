"""
__Main and only menu__
This module handles menu, that means it handles menu buttons,
game settings and starting or quiting game
"""
import copy
import pygame as pg
from button import Button
from utilities import HEIGHT, WIDTH, FONT, MIN, MAX, DEF_DIFF, DIFF

class Menu:
    """
    __Class representing and handling menu__
    Basically what is writen in module docstring on the top
    """
    def __init__( self, window : pg.Surface, def_diff : int = DEF_DIFF ):
        """
        __Constructor for class instance__
        Creates new instance and initialize everything required,
        that means buttons, font or game settings
        _Args:
            window (pg.Surface): pygame window
            def_diff (int): defaul difficulty index
        """
        self.m_window = window
        self.m_font = pg.font.Font( FONT, 35 )
        self.m_deff_diff = def_diff
        self.m_buttons = [
            Button( ( 100, 20 + 20 ), ( 50, 50, 50 ), [ self.m_font, 'start', 'start' ] ),
            Button( ( 170, 20 + 20 ), ( 50, 50, 50 ), [ self.m_font, 'mode', 'mode' ] ),
            Button( ( 220, 20 + 20 ), ( 50, 50, 50 ), [ self.m_font, 'diffc', 'difficulty' ] ),
            Button( ( 450, 20 + 20 ), ( 50, 50, 50 ), [ self.m_font, 'end', 'end' ] ),

            Button( ( 300, 180 + 20 ), ( 50, 50, 50 ), [ self.m_font, 'h_<', '<' ] ),
            Button( ( 300, 260 + 20 ), ( 50, 50, 50 ), [ self.m_font, 'h_>', '>' ] ),
            Button( ( 350, 180 + 20 ), ( 50, 50, 50 ), [ self.m_font, 'w_<', '<' ] ),
            Button( ( 350, 260 + 20 ), ( 50, 50, 50 ), [ self.m_font, 'w_>', '>' ] ),
            Button( ( 300, 550 + 20 ), ( 50, 50, 50 ), [ self.m_font, 'm_<', '<' ] ),
            Button( ( 300, 670 + 20 ), ( 50, 50, 50 ), [ self.m_font, 'm_>', '>' ] ),
            Button( ( 350, 550 + 20 ), ( 50, 50, 50 ), [ self.m_font, 't_<', '<' ] ),
            Button( ( 350, 670 + 20 ), ( 50, 50, 50 ), [ self.m_font, 't_>', '>' ] ),
        ]
        self.m_d_idx = def_diff
        self.m_game_settings = copy.deepcopy( DIFF[def_diff][1] )
        self.m_game_settings[3] = 0
        self.m_powerups = False

    def default( self ):
        """
        Sets all member variables to intialization values, except
        for buttons and font
        """
        self.m_d_idx = self.m_deff_diff
        self.m_game_settings = copy.deepcopy( DIFF[self.m_deff_diff][1] )
        self.m_game_settings[3] = 0
        self.m_powerups = False
        self.m_window = pg.display.set_mode( ( WIDTH, HEIGHT ) )

    def height( self ):
        """Returns the height of field"""
        return self.m_game_settings[0]

    def width( self ):
        """Returns the width of field"""
        return self.m_game_settings[1]

    def mines( self ):
        """Returns the number of mines that will be in game"""
        return self.m_game_settings[2]

    def tokens( self ):
        """Returns the number of powerup tokens that will be in game"""
        return self.m_game_settings[3]

    def __display_text( self, to_display : str, coords : tuple, color : tuple ):
        """
        Displays given text onto the pygame window
        _Args:
            to_display (str): text/string to display
            coords (tuple): coordinates telling where on the window text should be displayed
            color (tuple): color of text
        """
        text = self.m_font.render( to_display, True, color )
        t_rect = text.get_rect()
        t_rect.topleft = coords[::-1]
        self.m_window.blit( text, t_rect )

    def __settings_display( self ):
        """Displays game settings onto the pygame window"""

        # height: its value
        self.__display_text( 'height:', ( 300, 40 + 20 ), ( 50, 50, 50 ) )
        self.__display_text( str( self.m_game_settings[0] ), ( 300, 205 + 20 ), ( 255, 255, 255 ) )

        # width: its value
        self.__display_text( 'width:', ( 350, 40 + 20 ), ( 50, 50, 50 ) )
        self.__display_text( str( self.m_game_settings[1] ), ( 350, 205 + 20 ), ( 255, 255, 255 ) )

        # mines: its value
        self.__display_text( 'mines:', ( 300, 400 + 20 ), ( 50, 50, 50 ) )
        self.__display_text( str( self.m_game_settings[2] ), ( 300, 575 + 20 ), ( 255, 255, 255 ) )

        # tokens: its value
        self.__display_text( 'tokens:', ( 350, 400 + 20 ), ( 50, 50, 50 ) )
        self.__display_text( str( self.m_game_settings[3] ), ( 350, 575 + 20 ), ( 255, 255, 255 ) )

    def __increase( self, event : pg.event, set_idx : int ):
        """
        Increases game settings value given by index
        ( left click += 1, right click += 5, scroll wheell press = maximum )
        _Args:
            event (pg.event): pygame event to determine which mouse button was triggered
            set_idx (int): index of setting to increase ( height, width, mines or tokens )
        """
        height = self.height()
        width = self.width()
        mines = self.mines()
        tokens = self.tokens()

        if set_idx == 2:
            maximum = ( height - 1 )*( width - 1)
        elif set_idx == 3:
            maximum = ( height*width ) - mines
        else:
            maximum = MAX[set_idx]

        if event.button == 1:
            self.m_game_settings[set_idx] += 1
        if event.button == 2:
            self.m_game_settings[set_idx] = maximum
        if event.button == 3:
            self.m_game_settings[set_idx] += 5

        if self.m_game_settings[set_idx] > maximum:
            self.m_game_settings[set_idx] = maximum

        mines = self.mines()
        if tokens > ( ( height*width ) - mines ):
            self.m_game_settings[3] = ( height*width ) - mines

    def __decrease( self, event : pg.event, set_idx : int ):
        """
        Decreases game settings value given by index
        ( left click -= 1, right click -= 5, scroll wheell press = minimum )
        _Args:
            event (pg.event): pygame event to determine which mouse button was triggered
            set_idx (int): index of setting to decrease ( height, width, mines or tokens )
        """
        if event.button == 1:
            self.m_game_settings[set_idx] -= 1
        if event.button == 2:
            self.m_game_settings[set_idx] = MIN[set_idx]
        if event.button == 3:
            self.m_game_settings[set_idx] -= 5

        if self.m_game_settings[set_idx] < MIN[set_idx]:
            self.m_game_settings[set_idx] = MIN[set_idx]

    def __customization_buttons( self, event : pg.event, btn : str ):
        """
        Handles the buttons changing game settings
        _Args:
            event (pg.event): pygame event to determine which mouse button was triggered
            btn (str): button name to distinct the buttons
        """
        if btn == 'h_>':
            self.__increase( event, 0 )

        if btn == 'h_<':
            self.__decrease( event, 0 )

        if btn == 'w_>':
            self.__increase( event, 1 )

        if btn == 'w_<':
            self.__decrease( event, 1 )

        if btn == 'm_>':
            self.__increase( event, 2 )

        if btn == 'm_<':
            self.__decrease( event, 2 )

        if btn == 't_>':
            self.__increase( event, 3 )

        if btn == 't_<':
            self.__decrease( event, 3 )

    def display( self ):
        """Displays all the text and buttons on the pygame window"""
        # gamemode, classic or powerup
        mode_str = 'powerup' if self.m_powerups else 'classic'
        mode = self.m_font.render( mode_str, True, ( 255, 255, 255 ) )
        m_rect = mode.get_rect()
        m_rect.topleft = ( 150, 170 )

        # game predefined difficulty
        diffc = self.m_font.render( DIFF[self.m_d_idx][0], True, ( 255, 255, 255 ) )
        d_rect = diffc.get_rect()
        d_rect.topleft = ( 215, 220 )

        self.m_window.blit( mode, m_rect )
        self.m_window.blit( diffc, d_rect )

        # settings values and buttons
        self.__settings_display()
        for button in self.m_buttons:
            button.display( self.m_window )

    def click( self, event : pg.event ) -> str:
        """
        Handles the mouse click
        _Args:
            event (pg.event): pygame event to determine which mouse button was triggered
        _Returns:
            str: name of the pressed button to correctly check if button 'end' was pressed
        """
        for button in self.m_buttons:
            if event.type == pg.MOUSEBUTTONUP and event.button == 1 and button.is_cursor_on():
                if button.name() == 'mode':
                    self.m_powerups = not self.m_powerups

                if button.name() == 'diffc':
                    self.m_d_idx = self.m_d_idx + 1 if self.m_d_idx < 3 else 0

                if button.name() in ( 'mode', 'diffc' ):
                    self.m_game_settings = copy.deepcopy( DIFF[self.m_d_idx][1] )
                    if not self.m_powerups:
                        self.m_game_settings[3] = 0

                self.__customization_buttons( event, button.name() )
                return button.name()

        return 'none'
