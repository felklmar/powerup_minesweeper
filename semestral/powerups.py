import random as rd
import pygame as pg
import numpy as np
from button import Button
from minefield import Minefield, OUT_OF_BOUNDS

class Powerup( Button ):
    def __init__( self, coords : tuple, dim : tuple, color : tuple ):
        super().__init__( coords, dim, color )

    def apply_powerup( self, minefield : Minefield ) -> bool:
        return False

class Safe_Open( Powerup ):
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

class Open_Bubble( Powerup ):
    def __init__( self, coords : tuple, dim : tuple, color : tuple ):
        super().__init__( coords, dim, color )

    def apply_powerup( self, minefield: Minefield ) -> bool:
        c_click = minefield.mouse_pos_to_coords( pg.mouse.get_pos() )
        if c_click != OUT_OF_BOUNDS:
            #self.find_bubble( minefield )
            #minefield.display_field()
            #return True

            check = 0
            while True:
                if check % minefield.m_field.size == 0:
                    if self.no_bubbles( minefield ):
                        break

                c_tile = ( rd.randint( 0, minefield.height() - 1 ), rd.randint( 0, minefield.width() - 1 ) )
                tile = minefield.m_field[c_tile]
                if not tile.is_open() and not tile.is_mine() and tile.mines_around() == 0:
                    minefield.open( c_tile )
                    minefield.display_field()
                    break

            return True

        return False

    def no_bubbles( self, minefield : Minefield ) -> bool:
        for row in minefield.m_field:
            for tile in row:
                if not tile.is_open() and not tile.is_mine() and tile.mines_around() == 0: 
                    return False

        return True

    #def find_bubble( self, minefield : Minefield ):
    #    rot_degree = rd.randint( 1, 4 )
    #    field = np.rot90( minefield.m_field, rot_degree )
    #    for row in field:
    #        for tile in row:
    #            if not tile.is_open() and not tile.is_mine() and tile.mines_around() == 0:
    #                minefield.open( tile.arr_coords() )
    #                return
