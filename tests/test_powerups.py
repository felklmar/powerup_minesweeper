# pylint: disable=protected-access
#  - this pylint warning is disabled, because I have to forcefully access private
#    class method to test them
"""Tests powerups.py"""
import pytest
import numpy as np
import pygame as pg
from powerup_minesweeper.src.minefield import Minefield
from powerup_minesweeper.src.powerups import SafeOpen, OpenBubble, FlagRandom, CrossOpen
from powerup_minesweeper.src.utilities import COLORS

@pytest.fixture( name = 'mines' )
def mines_coords() -> tuple:
    """Mines coordinates fixture"""
    return ( ( 1, 4 ), ( 2, 4 ), ( 3, 5 ), ( 4, 6 ), ( 4, 7 ),
             ( 4, 1 ), ( 5, 2 ), ( 6, 3 ), ( 6, 4 ), ( 7, 5 ) )

@pytest.fixture( name = 'tokens' )
def tokens_coords() -> tuple:
    """Tokens coordinates fixture"""
    return ( ( 0, 4 ), ( 2, 1 ), ( 4, 4 ) )

@pytest.fixture( name = 'bubbles' )
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

@pytest.fixture( name = 'powerups' )
def powerup_tuple():
    """Powerups fixture"""
    pg.init()
    return ( SafeOpen(   ( 0, 0 ), COLORS['t_disabled'], 1    ),
             OpenBubble( ( 0, 0 ), COLORS['t_disabled'], 2    ),
             FlagRandom( ( 0, 0 ), COLORS['t_disabled'], 2, 7 ),
             CrossOpen(  ( 0, 0 ), COLORS['t_disabled'], 3, 2 ) )

def test_safeopen( minefield, powerups, bubbles ):
    """Test SafeOpen powerup"""
    powerup = powerups[0]
    assert powerup.m_value == 1
    minefield.open( ( 0, 0 ) )
    assert powerup.apply_powerup( pg.Surface( ( 0, 0 ) ),
                                  minefield,
                                  minefield.m_offset,
                                  ( 0, 0 ) ) == 'used'
    assert minefield.m_field[4, 4].is_open() is False

    assert powerup.apply_powerup( pg.Surface( ( 0, 0 ) ),
                                  minefield,
                                  minefield.m_offset,
                                  ( 4, 4 ) ) == 'applied'
    assert minefield.m_field[4, 4].is_open() is True

    assert minefield.m_field[4, 1].is_flag() is False
    assert powerup.apply_powerup( pg.Surface( ( 0, 0 ) ),
                                  minefield,
                                  minefield.m_offset,
                                  ( 1, 4 ) ) == 'applied'
    assert minefield.m_field[4, 1].is_open() is False
    assert minefield.m_field[4, 1].is_flag() is True

    for i in bubbles[3]:
        assert minefield.m_field[i].is_open() is False
    assert powerup.apply_powerup( pg.Surface( ( 0, 0 ) ),
                                  minefield,
                                  minefield.m_offset,
                                  ( 6, 7 ) ) == 'applied'
    for i in bubbles[3]:
        assert minefield.m_field[i].is_open() is True

def test_openbubble( minefield, powerups, bubbles ):
    """Test OpenBubble powerup"""
    powerup = powerups[1]
    assert powerup.m_value == 2
    assert minefield.no_bubbles() is False
    for _ in range( 4 ):
        assert powerup.apply_powerup( pg.Surface( ( 0, 0 ) ),
                                      minefield,
                                      minefield.m_offset,
                                      ( 0, 0 ) ) == 'applied'
    assert minefield.no_bubbles() is True

    for bubble in bubbles:
        for i in bubble:
            assert minefield.m_field[i].is_open() is True

def test_flagrandom( minefield, powerups ):
    """Test FlagRandom powerup"""
    powerup = powerups[2]
    assert powerup.m_value == 2
    for _, tile in np.ndenumerate( minefield.m_field ):
        assert tile.is_flag() is False

    assert powerup.apply_powerup( pg.Surface( ( 0, 0 ) ),
                                  minefield,
                                  minefield.m_offset,
                                  ( 0, 0 ) ) == 'applied'

    flag_tiles = 0
    for _, tile in np.ndenumerate( minefield.m_field ):
        flag_tiles += tile.is_flag()
    assert flag_tiles == powerup.m_mines

    assert powerup.apply_powerup( pg.Surface( ( 0, 0 ) ),
                                  minefield,
                                  minefield.m_offset,
                                  ( 0, 0 ) ) == 'applied'

    flag_tiles = 0
    for _, tile in np.ndenumerate( minefield.m_field ):
        flag_tiles += tile.is_flag()
    assert flag_tiles == powerup.m_mines

def test_opencross( minefield, powerups, bubbles ):
    """Test CrossOpen powerup"""
    powerup = powerups[3]
    assert powerup.m_value == 3
    cross = ( ( 4, 2 ), ( 4, 3 ), ( 4, 4 ), ( 4, 5 ), ( 4, 6 ),
              ( 2, 4 ), ( 3, 4 ), ( 5, 4 ), ( 6, 4 ) )
    assert powerup.apply_powerup( pg.Surface( ( 0, 0 ) ),
                                  minefield,
                                  minefield.m_offset,
                                  ( 4, 4 ) ) == 'applied'

    open_tiles = cross
    for i in cross:
        tile = minefield.m_field[i]
        if tile.is_mine():
            assert tile.is_open() is False
            assert tile.is_flag() is True
        else:
            assert tile.is_open() is True

    cross = ( ( 0, 0 ), ( 1, 0 ), ( 2, 0 ),
              ( 0, 1 ), ( 0, 2 ) )

    open_tiles += cross
    open_tiles += bubbles[0]
    assert powerup.apply_powerup( pg.Surface( ( 0, 0 ) ),
                                minefield,
                                minefield.m_offset,
                                ( 0, 0 ) ) == 'applied'

    for i in cross:
        tile = minefield.m_field[i]
        if tile.is_mine():
            assert tile.is_open() is False
            assert tile.is_flag() is True
        else:
            assert tile.is_open() is True

    for idx, tile in np.ndenumerate( minefield.m_field ):
        if tile.is_open():
            assert idx in open_tiles
