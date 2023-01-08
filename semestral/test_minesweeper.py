import pytest
import numpy as np
import pygame as pg
from tile import Tile
from minefield import Minefield, GameData

#@pytest.fixture
#def minefield():

@pytest.mark.parametrize( 
    'offset, c_tile, d_tile',
    [
        ( { 'f' : (  12,  25 ), 't' : (  1,  3 ) }, (  12,    25 ), (  5,  2 ) ),
        ( { 'f' : (  11,  11 ), 't' : ( 17, 17 ) }, ( 1155, 1722 ), ( 10, 10 ) ),
        ( { 'f' : (   3, 210 ), 't' : (  0,  0 ) }, ( 1201,  630 ), ( 21, 17 ) ),
        ( { 'f' : ( 414,   1 ), 't' : (  7, 88 ) }, ( 1111, 1111 ), ( 11, 11 ) ),
        ( { 'f' : ( 200, 200 ), 't' : (  9, 25 ) }, (  100,  151 ), ( 44, 22 ) ),
        ( { 'f' : ( 193,  56 ), 't' : ( 54, 86 ) }, ( 2955, 2524 ), ( 41, 81 ) ),
        ( { 'f' : ( 241, 199 ), 't' : ( 76, 69 ) }, ( 1298, 1050 ), (  8, 70 ) ),
        ( { 'f' : ( 245,  22 ), 't' : ( 78, 34 ) }, ( 2228,  806 ), ( 37, 85 ) ),
        ( { 'f' : ( 202,  26 ), 't' : ( 35, 51 ) }, (  194,  330 ), ( 34, 31 ) ),
        ( { 'f' : ( 246, 379 ), 't' : ( 84, 96 ) }, (  275,  774 ), ( 72, 53 ) ),
        ( { 'f' : ( 383, 139 ), 't' : ( 62, 50 ) }, (  990,  442 ), ( 10, 95 ) ),
        ( { 'f' : (  57, 321 ), 't' : ( 76, 84 ) }, ( 1300,  538 ), ( 27,  9 ) ),
        ( { 'f' : ( 430, 188 ), 't' : ( 66, 95 ) }, ( 2082, 1473 ), ( 96, 91 ) ),
        ( { 'f' : ( 338,  14 ), 't' : ( 44, 88 ) }, (  263,  985 ), ( 49, 56 ) ),
        ( { 'f' : ( 462, 370 ), 't' : ( 11,  0 ) }, ( 1771, 2921 ), ( 29,  5 ) ),
        ( { 'f' : ( 125, 203 ), 't' : ( 91, 72 ) }, ( 1684, 2614 ), ( 82,  2 ) ),
        ( { 'f' : ( 399, 110 ), 't' : (  0,  2 ) }, ( 1460,  610 ), (  1, 67 ) ),
        ( { 'f' : ( 100, 104 ), 't' : ( 14, 67 ) }, ( 2755, 1289 ), (  4, 59 ) ),
        ( { 'f' : (  21, 182 ), 't' : ( 96, 69 ) }, (  604, 1597 ), ( 74, 92 ) ),
        ( { 'f' : ( 377, 213 ), 't' : ( 81, 58 ) }, (  282,   46 ), ( 25, 35 ) ),
    ] 
)

def test_tile( offset, c_tile, d_tile ):
    """Test tile behavior"""
    tile = Tile( c_tile, d_tile )
    assert( isinstance( tile, Tile ) )
    
    # test arr_coords method
    y = ( c_tile[0] - offset['t'][0] )//d_tile[0]
    x = ( c_tile[1] - offset['t'][1] )//d_tile[1]
    arr_coords = ( ( y, x ) )
    assert( arr_coords == tile.arr_coords( offset['t'] ) )

    # test rect
    y = c_tile[0] + offset['f'][0]
    x = c_tile[1] + offset['f'][1]
    rect = pg.Rect( ( x, y ), d_tile[::-1] )
    assert( rect == tile.tile_rect( offset['f'] ) )
    
    # test tile properties
    assert( tile.dimensions() == d_tile )
    assert( tile.flag()    == True  )
    assert( tile.open()    == False )
    assert( tile.is_flag() == True  )
    assert( tile.is_open() == False )
    assert( tile.mines_around() == 0 )
    for i in range( 1, 8 ):
        tile.new_mine_neighbor()
        assert( tile.mines_around() == i )
    assert( tile.flag()     == False )
    assert( tile.is_flag()  == False )
    assert( tile.is_mine()  == False )
    assert( tile.is_boom()  == False )
    assert( tile.is_token() == False )
    tile.add_mine() 
    tile.boom() 
    tile.add_token()
    assert( tile.is_mine()  == True )
    assert( tile.is_boom()  == True )
    assert( tile.is_token() == True )
    tile.add_mine() 
    tile.boom() 
    tile.add_token()
    assert( tile.is_mine()  == True )
    assert( tile.is_boom()  == True )
    assert( tile.is_token() == True )

@pytest.mark.parametrize(
    'init_data, offset',
    [
        ( { 'dim' : ( 9, 13 ), 'tile_dim' : ( 10, 10 ), 'mines': 10, 'tokens': 5 }, { 'f' : ( 0, 0 ), 't' : ( 0, 0 ) } ),   
    ]
)
def test_minefield( init_data, offset ):
    # test instance creation
    field = Minefield( init_data, offset )
    assert( isinstance( field, Minefield ) )
    assert( isinstance( field.m_game_data, GameData ) )

    # test minefield properities
    assert( field.m_field.shape  == init_data['dim'] )
    assert( field.dimensions()   == init_data['dim'] )
    assert( field.t_dimensions() == init_data['tile_dim'] )
    assert( field.tokens() == 0 )
    assert( ( field.height(), field.width() ) == init_data['dim'] )

    # test mines and token generating
    mines, tokens = 0, 0
    for idx, _ in np.ndenumerate( field.m_field ):
        mines  += field.m_field[idx].is_mine()
        tokens += field.m_field[idx].is_token()
        tile_status = []
        tile_status.append( field.m_field[idx].is_open()  )
        tile_status.append( field.m_field[idx].is_flag()  )
        tile_status.append( field.m_field[idx].is_mine()  )
        tile_status.append( field.m_field[idx].is_boom()  )
        tile_status.append( field.m_field[idx].is_token() )
        tile_status.append( bool( field.m_field[idx].mines_around() ) )
        for i in tile_status:
            assert( not i )
    assert( mines == 0 and tokens == 0 )
    assert( field.m_game_data.m_t_running == False )
    assert( len( field.m_mines ) == 0 ) 
    field._Minefield__hide_mines_and_tokens( ( 0, 0 ) ) 
    assert( len( field.m_mines ) == init_data['mines'] ) 
    assert( field.m_field[ 0, 0 ].is_mine() == False )
    tok_mines = 0
    for idx, _ in np.ndenumerate( field.m_field ):
        assert( field.m_field[idx].is_open() == False )
        tok_mines += field.m_field[idx].is_mine() and field.m_field[idx].is_token()
        mines  += field.m_field[idx].is_mine()
        tokens += field.m_field[idx].is_token()
        neighbors = field._Minefield__get_neighbors( idx )
        mines_around = 0
        for n in neighbors:
            mines_around += n.is_mine()
        assert( mines_around == field.m_field[idx].mines_around() )
            
    assert( mines == init_data['mines'] and tokens == init_data['tokens'] and tok_mines == 0 )
    for c_mine in field.m_mines:
        assert( field.m_field[c_mine].is_mine() )

    #field = Minefield( init_data, offset )
