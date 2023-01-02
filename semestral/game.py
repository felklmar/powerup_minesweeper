import pygame as pg
from minefield import Minefield

WIDTH, HEIGHT = 1920, 1080
WIN = pg.display.set_mode( ( WIDTH, HEIGHT ), pg.RESIZABLE )
pg.display.set_caption( "minesweeper" )

def main( window : pg.Surface ):
    clock = pg.time.Clock()
    run, game_status, field_generated = True, 'r', False
    while run:
        clock.tick( 60 )
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.VIDEORESIZE:
                window.fill( (255,255,255) )
                minefield.display_field()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run = False

            if game_status == 'r':
                if not field_generated:
                    minefield = Minefield( ( 40, 70 ), ( 20, 20 ), 500, window )
                    window.fill( (255,255,255) )
                    minefield.display_field()
                    field_generated = True
                if event.type == pg.MOUSEBUTTONUP:
                    game_status = minefield.check_click( event.button )
                    minefield.display_field()
            elif game_status == 'l':
                if event.type == pg.MOUSEBUTTONUP:
                    game_status = 'r'
                    field_generated = False
            elif game_status == 'w':
                window.fill( (255,255,255) )
                if event.type == pg.MOUSEBUTTONUP:
                    game_status = 'r'
                    field_generated = False

        pg.display.update()

    pg.quit()

if __name__ == "__main__":
    main( WIN )
