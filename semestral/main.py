"""
Minesweeper
-----------
Module containing main function that runs minesweeper
"""
import pygame as pg
from game import Game
from menu import Menu
from utilities import WIDTH, HEIGHT, BACK_COLOR, TILE_DIM

def main():
    """
    Main application loop
    ---------------------
    Firstly initialize pygame and creates pygame window,
    then starts running an endless cycle, where it calls other
    classes and methods
    """
    pg.init()
    window = pg.display.set_mode( ( WIDTH, HEIGHT ) )
    pg.display.set_caption( "minesweeper" )

    clock = pg.time.Clock()
    running, game_running = True, False
    menu = Menu( window )
    while running:
        clock.tick( 60 )
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False

            if not game_running:
                window.fill( BACK_COLOR )
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
                    game = Game( menu.tokens(), game_data, window )
                    window.fill( BACK_COLOR )
                    game_running = True
            else:
                game_running = game.game_loop( event )
                if not game_running:
                    menu.default()

        if game_running:
            game.m_minefield.display_game_data( window )

        pg.display.update()

    pg.quit()

if __name__ == "__main__":
    main()
