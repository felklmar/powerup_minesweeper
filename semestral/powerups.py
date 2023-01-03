import pygame as pg
from button import Button
from minefield import Minefield, OUT_OF_BOUNDS

class Powerup( Button ):
    def __init__( self, coords : tuple, dim : tuple, color : tuple ):
        super().__init__( coords, dim, color )

    def apply_powerup( self, minefield : Minefield ) -> bool:
        return False

class Safe_open( Powerup ):
    def __init__( self, coords : tuple, dim : tuple, color : tuple ):
        super().__init__( coords, dim, color )

    def apply_powerup( self, minefield: Minefield ) -> bool:
        c_click = minefield.mouse_pos_to_coords( pg.mouse.get_pos() )
        if c_click != OUT_OF_BOUNDS:
            tile = minefield.m_field[c_click]
            if tile.is_mine():
                minefield.m_field[ c_click ].flag()
            else:
                minefield.m_field[ c_click ].open()

            minefield.display_field()    
            return True

        return False
        