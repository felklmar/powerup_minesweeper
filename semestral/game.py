import numpy as np
import pygame as pg
from powerups import SafeOpen, OpenBubble, CrossOpen, FlagRandom
from minefield import Minefield
from tile import OFFSET
from button import Button

NONE = -1

class Game:
    def __init__( self, powerups : bool, minefield_data : dict, window : pg.Surface ):
        self.m_powerups = np.array( [] )
        self.m_buttons  = np.array( [] )
        self.__init_buttons()
        if powerups:
            self.__init_powerups()
        self.m_minefield = Minefield( minefield_data )
        self.m_window = window
        self.m_curs_color = ( 255, 0, 0, 50 )
        self.m_active_powerup = NONE
        self.m_field_active = True
        self.m_tokens = 0
        width = self.m_minefield.width()*self.m_minefield.t_dimensions()[1]
        height = self.m_minefield.height()*self.m_minefield.t_dimensions()[0]
        w_offset = OFFSET['x'] + OFFSET['y'] + 2*OFFSET['t_x']
        h_offset = 2*( OFFSET['y'] + OFFSET['t_y'] )
        self.m_window = pg.display.set_mode( ( width + w_offset, height + h_offset ) )

    def __init_powerups( self ):
        self.m_powerups = [ SafeOpen(   ( 100, 15 ), ( 255, 255, 255 ), 1 ),
                            OpenBubble( ( 120, 15 ), ( 255, 255, 255 ), 2 ),
                            FlagRandom( ( 140, 15 ), ( 255, 255, 255 ), 2, 10 ),
                            CrossOpen(  ( 160, 15 ), ( 255, 255, 255 ), 3, 2 ) ]

    def __init_buttons( self ):
        btn_end = [ pg.font.Font( 'assets/Monocraft.otf', 17 ), 'end', '=>' ]
        btn_res = [ pg.font.Font( 'assets/Monocraft.otf', 17 ), 'res', '@>' ]
        self.m_buttons = [ Button( ( 15, 160 ), ( 255, 255, 255 ), btn_end ),
                           Button( ( 35, 160 ), ( 255, 255, 255 ), btn_res ) ]

    def __activate_powerups( self, token_amount ):
        for powerup in self.m_powerups:
            powerup.deactivate()
            powerup.activate( token_amount )

    def __pick_powerup( self, powerup_idx = NONE ):
        self.m_active_powerup = powerup_idx
        if powerup_idx != NONE:
            self.m_field_active = False
            for idx, i in enumerate( self.m_powerups ):
                if idx != powerup_idx:
                    i.deactivate()
                else:
                    i.change_color( ( 255, 255, 0 ) )
        else:
            self.m_field_active = True
            for i in self.m_powerups:
                i.activate( self.m_minefield.tokens() )

    def game_loop( self, event ) -> str:
        game_status = self.m_minefield.status()
        if self.m_minefield.tokens() != self.m_tokens:
            self.__activate_powerups( self.m_minefield.tokens() )
            self.m_tokens = self.m_minefield.tokens()

        if self.m_field_active:
            color = ( 255, 0, 0, 50 )
            if event.type == pg.MOUSEBUTTONUP:
                #print( self.m_tokens, self.m_minefield.tokens() )
                self.m_minefield.check_click( event.button, pg.mouse.get_pos() )
                self.m_minefield.display_field( self.m_window )
        else:
            color = ( 255, 255, 0, 100 )
            if event.type == pg.MOUSEBUTTONUP:
                powerup = self.m_powerups[self.m_active_powerup]
                if powerup.apply_powerup( self.m_window, self.m_minefield ):
                    self.m_minefield.add_powerup_token( -powerup.m_value )
                    self.__pick_powerup()

        self.m_minefield.show_cursor( self.m_window, color )
        for idx, i in enumerate( self.m_powerups ):
            i.display( self.m_window )
            if event.type == pg.MOUSEBUTTONUP and i.is_cursor_on():
                if i.m_color == i.m_default_color:
                    self.__pick_powerup( idx )
                else:
                    self.__pick_powerup()

        for btn in self.m_buttons:
            btn.display( self.m_window )
            if event.type == pg.MOUSEBUTTONUP and btn.is_cursor_on():
                if btn.name() == 'end':
                    game_status = 'l' 

        return game_status        