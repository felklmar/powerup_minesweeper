import numpy as np
import pygame as pg
import random as rd
from tile import Tile

OFFSET_Y, OFFSET_X = 10, 20

class Minefield:
    def __init__( self, 
                  height : np.uint32, 
                  width : np.uint32, 
                  tile_size : np.uint32, 
                  num_of_mines : np.uint32, 
                  window : pg.Surface ):

        self.m_height, self.m_width = height, width
        self.m_tile_size = tile_size
        self.m_window = window
        self.m_field  = np.empty( [height, width], dtype = Tile )
        self.m_mines  = []
        self.m_num_of_mines = num_of_mines

        for y in range( height ):
            for x in range( width ):
                self.m_field[y, x] = Tile( x*tile_size + OFFSET_X, y*tile_size + OFFSET_Y, tile_size )

    def hide_mines( self, start_click_coords : tuple ):
        for _ in range( self.m_num_of_mines ):
            while True:
                y, x = rd.randint( 0, self.m_height - 1 ), rd.randint( 0, self.m_width - 1 )
                if not self.m_field[y, x].contains_mine() and ( x, y ) != start_click_coords:
                    break
            
            self.m_field[y, x].is_mine()
            for neighbor in self.get_neighbors( ( x, y ) ):
                neighbor.m_mines_around = neighbor.m_mines_around + 1  
            self.m_mines.append( ( x, y ) )

    def dimensions( self ) -> tuple:
        return ( self.m_width, self.m_height )

    def display_field( self ):
        for row in self.m_field:
            for tile in row:
                tile.display( self.m_window )

    def check_click( self, button ) -> str:
        for row in self.m_field:
            for tile in row:
                coords = tile.click( button )
                if coords != ( -1, -1 ):
                    break
            else:
                continue
            break
        
        if coords != ( -1, -1 ):
            if button == 1:
                if len( self.m_mines ) == 0:
                    self.hide_mines( coords )
                if not self.m_field[coords[1], coords[0]].m_flaged and self.m_field[coords[1], coords[0]].contains_mine():
                    self.show_mines()
                    return 'l'
                else:
                    self.open( coords )
                if self.are_safe_tiles_open():
                    return 'w'
            if button == 3:
                self.m_field[coords[1], coords[0]].flag()

        return 'r'

    def get_neighbors( self, coords : tuple ) -> np.array:
        neighbors = self.m_field[
            max( coords[1] - 1, 0 ) : min( coords[1] + 2, self.m_height ),
            max( coords[0] - 1, 0 ) : min( coords[0] + 2, self.m_width ) ].flatten()
        return np.delete( neighbors, np.where( neighbors == Tile( coords[0]*self.m_tile_size + OFFSET_X, coords[1]*self.m_tile_size + OFFSET_Y ) ) )

    def open( self, coords ):
        if self.m_field[coords[1], coords[0]].open():
            self.flood_fill( coords )

    def flood_fill( self, coords ):
        if not self.m_field[coords[1], coords[0]].contains_mine(): 
            self.m_field[coords[1], coords[0]].open()

        for neighbor in self.get_neighbors( coords ):
            if not neighbor.is_opened() and neighbor.m_mines_around == 0:
                self.flood_fill( neighbor.arr_coords() )
            elif self.m_field[coords[1], coords[0]].m_mines_around == 0 and not self.m_field[coords[1], coords[0]].contains_mine():
                neighbor.open()

    def show_mines( self ):
        for mine in self.m_mines:
            self.m_field[mine[1], mine[0]].open()

    def are_safe_tiles_open( self ) -> bool:
        for row in self.m_field:
            for tile in row:
                if not tile.is_opened() and not tile.contains_mine():
                    return False
        return True
    