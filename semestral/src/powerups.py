"""
__Module handling powerups__
Contains Powerup class and its children
"""
import random as rd
import pygame as pg
import numpy as np
from src.button import Button
from src.minefield import Minefield
from src.utilities import FONT, OUT_OF_BOUNDS

class Powerup( Button ):
    """Class inherited from class Button representing powerup"""
    def __init__( self, coords : tuple, color : tuple, description : tuple, value : np.uint32 = 0 ):
        """
        Initializes class instance\n
        Args:
            coords (tuple): coordinates for powerup button
            color (tuple): text color
            description (tuple): name, button text and description
            value (np.uint32): cost of powerup. Defaults to 0.
        """
        text = ( pg.font.Font( FONT, 17 ), description[0][0], description[0][1]  )
        super().__init__( coords, color, text )

        self.m_description = description    # powerup description
        self.m_value = value                # value/cost of powerup

        # deactivation of powerup
        self.deactivate( color )

    def apply_powerup( self, window : pg.Surface, minefield: Minefield,
                       offset : dict, mouse_pos : tuple ) -> str:
        """
        Pure virtual method, that applies powerup\n
        Args:
            window (pg.Surface): pygame window/surface on which powerup button should be print
            minefield (Minefield): minefield on which are powerups applied
            mouse_pos (tuple): mouse position
        Returns:
            str: 'applied', 'used', 'not_used'
        """

    def deactivate( self, color : tuple ):
        """
        Deactivates powerup
        Args:
            color (tuple): disabled text color
        """
        self.m_color = color

    def activate( self, tokens : int, color : tuple ):
        """
        Activates powerup if powerup tokens are anough to pay for it\n
        Args:
            tokens (int): powerup tokens
            color (tuple): basic text color
        """
        if tokens >= self.m_value:
            self.m_color = color

    def display_description( self, window : pg.Surface, y_offset : np.uint32  ):
        """
        Displays powerup description on the pygame window\n
        Args:
            window (pg.Surface): pygame window/surface on which tile should display
            y_offset (np.uint32): offset of the displayed description
        """
        center_x = window.get_width()/2
        font = pg.font.Font( FONT, 15 )
        text = font.render( self.m_description[1], True, self.m_color )
        t_rect = text.get_rect()
        t_rect.center = ( center_x, y_offset/2 )
        window.blit( text, t_rect )

class SafeOpen( Powerup ):
    """
    __Class inherited from class Powerup__\n
    Safely reveals tile ( either opens it or flags it )
    """
    def __init__( self, coords : tuple, color : tuple, value : np.uint32 ):
        """
        Initializes class instance\n
        Args:
            coords (tuple): coordinates for powerup button
            color (tuple): text color
            value (np.uint32): cost of powerup
        """
        description = ( ( 'SafeOpen', f'({ value }) Reveal' ),
                        'Reveals selected tile' )
        super().__init__( coords, color, description, value )

    def apply_powerup( self, window : pg.Surface, minefield: Minefield,
                       offset : dict, mouse_pos : tuple ) -> str:
        """
        __Overrided parent method, that applies powerup__\n
        Safely reveals tile ( either opens it or flags it )
        Args:
            window (pg.Surface): pygame window/surface on which powerup button should be print
            minefield (Minefield): minefield on which are powerups applied
            offset (dict): offset to display everything correctly
            mouse_pos (tuple): mouse position
        Returns:
            str: 'applied', 'used', 'not_used'
        """
        c_click = minefield.mouse_pos_to_coords( mouse_pos )
        if c_click != OUT_OF_BOUNDS:
            tile = minefield.m_field[c_click]
            if not tile.is_flag() and not tile.is_open():
                if tile.is_mine():
                    tile.flag()
                else:
                    minefield.open( tile.arr_coords( offset['t'] ) )

                minefield.display_field( window )
                return 'applied'

            minefield.display_field( window )
            return 'used'

        return 'not_used'

class OpenBubble( Powerup ):
    """
    __Class inherited from class Powerup__\n
    Opens random bubble ( tile with zero mines around ) if there is one
    """
    def __init__( self, coords : tuple, color : tuple, value : np.uint32 ):
        """
        Initializes class instance\n
        Args:
            coords (tuple): coordinates for powerup button
            color (tuple): text color
            value (np.uint32): cost of powerup
        """
        description = ( ( 'OpenBubble', f'({ value }) Bubble' ),
                        'Reveals random bubble, if there is one' )
        super().__init__( coords, color, description, value )

    def apply_powerup( self, window : pg.Surface, minefield: Minefield,
                       offset : dict, mouse_pos : tuple ) -> str:
        """
        __Overrided parent method, that applies powerup__\n
        Opens random bubble ( tile with zero mines around ) if there is one
        Args:
            window (pg.Surface): pygame window/surface on which powerup button should be print
            minefield (Minefield): minefield on which are powerups applied
            offset (dict): offset to display everything correctly
            mouse_pos (tuple): mouse position
        Returns:
            str: 'applied', 'used', 'not_used'
        """
        c_click = minefield.mouse_pos_to_coords( mouse_pos )
        if c_click != OUT_OF_BOUNDS:
            check = 0
            while True:
                if check % minefield.m_field.size == 0:
                    if minefield.no_bubbles():
                        break
                check += 1

                col = rd.randint( 0, minefield.height() - 1 )
                row = rd.randint( 0, minefield.width() - 1 )
                c_tile = ( col, row )

                tile = minefield.m_field[c_tile]
                if not tile.is_open() and not tile.is_mine() and tile.mines_around() == 0:
                    minefield.open( c_tile )
                    break

            minefield.display_field( window )
            return 'applied'

        return 'not_used'

