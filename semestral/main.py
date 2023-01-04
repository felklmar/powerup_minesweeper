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
    run, game_status, field_generated, field_active = True, 'r', False, True
    arr = [ SafeOpen( ( 20, 100 ), ( 50, 50 ), ( 255, 0, 0 ) ),
            OpenBubble( ( 20, 160 ), ( 50, 50 ), ( 0, 0, 255 ) ),
            CrossOpen( ( 20, 220 ), ( 50, 50 ), ( 255, 0, 255 ) ),
            Powerup( ( 20, 280 ), ( 50, 50 ), ( 255, 255, 0 ) ),
            Powerup( ( 20, 340 ), ( 50, 50 ), ( 255, 255, 0 ) ) ]

    active_powerup = -1
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
                    game = Game( True, ( 40, 70 ), ( 20, 20 ), 500, window )
                    #minefield = Minefield( ( 40, 70 ), ( 20, 20 ), 500 )
                    #window = pg.display.set_mode( ( 2*( OFFSET['x'] + OFFSET['t_x'] ) + 70*20, OFFSET['y'] + OFFSET['x'] + 2*OFFSET['t_y'] + 40*20  ) )
                    window.fill( (255,255,255) )
                    field_generated = True

                game_status = game.game_loop( event )
                #if field_active:
                #    color = ( 255, 0, 0, 50 )
                #    if event.type == pg.MOUSEBUTTONUP:
                #        game_status = minefield.check_click( event.button, pg.mouse.get_pos() )
                #        minefield.display_field( window )
                #else:
                #    color = ( 255, 255, 0, 100 )
                #    if event.type == pg.MOUSEBUTTONUP and arr[active_powerup].apply_powerup( window, minefield ):
                #        active_powerup = -1
                #        activate_buttons( arr )
                #        field_active = True
                #minefield.show_cursor( window, color )
                #for idx, i in enumerate( arr ):
                #    if event.type == pg.MOUSEBUTTONUP and i.is_cursor_on():
                #        if i.m_color == i.m_default_color:
                #            i.change_color( ( 0, 255, 0 ) )
                #            deactivate_buttons( arr, idx )
                #            active_powerup = idx
                #            field_active = False
                #        else:
                #            active_powerup = -1
                #            activate_buttons( arr )
                #            field_active = True
                #    i.display( window )

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

        pg.display.update()

    pg.quit()

if __name__ == "__main__":
    main( WIN )
