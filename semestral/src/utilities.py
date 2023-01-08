"""
Module containing constants
"""
import pygame as pg

HEIGHT, WIDTH = 620, 1110
FONT = 'assets/NT Wagner.otf'
NO_POWERUP = -1
OUT_OF_BOUNDS = ( -1, -1 )
TILE_DIM = ( 23, 23 )

COLORS = {
    'background'  : ( 172, 172, 172 ),
    't_basic'     : ( 255, 255, 255 ),
    't_disabled'  : ( 50, 50, 50 ),
    't_highlight' : ( 255, 255, 0 ),
    'cursor'      : ( 255, 0, 0, 100 ),
    'pow_cursor'  : ( 255, 255, 0, 100 ),
}

"""offsets"""
OFFSET = {
    'x'   : 200,
    'y'   : 50,
    't_x' : 5,
    't_y' : 5,
    'm_x' : 20,
    'm_y' : 20,
}

OFF = {
    'f' : ( 50, 200 ),
    't' : (  5,   5 ),
    'm' : ( 20,  20 ),
}

LOGO = pg.image.load( 'assets/sprites/logo.svg' )

"""Dictionary for tile sprites"""
TILES = {
    'closed' : pg.image.load( 'assets/sprites/closed.svg' ),
    'flag' : pg.image.load( 'assets/sprites/flag.svg' ),
    'mine' : pg.image.load( 'assets/sprites/mine.svg' ),
    'boom' : pg.image.load( 'assets/sprites/boom.svg' ),
    '0' : pg.image.load( 'assets/sprites/0.svg' ),
    '1' : pg.image.load( 'assets/sprites/1.svg' ),
    '2' : pg.image.load( 'assets/sprites/2.svg' ),
    '3' : pg.image.load( 'assets/sprites/3.svg' ),
    '4' : pg.image.load( 'assets/sprites/4.svg' ),
    '5' : pg.image.load( 'assets/sprites/5.svg' ),
    '6' : pg.image.load( 'assets/sprites/6.svg' ),
    '7' : pg.image.load( 'assets/sprites/7.svg' ),
    '8' : pg.image.load( 'assets/sprites/8.svg' )
}

DEF_DIFFIC = 2
DIFFIC = (
    (    'Can I play, Daddy?', [  9,  9,  10,  5 ] ),
    (       'Don\'t hurt me.', [ 16, 16,  40, 13 ] ),
    (        'Bring \'em on!', [ 20, 24,  99, 23 ] ),
    ( 'I am Death incarnate!', [ 36, 50, 450, 89 ] ),
)

# height, width, mines, tokens
MIN = ( 9, 9, 10, 0 )

# height, width
MAX = ( 40, 70 )
