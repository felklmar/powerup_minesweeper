import random as rd
import numpy as np
import pygame as pg
import time as t
from tile import Tile
from utilities import OFFSET, OUT_OF_BOUNDS, COLORS, FONT

class GameData:
    def __init__( self, mines, tokens ):
        self.m_cursor = OUT_OF_BOUNDS
        self.m_status = 'r'
        self.m_data = {
            'mines'  : mines,
            'flags'  : 0,
            'tokens' : tokens,
            'coll'   : 0
        }
        self.m_start_time = 0
        self.m_time = 0
        self.m_running = False

    def display( self, window : pg.Surface ):
        font = pg.font.Font( FONT, 17 )
        strings = []
        strings.append( f"FLAGS: { str( self.m_data['mines'] - self.m_data['flags'] ) }" )
        strings.append( f"TOKENS: { str( self.m_data['coll'] ) }" )
        strings.append( f"TIME: { str( self.m_time ) }" )
        #height = window.get_height()/2 - 80
        height = OFFSET['y'] + OFFSET['t_y']
        pg.draw.rect( window, COLORS['background'], pg.Rect( ( 45, height ), ( 130, 70 ) ) )
        for string in strings:
            text = font.render( string, True, COLORS['text'] ) 
            t_rect = text.get_rect()
            t_rect.topleft = ( 50, height )
            height += 20
            window.blit( text, t_rect )

    def start_timer( self ):
        self.m_running = True
        self.m_start_time = t.time()

    def stop_timer( self ):
        self.m_running = False
        self.m_start_time = t.time() - self.m_start_time

