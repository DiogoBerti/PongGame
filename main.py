from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
from random import randint


class PongPlayer(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):

        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)

            bounced = Vector(-1 * vx, vy)
            if bounced.x < 12 and bounced.x > -12:
                vel = bounced * 1.1
            else:
                vel = bounced
            ball.velocity = vel.x, vel.y + offset


class PongEnemy(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):

        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)

            bounced = Vector(-1 * vx, vy)
            if bounced.x < 12 and bounced.x > -12:
                vel = bounced * 1.1
            else:
                vel = bounced
            ball.velocity = vel.x, vel.y + offset


class PongGame(Widget):

    def __init__(self, **kwargs):
        super(PongGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    enemy1 = ObjectProperty(None)

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel
        print self.ball.velocity

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y

    def update(self, dt):

        self.ball.move()
        self.player1.bounce_ball(self.ball)
        self.enemy1.bounce_ball(self.ball)

        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

            # went of to a side to score point?
        if self.ball.x < self.x:
            self.enemy1.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'w':
            self.player1.center_y += 20
        elif keycode[1] == 's':
            self.player1.center_y -= 20

        if keycode[1] == 'd':
            self.player1.center_x += 20
        elif keycode[1] == 'a':
            self.player1.center_x -= 20

class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    PongApp().run()