class CrossOpen( Powerup ):
    """
    __Class inherited from class Powerup__\n
    Safely opens tiles in 4 directions from clicked tile forming a cross
    """
    def __init__( self, coords : tuple, color : tuple, value : np.uint32, cross_range : np.uint32 ):
        """
        Initializes class instance\n
        Args:
            coords (tuple): coordinates for powerup button
            color (tuple): text color
            value (np.uint32): cost of powerup
            cross_range (int): range of cross
        """
        description = ( ( 'CrossOpen', f'({ value }) Cross' ),
                        'Reveals cross from selected tile' )
        super().__init__( coords, color, description, value )
        self.m_range = cross_range

    def apply_powerup( self, window : pg.Surface, minefield: Minefield,
                       offset : dict, mouse_pos : tuple ) -> str:
        """
        __Overrided parent method, that applies powerup__\n
        Safely opens tiles in 4 directions from clicked tile forming a cross
        Args:
            window (pg.Surface): pygame window/surface on which powerup button should be print
            minefield (Minefield): minefield on which are powerups applied
            offset (dict): offset to display everything correctly
            mouse_pos (tuple): mouse position
        Returns:
            str: 'applied', 'used', 'not_used'
        """
        c_click = minefield.mouse_pos_to_coords( mouse_pos )
        if c_click != OUT_OF_BOUNDS:
            if minefield.m_field[c_click].is_open():
                minefield.display_field( window )
                return 'used'

            field_dim = minefield.dimensions()

            min_y = max( 0, c_click[0] - self.m_range )
            max_y = min( field_dim[1], c_click[0] + self.m_range + 1 )

            min_x = max( 0, c_click[1] - self.m_range )
            max_x = min( field_dim[1], c_click[1] + self.m_range + 1 )

            col = minefield.m_field[ min_y : max_y, c_click[1] ]
            row = minefield.m_field[ c_click[0], min_x : max_x ]

            cross = np.append( col, row )
            for tile in cross:
                if not tile.is_flag():
                    if tile.is_mine():
                        tile.flag()
                    else:
                        minefield.open( tile.arr_coords( offset['t'] ) )

            minefield.display_field( window )
            return 'applied'

        return 'not_used'

class FlagRandom( Powerup ):
    """
    __Class inherited from class Powerup__\n
    Randomly flags m mines or does nothing if number of mines left to flag is less then m
    """
    def __init__( self, coords : tuple, color : tuple, value : np.uint32, mines : np.uint32 ):
        """
        Initializes class instance\n
        Args:
            coords (tuple): coordinates for powerup button
            color (tuple): text color
            value (np.uint32): cost of powerup
            mines (np.uint32): number of mines to flag
        """
        description = ( ( 'FlagRandom', f'({ value }) Flag_{mines}' ),
                        f'Randomly flags {mines} mines' )
        super().__init__( coords, color, description, value )
        self.m_mines = mines

    def apply_powerup( self, window : pg.Surface, minefield: Minefield,
                       offset : dict, mouse_pos : tuple ) -> str:
        """
        __Overrided parent method, that applies powerup__\n
        Randomly flags m mines or does nothing if number of mines left to flag is less then m
        Args:
            window (pg.Surface): pygame window/surface on which powerup button should be print
            minefield (Minefield): minefield on which are powerups applied
            offset (dict): offset to display everything correctly
            mouse_pos (tuple): mouse position
        Returns:
            str: 'applied', 'used', 'not_used'
        """
        c_click = minefield.mouse_pos_to_coords( mouse_pos )
        if c_click != OUT_OF_BOUNDS:
            non_flaged_mines = []
            for mine in minefield.m_mines:
                if not minefield.m_field[mine].is_flag():
                    non_flaged_mines.append( minefield.m_field[mine] )

            if len( non_flaged_mines ) > self.m_mines:
                indexes = rd.sample( range( 0, len( non_flaged_mines ) ), self.m_mines )
                for idx in indexes:
                    non_flaged_mines[idx].flag()

            minefield.display_field( window )
            return 'applied'

        return 'not_used'
