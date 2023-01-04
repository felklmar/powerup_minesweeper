import numpy as np
import pygame as pg
from powerups import Powerup, SafeOpen, OpenBubble, CrossOpen, FlagRandom
from minefield import Minefield

NONE = -1

class Game:
    def __init__( self,
                  powerups : bool,
                  minefield_data : dict,
                  window : pg.Surface ):

        self.m_powerups = np.array( [] )
        if powerups: 
            self.init_powerups()
        self.m_minefield = Minefield( minefield_data )
        self.m_window = window
        self.m_curs_color = ( 255, 0, 0, 50 )
        self.m_active_powerup = NONE
        self.m_field_active = True
        self.m_tokens = 0

    def init_powerups( self ):
        self.m_powerups = [ SafeOpen( ( 20, 100 ), ( 50, 50 ), ( 255, 0, 0 ) ),
                            OpenBubble( ( 20, 160 ), ( 50, 50 ), ( 0, 0, 255 ) ),
                            CrossOpen( ( 20, 220 ), ( 50, 50 ), ( 255, 0, 255 ) ),
                            FlagRandom( ( 20, 280 ), ( 50, 50 ), ( 255, 100, 0 ), 100 ) ]

    def activate_powerups( self, token_amount ):
        for powerup in self.m_powerups:
            powerup.deactivate()
            powerup.activate( token_amount )

    def pick_powerup( self, powerup_idx = NONE ):
        self.m_active_powerup = powerup_idx
        if powerup_idx != NONE:
            self.m_field_active = False
            for idx, i in enumerate( self.m_powerups ):
                if idx != powerup_idx:
                    i.deactivate()
                else:
                    i.change_color( ( 0, 255, 0 ) )
        else:
            self.m_field_active = True
            for i in self.m_powerups:
                i.activate( self.m_minefield.tokens() )

    def game_loop( self, event ) -> str:
        game_status = self.m_minefield.status()
        print( self.m_tokens, self.m_minefield.tokens() )
        if self.m_minefield.tokens() != self.m_tokens:
            self.activate_powerups( self.m_minefield.tokens() )
            self.m_tokens = self.m_minefield.tokens()

        if self.m_field_active:
            color = ( 255, 0, 0, 50 )
            if event.type == pg.MOUSEBUTTONUP:
                self.m_minefield.check_click( event.button, pg.mouse.get_pos() )
                self.m_minefield.display_field( self.m_window )
        else:
            color = ( 255, 255, 0, 100 )
            if event.type == pg.MOUSEBUTTONUP: 
                if self.m_powerups[self.m_active_powerup].apply_powerup( self.m_window, self.m_minefield ):
                    self.m_minefield.add_powerup_token( -self.m_powerups[self.m_active_powerup].m_value )
                    self.pick_powerup()

        self.m_minefield.show_cursor( self.m_window, color )
        for idx, i in enumerate( self.m_powerups ):
            i.display( self.m_window )
            if event.type == pg.MOUSEBUTTONUP and i.is_cursor_on():
                if i.m_color == i.m_default_color:
                    self.pick_powerup( idx )
                else:
                    self.pick_powerup()

        if event.type == pg.VIDEORESIZE:
            self.m_window.fill( (255,255,255) )
            self.m_minefield.display_field( self.m_window )

        return game_status        