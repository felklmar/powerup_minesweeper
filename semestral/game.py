"""
__Game instance__
Handles one game instance, from its start to the end. Game end can be reached by multiple ways,
one of them is end or reset button which this module also handle.
"""
import pygame as pg
from powerups import SafeOpen, OpenBubble, CrossOpen, FlagRandom
from minefield import Minefield
from button import Button
from utilities import OFFSET, NO_POWERUP, COLORS, FONT

class Game:
    """Same description as in module docstring"""
    def __init__( self, settings : dict ):
        """
        __Constructor for class instance__\n
        Creates new instance and initialize everything required,
        that means game window, minefield, powerups and buttons\n
        Args:
            settings (dict): game setings ( size of minefield, number of mines and tokens )
        """
        self.m_status = True                        # game status ( T - running or F - win/loss )
        self.m_settings = settings                  # game settings data
        self.m_minefield = Minefield( settings )    # minefield
        self.m_active_powerup = NO_POWERUP          # index of currently picked to use powerup

        # pygame window
        self.m_window = self.__init_window( settings['dim'], settings['tile_dim'] )

        # intialization of powerups and buttons ( both member variables are tuple )
        self.m_powerups = self.__init_powerups() if settings['tokens'] else ()
        self.m_buttons = self.__init_buttons()

    @staticmethod
    def __init_window( field_dim : tuple, tile_dim : tuple ) -> pg.Surface:
        """
        Initializes app/game window\n
        Args:
            field_dim (tuple): dimensions of minefield
            tile_dim (tuple): dimensions of a minefield tile
        Returns:
            pg.Surface: pygame window, with size according to arguments
        """
        height = field_dim[0]*tile_dim[0] + OFFSET['y'] + 4*OFFSET['t_x']
        width  = field_dim[1]*tile_dim[1] + OFFSET['x'] + 4*OFFSET['t_x']
        return pg.display.set_mode( ( width, height ) )

    @staticmethod
    def __init_powerups() -> tuple:
        """
        Initializes powerups\n
        Returns:
            tuple: tuple of powerups
        """
        height = OFFSET['y'] + OFFSET['t_y'] + 80
        return ( SafeOpen(   ( height     , 50 ), COLORS['t_basic'], 1     ),
                 OpenBubble( ( height + 25, 50 ), COLORS['t_basic'], 2     ),
                 FlagRandom( ( height + 50, 50 ), COLORS['t_basic'], 2, 10 ),
                 CrossOpen(  ( height + 75, 50 ), COLORS['t_basic'], 3,  2 ) )

    @staticmethod
    def __init_buttons() -> tuple:
        """
        Initializes buttons\n
        Returns:
            tuple: tuple of buttons
        """
        btn_end = [ pg.font.Font( FONT, 17 ), 'end', 'E' ]
        btn_res = [ pg.font.Font( FONT, 17 ), 'res', 'R' ]
        height = OFFSET['y'] + OFFSET['t_y']
        return ( Button( ( height     , 15 ), COLORS['t_basic'], btn_end ),
                 Button( ( height + 20, 15 ), COLORS['t_basic'], btn_res ) )

    def __reset( self ):
        """Resets the game to default values"""
        self.m_active_powerup = NO_POWERUP
        self.m_status = True
        self.m_minefield = Minefield( self.m_settings )
        self.m_powerups = self.__init_powerups() if self.m_powerups else ()

    def __activate_powerups( self, token_amount : int ):
        """
        Activates powerups if player has enough tokens to buy them\n
        Args:
            token_amount (int): token amount
        """
        for powerup in self.m_powerups:
            powerup.deactivate()
            powerup.activate( token_amount )

    def __pick_powerup( self, powerup_idx : int = NO_POWERUP ):
        """
        Picks/selects the powerup that will be used\n
        Args:
            powerup_idx (int, optional): powerup index. Defaults to NO_POWERUP.
        """
        self.m_active_powerup = powerup_idx
        if powerup_idx != NO_POWERUP:
            for p_idx, powerup in enumerate( self.m_powerups ):
                if p_idx != powerup_idx:
                    powerup.deactivate()
                else:
                    powerup.display_description( self.m_window )
                    powerup.change_color( COLORS['t_highlight'] )
        else:
            self.m_active_powerup = NO_POWERUP
            self.__activate_powerups( self.m_minefield.tokens() )

    def __handle_powerups( self, event : pg.event ):
        """
        Handles powerups selecting by determining mouse position and button click\n
        Args:
            event (pg.event): pygame event to get mouse button click
        """
        clear_surf = pg.Surface( ( self.m_window.get_width(), OFFSET['y'] ) )
        clear_surf.fill( COLORS['background'] )
        self.m_window.blit( clear_surf, ( 0, 0 ) )

        for p_idx, powerup in enumerate( self.m_powerups ):
            powerup.display( self.m_window )

            if powerup.is_cursor_on():
                powerup.display_description( self.m_window )

            if event.type == pg.MOUSEBUTTONUP and event.button == 1 and powerup.is_cursor_on():
                if powerup.m_color == COLORS['t_basic']:
                    self.__pick_powerup( p_idx )
                else:
                    self.__pick_powerup()

    def __handle_buttons( self, event ) -> bool:
        """
        Handles game buttons by determining mouse position and button click\n
        Args:
            event (pg.event): pygame event to get mouse button click
        Returns:
            bool: False if end button was pressed otherwise True
        """
        for btn in self.m_buttons:
            btn.display( self.m_window )
            if event.type == pg.MOUSEBUTTONUP and event.button == 1 and btn.is_cursor_on():
                if btn.name() == 'end':
                    self.m_minefield.m_field_data.stop_timer()
                    return False

                if btn.name() == 'res':
                    self.__reset()

        return True

    def game_loop( self, event : pg.event ) -> bool:
        """
        Manages the game loop\n
        Args:
            event (pg.event): pygame event to determine if and what mouse button was pressed
        Returns:
            bool: return value of method __handle_buttons ( True if game is still running )
        """
        if self.m_status:
            if self.m_minefield.tokens() and self.m_active_powerup == NO_POWERUP:
                self.__activate_powerups( self.m_minefield.tokens() )

            if self.m_active_powerup == NO_POWERUP:
                color = COLORS['cursor']
                if event.type == pg.MOUSEBUTTONUP:
                    self.m_status = self.m_minefield.check_click( event.button, pg.mouse.get_pos() )
                    self.m_minefield.display_field( self.m_window )
            else:
                color = COLORS['pow_cursor']
                if event.type == pg.MOUSEBUTTONUP:
                    powerup = self.m_powerups[self.m_active_powerup]
                    usage = powerup.apply_powerup( self.m_window, self.m_minefield )
                    if usage in ( 'applied', 'used' ):
                        if usage == 'applied':
                            self.m_minefield.add_powerup_token( -powerup.m_value )
                        self.__pick_powerup()

            self.m_minefield.show_cursor( self.m_window, color )
            self.__handle_powerups( event )

        return self.__handle_buttons( event )
