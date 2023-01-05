import random as rd
import numpy as np
import pygame as pg
from tile import Tile, OFFSET

OUT_OF_BOUNDS = ( -1, -1 )

def random_bool( prob : int ) -> bool:
    return rd.random() < prob

class GameData:
    def __init__( self, mines, tokens ):
        self.m_cursor = OUT_OF_BOUNDS
        self.m_status = 'r'
        self.m_mines, self.m_tokens = mines, tokens
        self.m_tokens_coll = 0

class Minefield:
    def __init__( self, init_data : dict ):
        dim, tile_dim = init_data['dim'], init_data['tile_dim']
        self.m_field = np.empty( [dim[0], dim[1]], dtype = Tile )
        for col in range( self.height() ):
            for row in range( self.width() ):
                tile_y = col*tile_dim[0] + OFFSET['t_y']
                tile_x = row*tile_dim[1] + OFFSET['t_x']
                self.m_field[col, row] = Tile( ( tile_y, tile_x ), tile_dim )

        self.m_surface = self.init_surface()
        self.m_mines = []
        self.m_field_data = GameData( init_data['mines'], init_data['tokens'] )

    def init_surface( self ) -> pg.Surface:
        surf_x = self.width()*self.tile_dimensions()[1] + 2*OFFSET['t_x']
        surf_y = self.height()*self.tile_dimensions()[0] + 2*OFFSET['t_y']
        return pg.Surface( ( surf_x, surf_y ), pg.SRCALPHA )

    def height( self ) -> int:
        return self.m_field.shape[0]

    def width( self ) -> int:
        return self.m_field.shape[1]

    def dimensions( self ) -> tuple:
        return self.m_field.shape

    def tile_dimensions( self ) -> tuple:
        return self.m_field[0, 0].dimensions()

    def status( self ) -> str:
        return self.m_field_data.m_status

    def tokens( self ) -> np.uint32:
        return self.m_field_data.m_tokens_coll

    def hide_mines_and_tokens( self, c_start_click : tuple ):
        for _ in range( self.m_field_data.m_mines ):
            while True:
                c_mine = ( rd.randint( 0, self.height() - 1 ), rd.randint( 0, self.width() - 1 ) )
                if not self.m_field[c_mine].is_mine() and c_mine != c_start_click:
                    break

            self.m_field[c_mine].add_mine()
            for neighbor in self.get_neighbors( c_mine ):
                neighbor.new_mine_neighbor()

            self.m_mines.append( c_mine )
        
        print( self.m_field_data.m_tokens )
        for _ in range( self.m_field_data.m_tokens ):
            while True:
                c_token = ( rd.randint( 0, self.height() - 1 ), rd.randint( 0, self.width() - 1 ) )
                if not self.m_field[c_token].is_mine() and not self.m_field[c_token].is_token():
                    break
            
            print( c_token )
            self.m_field[c_token].add_token()

    def show_cursor( self, window : pg.Surface, color : tuple = ( 255, 0, 0, 50 ) ):
        c_cursor = self.mouse_pos_to_coords( pg.mouse.get_pos() )
        surface = pg.Surface( window.get_size(), pg.SRCALPHA )
        if c_cursor not in ( OUT_OF_BOUNDS, self.m_field_data.m_cursor ):
            self.display_field( window, self.m_field_data.m_cursor )
            rect = self.m_field[c_cursor].m_rect
            pg.draw.rect( surface, color, rect )
            window.blit( surface, ( 0, 0 ) )
            self.m_field_data.m_cursor = c_cursor

        if c_cursor == OUT_OF_BOUNDS:
            self.display_field( window, self.m_field_data.m_cursor )
            window.blit( surface, ( 0, 0 ) )

    def display_field( self, window : pg.Surface, c_tile = OUT_OF_BOUNDS ):
        if c_tile == OUT_OF_BOUNDS:
            self.m_surface.fill( ( 100, 100, 100, 255 ) )
            for row in self.m_field:
                for tile in row:
                    tile.display( self.m_surface )
        else:
            self.m_surface.fill( ( 0, 0, 0, 0 ) )
            self.m_field[c_tile].display( self.m_surface )

        window.blit( self.m_surface, ( OFFSET['x'], OFFSET['y'] ) )

    def mouse_pos_to_coords( self, mouse_pos : tuple ) -> tuple:
        mouse_pos = mouse_pos[::-1]
        col = ( mouse_pos[0] - OFFSET['y'] - OFFSET['t_y'] )//self.tile_dimensions()[0]
        row = ( mouse_pos[1] - OFFSET['x'] - OFFSET['t_x'] )//self.tile_dimensions()[1]
        if 0 <= col < self.height() and 0 <= row < self.width():
            return ( col, row )

        return OUT_OF_BOUNDS

    def check_click( self, button : np.uint32, mouse_pos : tuple ):
        c_click = self.mouse_pos_to_coords( mouse_pos )

        if c_click != OUT_OF_BOUNDS:
            if button == 1 and not self.m_field[c_click].is_flag():
                if len( self.m_mines ) == 0:
                    self.hide_mines_and_tokens( c_click )
                if not self.open( c_click ):
                    self.open_mines()
                if self.are_safe_tiles_open():
                    self.m_field_data.m_status = 'w'
            if button == 3:
                self.m_field[c_click].flag()

    def get_neighbors( self, c_tile : tuple ) -> np.array:
        neighbors = self.m_field[
            max( c_tile[0] - 1, 0 ) : min( c_tile[0] + 2, self.height() ),
            max( c_tile[1] - 1, 0 ) : min( c_tile[1] + 2, self.width() ) ].flatten()

        tile_y = c_tile[0]*self.tile_dimensions()[0] + OFFSET['t_y']
        tile_x = c_tile[1]*self.tile_dimensions()[1] + OFFSET['t_x']
        neighbors = neighbors[ neighbors != Tile( ( tile_y, tile_x ), self.tile_dimensions() ) ]
        return neighbors

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

    def open( self, c_tile ) -> bool:
        if self.m_field[c_tile].is_mine():
            return False

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

        if self.m_field[c_tile].open():
            #self.m_field_data.m_tokens_coll += 1
            self.add_powerup_token( 1 )

        if self.m_field[c_tile].mines_around() != 0:
            for neighbor in self.get_neighbors( c_tile ):
                if not neighbor.is_mine() and neighbor.mines_around() == 0:
                    queue.append( neighbor.arr_coords() )
                    visited.append( neighbor.arr_coords() )

        while queue:
            c_exam_tile = queue.pop( 0 )
            if self.m_field[c_exam_tile].mines_around() == 0:
                if self.m_field[c_exam_tile].open():
                    #self.m_field_data.m_tokens_coll += 1
                    self.add_powerup_token( 1 )
            else:
                continue

            for neighbor in self.get_neighbors( c_exam_tile ):
                if not neighbor.arr_coords() in visited:
                    if self.has_nomine_neighbor( neighbor.arr_coords() ):
                        if neighbor.open():
                            #self.m_field_data.m_tokens_coll += 1
                            self.add_powerup_token( 1 )
                    queue.append( neighbor.arr_coords() )
                    visited.append( neighbor.arr_coords() )

    def open_mines( self ):
        self.m_field_data.m_status = 'l'
        for c_mine in self.m_mines:
            if self.m_field[c_mine].is_flag():
                self.m_field[c_mine].flag()
            self.m_field[c_mine].open()

    def has_nomine_neighbor( self, c_tile : tuple ) -> bool:
        for neighbor in self.get_neighbors( c_tile ):
            if neighbor.mines_around() == 0:
                return True
        return False

    def are_safe_tiles_open( self ) -> bool:
        for row in self.m_field:
            for tile in row:
                if not tile.is_open() and not tile.is_mine():
                    return False
        return True

    def add_powerup_token( self, how_much : int ):
        self.m_field_data.m_tokens_coll += how_much
