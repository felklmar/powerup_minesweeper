import numpy as np
import pygame as pg
import random as rd
from tile import *

class Minefield:
    def __init__( self,
                  dim : tuple, tile_dim : tuple,
                  num_of_mines : np.uint32,
                  window : pg.Surface ):

        self.m_dim = dim
        self.m_t_dim  = tile_dim
        self.m_window = window
        self.m_rect   = pg.Rect( ( OFFSET['x'], OFFSET['y'] ), ( dim[1]*tile_dim[1] + 2*OFFSET['t_x'], dim[0]*tile_dim[0] + 2*OFFSET['t_y'] ) )
        self.m_field  = np.empty( [dim[0], dim[1]], dtype = Tile )
        self.m_mines  = []
        self.m_num_of_mines = num_of_mines

        for y in range( dim[0] ):
            for x in range( dim[1] ):
                tile_coords = ( y*tile_dim[0] + OFFSET['t_y'], x*tile_dim[1] + OFFSET['t_x'] )
                self.m_field[y, x] = Tile( tile_coords, tile_dim )

    def height( self ) -> int:
        return self.m_dim[0]

    def width( self ) -> int:
        return self.m_dim[1]

    def dimensions( self ) -> tuple:
        return self.m_dim

    def hide_mines( self, start_click_coords : tuple ):
        for _ in range( self.m_num_of_mines ):
            while True:
                y_idx, x_idx = rd.randint( 0, self.height() - 1 ), rd.randint( 0, self.width() - 1 )
                if not self.m_field[y_idx, x_idx].is_mine() and ( y_idx, x_idx ) != start_click_coords:
                    break
            
            self.m_field[y_idx, x_idx].add_mine()
            for neighbor in self.get_neighbors( ( y_idx, x_idx ) ):
                neighbor.m_min_arnd += 1

            self.m_mines.append( ( y_idx, x_idx ) )

    def display_field( self ):
        surface = pg.Surface( self.m_rect.size ) 
        for row in self.m_field:
            for tile in row:
                tile.display( surface )

        self.m_window.blit( surface, ( OFFSET['x'], OFFSET['y'] ) )

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
            if button == 1 and not self.m_field[coords[0], coords[1]].is_flaged():
                if len( self.m_mines ) == 0:
                    self.hide_mines( coords )
                if self.m_field[coords[0], coords[1]].is_mine():
                    self.show_mines()
                    return 'l'
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
        tile_to_del = Tile( ( coords[0]*self.m_t_dim[0] + OFFSET['t_y'], coords[1]*self.m_t_dim[1] + OFFSET['t_x'] ), self.m_t_dim )
        neighbors = neighbors[ neighbors != tile_to_del ]
        return neighbors

    def open( self, coords ) -> bool:
        if not self.m_field[coords[0], coords[1]].is_flaged():
            if not self.m_field[coords[0], coords[1]].is_opened():
                self.bfs_flood_fill( coords )
            else:
                check = self.check_neighbors( coords )
                if check == 'open':
                    for neighbor in self.get_neighbors( coords ):
                        self.bfs_flood_fill( neighbor.arr_coords() )
                elif check == 'boom':
                    return False
        return True

    #def flood_fill( self, coords ):
    #    if not self.m_field[coords[0], coords[1]].is_mine():
    #        self.m_field[coords[0], coords[1]].open()
    #
    #    for neighbor in self.get_neighbors( coords ):
    #        if neighbor.arr_coords() != coords:
    #            if not neighbor.is_opened() and neighbor.m_min_arnd == 0:
    #                self.flood_fill( neighbor.arr_coords() )
    #            elif self.m_field[coords[0], coords[1]].m_min_arnd == 0 and not self.m_field[coords[0], coords[1]].is_mine():
    #                neighbor.open()

    def bfs_flood_fill( self, coords ):
        queue, visited = [], []
        queue.append( coords )
        visited.append( coords )

        self.m_field[coords[0], coords[1]].open()

        if self.m_field[coords[0], coords[1]].m_min_arnd != 0:
            for neighbor in self.get_neighbors( coords ):
                if not neighbor.is_mine() and neighbor.m_min_arnd == 0:
                    queue.append( neighbor.arr_coords() )
                    visited.append( neighbor.arr_coords() )

        while queue:
            s = queue.pop( 0 )
            if self.m_field[s[0], s[1]].m_min_arnd == 0:
                self.m_field[s[0], s[1]].open()
            else:
                continue

            for neighbor in self.get_neighbors( s ):
                if not neighbor.arr_coords() in visited: 
                    if self.has_nomine_neighbor( neighbor.arr_coords() ):
                        neighbor.open()
                    queue.append( neighbor.arr_coords() )
                    visited.append( neighbor.arr_coords() )

    def has_nomine_neighbor( self, coords ) -> bool:
        for neighbor in self.get_neighbors( coords ):
            if neighbor.m_min_arnd == 0:
                return True
        return False

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
