import pygame as pg
from button import Button
from minefield import Minefield

class Powerup( Button ):
    def __init__( self, coords : tuple, dim : tuple, color : tuple ):
        super().__init__( coords, dim, color )

#WIDTH, HEIGHT = 500, 500
#WIN = pg.display.set_mode( ( WIDTH, HEIGHT ), pg.RESIZABLE )

#arr = [ Powerup( (  50, 25 ), ( 100, 100 ), ( 255, 255, 0 ) ), Button( ( 50, 135 ), ( 320, 50 ), ( 0, 255, 255 ) ),
#        Powerup( ( 160, 25 ), ( 100, 100 ), ( 255, 255, 0 ) ), Button( ( 50, 195 ), ( 320, 50 ), ( 0, 255, 255 ) ),
#        Powerup( ( 270, 25 ), ( 100, 100 ), ( 255, 255, 0 ) ), Button( ( 50, 255 ), ( 320, 50 ), ( 0, 255, 255 ) ) ]
#run = True 
#
#def deactivate_buttons( l : list, index ):
#    for idx, i in enumerate( l ):
#        if idx != index:
#            i.deactivate()
#
#def activate_buttons( l : list ):
#    for i in l:
#        i.activate()    
#
#while run:
#    for event in pg.event.get():
#        if event.type == pg.QUIT:
#            run = False
#        for idx, i in enumerate( arr ):
#            if event.type == pg.MOUSEBUTTONUP and i.is_cursor_on():
#                if i.m_color == i.m_default_color:
#                    i.change_color( ( 0, 255, 0 ) )
#                    deactivate_buttons( arr, idx )
#                else:
#                    activate_buttons( arr )
#            i.display( WIN )
#
#    pg.display.update()
#
#pg.quit()