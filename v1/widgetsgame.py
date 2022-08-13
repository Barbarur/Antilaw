import csv
import random

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle
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


class AntiCard(ButtonBehavior, BoxLayout):
    frame = NumericProperty()
    # f = [0]

    flame = 'Black'
    Color_Dict = {'Red': '#FB98AE', 'Green': '#BEF0A2', 'Blue': '#5DBAE8', 'Purple': '#7851A7', 'Depleted': '#C4BCAA', 'Solar': '#EFDC75'}
    card_color = ObjectProperty('#000000')
    frame_color = ListProperty([.25, .25, .25, .5])
    number = ObjectProperty('9')
    label = ObjectProperty('0')
    icon = 'Skull'
    icon_Dict = {'Key': 'images/key.png', 'Skull': 'images/skull.png', 'Ring': 'images/ring.png', 'Feather': 'images/feather.png', 'Sun': 'images/sun.png'}
    image = ObjectProperty('images/Skull.png')

    all = []

    stage = ObjectProperty('Setup')
    active_card = ObjectProperty(None)

    def __init__(self, flame, number, icon, **kwargs):
        super(AntiCard, self).__init__(**kwargs)
        self.flame = flame
        self.card_color = self.Color_Dict.get(flame)
        # self.frame_color = self.Color_Dict.get(flame)
        if len(number) == 1:
            self.number = number
        else:
            self.number = list(number.split(' '))
        self.label = number.replace(" ", "/")
        self.icon = icon
        self.image = self.icon_Dict.get(icon)

        AntiCard.all.append(self)

        self.position = None
        self.location = None
        self.pos = (0, 0)

    @classmethod
    def instantiate_from_csv(cls):
        with open('RelicCards.csv', 'r') as f:
            reader = csv.DictReader(f)
            items = list(reader)

        for item in items:
            AntiCard(
                flame=item.get('Flame'),
                number=item.get('Number'),
                icon=item.get('Icon'),
            )

    def __repr__(self):
        return f"{self.flame}_{self.label}_{self.icon}"


    def move(self, pos):
        self.pos = pos

    def resize(self, size):
        self.size = size
        # self.frame = self.size[0] / 15
        self.frame = size[0] / 4
        # self.f = [27]


    def update_color(self):
        if self.disabled:
            self.frame_color = (.25, .25, .25, .5)
        else:
            self.frame_color = (0, 0, 0, 1)

    def on_release(self):
        print('AntiCard.on_release')
        app = MDApp.get_running_app().sm.get_screen('Home')
        s = app.game_mode
        app = MDApp.get_running_app().sm.get_screen(s)
        if self.stage == 'set_first_sorcerer':
            app.move_sorcerer(self)

        elif self.stage == 'stage_one':
            app.stage_two(self)

        elif self.stage == 'stage_two':
            if self.location == 'Hand':
                app.stage_one()
            elif self.location == 'Table':
                app.swap_relic_cards(self)

        elif self.stage == 'stage_three':
            app.replace_table_card(self)

        elif self.stage == 'stage_four':
            app.replace_hand_card(self)

        elif self.stage == 'stage_five':
            app.swap_full_hand(self)

        elif self.stage == 'chose_reliquary_card':
            app.remove_reliquary_card(self)


class Sorcerer(BoxLayout):
    points = ListProperty([0, 0, 0, 0])
    width_gap = NumericProperty(0)
    height_gap = NumericProperty(0)
    side = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.position = None

    def resize(self, card, width_gap, height_gap, side):
        self.width_gap = width_gap
        self.height_gap = height_gap
        self.side = side
        if self.side == 'Front':
            self.points = (card.pos[0],
                           card.pos[1] - self.height_gap * .5,
                           card.pos[0] + card.size[0],
                           card.pos[1] - self.height_gap * .5)
        elif self.side == 'Back':
            self.points = (card.pos[0],
                           card.pos[1] + card.size[1] + self.height_gap * .5,
                           card.pos[0] + card.size[0],
                           card.pos[1] + card.size[1] + self.height_gap * .5)

    def reposition(self, position):
        self.position = position

    def moving(self, card):
        self.reposition(card.position)
        if self.side == 'Front':
            animate = Animation(points=(card.pos[0],
                                        card.pos[1] - self.height_gap * .5,
                                        card.pos[0] + card.size[0],
                                        card.pos[1] - self.height_gap * .5),
                                duration=.3)
        elif self.side == 'Back':
            animate = Animation(points=(card.pos[0],
                                        card.pos[1] + card.size[1] + self.height_gap * .5,
                                        card.pos[0] + card.size[0],
                                        card.pos[1] + card.size[1] + self.height_gap * .5),
                                duration=.3)
        animate.start(self)


class Skipping(Button):
    def on_press(self):
        print('Skipping.on_press')
        app = MDApp.get_running_app().sm.get_screen('GameSolo')

        if len(app.deck) > 0:
            self.time = 0
            Clock.schedule_interval(self.timer, 0.01)
        else:
            # NEED TO SEND NOTIFICATION
            self.disabled = True

    def on_release(self):
        Clock.unschedule(self.timer)

    def timer(self, dt):
        self.time = self.time + dt
        if self.time > 0.7:
            Clock.unschedule(self.timer)
            app = MDApp.get_running_app().sm.get_screen('GameSolo')
            app.save_game('stage_one')
            app.stage_three()
            print('SKIP!')


class Codex(RelativeLayout):
    codex_order = ('Green', 'Blue', 'Red', 'Purple')
    active_flame = ObjectProperty('None')
    point = ListProperty([1, 1])

    def resize(self, pos, size):
        self.pos = pos
        self.size = size

    def advance_codex(self):
        ci = self.codex_order.index(self.active_flame)
        self.active_flame = self.codex_order[ci-1]
        self.move_indicator()

    def move_indicator(self):
        if self.active_flame == 'Blue':
            self.point = self.width * 0.25, self.height * 0.75
        elif self.active_flame == 'Green':
            self.point = self.width * 0.75, self.height * 0.75
        elif self.active_flame == 'Red':
            self.point = self.width * 0.25, self.height * 0.25
        elif self.active_flame == 'Purple':
            self.point = self.width * 0.75, self.height * 0.25



Builder.load_file("widgetsgame.kv")



