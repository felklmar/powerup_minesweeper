import pytest
import pygame as pg
from tile import Tile

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
    assert isinstance( tile, Tile )

    # test arr_coords method
    col = ( c_tile[0] - offset['t'][0] )//d_tile[0]
    row = ( c_tile[1] - offset['t'][1] )//d_tile[1]
    arr_coords = ( ( col, row ) )
    assert arr_coords == tile.arr_coords( offset['t'] )

    # test rect
    col = c_tile[0] + offset['f'][0]
    row = c_tile[1] + offset['f'][1]
    rect = pg.Rect( ( row, col ), d_tile[::-1] )
    assert rect == tile.tile_rect( offset['f'] )

    # test tile properties
    assert tile.dimensions() == d_tile
    assert tile.flag()    is True
    assert tile.open()    is False
    assert tile.is_flag() is True
    assert tile.is_open() is False
    assert tile.mines_around() == 0
    for i in range( 1, 8 ):
        tile.new_mine_neighbor()
        assert tile.mines_around() == i
    assert tile.flag()     is False
    assert tile.is_flag()  is False
    assert tile.is_mine()  is False
    assert tile.is_boom()  is False
    assert tile.is_token() is False
    tile.add_mine()
    tile.boom()
    tile.add_token()
    assert tile.is_mine()  is True
    assert tile.is_boom()  is True
    assert tile.is_token() is True
    tile.add_mine()
    tile.boom()
    tile.add_token()
    assert tile.is_mine()  is True
    assert tile.is_boom()  is True
    assert tile.is_token() is True
