from kivy.config import Config

Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '563')

import antidata
import random

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ListProperty, ObjectProperty, NumericProperty, partial
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.card import MDCard

from widgetsmenu import MenuButton, MenuLabel, MenuToggleButton
from widgetsgame import AntiCard, Sorcerer, Skipping, Codex


class HomeScreen(Screen):
    game_mode = None
    game_saved = False

    # def on_pre_enter(self, *args):
    #     AntiCard.instantiate_from_csv()

    def on_pre_enter(self, *args):
        print('HomeScreen.on_pre_enter')
        MDApp.get_running_app().screen_history('Home')

    # def test(self):
    #     for i in AntiCard.all:
    #         if repr(i) == 'Flame: Purple, Number: 1, Icon: Ring':
    #             print('Yes')
    #         else:
    #             print('no')

    def solo_game(self):
        print('HomeScreen.solo_game')
        self.game_mode = "GameSolo"
        MDApp.get_running_app().sm.get_screen('ContinueNewSolo').continue_game = False
        if antidata.solo_check_saves():
            MDApp.get_running_app().sm.current = "ContinueNewSolo"
        else:
            MDApp.get_running_app().sm.current = "SoloLevel"



# class ContinueNextPop(Widget):
#     def __init__(self, **kwargs):
#         super(ContinueNextPop, self).__init__(**kwargs)
#
#         # Background button
#         # background_layout = BoxLayout(size=self.size)
#         # self.add_widget(background_layout)
#         # background = Button(background_color=(1, 1, 1, .4))
#         # background_layout.add_widget(background)
#
#
#         # Popup window message
#         pop_layout = BoxLayout(size_hint=(None, None),
#                                size=(self.width * .6, self.height * .6),
#                                pos=(self.width * .2, self.height * .2),
#                                orientation='vertical',
#                                padding=(15, 0, 15, 15)
#                                )
#         self.add_widget(pop_layout)
#
#         question = Label(text='Do you want to resume your paused game,\nor start a new one?',
#                          halign='center',
#                          valign='bottom',
#                          color=(.1, .1, .1, 1),
#                          font_size=pop_layout.height * .075)
#         pop_layout.add_widget(question)
#
#         buttons = BoxLayout(orientation='vertical',
#                             size_hint=(1, 1.5),
#                             padding=(15, 0, 15, 15),
#                             spacing=40)
#         pop_layout.add_widget(buttons)
#
#         options = BoxLayout(spacing=40)
#         buttons.add_widget(options)
#
#         c = Button(text='Continue', background_color=(1, 0, 0, 1))
#         options.add_widget(c)
#         n = Button(text='New Game')
#         options.add_widget(n)
#
#         b = Button(text='Cancel')
#         buttons.add_widget(b)
#
#         with pop_layout.canvas.before:
#             Color(0, 0, 0, .3)
#             Rectangle(size=self.size)
#             Color(1, 1, 1, 1)
#             RoundedRectangle(size=pop_layout.size,
#                              pos=pop_layout.pos,
#                              radius=[20])


class HowToPlayScreen(Screen):

    def test(self):
        MDApp.get_running_app().get_previous_screen()
        # MDApp.get_running_app().sm.current = MDApp.get_running_app().sm.previous()
        print('test')

    def on_leave(self, *args):
        MDApp.get_running_app().screen_history('HowTo')


class Statistics(Screen):

    def on_leave(self, *args):
        MDApp.get_running_app().screen_history('Statistics')


class Settings(Screen):
    def on_leave(self, *args):
        MDApp.get_running_app().screen_history('Settings')


class ContinueNewSoloGameScreen(Screen):
    continue_game = False

    def on_pre_enter(self, *args):
        print('ContinueNewSoloGameScreen.on_pre_enter')

    def continue_solo_game(self):
        print('ContinueNewSoloGameScreen.continue_solo_game')
        self.continue_game = True
        MDApp.get_running_app().sm.current = 'Loading'

    def new_solo_game(self):
        print('ContinueNewSoloGameScreen.new_solo_game')
        self.continue_game = False
        MDApp.get_running_app().sm.current = 'SoloLevel'


