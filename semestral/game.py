from minefield import *
from tile import TILES

WIDTH, HEIGHT = 1920, 1080
WIN = pg.display.set_mode( ( WIDTH, HEIGHT ), pg.RESIZABLE )
pg.display.set_caption( "minesweeper" )

def main( window : pg.Surface ):
    clock = pg.time.Clock()
    m = Minefield( 10, 10, 50, 10, window )
    run, game_status = True, 'r'
    fullscreen = False
    window.fill( (255,255,255) )
    m.display_field()
    while run:
        clock.tick( 60 )
        for event in pg.event.get():
            #print( game_status )
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.VIDEORESIZE:
                window.fill( (255,255,255) )
                m.display_field()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run = False
                if event.key == pg.K_f:
                    fullscreen = not fullscreen
                    if fullscreen:
                        window = pg.display.set_mode( ( WIDTH, HEIGHT ), pg.FULLSCREEN )
                    else:
                        window = pg.display.set_mode( ( WIDTH, HEIGHT ), pg.RESIZABLE )       

            if game_status == 'r':
                if event.type == pg.MOUSEBUTTONUP:
                    game_status = m.check_click( event.button )
                    m.display_field()
            elif game_status == 'l':
                window.fill( (255,255,255) )
                m.display_field()
                if event.type == pg.MOUSEBUTTONUP:
                    run = False
            elif game_status == 'w':
                window.fill( (255,255,255) )
                if event.type == pg.MOUSEBUTTONUP:
                    run = False
                    
        pg.display.update()

    pg.quit()

if __name__ == "__main__":
    main( WIN )