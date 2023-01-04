import pygame as pg
from minefield import Minefield
from game import Game
from tile import OFFSET
from powerups import Powerup, SafeOpen, OpenBubble, CrossOpen

WIDTH, HEIGHT = 1920, 1080
WIN = pg.display.set_mode( ( WIDTH, HEIGHT ), pg.RESIZABLE )
pg.display.set_caption( "minesweeper" )

def main( window : pg.Surface ):
    pg.init()

    clock = pg.time.Clock()
    run, game_status, field_generated = True, 'r', False
    while run:        
        clock.tick( 60 )
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run = False

            if game_status == 'r':
                if not field_generated:
                    game = Game( True, { 'dim': ( 40, 70 ), 'tile_dim' : ( 20, 20 ), 'mines' : 500 }, window )
                    window.fill( (255,255,255) )
                    field_generated = True
                game_status = game.game_loop( event )

            elif game_status == 'l':
                if event.type == pg.MOUSEBUTTONUP:
                    game_status = 'r'
                    field_generated = False

            elif game_status == 'w':
                window.fill( (255,255,255) )
                if event.type == pg.MOUSEBUTTONUP:
                    game_status = 'r'
                    field_generated = False
            
            #if event.type == pg.VIDEORESIZE:
            #    window.fill( (255,255,255) )
            #    minefield.display_field( window )

        font = pg.font.Font( 'assets/Monocraft.otf', 50 )
        text = font.render('test', False, ( 0, 0, 0 ) )
        text_rect = text.get_rect()
        text_rect.topleft = ( 400, 20 )
        window.blit( text, text_rect )
        pg.display.update()

    pg.quit()

if __name__ == "__main__":
    main( WIN )