class SoloLevelScreen(Screen):
    counter = NumericProperty(3)
    crystals = NumericProperty(5)

    reliquary = ObjectProperty(None)

    def on_pre_enter(self, *args):
        print('SoloLevelScreen.on_pre_enter')

    def difficulty_level(self, button):
        print(f'SoloLevelScreen.difficulty_level - {button.text}')
        if button.text == 'Easy':
            self.counter = 4
            self.crystals = 5
        elif button.text == 'Standard':
            self.counter = 3
            self.crystals = 5
        elif button.text == 'Hard':
            self.counter = 3
            self.crystals = 6
        if button.state == 'normal':
            button.state = 'down'

    def reliquary_level(self, button):
        print(f'SoloLevelScreen.reliquary_level {button.state}')
        if button.state == 'down':
            self.reliquary = True
        else:
            self.reliquary = False

    def get_counter(self):
        print(f'SoloLevelScreen.get_counter {self.counter}')
        return self.counter

    def get_crystals(self):
        print(f'SoloLevelScreen.get_crystals {self.crystals}')
        return self.crystals

    def on_leave(self, *args):
        MDApp.get_running_app().screen_history('SoloLevel')


class AILevelScreen(Screen):
    ai_difficulty = 'Standard'
    player_side = 'Back'

    def difficulty_level(self, button):
        print(button.state)
        if button.state == 'normal':
            button.state = 'down'

        if button.text == 'Easy':
            self.difficulty = 'Easy'
        elif button.text == 'Standard':
            self.difficulty = 'Standard'
        elif button.text == 'Hard':
            self.difficulty = 'Hard'

    def position_player(self, button):
        if button.state == 'normal':
            button.state = 'down'

        if button.text == 'Yes':
            self.player_side = 'Back'
        elif button.text == 'No':
            self.player_side = 'Front'

    def on_leave(self, *args):
        MDApp.get_running_app().screen_history('AILevel')


class LoadingScreen(Screen):
    card_size = ListProperty([0, 0])
    width_gap = NumericProperty(0)
    height_gap = NumericProperty(0)

    def on_size(self, *args):
        print('LoadingScreen.on_size')
        width_based_size = (self.width * 0.8 / 9, self.width * 0.8 / 9 * 1.778)
        height_based_size = (self.height * 0.9 / 3 * .563, self.height * 0.9 / 3)
        self.card_size = min(width_based_size, height_based_size)
        print(f'LoadingScreen.on_size - card_size: {self.card_size}')
        self.width_gap = (self.width - self.card_size[0] * 9) / 10
        print(f'LoadingScreen.on_size - width_gap: {self.width_gap}')
        self.height_gap = (self.height - self.card_size[1] * 3) / 4
        print(f'LoadingScreen.on_size - height_gap: {self.height_gap}')

    def on_enter(self):
        print('LoadingScreen.on_enter')
        Clock.schedule_once(self.go_to_game, 1)

    def go_to_game(self, *args):
        print('LoadingScreen.go_to_game')
        home = MDApp.get_running_app().sm.get_screen('Home')
        game_mode = home.game_mode
        MDApp.get_running_app().sm.current = game_mode


class GameMenuScreen(Screen):

    def on_pre_enter(self, *args):
        print('GameMenuScreen.on_pre_enter')
        self.game_mode = MDApp.get_running_app().sm.get_screen('Home').game_mode
        self.screen = MDApp.get_running_app().sm.get_screen(self.game_mode)

    def go_back(self):
        print('GameMenuScreen.go_back')
        MDApp.get_running_app().sm.current = self.game_mode

    def restart(self):
        print('GameMenuScreen.restart')
        self.screen.restart()
        MDApp.get_running_app().sm.current = self.game_mode

    def go_home(self):
        print('GameMenuScreen.go_home')
        self.screen.save_quit()
        MDApp.get_running_app().sm.current = 'Home'


