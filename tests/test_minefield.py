# pylint: disable=protected-access
#  - this pylint warning is disabled, because I have to forcefully access private
#    class method to test them
"""Tests minefield.py"""
import pytest
import numpy as np
from powerup_minesweeper.src.minefield import Minefield, GameData
from powerup_minesweeper.src.utilities import COLORS, OUT_OF_BOUNDS

@pytest.mark.parametrize(
    'init_data, offset',
    [
        ( { 'dim' : ( 9, 13 ), 'tile_dim' : ( 10, 10 ), 'mines': 10, 'tokens': 5 },
          { 'f' : ( 0, 0 ), 't' : ( 0, 0 ) } ),
        ( { 'dim' : ( 63, 14 ), 'tile_dim' : ( 13,  4 ), 'mines':  337, 'tokens':  531 },
          { 'f' : ( 33, 44 ), 't' : ( 30, 18 ) } ),
        ( { 'dim' : ( 73, 12 ), 'tile_dim' : (  3, 13 ), 'mines':  198, 'tokens':  633 },
          { 'f' : ( 33, 28 ), 't' : ( 87, 85 ) } ),
        ( { 'dim' : ( 11, 46 ), 'tile_dim' : (  4, 12 ), 'mines':  276, 'tokens':   96 },
          { 'f' : ( 56, 90 ), 't' : ( 74, 61 ) } ),
        ( { 'dim' : ( 91, 42 ), 'tile_dim' : ( 13, 13 ), 'mines': 2880, 'tokens':  640 },
          { 'f' : ( 85, 94 ), 't' : ( 57,  1 ) } ),
        ( { 'dim' : ( 92, 51 ), 'tile_dim' : (  4,  0 ), 'mines': 3107, 'tokens': 1059 },
          { 'f' : ( 55, 75 ), 't' : (  9, 32 ) } ),
        ( { 'dim' : ( 84, 49 ), 'tile_dim' : ( 11,  3 ), 'mines': 3694, 'tokens':  317 },
          { 'f' : ( 30, 83 ), 't' : ( 77, 62 ) } ),
        ( { 'dim' : ( 66, 89 ), 'tile_dim' : (  3,  0 ), 'mines': 2656, 'tokens':  464 },
          { 'f' : ( 56, 11 ), 't' : ( 16, 91 ) } ),
        ( { 'dim' : ( 19, 17 ), 'tile_dim' : (  6,  3 ), 'mines':  222, 'tokens':   15 },
          { 'f' : ( 43, 99 ), 't' : ( 87, 99 ) } ),
        ( { 'dim' : ( 13, 90 ), 'tile_dim' : (  9,  0 ), 'mines':  323, 'tokens':   88 },
          { 'f' : ( 12, 21 ), 't' : ( 50,  8 ) } ),
    ]
)

def test_minefield_creation( init_data, offset ):
    """Tests minefield cretion and mine generation"""
    # test instance creation
    field = Minefield( init_data, offset, COLORS )
    assert isinstance( field, Minefield )
    assert isinstance( field.m_game_data, GameData )

    # test minefield properities
    assert field.m_field.shape  == init_data['dim']
    assert field.dimensions()   == init_data['dim']
    assert field.t_dimensions() == init_data['tile_dim']
    assert field.tokens() == 0
    assert ( field.height(), field.width() ) == init_data['dim']

    # test mines and token generating
    mines_num, tokens_num = 0, 0
    for idx, _ in np.ndenumerate( field.m_field ):
        mines_num  += field.m_field[idx].is_mine()
        tokens_num += field.m_field[idx].is_token()
        tile_status = []
        tile_status.append( field.m_field[idx].is_open()  )
        tile_status.append( field.m_field[idx].is_flag()  )
        tile_status.append( field.m_field[idx].is_mine()  )
        tile_status.append( field.m_field[idx].is_boom()  )
        tile_status.append( field.m_field[idx].is_token() )
        tile_status.append( bool( field.m_field[idx].mines_around() ) )
        for i in tile_status:
            assert i is False
    assert mines_num == 0 and tokens_num == 0

    assert field.m_game_data.m_t_running is False
    assert len( field.m_mines ) == 0
    field._Minefield__hide_mines_and_tokens( ( 0, 0 ) )
    assert len( field.m_mines ) == init_data['mines']
    assert field.m_field[0, 0].is_mine() is False

    tok_mines = 0
    for idx, _ in np.ndenumerate( field.m_field ):
        assert field.m_field[idx].is_open() is False
        tok_mines  += field.m_field[idx].is_mine() and field.m_field[idx].is_token()
        mines_num  += field.m_field[idx].is_mine()
        tokens_num += field.m_field[idx].is_token()
        neighbors = field._Minefield__get_neighbors( idx )
        mines_around = 0
        for i in neighbors:
            mines_around += i.is_mine()
        assert mines_around == field.m_field[idx].mines_around()

    assert mines_num == init_data['mines'] and tokens_num == init_data['tokens'] and tok_mines == 0
    for c_mine in field.m_mines:
        assert field.m_field[c_mine].is_mine()

