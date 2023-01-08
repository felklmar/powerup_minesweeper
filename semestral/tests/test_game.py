# pylint: disable=protected-access
#  - this pylint warning is disabled, because I have to forcefully access private
#    class method to test them
"""Tests game.py"""
import pytest
import pygame as pg
from src.game import Game
from src.utilities import COLORS, OFF, NO_POWERUP

@pytest.fixture( name = 'game_pow' )
def game_powerups() -> Game:
    """Game fixture"""
    pg.init()
    game_data = {
            'dim'      : ( 9, 9 ),
            'tile_dim' : ( 1, 1 ),
            'mines'    : 10,
            'tokens'   : 5
        }
    return Game( game_data, OFF, COLORS )

@pytest.fixture( name = 'game_nopow' )
def game_nopowerups() -> Game:
    """Game fixture"""
    pg.init()
    game_data = {
            'dim'      : ( 9, 9 ),
            'tile_dim' : ( 1, 1 ),
            'mines'    : 10,
            'tokens'   : 0
        }
    return Game( game_data, OFF, COLORS )

def test_game( game_pow, game_nopow ):
    """Tests game creation and reset"""
    game_p, game = game_pow, game_nopow
    assert game_p.m_status is True
    assert game.m_status is True
    assert game_p.m_active_powerup == NO_POWERUP
    assert len( game_p.m_buttons ) == 2
    assert len( game.m_buttons ) == 2
    assert len( game_p.m_powerups ) == 4
    assert len( game.m_powerups ) == 0

    game_p.m_status, game.m_status = False, False
    game_p.m_active_powerup = 1
    game_p._Game__reset()
    game._Game__reset()

    assert game_p.m_status is True
    assert game.m_status is True
    assert game_p.m_active_powerup == NO_POWERUP
    assert len( game_p.m_buttons ) == 2
    assert len( game.m_buttons ) == 2
    assert len( game_p.m_powerups ) == 4
    assert len( game.m_powerups ) == 0

def test_powerup_handling( game_pow ):
    """Test powerups handling"""
    game = game_pow
    # test powerup activation
    for i in game.m_powerups:
        assert i.m_color == COLORS['t_disabled']

    game._Game__activate_powerups( 1 )
    for i in game.m_powerups:
        if i.m_color != COLORS['t_disabled']:
            assert i.name() == 'SafeOpen'
            assert i.m_value == 1

    game._Game__activate_powerups( 2 )
    for i in game.m_powerups:
        if i.m_color != COLORS['t_disabled']:
            assert i.name() in ( 'SafeOpen', 'OpenBubble', 'FlagRandom' )
            assert i.m_value <= 2

    game._Game__activate_powerups( -5 )
    for i in game.m_powerups:
        assert i.m_color == COLORS['t_disabled']

    game._Game__activate_powerups( 3 )
    for i in game.m_powerups:
        if i.m_color != COLORS['t_disabled']:
            assert i.name() in ( 'SafeOpen', 'OpenBubble', 'FlagRandom', 'CrossOpen' )
            assert i.m_value <= 3

    # test powerup picking
    game._Game__pick_powerup( 2 )
    assert game.m_active_powerup == 2
    for idx, i in enumerate( game.m_powerups ):
        if idx == game.m_active_powerup:
            assert i.m_color == COLORS['t_highlight']
    assert game.m_powerups[game.m_active_powerup].name() == 'FlagRandom'

    game._Game__pick_powerup()
    assert game.m_active_powerup == NO_POWERUP
    for i in game.m_powerups:
        assert i.m_color != COLORS['t_highlight']
