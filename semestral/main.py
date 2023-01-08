"""
__Minesweeper__
Module containing main function that runs minesweeper
"""
import pygame as pg
from src.game import Game
from src.menu import Menu
from src.utilities import WIDTH, HEIGHT, TILE_DIM, COLORS, OFF, DEF_DIFFIC

def main():
    """
    __Main application loop__
    Firstly initialize pygame and creates pygame window,
    then starts running an endless cycle, where it calls other
    classes and methods
    """
    pg.init()
    window = pg.display.set_mode( ( WIDTH, HEIGHT ) )
    pg.display.set_caption( "minesweeper" )

    clock = pg.time.Clock()
    running, game_running = True, False
    menu = Menu( window, OFF['m'], COLORS, DEF_DIFFIC )
    while running:
        clock.tick( 60 )
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False

            if not game_running:
                window.fill( COLORS['background'] )
                menu.display()
                click = menu.click( event )
                if click == 'end':
                    running = False

                if click == 'start':
                    game_data = {
                            'dim': ( menu.height(), menu.width() ),
                            'tile_dim' : TILE_DIM,
                            'mines' : menu.mines(),
                            'tokens' : menu.tokens()
                        }
                    game = Game( game_data, OFF, COLORS )
                    window.fill( COLORS['background'] )
                    game_running = True
            else:
                game_running = game.game_loop( event )
                if not game_running:
                    menu.default()

        if game_running:
            game.m_minefield.display_game_data( window, COLORS )

        pg.display.update()

    pg.quit()

if __name__ == "__main__":
    main()
