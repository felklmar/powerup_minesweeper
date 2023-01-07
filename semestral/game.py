import numpy as np
import pygame as pg
from powerups import SafeOpen, OpenBubble, CrossOpen, FlagRandom
from minefield import Minefield
from button import Button
from utilities import OFFSET, NO_POWERUP, COLORS, FONT

class Game:
    def __init__( self, powerups : bool, minefield_data : dict, window : pg.Surface ):
        self.m_powerups = np.array( [] )
        self.m_buttons  = np.array( [] )
        self.m_minefield_data = minefield_data
        self.m_minefield = Minefield( minefield_data )
        self.m_window = window
        self.m_active_powerup = NO_POWERUP
        self.m_status = 'r'
        width = self.m_minefield.width()*self.m_minefield.t_dimensions()[1]
        height = self.m_minefield.height()*self.m_minefield.t_dimensions()[0]
        w_offset = OFFSET['x'] + 4*OFFSET['t_x']
        h_offset = OFFSET['y'] + 4*OFFSET['t_x']
        self.m_window = pg.display.set_mode( ( width + w_offset, height + h_offset ) )
        self.__init_buttons()
        if powerups:
            self.__init_powerups()

    def __init_powerups( self ):
        #height = self.m_window.get_height()/2
        height = OFFSET['y'] + OFFSET['t_y'] + 80
        self.m_powerups = [ SafeOpen(   ( height, 50 ), ( 255, 255, 255 ), 1 ),
                            OpenBubble( ( height + 25, 50 ), ( 255, 255, 255 ), 2 ),
                            FlagRandom( ( height + 50, 50 ), ( 255, 255, 255 ), 2, 10 ),
                            CrossOpen(  ( height + 75, 50 ), ( 255, 255, 255 ), 3, 2 ) ]

    def __init_buttons( self ):
        btn_end = [ pg.font.Font( FONT, 17 ), 'end', 'E' ]
        btn_res = [ pg.font.Font( FONT, 17 ), 'res', 'R' ]
        #height = self.m_window.get_height()/2
        height = OFFSET['y'] + OFFSET['t_y']
        self.m_buttons = [ Button( ( height, 15 ), ( 255, 255, 255 ), btn_end ),
                           Button( ( height + 20, 15 ), ( 255, 255, 255 ), btn_res ) ]

    def __reset( self ):
        self.m_active_powerup = NO_POWERUP
        self.m_status = 'r'
        self.m_minefield = Minefield( self.m_minefield_data )
        if self.m_powerups:
            self.__init_powerups()

    def __activate_powerups( self, token_amount ):
        for powerup in self.m_powerups:
            powerup.deactivate()
            powerup.activate( token_amount )

    def __pick_powerup( self, powerup_idx = NO_POWERUP ):
        self.m_active_powerup = powerup_idx
        if powerup_idx != NO_POWERUP:
            for idx, i in enumerate( self.m_powerups ):
                if idx != powerup_idx:
                    i.deactivate()
                else:
                    i.display_description( self.m_window )
                    i.change_color( ( 255, 255, 0 ) )
        else:
            self.m_active_powerup = NO_POWERUP
            self.__activate_powerups( self.m_minefield.tokens() )

    def __handle_powerups( self, event ):
        clear_surf = pg.Surface( ( self.m_window.get_width(), OFFSET['y'] ) )
        clear_surf.fill( COLORS['background'] )
        self.m_window.blit( clear_surf, ( 0, 0 ) )

        for idx, i in enumerate( self.m_powerups ):
            i.display( self.m_window )

            if i.is_cursor_on():
                i.display_description( self.m_window )

            if event.type == pg.MOUSEBUTTONUP and event.button == 1 and i.is_cursor_on():
                if i.m_color == i.m_default_color:
                    self.__pick_powerup( idx )
                else:
                    self.__pick_powerup()

    def __handle_buttons( self, event ) -> bool:
        for btn in self.m_buttons:
            btn.display( self.m_window )
            if event.type == pg.MOUSEBUTTONUP and event.button == 1 and btn.is_cursor_on():
                if btn.name() == 'end':
                    self.m_minefield.m_field_data.stop_timer()
                    return False
                if btn.name() == 'res':
                    self.__reset()

        return True

    def game_loop( self, event ) -> bool:
        if self.m_status == 'r':
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