class GameSoloScreen(Screen):
    hand_cards = []
    table_cards = []
    deck = []
    reliquary_cards = []
    reliquary_level = False
    counter = NumericProperty(0)
    counter_max = NumericProperty(0)
    crystals = NumericProperty(0)
    crystals_target = NumericProperty(0)
    sorcerer = ObjectProperty('None')
    codex = ObjectProperty('None')

    card_size = ListProperty([0, 0])
    width_gap = NumericProperty(0)
    height_gap = NumericProperty(0)

    skipping_button = ObjectProperty()

    past = ObjectProperty('no')
    future = ObjectProperty('no')

    final_score = ObjectProperty('Something is wrong here')

    started_game = False

    def on_pre_enter(self, *args):
        print('GameSoloScreen.on_pre_enter')
        size = MDApp.get_running_app().sm.get_screen('Loading')
        self.card_size = size.card_size
        self.width_gap = size.width_gap
        self.height_gap = size.height_gap

        continue_game = MDApp.get_running_app().sm.get_screen('ContinueNewSolo').continue_game

        # Start a new game
        if not self.started_game and not continue_game:
            self.new_game()

        # Load saved game
        if not self.started_game and continue_game:
            self.game_to_load = antidata.solo_get_last_save()
            self.load_game()

        # Set variable a game has started to avoid issue
        # It's used when coming back from GameMenuScreen
        self.started_game = True

    def new_game(self):
        print('GameSoloScreen.new_game')

        # Deleting previous saved game and create new table
        antidata.solo_delete_all()
        antidata.solo_create_table()

        # Collect all cards and divide them
        # between game cards and solo cards
        all_cards = AntiCard.all.copy()
        print(f'All cards, {len(all_cards)}: {all_cards}')

        flame_cards = list(all_cards[0:16])
        random.shuffle(flame_cards)
        print(f'All Flames, {len(flame_cards)}: {flame_cards}')

        solo_cards = list(all_cards[16:])
        print(f'All Solo, {len(solo_cards)}: {solo_cards}')

        # Deal 3 cards to the hand
        self.hand_cards = flame_cards[0:3]
        print(f'Hand cards: {self.hand_cards}')

        # Deal 9 cards on the table. The Continuum
        self.table_cards = flame_cards[3:12]
        print(f'Table cards: {self.table_cards}')

        # Prepare the draw deck
        self.deck = flame_cards[12:15] + solo_cards
        random.shuffle(self.deck)
        print(f'Deck cards: {self.deck}')

        # Prepare Sorcerer
        self.sorcerer.reposition(0)

        # Prepare Codex
        self.codex.active_flame = self.table_cards[0].flame
        print(f'Codex: {self.codex.active_flame}')

        # Set game difficulty (game level)
        level = MDApp.get_running_app().sm.get_screen('SoloLevel')
        self.counter_max = level.get_counter()
        print(f'Counter Max: {self.counter_max}')
        self.counter = self.counter_max
        self.crystals_target = level.get_crystals()
        print(f'Crystals Target: {self.crystals_target}')
        self.crystals = 0
        self.reliquary_level = level.reliquary
        print(f'Reliquary: {self.reliquary_level}')

        # Adding all the widgets to the table
        self.arrange_board()

        # Start game
        self.set_first_sorcerer()

    def load_game(self):
        print('GameSoloScreen.load_game')

        if not self.game_to_load:
            print('GameSoloScreen.load_game - No more saves')
            return

        # Reset deletes all current widgets from the screen
        self.reset_game()

        # Deal 3 cards to the hand
        self.hand_cards = self.matching_cards(self.game_to_load[0])
        print(f'Hand cards: {self.hand_cards}')

        # Deal 9 cards on the table. The Continuum
        self.table_cards = self.matching_cards(self.game_to_load[1])
        print(f'Table cards: {self.table_cards}')

        # Prepare the draw deck
        self.deck = self.matching_cards(self.game_to_load[2])
        print(f'Deck cards: {self.deck}')

        # Prepare Sorcerer
        self.sorcerer.reposition(self.game_to_load[3])
        print(f'Sorcerer position: {self.sorcerer.position}')

        # Prepare Codex
        self.codex.active_flame = self.game_to_load[4]
        print(f'Codex: {self.codex.active_flame}')

        # Set game difficulty (game level)
        self.counter = self.game_to_load[5]
        self.counter_max = self.game_to_load[6]
        self.crystals = self.game_to_load[7]
        self.crystals_target = self.game_to_load[8]

        # Set Reliquary
        self.reliquary_level = self.game_to_load[10]
        self.reliquary_cards = self.matching_cards(self.game_to_load[11])
        print(f'Reliquary cards: {self.reliquary_cards}')

        # Adding all the widgets to the table
        self.arrange_board()

        antidata.solo_delete_last_save()

        # Set stage of the saved game
        eval('self.' + self.game_to_load[9] + '()')

    def matching_cards(self, item_list):
        print('GameSoloScreen.matching_cards')
        print(f'Item List: {item_list}')
        card_list = []
        for string in item_list:
            for card in AntiCard.all:
                if string == str(card):
                    # print(card)
                    card_list.append(card)
                    break
        return card_list

    # Method to be shared between methods new_game and load_games
    # To add all the widgets on the screen
    def arrange_board(self):
        print('GameSoloScreen.arrange_board')
        width_card_space = self.card_size[0] + self.width_gap
        height_card_space = self.card_size[1] + self.height_gap

        # HAND CARDS
        n = 0
        for i in self.hand_cards:
            print(f'Hand card - Adding widget: {i}', end=' ')
            start_point = self.width / 2 - self.card_size[0] * 1.5 - self.width_gap
            i.move(pos=(start_point + width_card_space * n, self.height_gap))
            i.resize(size=self.card_size)
            i.update_color()
            i.location = 'Hand'
            self.add_widget(i)
            n = n + 1
        print('Finish adding Hand card widgets')

        # TABLE CARDS
        n = 0
        for i in self.table_cards:
            print(f'Table card - Adding widget: {i}', end=' ')
            i.move(pos=((self.width_gap + width_card_space * n), self.height_gap + height_card_space))
            i.resize(size=self.card_size)
            i.update_color()
            i.location = 'Table'
            i.position = n
            self.add_widget(i)
            n = n + 1
        print('Finish adding Table card widgets')

        # SORCERER
        p = int(self.sorcerer.position)
        self.sorcerer.resize(self.table_cards[p], self.width_gap, self.height_gap, 'Front')

        # CODEX
        print(f'Codex -Adding widget: {self.codex.active_flame}')
        self.codex.move_indicator()

        # RELIQUARY
        n = 0
        print(f'Reliquary card - Adding widget:', end=' ')
        for i in self.reliquary_cards:
            print(f' {i},', end=' ')
            i.resize(size=self.card_size)
            self.place_card_in_reliquary(i, n)
            self.add_widget(i)
            n = n + 1
        print(' Finish adding Reliquary card widgets')

    def place_card_in_reliquary(self, card, pos, *args):
        # self.add_widget()
        # pass
        card.disabled = True
        card.update_color()
        n = self.width_gap + self.card_size[0]
        card.move(pos=(self.width_gap + n * (6 - pos), self.height_gap * 3 + self.card_size[1] * 2))

    def set_first_sorcerer(self):
        print('GameSoloScreen.set_first_sorcerer')
        self.skipping_button.disabled = True
        self.disabled_hand_cards()
        for i in self.table_cards:
            if i.flame != self.codex.active_flame:
                i.disabled = True
                i.update_color()
            else:
                i.disabled = False
                i.update_color()
        AntiCard.stage = 'set_first_sorcerer'
        self.save_game('set_first_sorcerer')

    def move_sorcerer(self, card):
        print('GameSoloScreen.move_sorcerer')
        self.sorcerer.moving(card)
        self.stage_one()

    # SELECT HAND CARD FOR MOVEMENT
    def stage_one(self, *args):
        print('GameSoloScreen.stage_one')
        self.disable_table_cards()
        self.enable_hand_cards()
        if len(self.deck) > 0:
            self.skipping_button.disabled = False
        else:
            self.skipping_button.disabled = True
        self.undo_button.disabled = False

        AntiCard.active_card = None

        AntiCard.stage = 'stage_one'
        self.save_game('stage_one')

    # SELECT TABLE CARD FOR DESTINATION
    def stage_two(self, card):
        print('GameSoloScreen.stage_two')

        # Disabling unselected hand cards
        for i in self.hand_cards:
            if i != card:
                disable_card(i)
            else:
                AntiCard.active_card = card

        # Enabling matching table cards
        for i in self.table_cards:
            if i.position < self.sorcerer.position and (i.flame != 'Depleted' or card.flame != 'Depleted') and (i.flame == card.flame or i.icon == card.icon) and i.flame != 'Solar':
                enable_card(i)
        for i in card.number:
            n = int(self.sorcerer.position) + int(i)
            if n < 9 and self.table_cards[n].icon != 'Sun':
                enable_card(self.table_cards[n])

        # Setup game stage on cards
        AntiCard.stage = 'stage_two'

    def swap_relic_cards(self, table):
        print('GameSoloScreen.swap_relic_cards')
        self.disable_table_cards()
        self.disabled_hand_cards()
        self.skipping_button.disabled = True
        self.sorcerer.moving(table)

        hand = AntiCard.active_card

        fadeout_card(hand)
        fadeout_card(table)

        swap_card_in_list(hand, self.hand_cards, table, self.table_cards)

        Clock.schedule_once(partial(swap_card_pos, hand, table), .3)
        Clock.schedule_once(partial(fadein_card, hand), .3)
        Clock.schedule_once(partial(fadein_card, table), .3)
        Clock.schedule_once(self.paradox_check, .6)

    # CHECK IF A PARADOX IS FORMED AFTER CARD SWAP
    def paradox_check(self, *args):
        print('GameSoloScreen.paradox_check')
        x = self.hand_cards

        # Actions if there is a paradox
        if ((x[0].flame == x[1].flame == x[2].flame)
            or (x[0].number == x[1].number == x[2].number)
            or (x[0].icon == x[1].icon == x[2].icon)) \
                and 'Depleted' != x[0].flame != self.codex.active_flame \
                and 'Depleted' != x[1].flame != self.codex.active_flame \
                and 'Depleted' != x[2].flame != self.codex.active_flame:
            print('Paradox!')
            self.crystals = self.crystals + 1
            if self.crystals == self.crystals_target:
                print('YOU WON!')
                self.final_score = 'Win'
                self.endgame()
            else:
                s = self.sorcerer.position
                print(f'Sorcerer position {s}')

                if 0 <= s <= 5\
                        and self.table_cards[s+1].flame != 'Solar'\
                        and self.table_cards[s+2].flame != 'Solar'\
                        and self.table_cards[s+3].flame != 'Solar':
                    self.future = True
                else:
                    self.future = False

                if 3 <= s <= 8 \
                        and self.table_cards[s-1].flame != 'Solar'\
                        and self.table_cards[s-2].flame != 'Solar'\
                        and self.table_cards[s-3].flame != 'Solar':
                    self.past = True
                else:
                    self.past = False

                if self.past or self.future:
                    self.codex.advance_codex()
                    self.stage_four()
                else:
                    print('LOST!')
                    self.final_score = 'Lose'
                    self.endgame()

        # Actions if there is no paradox
        else:
            self.counter = self.counter - 1
            print(f'Counter: {self.counter}')
            if self.counter != 0:
                self.stage_one()
            elif len(self.deck) != 0:
                self.stage_three()
                self.counter = self.counter_max
            else:
                print('LOST!')
                self.final_score = 'Lose'
                self.endgame()

    # SELECT TABLE CARD TO BE REPLACED IN CASE OF NO PARADOX
    def stage_three(self):
        print('GameSoloScreen.stage_three')

        # Add replacement card on the table
        self.add_replacement_card()

        # Disable Hand Cards and Skip Button
        self.disabled_hand_cards()
        self.skipping_button.disabled = True

        # Enabling matching table cards because must be replaced
        card = AntiCard.active_card
        matching_cards = 0
        for i in self.table_cards:
            if i.flame == 'Solar' and card.flame != 'Solar' and card.number in i.number:
                enable_card(i)
                matching_cards = matching_cards + 1
            elif i.flame != 'Solar' \
                    and (i.flame != 'Depleted' or card.flame != 'Depleted')\
                    and (i.flame == card.flame or i.number in card.number or i.icon == card.icon):
                enable_card(i)
                matching_cards = matching_cards + 1
            else:
                disable_card(i)

        # Enabling all table cards if no matching cards on table
        if matching_cards == 0:
            self.enable_table_cards()

        AntiCard.stage = 'stage_three'
        self.save_game('stage_three')

    def add_replacement_card(self):
        print('GameSoloScreen.add_replacement_card')
        replace_card = self.deck[0]
        replace_card.disabled = True
        replace_card.move(pos=(self.width_gap * 2 + self.card_size[0], self.height_gap * 3 + self.card_size[1] * 2))
        replace_card.resize(size=self.card_size)
        self.add_widget(replace_card)
        AntiCard.active_card = replace_card

    def replace_table_card(self, table):
        print('GameSoloScreen.replace_table_card')
        new = AntiCard.active_card
        self.deck.remove(new)

        fadeout_card(new)
        fadeout_card(table)

        ti = self.table_cards.index(table)
        self.table_cards.remove(table)
        self.table_cards.insert(ti, new)
        new.location = table.location
        new.position = ti

        Clock.schedule_once(partial(swap_card_pos, new, table), .3)
        Clock.schedule_once(partial(fadein_card, new), .3)
        Clock.schedule_once(partial(self.move_card_to_reliquary, table), .3)
        print(f'Number of reliquary cards: {len(self.reliquary_cards)}')
        if len(self.reliquary_cards) > 4:
            Clock.schedule_once(self.chose_reliquary_card, .6)
        else:
            Clock.schedule_once(self.stage_one, .6)

    def move_card_to_reliquary(self, card, *args):
        print('GameSoloScreen.move_card_to_reliquary')
        # self.remove_widget(card)
        # card.disabled = True
        # card.update_color()
        if self.reliquary_level and card.flame != "Solar" and card.flame != "Depleted":
            self.reliquary_cards.append(card)
            pos = len(self.reliquary_cards) - 1
            self.place_card_in_reliquary(card, pos)
            fadein_card(card)
        else:
            self.remove_widget(card)

    def chose_reliquary_card(self, *args):
        print('GameSoloScreen.chose_reliquary_card')
        # Disable Table and Hand cards, no used during this phase
        self.disabled_hand_cards()
        self.disable_table_cards()

        print(f'Number of reliquary cards: {len(self.reliquary_cards)}')
        # Enable Reliquary Cards
        for i in self.reliquary_cards:
            i.disabled = False
            i.update_color()

        AntiCard.stage = "chose_reliquary_card"

    def remove_reliquary_card(self, card):
        print('GameSoloScreen.remove_reliquary_card')

        for i in self.reliquary_cards:
            i.disabled = True
            fadeout_card(i)

        self.reliquary_cards.remove(card)

        n = 0
        for i in self.reliquary_cards:
            print(f'Reliquary card - relocate card: {i}', end=' ')
            Clock.schedule_once(partial(self.place_card_in_reliquary, i, n), .3)
            # self.place_card_in_reliquary(i, n)
            n = n + 1
        print('Finish relocating Reliquary card')

        for i in self.reliquary_cards:
            Clock.schedule_once(partial(fadein_card, i), .3)

        Clock.schedule_once(partial(self.remove_card_widget, card), .3)
        # self.remove_widget(card)

        Clock.schedule_once(self.stage_one, .6)

    def remove_card_widget(self, card, *args):
        self.remove_widget(card)

    # SELECT HAND CARD TO BE REPLACED IF PARADOX
    def stage_four(self):
        print('GameSoloScreen.stage_four')

        # Add replacement card on the table
        self.add_replacement_card()

        # Disable Table Cards and Skip Button
        self.disable_table_cards()
        self.skipping_button.disabled = True

        # Enable Hand cards because one must be replaced
        self.enable_hand_cards()

        AntiCard.stage = 'stage_four'
        self.save_game('stage_four')

    def replace_hand_card(self, hand):
        print('GameSoloScreen.replace_hand_card')
        self.disabled_hand_cards()

        new = AntiCard.active_card
        self.deck.remove(new)

        fadeout_card(new)
        fadeout_card(hand)

        hi = self.hand_cards.index(hand)
        self.hand_cards.remove(hand)
        self.hand_cards.insert(hi, new)
        new.location = hand.location
        new.position = hi

        Clock.schedule_once(partial(swap_card_pos, new, hand), .3)
        Clock.schedule_once(partial(fadein_card, new), .3)
        Clock.schedule_once(partial(self.move_card_to_reliquary, hand), .3)
        Clock.schedule_once(self.stage_five, .6)

    def stage_five(self, *args):
        print('GameSoloScreen.stage_five')

        # Disable Hand Cards and Skip Button
        self.disable_table_cards()
        self.disabled_hand_cards()
        self.skipping_button.disabled = True

        s = self.sorcerer.position
        if 3 <= s <= 8 \
                and self.table_cards[s - 1].flame != 'Solar' \
                and self.table_cards[s - 2].flame != 'Solar' \
                and self.table_cards[s - 3].flame != 'Solar':
            for i in self.table_cards[s-3:s]:
                enable_card(i)

        if 0 <= s <= 5 \
                and self.table_cards[s + 1].flame != 'Solar' \
                and self.table_cards[s + 2].flame != 'Solar' \
                and self.table_cards[s + 3].flame != 'Solar':
            for i in self.table_cards[s+1:s+4]:
                enable_card(i)

        AntiCard.stage = 'stage_five'
        self.save_game('stage_five')

    def swap_full_hand(self, card):
        print('GameSoloScreen.swap_full_hand')
        self.disable_table_cards()
        s = self.sorcerer.position

        random.shuffle(self.hand_cards)

        h = 0
        if card.position < s:
            for table in self.table_cards[s-3:s]:
                hand = self.hand_cards[h]
                fadeout_card(table)
                fadeout_card(hand)
                swap_card_in_list(hand, self.hand_cards, table, self.table_cards)
                Clock.schedule_once(partial(swap_card_pos, hand, table), .3)
                Clock.schedule_once(partial(fadein_card, hand), .3)
                Clock.schedule_once(partial(fadein_card, table), .3)
                h = h + 1

        elif card.position > s:
            for table in self.table_cards[s+1:s+4]:
                hand = self.hand_cards[h]
                fadeout_card(table)
                fadeout_card(hand)
                swap_card_in_list(hand, self.hand_cards, table, self.table_cards)
                Clock.schedule_once(partial(swap_card_pos, hand, table), .3)
                Clock.schedule_once(partial(fadein_card, hand), .3)
                Clock.schedule_once(partial(fadein_card, table), .3)
                h = h + 1

        if len(self.reliquary_cards) > 5:
            Clock.schedule_once(self.chose_reliquary_card, .6)
        else:
            Clock.schedule_once(self.stage_one, .6)

    def endgame(self):
        print('GameSoloScreen.endgame')

        # Disabling all widget on the screen
        self.disabled_hand_cards()
        self.disable_table_cards()
        self.undo_button.disabled = True
        self.skipping_button.disabled = True
        antidata.solo_delete_all()

        message = '???'
        if self.final_score == 'Win':
            message = 'Congratulations you Won!'
        elif self.final_score == 'Lose':
            message = 'You Lose'

        self.endgame_menu = MDCard(orientation='vertical',
                                size_hint=(.5, .5),
                                pos_hint={'center_x': .5, 'center_y': .5},
                                radius=(50, 15, 50, 15),
                                padding=(30, 0, 30, 30),
                                spacing=40)
        self.add_widget(self.endgame_menu)

        lbl = Label(text=message, color=(1, 0, 0, 1))
        self.endgame_menu.add_widget(lbl)

        bx = BoxLayout(orientation='horizontal',
                       spacing=40)
        self.endgame_menu.add_widget(bx)

        btn1 = Button(text='Back', size_hint=(.5, .5),
                      on_release=self.go_back)
        bx.add_widget(btn1)

        btn2 = Button(text='Home', size_hint=(.5, .5))
        bx.add_widget(btn2)

    def go_back(self, obj):
        self.remove_widget(self.endgame_menu)

    def undo_movement(self):
        print('GameSoloScreen.undo_movement')
        self.game_to_load = antidata.solo_get_undo_save()
        self.load_game()

    def restart(self):
        print('GameSoloScreen.restart')

        # Delete all widgets from screen and saved games
        self.reset_game()
        antidata.solo_delete_all()

        # Screen needs to set a game on_pre_enter
        self.started_game = False

        # Ensure it doesn't try to load the last game
        MDApp.get_running_app().sm.get_screen('ContinueNewSolo').continue_game = False

        # Transfer current game level settings
        level = MDApp.get_running_app().sm.get_screen('SoloLevel')
        level.counter = self.counter_max
        level.crystals = self.crystals_target
        level.reliquary = self.reliquary_level

    def save_quit(self):
        print('GameSoloScreen.save_quit')
        # go_home()
        self.reset_game()
        self.started_game = False

    def save_game(self, stage):
        print('GameSoloScreen.save_game')
        antidata.solo_add_save(self.hand_cards,
                               self.table_cards,
                               self.deck,
                               self.sorcerer.position,
                               self.codex.active_flame,
                               self.counter,
                               self.counter_max,
                               self.crystals,
                               self.crystals_target,
                               stage,
                               self.reliquary_level,
                               self.reliquary_cards)

    def reset_game(self):
        print('GameSoloScreen.reset_game')
        # Clear all the screen
        for i in AntiCard.all:
            self.remove_widget(i)
            i.opacity = 1
        self.hand_cards = []
        self.table_cards = []
        self.deck = []
        self.reliquary_cards = []
        # self.counter = 0
        # self.counter_max = 0
        # self.crystals = 0
        # self.crystals_target = 0

    def on_leave(self):
        print('GameSoloScreen.on_leave')
        MDApp.get_running_app().screen_history('GameSolo')

    def enable_table_cards(self):
        for i in self.table_cards:
            enable_card(i)

    def disable_table_cards(self):
        for i in self.table_cards:
            disable_card(i)

    def enable_hand_cards(self):
        for i in self.hand_cards:
            enable_card(i)

    def disabled_hand_cards(self):
        for i in self.hand_cards:
            disable_card(i)


