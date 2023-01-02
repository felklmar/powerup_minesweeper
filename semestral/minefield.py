import random as rd
import numpy as np
import pygame as pg
from tile import Tile, OFFSET

class Minefield:
    def __init__( self,
                  dim : tuple, tile_dim : tuple,
                  num_of_mines : np.uint32,
                  window : pg.Surface ):

        self.m_dim = dim
        self.m_t_dim  = tile_dim
        self.m_window = window
        self.m_rect   = pg.Rect(
                            ( OFFSET['x'], OFFSET['y'] ),
                            ( dim[1]*tile_dim[1] + 2*OFFSET['t_x'],
                              dim[0]*tile_dim[0] + 2*OFFSET['t_y'] ) )
        self.m_field  = np.empty( [dim[0], dim[1]], dtype = Tile )
        self.m_mines  = []
        self.m_num_of_mines = num_of_mines

        for y_idx in range( dim[0] ):
            for x_idx in range( dim[1] ):
                c_tile = ( y_idx*tile_dim[0] + OFFSET['t_y'], x_idx*tile_dim[1] + OFFSET['t_x'] )
                self.m_field[y_idx, x_idx] = Tile( c_tile, tile_dim )

    def height( self ) -> int:
        return self.m_dim[0]

    def width( self ) -> int:
        return self.m_dim[1]

    def dimensions( self ) -> tuple:
        return self.m_dim

    def hide_mines( self, c_start_click : tuple ):
        for _ in range( self.m_num_of_mines ):
            while True:
                c_mine = ( rd.randint( 0, self.height() - 1 ), rd.randint( 0, self.width() - 1 ) )
                if not self.m_field[c_mine].is_mine() and c_mine != c_start_click:
                    break

            self.m_field[c_mine].add_mine()
            for neighbor in self.get_neighbors( c_mine ):
                neighbor.m_min_arnd += 1

            self.m_mines.append( c_mine )

    def display_field( self ):
        surface = pg.Surface( self.m_rect.size )
        for row in self.m_field:
            for tile in row:
                tile.display( surface )

        self.m_window.blit( surface, ( OFFSET['x'], OFFSET['y'] ) )

    def check_click( self, button ) -> str:
        for row in self.m_field:
            for tile in row:
                c_click = tile.click()
                if c_click != ( -1, -1 ):
                    break
            else:
                continue
            break

        if c_click != ( -1, -1 ):
            if button == 1 and not self.m_field[c_click].is_flaged():
                if len( self.m_mines ) == 0:
                    self.hide_mines( c_click )
                if self.m_field[c_click].is_mine():
                    self.show_mines()
                    return 'l'
                if not self.open( c_click ):
                    self.show_mines()
                    return 'l'
                if self.are_safe_tiles_open():
                    return 'w'
            if button == 3:
                self.m_field[c_click].flag()

        return 'r'

    def get_neighbors( self, c_tile : tuple ) -> np.array:
        neighbors = self.m_field[
            max( c_tile[0] - 1, 0 ) : min( c_tile[0] + 2, self.height() ),
            max( c_tile[1] - 1, 0 ) : min( c_tile[1] + 2, self.width() ) ].flatten()
        tile_to_del = Tile( ( c_tile[0]*self.m_t_dim[0] + OFFSET['t_y'],
                              c_tile[1]*self.m_t_dim[1] + OFFSET['t_x'] ), self.m_t_dim )
        neighbors = neighbors[ neighbors != tile_to_del ]
        return neighbors

    def open( self, c_tile ) -> bool:
        if not self.m_field[c_tile].is_flaged():
            if not self.m_field[c_tile].is_opened():
                self.flood_fill( c_tile )
            else:
                n_check = self.check_neighbors( c_tile )
                if n_check == 'open':
                    for neighbor in self.get_neighbors( c_tile ):
                        if not neighbor.is_mine():
                            self.flood_fill( neighbor.arr_coords() )
                elif n_check == 'boom':
                    return False
        return True

    def flood_fill( self, c_tile : tuple ):
        queue, visited = [], []
        queue.append( c_tile )
        visited.append( c_tile )

        if self.m_field[c_tile].is_opened():
            return

        self.m_field[c_tile].open()

        if self.m_field[c_tile].m_min_arnd != 0:
            for neighbor in self.get_neighbors( c_tile ):
                if not neighbor.is_mine() and neighbor.m_min_arnd == 0:
                    queue.append( neighbor.arr_coords() )
                    visited.append( neighbor.arr_coords() )

        while queue:
            c_exam_tile = queue.pop( 0 )
            if self.m_field[c_exam_tile].m_min_arnd == 0:
                self.m_field[c_exam_tile].open()
            else:
                continue

            for neighbor in self.get_neighbors( c_exam_tile ):
                if not neighbor.arr_coords() in visited:
                    if self.has_nomine_neighbor( neighbor.arr_coords() ):
                        neighbor.open()
                    queue.append( neighbor.arr_coords() )
                    visited.append( neighbor.arr_coords() )

    def has_nomine_neighbor( self, c_tile : tuple ) -> bool:
        for neighbor in self.get_neighbors( c_tile ):
            if neighbor.m_min_arnd == 0:
                return True
        return False

    def show_mines( self ):
        for c_mine in self.m_mines:
            self.m_field[c_mine].open()

    def are_safe_tiles_open( self ) -> bool:
        for row in self.m_field:
            for tile in row:
                if not tile.is_opened() and not tile.is_mine():
                    return False
        return True

    def check_neighbors( self, c_tile : tuple ) -> str:
        flaged, mines, flaged_mines = 0, 0, 0
        for neighbor in self.get_neighbors( c_tile ):
            if neighbor.is_mine():
                mines += 1
            if neighbor.is_flaged():
                flaged += 1
            if neighbor.is_mine() and neighbor.is_flaged():
                flaged_mines += 1

        if flaged == mines:
            return 'open' if flaged_mines == mines else 'boom'

        return 'ok'
