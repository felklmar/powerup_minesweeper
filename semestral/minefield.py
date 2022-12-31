import numpy as np
import pygame as pg
from tile import *

OFFSET_Y, OFFSET_X = 10, 20 

class Minefield:
    def __init__( self, height : np.uint32, width : np.uint32, tile_size : np.uint32 ,window : pg.Surface ):
        self.m_height, self.m_width = height, width
        self.m_tile_size = tile_size
        self.m_window = window
        self.m_field  = np.empty( [height, width], dtype = Tile )
        
        for y in range( height ):
            for x in range( width ):
                self.m_field[y][x] = Tile( x*tile_size + OFFSET_X, y*tile_size + OFFSET_Y, tile_size ) 
        
        #self.m_field  = np.full( [height, width], Tile(), dtype = Tile )
        #for y in range( self.m_height ):
        #    self.m_field = np.append( self.m_field, [ Tile() ] )
        
    def dimensions( self ) -> tuple:
        return ( self.m_width, self.m_height )

    def display_field( self ):
        for row in self.m_field:
            for tile in row:
                tile.display( self.m_window )

#m = Minefield( 10, 10 )
#print( m.dimensions() )

#print( m.m_field )
#for i in m.m_field:
#    for j in i:
#        print( j.contains_mine(), end = ' ' )
#    print()