class GameAIScreen(Screen):
    player_cards = []
    ai_cards = []
    table_cards = []
    player_crystals = NumericProperty(0)
    ai_crystals = NumericProperty(0)
    player_sorcerer = ObjectProperty('None')
    ai_sorcerer = ObjectProperty('None')
    codex = ObjectProperty('None')

    ai_difficulty = None
    player_side = None

    card_size = ListProperty([0, 0])
    width_gap = NumericProperty(0)
    height_gap = NumericProperty(0)

    def on_pre_enter(self, *args):

        print('on_pre_enter')
        level = MDApp.get_running_app().sm.get_screen('AILevel')
        self.ai_difficulty = level.ai_difficulty
        self.player_side = level.player_side
        print(f'AI Difficulty: {self.ai_difficulty}')
        print(f'Table side: {self.player_side}')
        size = MDApp.get_running_app().sm.get_screen('Loading')
        self.card_size = size.card_size
        self.width_gap = size.width_gap
        self.height_gap = size.height_gap

    # def on_enter(self, *args):
    #     print('on_enter')

        all_cards = AntiCard.all.copy()
        flame_cards = list(all_cards[0:16])
        random.shuffle(flame_cards)

        width_card_space = self.card_size[0] + self.width_gap
        height_card_space = self.card_size[1] + self.height_gap

        # Set 3 player cards
        for i in range(3):
            c = flame_cards.pop(0)
            start_point = self.width/2 - self.card_size[0] * 1.5 - self.width_gap
            c.move(pos=(start_point + width_card_space * i, self.height_gap))
            c.resize(size=self.card_size)
            c.disabled = True
            c.update_color()
            c.location = 'Hand'
            self.player_cards.append(c)
            self.add_widget(c)

        # Set 3 AI cards
        for i in range(3):
            c = flame_cards.pop(0)
            start_point = self.width/2 - self.card_size[0] * 1.5 - self.width_gap
            c.move(pos=(start_point + width_card_space * i, self.height_gap))
            c.resize(size=self.card_size)
            c.disabled = True
            c.update_color()
            c.location = 'AI'
            self.ai_cards.append(c)

        # Set starting Codex
        del flame_cards[0]
        if self.player_side == 'Front':
            self.codex.active_flame = flame_cards[0].flame
            self.codex.move_indicator()
        elif self.player_side == 'Back':
            self.codex.active_flame = flame_cards[-1].flame
            self.codex.move_indicator()

        # Set 9 table cards
        for i in range(9):
            c = flame_cards.pop(0)
            c.move(pos=((self.width_gap + width_card_space * i), self.height_gap + height_card_space))
            c.resize(size=self.card_size)
            if c.flame != self.codex.active_flame:
                c.disabled = True
            c.update_color()
            c.location = 'Table'
            c.position = i
            self.table_cards.append(c)
            self.add_widget(c)

        # Set Sorcerer positions
        if self.player_side == 'Front':
            self.player_sorcerer.resize(self.table_cards[0], self.width_gap, self.height_gap, 'Front')
            self.player_sorcerer.reposition(self.table_cards[0].position)
            self.ai_sorcerer.resize(self.table_cards[0], self.width_gap, self.height_gap, 'Back')
            self.ai_sorcerer.reposition(self.table_cards[0].position)
        elif self.player_side == 'Back':
            self.player_sorcerer.resize(self.table_cards[-1], self.width_gap, self.height_gap, 'Front')
            self.player_sorcerer.reposition(self.table_cards[-1].position)
            self.ai_sorcerer.resize(self.table_cards[-1], self.width_gap, self.height_gap, 'Back')
            self.ai_sorcerer.reposition(self.table_cards[-1].position)

    def setup(self, card):
        print('Hi here is setup')

    def on_leave(self):
        MDApp.get_running_app().screen_history('GameAI')