class Minefield:
    def __init__( self, init_data : dict ):
        dim, tile_dim = init_data['dim'], init_data['tile_dim']
        self.m_field = np.empty( [dim[0], dim[1]], dtype = Tile )
        for col in range( self.height() ):
            for row in range( self.width() ):
                tile_y = col*tile_dim[0] + OFFSET['t_y']
                tile_x = row*tile_dim[1] + OFFSET['t_x']
                self.m_field[col, row] = Tile( ( tile_y, tile_x ), tile_dim )

        self.m_surface = self.__init_surface()
        self.m_mines = []
        self.m_field_data = GameData( init_data['mines'], init_data['tokens'] )

    def __init_surface( self ) -> pg.Surface:
        surf_x = self.width()*self.t_dimensions()[1] + 2*OFFSET['t_x']
        surf_y = self.height()*self.t_dimensions()[0] + 2*OFFSET['t_y']
        return pg.Surface( ( surf_x, surf_y ), pg.SRCALPHA )

    def height( self ) -> int:
        return self.m_field.shape[0]

    def width( self ) -> int:
        return self.m_field.shape[1]

    def dimensions( self ) -> tuple:
        return self.m_field.shape

    def t_dimensions( self ) -> tuple:
        return self.m_field[0, 0].dimensions()

    def status( self ) -> str:
        return self.m_field_data.m_status

    def tokens( self ) -> np.uint32:
        return self.m_field_data.m_data['coll']

    def hide_mines_and_tokens( self, c_start_click : tuple ):
        for _ in range( self.m_field_data.m_data['mines'] ):
            while True:
                c_mine = ( rd.randint( 0, self.height() - 1 ), rd.randint( 0, self.width() - 1 ) )
                if not self.m_field[c_mine].is_mine() and c_mine != c_start_click:
                    break

            self.m_field[c_mine].add_mine()
            for neighbor in self.__get_neighbors( c_mine ):
                neighbor.new_mine_neighbor()

            self.m_mines.append( c_mine )
        
        for _ in range( self.m_field_data.m_data['tokens'] ):
            while True:
                c_token = ( rd.randint( 0, self.height() - 1 ), rd.randint( 0, self.width() - 1 ) )
                if not self.m_field[c_token].is_token():
                    break

            self.m_field[c_token].add_token()

    def show_cursor( self, window : pg.Surface, color : tuple = COLORS['cursor'] ):
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

    def display_game_data( self, window : pg.Surface, display: bool = False ):
        if self.m_field_data.m_running:
            self.m_field_data.display( window )
            self.m_field_data.m_time = int( t.time() - self.m_field_data.m_start_time ) 

        if display:
            self.m_field_data.display( window )

    def display_field( self, window : pg.Surface, c_tile = OUT_OF_BOUNDS ):
        if c_tile == OUT_OF_BOUNDS:
            self.m_surface.fill( ( 50, 50, 50, 255 ) )
            for row in self.m_field:
                for tile in row:
                    tile.display( self.m_surface )
        else:
            #self.m_surface.fill( ( 0, 0, 0, 0 ) )
            self.m_field[c_tile].display( self.m_surface )

        window.blit( self.m_surface, ( OFFSET['x'], OFFSET['y'] ) )
        self.display_game_data( window, True )

    def check_click( self, button : np.uint32, mouse_pos : tuple ) -> bool:
        c_click = self.mouse_pos_to_coords( mouse_pos )
        
        if c_click != OUT_OF_BOUNDS:
            if button == 1 and not self.m_field[c_click].is_flag():
                if len( self.m_mines ) == 0:
                    self.m_field_data.start_timer()
                    self.hide_mines_and_tokens( c_click )
                if not self.open( c_click ):
                    self.m_field_data.stop_timer()
                    self.m_field[c_click].boom()
                    self.open_mines()
                    return 'l'
                if not self.open( c_click ) or self.__are_safe_tiles_open():
                    self.m_field_data.stop_timer()
                    self.open_mines()
                    return 'w'
            if button == 3:
                if self.m_field[c_click].flag():
                    self.m_field_data.m_data['flags'] += 1
                else:
                    self.m_field_data.m_data['flags'] -= 1

        return 'r'

    def __get_neighbors( self, c_tile : tuple ) -> np.array:
        neighbors = self.m_field[
            max( c_tile[0] - 1, 0 ) : min( c_tile[0] + 2, self.height() ),
            max( c_tile[1] - 1, 0 ) : min( c_tile[1] + 2, self.width() ) ].flatten()

        tile_y = c_tile[0]*self.t_dimensions()[0] + OFFSET['t_y']
        tile_x = c_tile[1]*self.t_dimensions()[1] + OFFSET['t_x']
        neighbors = neighbors[ neighbors != Tile( ( tile_y, tile_x ), self.t_dimensions() ) ]
        return neighbors

    def __check_neighbors( self, c_tile : tuple ) -> str:
        flaged, mines, flaged_mines = 0, 0, 0
        for neighbor in self.__get_neighbors( c_tile ):
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
            self.__flood_fill( c_tile )
        else:
            n_check = self.__check_neighbors( c_tile )
            if n_check == 'open':
                for neighbor in self.__get_neighbors( c_tile ):
                    if not neighbor.is_mine():
                        self.__flood_fill( neighbor.arr_coords() )
            elif n_check == 'boom':
                return False
        return True

    def __flood_fill( self, c_tile : tuple ):
        queue, visited = [], []
        queue.append( c_tile )
        visited.append( c_tile )

        if self.m_field[c_tile].is_open():
            return

        if self.m_field[c_tile].open():
            self.add_powerup_token( 1 )

        if self.m_field[c_tile].mines_around() != 0:
            for neighbor in self.__get_neighbors( c_tile ):
                if not neighbor.is_mine() and neighbor.mines_around() == 0:
                    queue.append( neighbor.arr_coords() )
                    visited.append( neighbor.arr_coords() )

        while queue:
            c_exam_tile = queue.pop( 0 )
            if self.m_field[c_exam_tile].mines_around() == 0:
                if self.m_field[c_exam_tile].open():
                    self.add_powerup_token( 1 )
            else:
                continue

            for neighbor in self.__get_neighbors( c_exam_tile ):
                if not neighbor.arr_coords() in visited:
                    if self.__has_nomine_neighbor( neighbor.arr_coords() ):
                        if neighbor.open():
                            self.add_powerup_token( 1 )
                    queue.append( neighbor.arr_coords() )
                    visited.append( neighbor.arr_coords() )

    def open_mines( self ):
        for c_mine in self.m_mines:
            if self.m_field[c_mine].is_flag():
                self.m_field[c_mine].flag()
            self.m_field[c_mine].open()

    def __has_nomine_neighbor( self, c_tile : tuple ) -> bool:
        for neighbor in self.__get_neighbors( c_tile ):
            if neighbor.mines_around() == 0:
                return True
        return False

    def __are_safe_tiles_open( self ) -> bool:
        for row in self.m_field:
            for tile in row:
                if not tile.is_open() and not tile.is_mine():
                    return False
        return True

    def mouse_pos_to_coords( self, mouse_pos : tuple ) -> tuple:
        mouse_pos = mouse_pos[::-1]
        col = ( mouse_pos[0] - OFFSET['y'] - OFFSET['t_y'] )//self.t_dimensions()[0]
        row = ( mouse_pos[1] - OFFSET['x'] - OFFSET['t_x'] )//self.t_dimensions()[1]
        if 0 <= col < self.height() and 0 <= row < self.width():
            return ( col, row )

        return OUT_OF_BOUNDS

    def no_bubbles( self ) -> bool:
        for row in self.m_field:
            for tile in row:
                if not tile.is_open() and not tile.is_mine() and tile.mines_around() == 0:
                    return False

        return True

    def add_powerup_token( self, how_much : int ):
        self.m_field_data.m_data['coll'] += how_much