@pytest.fixture( name = 'mines' )
def mines_coords() -> tuple:
    """Mines coordinates fixture"""
    return ( ( 1, 4 ), ( 2, 4 ), ( 3, 5 ), ( 4, 6 ), ( 4, 7 ),
             ( 4, 1 ), ( 5, 2 ), ( 6, 3 ), ( 6, 4 ), ( 7, 5 ) )

@pytest.fixture( name = 'tokens' )
def tokens_coords() -> tuple:
    """Tokens coordinates fixture"""
    return ( ( 0, 4 ), ( 2, 1 ), ( 4, 4 ) )

@pytest.fixture( name =  'bubbles' )
def bubbles_coords() -> tuple:
    """Bubbles coordinates fixture"""
    b_0 = ( ( 0, 0 ), ( 0, 1 ), ( 0, 2 ), ( 0, 3 ),
            ( 1, 0 ), ( 1, 1 ), ( 1, 2 ), ( 1, 3 ),
            ( 2, 0 ), ( 2, 1 ), ( 2, 2 ), ( 2, 3 ),
            ( 3, 0 ), ( 3, 1 ), ( 3, 2 ), ( 3, 3 ) )

    b_1 = ( ( 0, 5 ), ( 0, 6 ), ( 0, 7 ), ( 0, 8 ),
            ( 1, 5 ), ( 1, 6 ), ( 1, 7 ), ( 1, 8 ),
            ( 2, 5 ), ( 2, 6 ), ( 2, 7 ), ( 2, 8 ),
                      ( 3, 6 ), ( 3, 7 ), ( 3, 8 ) )

    b_2 = ( ( 5, 0 ), ( 5, 1 ),
            ( 6, 0 ), ( 6, 1 ), ( 6, 2 ),
            ( 7, 0 ), ( 7, 1 ), ( 7, 2 ), ( 7, 3 ), ( 7, 4 ),
            ( 8, 0 ), ( 8, 1 ), ( 8, 2 ), ( 8, 3 ), ( 8, 4 ) )

    b_3 = ( ( 5, 6 ), ( 5, 7 ), ( 5, 8 ),
            ( 6, 6 ), ( 6, 7 ), ( 6, 8 ),
            ( 7, 6 ), ( 7, 7 ), ( 7, 8 ),
            ( 8, 6 ), ( 8, 7 ), ( 8, 8 ) )

    return ( b_0, b_1, b_2, b_3 )

# _|_|_|1|1|1|_|_|_     _|_|_|1|T|1|_|_|_
# _|_|_|2|M|2|_|_|_     _|_|_|2|M|2|_|_|_
# _|_|_|2|M|3|1|_|_     _|T|_|2|M|3|1|_|_
# 1|1|1|1|2|M|3|2|1     1|1|1|1|2|M|3|2|1
# 1|M|2|1|1|2|M|M|1     1|M|2|1|T|2|M|M|1
# 1|2|M|3|1|2|2|2|1     1|2|M|3|1|2|2|2|1
# _|1|2|M|M|2|1|_|_     _|1|2|M|M|2|1|_|_
# _|_|1|2|3|M|1|_|_     _|_|1|2|3|M|1|_|_
# _|_|_|_|1|1|1|_|_     _|_|_|_|1|1|1|_|_

@pytest.fixture( name = 'minefield' )
def mine_field( mines, tokens ) -> Minefield:
    """Minefield fixture"""
    init_data = {
        'dim' : ( 9, 9 ),
        'tile_dim' : ( 1, 1 ),
        'mines': 10,
        'tokens': 3
    }
    offset = {
        'f' : ( 0, 0 ),
        't' : ( 0, 0 )
    }
    field = Minefield( init_data, offset, COLORS )
    for c_mine in mines:
        field.m_field[c_mine].add_mine()
        neighbors = field._Minefield__get_neighbors( c_mine )
        for i in neighbors:
            i.new_mine_neighbor()
    field.m_mines = mines
    for c_token in tokens:
        field.m_field[c_token].add_token()

    return field