def enable_card(card):
    card.disabled = False
    card.update_color()

def disable_card(card):
    card.disabled = True
    card.update_color()

def fadeout_card(card, *args):
    animate = Animation(duration=.25, opacity=0)
    animate.start(card)

def fadein_card(card, *args):
    animate = Animation(duration=.25, opacity=1)
    animate.start(card)

def swap_card_pos(card1, card2, *args):
    pos1 = card1.pos.copy()
    pos2 = card2.pos.copy()
    card1.move(pos=pos2)
    card2.move(pos=pos1)

def swap_card_in_list(hand_card, hand_list, table_card, table_list):
    i1 = hand_list.index(hand_card)
    i2 = table_list.index(table_card)
    hand_list.remove(hand_card)
    table_list.remove(table_card)
    hand_list.insert(i1, table_card)
    table_list.insert(i2, hand_card)
    hand_card.location = 'Table'
    table_card.location = 'Hand'
    hand_card.position = i2


Builder.load_file("maindesign.kv")


class Antilaw(MDApp):
    sm = None
    previous_screen = []

    def build(self):
        AntiCard.instantiate_from_csv()
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Blue'
        self.sm = ScreenManager(transition=FadeTransition(duration=.3))
        self.sm.add_widget(HomeScreen(name='Home'))
        self.sm.add_widget(HowToPlayScreen(name='HowTo'))
        self.sm.add_widget(Statistics(name='Statistics'))
        self.sm.add_widget(Settings(name='Settings'))
        self.sm.add_widget(ContinueNewSoloGameScreen(name='ContinueNewSolo'))
        self.sm.add_widget(SoloLevelScreen(name='SoloLevel'))
        self.sm.add_widget(AILevelScreen(name='AILevel'))
        self.sm.add_widget(LoadingScreen(name='Loading'))
        self.sm.add_widget(GameMenuScreen(name='GameMenu'))
        self.sm.add_widget(GameSoloScreen(name='GameSolo'))
        self.sm.add_widget(GameAIScreen(name='GameAI'))
        self.sm.current = 'Home'
        return self.sm

    def on_pause(self):
        return True

    def key_input(self, window, key, scancode, codepoint, modifier):
        if key == 27:
            return True
        else:
            return False

    def screen_history(self, screen):
        if screen == 'Home':
            self.previous_screen = []

        self.previous_screen.append(screen)

    def get_previous_screen(self):
        if len(self.previous_screen) == 0:
            return
        else:
            s = self.previous_screen.pop(-1)
            self.sm.current = s


Antilaw().run()
