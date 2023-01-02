import numpy as np
import pygame as pg
import random as rd
from tile import Tile

OFFSET_Y, OFFSET_X = 10, 20

class Minefield:
    def __init__( self, 
                  dim : tuple,
                  tile_dim : tuple, 
                  num_of_mines : np.uint32, 
                  window : pg.Surface ):

        self.m_dim = dim
        self.m_t_dim = tile_dim
        self.m_window = window
        self.m_field  = np.empty( [dim[0], dim[1]], dtype = Tile )
        self.m_mines  = []
        self.m_num_of_mines = num_of_mines

        for y in range( dim[0] ):
            for x in range( dim[1] ):
                self.m_field[y, x] = Tile( ( y*tile_dim[0] + OFFSET_Y, x*tile_dim[1] + OFFSET_X ), tile_dim )

    def height( self ) -> int:
        return self.m_dim[0]

    def width( self ) -> int:
        return self.m_dim[1]

    def dimensions( self ) -> tuple:
        return self.m_dim

    def hide_mines( self, start_click_coords : tuple ):
        for _ in range( self.m_num_of_mines ):
            while True:
                y, x = rd.randint( 0, self.height() - 1 ), rd.randint( 0, self.width() - 1 )
                if not self.m_field[y, x].is_mine() and ( x, y ) != start_click_coords:
                    break
            
            self.m_field[y, x].add_mine()
            for neighbor in self.get_neighbors( ( y, x ) ):
                neighbor.m_min_arnd += 1

            self.m_mines.append( ( y, x ) )

    def display_field( self ):
        for row in self.m_field:
            for tile in row:
                tile.display( self.m_window )

    def check_click( self, button ) -> str:
        for row in self.m_field:
            for tile in row:
                coords = tile.click()
                if coords != ( -1, -1 ):
                    break
            else:
                continue
            break
        
        if coords != ( -1, -1 ):
            if button == 1:
                if len( self.m_mines ) == 0:
                    self.hide_mines( coords )
                if not self.m_field[coords[0], coords[1]].is_flaged() and self.m_field[coords[0], coords[1]].is_mine():
                    self.show_mines()
                    return 'l'
                else:
                    if not self.open( coords ):
                        self.show_mines()
                        return 'l'
                if self.are_safe_tiles_open():
                    return 'w'
            if button == 3:
                self.m_field[coords[0], coords[1]].flag()

        return 'r'

    def get_neighbors( self, coords : tuple ) -> np.array:
        neighbors = self.m_field[
            max( coords[0] - 1, 0 ) : min( coords[0] + 2, self.height() ),
            max( coords[1] - 1, 0 ) : min( coords[1] + 2, self.width() ) ].flatten()
        return np.delete( neighbors, np.where( neighbors == Tile( ( coords[0]*self.m_t_dim[0] + OFFSET_X, coords[1]*self.m_t_dim[1] + OFFSET_Y ), self.m_t_dim ) ) )

    def open( self, coords ) -> bool:
        if not self.m_field[coords[0], coords[1]].is_flaged():
            if self.m_field[coords[0], coords[1]].open():
                self.flood_fill( coords )
            else:
                check = self.check_neighbors( coords )
                if check == 'open':
                    for neighbor in self.get_neighbors( coords ):
                        self.flood_fill( neighbor.arr_coords() )
                elif check == 'boom':
                    return False
        return True

    def flood_fill( self, coords ):
        if not self.m_field[coords[0], coords[1]].is_mine(): 
            self.m_field[coords[0], coords[1]].open()

        for neighbor in self.get_neighbors( coords ):
            if not neighbor.is_opened() and neighbor.m_min_arnd == 0:
                self.flood_fill( neighbor.arr_coords() )
            elif self.m_field[coords[0], coords[1]].m_min_arnd == 0 and not self.m_field[coords[0], coords[1]].is_mine():
                neighbor.open()

    def show_mines( self ):
        for mine in self.m_mines:
            self.m_field[mine[0], mine[1]].open()

    def are_safe_tiles_open( self ) -> bool:
        for row in self.m_field:
            for tile in row:
                if not tile.is_opened() and not tile.is_mine():
                    return False
        return True

    def check_neighbors( self, coords ) -> str:
        flaged, mines, flaged_mines = 0, 0, 0
        for neighbor in self.get_neighbors( coords ):
            if neighbor.is_mine():
                mines += 1
            if neighbor.is_flaged():
                flaged += 1 
            if neighbor.is_mine() and neighbor.is_flaged():
                flaged_mines += 1

        if flaged_mines == mines:
            return 'open'
        elif flaged == mines:
            return 'boom'

        return 'ok'