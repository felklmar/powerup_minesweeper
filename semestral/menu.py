"""
__Main ( and only )  menu__
Handles menu, that means it handles menu buttons,
game settings and starting or quiting game
"""
import copy
import pygame as pg
from button import Button
from utilities import HEIGHT, WIDTH, FONT, MIN, MAX, DEF_DIFFIC, DIFFIC, LOGO, OFFSET, COLORS

class Menu:
    """Class representing app/game menu"""
    def __init__( self, window : pg.Surface, def_diff : int = DEF_DIFFIC ):
        """
        Initializes class instance\n
        Args:
            window (pg.Surface): pygame window
            def_diff (int): defaul difficulty index
        """
        self.m_window = window
        self.m_font = pg.font.Font( FONT, 35 )
        self.m_deff_diff = def_diff

        y_off = OFFSET['m_y'] + LOGO.get_height() + 20
        x_off = 2*OFFSET['m_x']
        self.m_buttons = [
            Button( (   0 + y_off,   0 + x_off ), COLORS['t_disabled'],
                    ( self.m_font, 'start', 'start' ) ),

            Button( (  70 + y_off,   0 + x_off ), COLORS['t_disabled'],
                    ( self.m_font, 'mode', 'mode' ) ),

            Button( ( 120 + y_off,   0 + x_off ), COLORS['t_disabled'],
                    ( self.m_font, 'diffic', 'difficulty' ) ),

            Button( ( 340 + y_off,   0 + x_off ), COLORS['t_disabled'],
                    ( self.m_font, 'end', 'end' ) ),

            Button( ( 200 + y_off, 200 + x_off ), COLORS['t_disabled'],
                    ( self.m_font, 'h_<', '<' ) ),

            Button( ( 200 + y_off, 280 + x_off ), COLORS['t_disabled'],
                    ( self.m_font, 'h_>', '>' ) ),

            Button( ( 250 + y_off, 200 + x_off ), COLORS['t_disabled'],
                    ( self.m_font, 'w_<', '<' ) ),

            Button( ( 250 + y_off, 280 + x_off ), COLORS['t_disabled'],
                    ( self.m_font, 'w_>', '>' ) ),

            Button( ( 200 + y_off, 570 + x_off ), COLORS['t_disabled'],
                    ( self.m_font, 'm_<', '<' ) ),

            Button( ( 200 + y_off, 690 + x_off ), COLORS['t_disabled'],
                    ( self.m_font, 'm_>', '>' ) ),

            Button( ( 250 + y_off, 570 + x_off ), COLORS['t_disabled'],
                    ( self.m_font, 't_<', '<' ) ),

            Button( ( 250 + y_off, 690 + x_off ), COLORS['t_disabled'],
                    ( self.m_font, 't_>', '>' ) ),
        ]
        self.m_d_idx = def_diff
        self.m_game_settings = copy.deepcopy( DIFFIC[def_diff][1] )
        self.m_game_settings[3] = 0
        self.m_powerups = False

    def default( self ):
        """Sets all member variables to intialization values, except for buttons and font"""
        self.m_d_idx = self.m_deff_diff
        self.m_game_settings = copy.deepcopy( DIFFIC[self.m_deff_diff][1] )
        self.m_game_settings[3] = 0
        self.m_powerups = False
        self.m_window = pg.display.set_mode( ( WIDTH, HEIGHT ) )

    def height( self ) -> int:
        """Returns: int: the height of field"""
        return self.m_game_settings[0]

    def width( self ) -> int:
        """Returns: int: the width of field"""
        return self.m_game_settings[1]

    def mines( self ) -> int:
        """Returns: int: the number of mines that will be in game"""
        return self.m_game_settings[2]

    def tokens( self ) -> int:
        """Returns: int: the number of powerup tokens that will be in game"""
        return self.m_game_settings[3]

    def __display_text( self, to_display : str, coords : tuple, t_color : tuple ):
        """
        Displays given text onto the pygame window\n
        Args:
            to_display (str): text/string to display
            coords (tuple): coordinates telling where on the window text should be displayed
            color (tuple): color of text
        """
        text = self.m_font.render( to_display, True, t_color )
        t_rect = text.get_rect()
        t_rect.topleft = coords[::-1]
        self.m_window.blit( text, t_rect )

    def __settings_display( self ):
        """Displays game settings onto the pygame window"""
        y_off = OFFSET['m_y'] + LOGO.get_height() + 20
        x_off = 2*OFFSET['m_x']
        # height: its value
        self.__display_text( 'height:', ( 200 + y_off, 60 + x_off ), COLORS['t_disabled'] )
        self.__display_text( str( self.m_game_settings[0] ),
                             ( 200 + y_off, 225 + x_off ), COLORS['t_basic'] )

        # width: its value
        self.__display_text( 'width:', ( 250 + y_off, 60 + x_off ), COLORS['t_disabled'] )
        self.__display_text( str( self.m_game_settings[1] ),
                             ( 250 + y_off, 225 + x_off ), COLORS['t_basic'] )

        # mines: its value
        self.__display_text( 'mines:', ( 200 + y_off, 420 + x_off ), COLORS['t_disabled'] )
        self.__display_text( str( self.m_game_settings[2] ),
                             ( 200 + y_off, 595 + x_off ), COLORS['t_basic'] )

        # tokens: its value
        self.__display_text( 'tokens:', ( 250 + y_off, 420 + x_off ), COLORS['t_disabled'] )
        self.__display_text( str( self.m_game_settings[3] ),
                             ( 250 + y_off, 595 + x_off ), COLORS['t_basic'] )

    def __increase( self, event : pg.event, set_idx : int ):
        """
        Increases game settings value given by index\n
        ( left click += 1, right click += 5, scroll wheell press = maximum )\n
        Args:
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
        Decreases game settings value given by index\n
        ( left click -= 1, right click -= 5, scroll wheell press = minimum )\n
        Args:
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
        Handles the buttons changing game settings\n
        Args:
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
        x_off, y_off = OFFSET['m_x'], OFFSET['m_y']
        #self.m_window.blit( pg.transform.smoothscale( LOGO, ( 1072, 154 ) ), ( x_off, y_off ) )
        self.m_window.blit( LOGO, ( x_off, y_off ) )

        y_off += LOGO.get_height() + 20
        x_off = 2*OFFSET['m_x']
        # gamemode, classic or powerup
        mode_str = 'powerup' if self.m_powerups else 'classic'
        mode = self.m_font.render( mode_str, True, COLORS['t_basic'] )
        m_rect = mode.get_rect()
        m_rect.topleft = ( 140 + x_off, 70 + y_off )

        # game predefined difficulty
        diffc = self.m_font.render( DIFFIC[self.m_d_idx][0], True, COLORS['t_basic'] )
        d_rect = diffc.get_rect()
        d_rect.topleft = ( 205 + x_off, 120 + y_off )

        self.m_window.blit( mode, m_rect )
        self.m_window.blit( diffc, d_rect )

        # settings values and buttons
        self.__settings_display()
        for button in self.m_buttons:
            button.display( self.m_window )

    def click( self, event : pg.event ) -> str:
        """
        Handles the mouse click\n
        Args:
            event (pg.event): pygame event to determine which mouse button was triggered
        Returns:
            str: name of the pressed button to correctly check if button 'end' was pressed
        """
        for button in self.m_buttons:
            if event.type == pg.MOUSEBUTTONUP and button.is_cursor_on():
                if event.button == 1:
                    if button.name() == 'mode':
                        self.m_powerups = not self.m_powerups

                    if button.name() == 'diffic':
                        self.m_d_idx = self.m_d_idx + 1 if self.m_d_idx < 3 else 0

                    if button.name() in ( 'mode', 'diffic' ):
                        self.m_game_settings = copy.deepcopy( DIFFIC[self.m_d_idx][1] )
                        if not self.m_powerups:
                            self.m_game_settings[3] = 0

                    return button.name()

                self.__customization_buttons( event, button.name() )

        return 'none'
