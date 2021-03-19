import kivy ,random ,time

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import  ScreenManager , Screen
from kivy.lang import Builder
from kivy.properties import *
from kivy.properties import ColorProperty
from kivy.app import *
from kivy.vector import Vector
from kivy.clock import  Clock
from kivy.uix.scatter import Scatter
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.uix.progressbar import ProgressBar

Window.size = ((300,600))
Window.clearcolor = .5,.5,.5,.7




###paddle class

class Table_selection(Screen):
    current_color  = StringProperty()

    def get_selected_table(self):
        ### gets  the  default table in the  game data file :: pong.csv

        pass
    def change_of_table(self):
        #  changes  the  game data  on  default table
        pass
    pass

class About_developer(Screen):
    pass

class Pause(Screen):
    pass
class Setting(Screen):
    pass


    

class Paddle(Widget):
    score = NumericProperty(0)
    collide_color = ColorProperty((0,0,0,1))
    normal_color = ColorProperty((0,.3,.5,1))
    hit = BooleanProperty(False)
    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            self.hit = True
            vx, vy = ball.vel
            offset = (ball.center_x - self.center_x) / (self.width / 2)
            bounced = Vector( vx, -1*vy)
            vel = bounced *1
            ball.vel = vel.x + offset, vel.y
        else:
            self.hit = False

    def on_touch_move(self, touch):
        if self.collide_point(touch.x,touch.y):
            self.center_x = touch.x

    pass


## ball class
class Ball(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    vel = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.vel) + self.pos



    pass


## game class
class Game(Widget):

    ball = ObjectProperty(None)
    pad1 = ObjectProperty(None)
    pad2 = ObjectProperty(None)
    turn = NumericProperty(2)
    game_paused = BooleanProperty(False)
    def on_touch_down(self, touch):
        if touch.is_double_tap:
            self.game_paused = False if self.game_paused == True  else  True
            pass
    def serve_ball(self, vel=(0, 4)):
        ###  new  serve
        if self.turn == 1:
            vel = (0,-4)
        elif self.turn == 2:
            vel = ( 0 , 4)
        self.ball.center = self.center
        self.ball.vel = vel
    def update(self , dt):

        if self.game_paused is False:

            self.ball.move()

            # bounce of paddles
            self.pad1.bounce_ball(self.ball)
            self.pad2.bounce_ball(self.ball)

            # bounce ball off bottom or top
            if (self.ball.x < self.x) or (self.ball.right > self.right):
                self.ball.velocity_x *= -1

            # went of to a side to score point?
            if self.ball.y < self.y:
                self.pad2.score += 1
                self.serve_ball(vel=(0, 2))
            if self.ball.y > self.height:
                self.pad1.score += 1
                self.serve_ball(vel=(0, -2))

        def on_touch_move(self, touch):
            if touch.y < self.height / 3:
                self.pad1.center_x = touch.x
            if touch.y > self.height - self.width / 3:
                self.pad2.center_x = touch.x


        pass




## scoreboasd class
class Computer_table(Widget):
    ball =ObjectProperty(None)
    pad1 = ObjectProperty(None)
    computer_paddle = ObjectProperty(None)
    turn = NumericProperty(1)
    target =NumericProperty(None)
    start = BooleanProperty(False)
    waiting_for_start = BooleanProperty(True)
    game_paused = BooleanProperty(False)
    pos1 = ListProperty(None)
    pos2 =ListProperty(None)
    ball_gradient = NumericProperty(None)
    constant = NumericProperty(None)
    def get_constant(self , y ,g ,x):
        return y - (g*x)
        pass

    def on_touch_down(self, touch):

        # PAUISING  GAME
        if touch.is_double_tap:
            self.game_paused = False if self.game_paused is True else True
            pass
        ## wait  for touch to start game

        if self.waiting_for_start == True:
            self.waiting_for_start = False
            self.start = True
            self.serve_ball()

            Clock.schedule_interval(self.update, 1.0 / 60.0)
            Clock.schedule_interval(self.predict_ball_movement, 1.0 / 60.0)


    def predict_ball_movement(self  , dt ):
        ## predicts  where the ball will  go to  next
        ##  directs  the  compurter paddle  to  a destination

        ball_vel = self.ball.vel
        ball_pos = self.ball.pos


        if self.ball.velocity_y <= -1:
            pass
        elif self.ball.velocity_y > 0:
            if random.randint(0,10) < 5:

                self.computer_paddle.center_x = self.ball.x
            else:
                self.computer_paddle.center_x = random.randrange(int(self.ball.x - 20)  ,int( self.ball.x +20))



    def serve_ball(self, vel=(0, 4)):
        ###  new  serve
        if self.turn == 1:
            vel = (0,-9)
        elif self.turn == 2:
            vel = ( 0 , 9)
        self.ball.center = self.center
        self.ball.vel = vel
    def update(self , dt):
        if self.game_paused == False:
            self.ball.move()

            # bounce of paddles
            self.pad1.bounce_ball(self.ball)
            self.computer_paddle.bounce_ball(self.ball)

            # bounce ball off bottom or top
            if (self.ball.x < self.x) or (self.ball.right > self.right):
                self.ball.velocity_x *= -1

            # went of to a side to score point?
            if self.ball.y < self.y:
                self.computer_paddle.score += 1
                self.serve_ball(vel=(0, 4))
                self.turn = 2

            if self.ball.y > self.height:
                self.pad1.score += 1
                self.serve_ball(vel=(0, -4))
                self.turn = 1

    def on_touch_move(self, touch):
        if touch.y < self.height / 3:
            self.pad1.center_x = touch.x


    pass




    pass
class Computer(Screen):

    vs_computer =ObjectProperty(None)

    def start_vs_computer(self):
        ##  starting game vs computer
       self.vs_computer.serve_ball()

       Clock.schedule_interval(self.vs_computer.update, .01)
       Clock.schedule_interval(self.vs_computer.predict_ball_movement, 1.0 / 60.0)


class  Interface(Screen):
    pass
class  Main_game(Screen):
    game = ObjectProperty(None)
    def start_first_time(self):

        self.game.serve_ball()
        self.game.pad1.x = 30
        Clock.schedule_interval(self.game.update, 1.0 / 60.0)


    pass
class Manager(ScreenManager):
    pass


kv = Builder.load_file('TableTennis.kv')
class TableTennisApp(App):
    def build(self):

        return kv



if __name__ == '__main__':
    TableTennisApp().run()
