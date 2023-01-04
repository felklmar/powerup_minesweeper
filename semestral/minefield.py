import random as rd
import numpy as np
import pygame as pg
from tile import Tile, OFFSET

OUT_OF_BOUNDS = ( -1, -1 )

class Minefield:
    def __init__( self,
                  dim : tuple, tile_dim : tuple,
                  num_of_mines : np.uint32,
                  window : pg.Surface ):

        self.m_dim = dim
        self.m_t_dim  = tile_dim
        self.m_window = window
        self.m_surface = pg.Surface( ( dim[1]*tile_dim[1] + 2*OFFSET['t_x'],
                                       dim[0]*tile_dim[0] + 2*OFFSET['t_y'] ), pg.SRCALPHA )
        self.m_field  = np.empty( [dim[0], dim[1]], dtype = Tile )
        self.m_mines  = []
        self.m_num_of_mines = num_of_mines
        self.m_last_coords = OUT_OF_BOUNDS

        for y_idx in range( dim[0] ):
            for x_idx in range( dim[1] ):
                c_tile = ( y_idx*tile_dim[0] + OFFSET['t_y'], x_idx*tile_dim[1] + OFFSET['t_x'] )
                self.m_field[y_idx, x_idx] = Tile( c_tile, tile_dim )

    def height( self ) -> int:
        return self.m_field.shape[0]

    def width( self ) -> int:
        return self.m_field.shape[1]

    def dimensions( self ) -> tuple:
        return self.m_field.shape

    def hide_mines( self, c_start_click : tuple ):
        for _ in range( self.m_num_of_mines ):
            while True:
                c_mine = ( rd.randint( 0, self.height() - 1 ), rd.randint( 0, self.width() - 1 ) )
                if not self.m_field[c_mine].is_mine() and c_mine != c_start_click:
                    break

            self.m_field[c_mine].add_mine()
            for neighbor in self.get_neighbors( c_mine ):
                neighbor.new_mine_neighbor()

            self.m_mines.append( c_mine )

    def show_cursor( self, color : tuple = ( 255, 0, 0, 50 ) ):
        c_cursor = self.mouse_pos_to_coords( pg.mouse.get_pos() )
        surface = pg.Surface( self.m_window.get_size(), pg.SRCALPHA )
        if c_cursor != OUT_OF_BOUNDS and c_cursor != self.m_last_coords:
            self.display_field( self.m_last_coords )
            rect = self.m_field[c_cursor].m_rect
            pg.draw.rect( surface, color, rect )            
            self.m_window.blit( surface, ( 0, 0 ) )
            self.m_last_coords = c_cursor
        
        if c_cursor == OUT_OF_BOUNDS:
            self.display_field( self.m_last_coords )
            self.m_window.blit( surface, ( 0, 0 ) )

    def display_field( self, coords = OUT_OF_BOUNDS ):
        if coords == OUT_OF_BOUNDS:
            self.m_surface.fill( ( 100, 100, 100, 255 ) )
            for row in self.m_field:
                for tile in row:
                    tile.display( self.m_surface )
        else:
            self.m_surface.fill( ( 0, 0, 0, 0 ) )
            self.m_field[coords].display( self.m_surface )
        
        self.m_window.blit( self.m_surface, ( OFFSET['x'], OFFSET['y'] ) )

    def mouse_pos_to_coords( self, mouse_pos : tuple ) -> tuple:
        mouse_pos = mouse_pos[::-1]
        y = ( mouse_pos[0] - OFFSET['y'] - OFFSET['t_y'] )//self.m_t_dim[0]
        x = ( mouse_pos[1] - OFFSET['x'] - OFFSET['t_x'] )//self.m_t_dim[1] 
        return ( y, x ) if 0 <= y < self.m_dim[0] and 0 <= x < self.m_dim[1] else OUT_OF_BOUNDS

    def check_click( self, button : np.uint32, mouse_pos : tuple ) -> str:
        c_click = self.mouse_pos_to_coords( mouse_pos )

        if c_click != OUT_OF_BOUNDS:
            if button == 1 and not self.m_field[c_click].is_flag():
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
        if not self.m_field[c_tile].is_open():
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

        if self.m_field[c_tile].is_open():
            return

        self.m_field[c_tile].open()

        if self.m_field[c_tile].mines_around() != 0:
            for neighbor in self.get_neighbors( c_tile ):
                if not neighbor.is_mine() and neighbor.mines_around() == 0:
                    queue.append( neighbor.arr_coords() )
                    visited.append( neighbor.arr_coords() )

        while queue:
            c_exam_tile = queue.pop( 0 )
            if self.m_field[c_exam_tile].mines_around() == 0:
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
            if neighbor.mines_around() == 0:
                return True
        return False

    def show_mines( self ):
        for c_mine in self.m_mines:
            self.m_field[c_mine].open()

    def are_safe_tiles_open( self ) -> bool:
        for row in self.m_field:
            for tile in row:
                if not tile.is_open() and not tile.is_mine():
                    return False
        return True

    def check_neighbors( self, c_tile : tuple ) -> str:
        flaged, mines, flaged_mines = 0, 0, 0
        for neighbor in self.get_neighbors( c_tile ):
            if neighbor.is_mine():
                mines += 1
            if neighbor.is_flag():
                flaged += 1
            if neighbor.is_mine() and neighbor.is_flag():
                flaged_mines += 1

        if flaged == mines:
            return 'open' if flaged_mines == mines else 'boom'

        return 'ok'