def test_minefield_tile_opening( minefield, mines, tokens, bubbles ):
    """Tests tile opening"""
    assert minefield.no_bubbles() is False
    for i in mines:
        assert minefield.m_field[i].is_mine() is True

    tokens_num = 0
    for idx, tile in np.ndenumerate( minefield.m_field ):
        tokens_num += tile.is_token()
        assert tile.is_open() is False
        if idx in tokens:
            assert tile.is_token() is True
    assert tokens_num == 3
    assert minefield.tokens() == 0

    # test slicing neighbor tiles
    height = minefield.height()
    width = minefield.width()
    neighbors = minefield._Minefield__get_neighbors( ( height - 1, width - 1 ) )
    assert neighbors.size == 4
    neighbors = minefield._Minefield__get_neighbors( ( height - 2, width - 1 ) )
    assert neighbors.size == 6
    neighbors = minefield._Minefield__get_neighbors( ( height - 2, width - 2 ) )
    assert neighbors.size == 9

    open_tiles = bubbles[0]
    # test flood fill opening
    assert minefield.open( ( 0, 0 ) ) is True
    for idx, tile in np.ndenumerate( minefield.m_field ):
        if tile.is_open():
            assert idx in bubbles[0]
    assert minefield.no_bubbles() is False
    assert minefield.tokens() == 1

    # test open tile neighbors opening
    click = ( 0, 3 )
    assert minefield._Minefield__check_neighbors( click ) == 'ok'
    assert minefield.m_field[1,4].flag() is True
    assert minefield._Minefield__check_neighbors( click ) == 'open'
    assert minefield.open( click ) is True
    assert minefield.tokens() == 2
    open_tiles += bubbles[1]
    open_tiles += ( ( 0, 4 ), )
    for idx, tile in np.ndenumerate( minefield.m_field ):
        if tile.is_open():
            assert idx in open_tiles
    click = ( 4, 4 )
    assert minefield.open( click ) is True
    assert minefield.m_field[3, 4].flag() is True
    assert minefield.m_field[3, 4].flag() is False
    assert minefield.m_field[3, 4].flag() is True
    assert minefield._Minefield__check_neighbors( click ) == 'boom'

def test_minefield_win( minefield ):
    """Tests win recognition"""
    click = ( 4, 4 )
    assert minefield.m_field[click].flag() is True
    for _, tile in np.ndenumerate( minefield.m_field ):
        if not tile.is_mine():
            tile.open()
    assert minefield._Minefield__are_safe_tiles_open() is False

    assert minefield.handle_click( 3, click ) is True
    for _, tile in np.ndenumerate( minefield.m_field ):
        if not tile.is_mine():
            tile.open()
    assert minefield._Minefield__are_safe_tiles_open() is True
    assert minefield.no_bubbles() is True

def test_minefield_loss( minefield, mines ):
    """Tests loss recognition"""
    click = mines[0]
    assert click == minefield.mouse_pos_to_coords( click[::-1] )
    minefield.m_game_data.start_timer()
    assert minefield.m_game_data.m_t_running is True
    assert minefield.handle_click( 3, click[::-1] ) is True
    assert minefield.handle_click( 1, click[::-1] ) is True
    assert minefield.handle_click( 3, click[::-1] ) is True
    assert minefield.handle_click( 1, click[::-1] ) is False
    assert minefield.m_game_data.m_t_running is False
    assert minefield.m_field[click].is_boom() is True
    for i in mines:
        assert minefield.m_field[i].is_open() and minefield.m_field[i].is_mine()
        if i != click:
            assert minefield.m_field[i].is_boom() is False

def test_minefield_game_data( minefield ):
    """Tests helper GameData class"""
    game_data = minefield.m_game_data
    assert game_data.m_cursor == OUT_OF_BOUNDS
    assert game_data.m_data['mines']  == 10
    assert game_data.m_data['flags']  ==  0
    assert game_data.m_data['tokens'] ==  3
    assert game_data.m_data['coll']   ==  0
    minefield.add_powerup_token(  1 )
    minefield.add_powerup_token(  5 )
    minefield.add_powerup_token( 10 )
    minefield.add_powerup_token( -6 )
    assert game_data.m_data['coll'] ==  10

    # test timer
    assert game_data.m_start_time == 0
    assert game_data.m_time == 0
    assert game_data.m_t_running is False
    game_data.start_timer()
    assert game_data.m_start_time != 0
    assert game_data.m_t_running is True
    game_data.stop_timer()
    assert game_data.m_t_running is False
