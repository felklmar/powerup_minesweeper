import copy
import pygame as pg
from button import Button

D = (
    # non powerup difficulties
    (    'Can I play, Daddy?', [  9,  9,  10, 0 ] ), 
    (       'Don\'t hurt me.', [ 16, 16,  40, 0 ] ),
    (        'Bring \'em on!', [ 20, 24,  99, 0 ] ),
    ( 'I am Death incarnate!', [ 36, 50, 450, 0 ] ),

    # powerup difficulties
    (    'Can I play, Daddy?', [  9,  9,  10,  5 ] ), 
    (       'Don\'t hurt me.', [ 16, 16,  40, 13 ] ),
    (        'Bring \'em on!', [ 20, 24,  99, 23 ] ),
    ( 'I am Death incarnate!', [ 36, 50, 450, 89 ] ),
)

MIN = (
    # height
    9,
    # width
    9,
    # mines
    10,
    # tokens
    0
)

MAX = ( 40, 70 )

def get_text_rect( text, coords : tuple ):
    rect = text.get_rect()
    rect.topleft = coords
    return rect

class Menu:
    def __init__( self, window : pg.Surface ):
        self.m_window = window
        self.m_font = pg.font.Font( 'assets/Monocraft.otf', 20 )
        self.m_buttons = [
            Button( (  10, 10 ), ( 50, 50, 50 ), [ self.m_font, 'start', 'start' ] ),
            Button( (  50, 10 ), ( 50, 50, 50 ), [ self.m_font, 'mode', 'mode' ] ),
            Button( (  90, 10 ), ( 50, 50, 50 ), [ self.m_font, 'diffc', 'difficulty' ] ),
            Button( ( 130, 10 ), ( 50, 50, 50 ), [ self.m_font, 'end', 'end' ] ),

            Button( ( 170,  10 ), ( 50, 50, 50 ), [ self.m_font, 'h_<', '<' ] ),
            Button( ( 170, 100 ), ( 50, 50, 50 ), [ self.m_font, 'h_>', '>' ] ),
            Button( ( 210,  10 ), ( 50, 50, 50 ), [ self.m_font, 'w_<', '<' ] ),
            Button( ( 210, 100 ), ( 50, 50, 50 ), [ self.m_font, 'w_>', '>' ] ),
            Button( ( 250,  10 ), ( 50, 50, 50 ), [ self.m_font, 'm_<', '<' ] ),
            Button( ( 250, 100 ), ( 50, 50, 50 ), [ self.m_font, 'm_>', '>' ] ),
            Button( ( 290,  10 ), ( 50, 50, 50 ), [ self.m_font, 't_<', '<' ] ),
            Button( ( 290, 100 ), ( 50, 50, 50 ), [ self.m_font, 't_>', '>' ] ),
        ]
        self.m_game_settings = copy.deepcopy( D[0][1] )
        self.m_d_idx = 0
        self.m_powerups = False

    def default( self ):
        self.m_game_settings = copy.deepcopy( D[0][1] )
        self.m_d_idx = 0
        self.m_powerups = False

    def height( self ):
        return self.m_game_settings[0]

    def width( self ):
        return self.m_game_settings[1]

    def mines( self ):
        return self.m_game_settings[2]

    def tokens( self ):
        return self.m_game_settings[3]

    def __settings_display( self ):
        height = self.m_font.render( str( self.m_game_settings[0] ), False, ( 255, 255, 255 ) )
        h_rect = get_text_rect( height, ( 35, 170 ) )
        self.m_window.blit( height, h_rect )

        width = self.m_font.render( str( self.m_game_settings[1] ), False, ( 255, 255, 255 ) )
        w_rect = get_text_rect( width, ( 35, 210 ) )
        self.m_window.blit( width, w_rect )

        mines = self.m_font.render( str( self.m_game_settings[2] ), False, ( 255, 255, 255 ) )
        m_rect = get_text_rect( mines, ( 35, 250 ) )
        self.m_window.blit( mines, m_rect )

        tokens = self.m_font.render( str( self.m_game_settings[3] ), False, ( 255, 255, 255 ) )
        t_rect = get_text_rect( tokens, ( 35, 290 ) )
        self.m_window.blit( tokens, t_rect )

    def __increase( self, event, idx ):
        height = self.height()
        width = self.width()
        mines = self.mines()
        tokens = self.tokens()

        if idx == 2:
            maximum = ( height - 1 )*( width - 1) 
        elif idx == 3:
            maximum = ( height*width ) - mines
        else:
            maximum = MAX[idx]

        if event.button == 1:
            self.m_game_settings[idx] += 1
        if event.button == 2:
            self.m_game_settings[idx] = maximum
        if event.button == 3:            
            self.m_game_settings[idx] += 5
        
        if self.m_game_settings[idx] > maximum: 
            self.m_game_settings[idx] = maximum

        mines = self.mines()
        if tokens > ( ( height*width ) - mines ):
            self.m_game_settings[3] = ( height*width ) - mines

    def __decrease( self, event, idx ):
        if event.button == 1:
            self.m_game_settings[idx] -= 1
        if event.button == 2:
            self.m_game_settings[idx] = MIN[idx]
        if event.button == 3:            
            self.m_game_settings[idx] -= 5

        if self.m_game_settings[idx] < MIN[idx]: 
            self.m_game_settings[idx] = MIN[idx]

    def customization_buttons( self, event, btn ):
        if btn == 'h_>':
            self.__increase( event, 0 )

        if btn == 'h_<':
            self.__decrease( event, 0 )

        if btn == 'w_>':
            self.__increase( event, 1 )

        if btn == 'w_<':
            self.__decrease( event, 1 )

        if btn == 'm_>':
            self.__increase( event, 2 )

        if btn == 'm_<':
            self.__decrease( event, 2 )

        if btn == 't_>':
            self.__increase( event, 3 )

        if btn == 't_<':
            self.__decrease( event, 3 )

    def display( self ):
        mode = 'powerup' if self.m_powerups else 'classic'
        text = self.m_font.render( mode, False, ( 255, 255, 255 ) )
        text_rect = text.get_rect()
        text_rect.topleft = ( 100, 50 )

        text2 = self.m_font.render( D[self.m_d_idx][0], False, ( 255, 255, 255 ) )
        text2_rect = text2.get_rect()
        text2_rect.topleft = ( 200, 90 )

        self.m_window.blit( text, text_rect )
        self.m_window.blit( text2, text2_rect )

        self.__settings_display()
        for button in self.m_buttons:
            button.display( self.m_window )

    def click( self, event ) -> str:
        for button in self.m_buttons:
            #print( self.m_powerups )
            if event.type == pg.MOUSEBUTTONUP and button.is_cursor_on():
                if button.name() == 'mode':
                    self.m_powerups = not self.m_powerups

                if button.name() == 'diffc':
                    self.m_d_idx = self.m_d_idx + 1 if self.m_d_idx < 3 else 0

                if button.name() in ( 'mode', 'diffc' ):
                    if self.m_powerups:
                        self.m_game_settings = copy.deepcopy( D[self.m_d_idx + 4][1] )
                    else: 
                        self.m_game_settings = copy.deepcopy( D[self.m_d_idx][1] )

                self.customization_buttons( event, button.name() )
                print( self.m_powerups, self.m_game_settings, D[0][1] )
                return button.name()

        return 'none'
