import pygame as pg
from minefield import Minefield
from game import Game
from tile import OFFSET
from powerups import Powerup, SafeOpen, OpenBubble, CrossOpen
from menu import Menu

WIDTH, HEIGHT = 1240, 680
WIN = pg.display.set_mode( ( WIDTH, HEIGHT ) )
pg.display.set_caption( "minesweeper" )

def main( window : pg.Surface ):
    pg.init()

    clock = pg.time.Clock()
    run, app_status, field_generated = True, 'm', False

    menu = Menu( window )
    while run:        
        clock.tick( 60 )
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run = False

            if app_status == 'm':
                #field_generated = False
                window.fill( ( 0, 0, 0 ) )
                menu.display()
                click = menu.click( event )
                if click == 'end':
                    run = False

                #print( menu.m_game_settings, menu.m_d_idx )
                if click == 'start':
                    window.fill( ( 0, 0, 0 ) )
                    height = menu.m_game_settings[0] 
                    width = menu.m_game_settings[1]
                    mines = menu.m_game_settings[2]
                    tokens = menu.m_game_settings[3]
                    game = Game( True, { 'dim': ( height, width ), 'tile_dim' : ( 20, 20 ), 'mines' : mines, 'tokens' : tokens }, window )
                    field_generated = True
                    app_status = 'r'

            if app_status == 'r':
                #if not field_generated:
                #    game = Game( True, { 'dim': ( 30, 50 ), 'tile_dim' : ( 20, 20 ), 'mines' : 200, 'tokens' : 20 }, window )
                #    window.fill( (255,255,255) )
                #    field_generated = True
                app_status = game.game_loop( event )

            elif app_status == 'l':
                if event.type == pg.MOUSEBUTTONUP:
                    menu.default()
                    app_status = 'm'

            elif app_status == 'w':
                if event.type == pg.MOUSEBUTTONUP:
                    menu.default()
                    app_status = 'm'
            
            #if event.type == pg.VIDEORESIZE:
            #    window.fill( (255,255,255) )
            #    minefield.display_field( window )

        if field_generated:
            game.m_minefield.display_game_data( window )

        #font = pg.font.Font( 'assets/Monocraft.otf', 50 )
        #text = font.render('test', False, ( 0, 0, 0 ) )
        #text_rect = text.get_rect()
        #text_rect.topleft = ( 400, 20 )
        #window.blit( text, text_rect )
        pg.display.update()

    pg.quit()

if __name__ == "__main__":
    main( WIN )
