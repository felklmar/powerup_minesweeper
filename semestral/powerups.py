import random as rd
import pygame as pg
import numpy as np
from button import Button
from minefield import Minefield, OUT_OF_BOUNDS

def random_bool( prob : int ) -> bool:
    return rd.random() < prob

class Powerup( Button ):
    def __init__( self, coords : tuple, color : tuple, description : list, value = 0 ):
        text = [ pg.font.Font( 'assets/Monocraft.otf', 17 ), description[0][0], description[0][1]  ]
        super().__init__( coords, color, text )

        self.m_description = description
        self.m_last_coords = OUT_OF_BOUNDS
        self.m_value = value
        self.deactivate()

    def __str__( self ) -> str:
        return self.m_description

    def deactivate( self ):
        self.m_color  = ( 100, 100, 100 )

    def activate( self, tokens ):
        if tokens >= self.m_value:
            self.m_color = self.m_default_color

class SafeOpen( Powerup ):
    def __init__( self, coords : tuple, color : tuple, value ):
        description = [ [ 'SafeOpen', 'SafeOpen' ] , 'without risk reveal one tile' ]
        super().__init__( coords, color, description, value )

    def apply_powerup( self, window : pg.Surface, minefield: Minefield ) -> bool:
        #print( self )
        c_click = minefield.mouse_pos_to_coords( pg.mouse.get_pos() )
        if c_click != OUT_OF_BOUNDS:
            tile = minefield.m_field[c_click]
            if not tile.is_flag():
                if tile.is_mine():
                    tile.flag()
                else:
                    minefield.open( tile.arr_coords() )

            minefield.display_field( window )
            return True

        return False

class OpenBubble( Powerup ):
    def __init__( self, coords : tuple, color : tuple, value ):
        description = [ [ 'OpenBubble', 'OpenBubble' ], 'Reveals random bubble, if there is one' ]
        super().__init__( coords, color, description, value )

    def apply_powerup( self, window : pg.Surface, minefield: Minefield ) -> bool:
        #print( self )
        c_click = minefield.mouse_pos_to_coords( pg.mouse.get_pos() )
        if c_click != OUT_OF_BOUNDS:
            check = 0
            while True:
                if check % minefield.m_field.size == 0:
                    if minefield.no_bubbles():
                        break
                check += 1

                col = rd.randint( 0, minefield.height() - 1 )
                row = rd.randint( 0, minefield.width() - 1 )
                c_tile = ( col, row )

                tile = minefield.m_field[c_tile]
                if not tile.is_open() and not tile.is_mine() and tile.mines_around() == 0:
                    minefield.open( c_tile )
                    minefield.display_field( window )
                    break

            return True

        return False

class CrossOpen( Powerup ):
    def __init__( self, coords : tuple, color : tuple, value, cross_range ):
        description = [ [ 'CrossOpen', 'CrossOpen' ], 'safely reveals tiles in a cross shape' ]
        super().__init__( coords, color, description, value )
        self.m_range = cross_range

    def apply_powerup( self, window : pg.Surface, minefield: Minefield ) -> bool:
        #print( self )
        c_click = minefield.mouse_pos_to_coords( pg.mouse.get_pos() )
        if c_click != OUT_OF_BOUNDS:
            field_dim = minefield.dimensions()

            min_y = max( 0, c_click[0] - self.m_range )
            max_y = min( field_dim[1], c_click[0] + self.m_range + 1 )

            min_x = max( 0, c_click[1] - self.m_range )
            max_x = min( field_dim[1], c_click[1] + self.m_range + 1 )

            #print( c_click, min_y, max_y, min_x, max_x )
            col = minefield.m_field[ min_y : max_y, c_click[1] ]
            row = minefield.m_field[ c_click[0], min_x : max_x ]

            #col = minefield.m_field[ 0 : field_dim[0], c_click[1] ]
            #row = minefield.m_field[ c_click[0], 0 : field_dim[1] ]
            cross = np.append( col, row )
            for tile in cross:
                if not tile.is_flag():
                    if tile.is_mine():
                        tile.flag()
                    else:
                        #tile.open()
                        minefield.open( tile.arr_coords() )

            minefield.display_field( window )
            return True

        return False

class FlagRandom( Powerup ):
    def __init__( self, coords : tuple, color : tuple, value, mines : np.uint32 ):
        description = [ [ 'FlagRandom', 'FlagRandom' ], 'flags random mines' ]
        super().__init__( coords, color, description, value )
        self.m_mines = mines

    def apply_powerup( self, window : pg.Surface, minefield: Minefield ) -> bool:
        #print( self )
        c_click = minefield.mouse_pos_to_coords( pg.mouse.get_pos() )
        if c_click != OUT_OF_BOUNDS:
            non_flaged_mines = []
            for mine in minefield.m_mines:
                if not minefield.m_field[mine].is_flag():
                    non_flaged_mines.append( minefield.m_field[mine] )

            if len( non_flaged_mines ) > self.m_mines:
                indexes = rd.sample( range( 0, len( non_flaged_mines ) ), self.m_mines )
                for idx in indexes:
                    non_flaged_mines[idx].flag()

            boom_chance = random_bool( 0.1 )
            if boom_chance:
                minefield.open_mines()
                minefield.m_status = 'l'

            minefield.display_field( window )
            return True

        return False
