from kivy.uix.widget import Widget
from kivy.graphics import Line, Color, Rectangle
from kivy.clock import Clock
import random

# Configurações
FPS = 30
LINE_WIDTH = 1
MAX_LENGTH = 120
DELAY_BETWEEN_LINES = 0.5
RANDOM_Y_RANGE = (-10, 10)
MIN_DISTANCE_BETWEEN_LINES = 50

class LineGraphLine:
    def __init__(self, width, height, max_length, start_time, line_color):
        self.x = 0
        self.y = random.randint(0, height)
        self.points = []
        self.draw_speed = 9
        self.erase_speed = 9
        self.restart_line = False
        self.start_time = start_time
        self.width = width
        self.height = height
        self.max_length = max_length
        self.line_color = line_color

    def update(self, current_time):
        elapsed_time = current_time - self.start_time

        if not self.restart_line and elapsed_time >= self.erase_speed:
            self.x += self.draw_speed
            self.y += random.randint(*RANDOM_Y_RANGE)

        if self.x > self.width:
            self.restart_line = True

        if self.restart_line and self.x <= 0:
            self.restart_line = False
            self.x = 0
            self.y = random.randint(0, self.height)
            self.points = []
            self.start_time = current_time

        self.points.extend([self.x, self.y])

        if len(self.points) > self.max_length * 2:
            self.points = self.points[-(self.max_length * 2):]

class LineGraphWidget(Widget):
    def __init__(self, **kwargs):
        super(LineGraphWidget, self).__init__(**kwargs)
        self.lines = []
        self.line_width = LINE_WIDTH
        self.max_length = MAX_LENGTH
        self.delay_between_lines = DELAY_BETWEEN_LINES
        self.last_line_end = 0  # Guarda a posição x da última linha gerada
        self.start_time = Clock.get_time()

        Clock.schedule_interval(self.update, 1 / FPS)

    def update(self, dt):
        current_time = Clock.get_time()

        if current_time - self.start_time >= self.delay_between_lines:
            # Alterna a cor entre verde e vermelho
            line_color = (0, 1, 0, 0.6) if len(self.lines) % 2 == 0 else (1, 0, 0, 0.6)
            
            # Verifica se a última linha está a uma distância mínima
            if self.last_line_end == 0 or self.width - self.last_line_end >= MIN_DISTANCE_BETWEEN_LINES:
                self.lines.append(LineGraphLine(self.width, self.height, self.max_length, self.start_time, line_color))
                self.last_line_end = self.lines[-1].x
                self.start_time = current_time

        for line in self.lines:
            line.update(current_time)

        self.canvas.clear()
        with self.canvas:
            Color(0, 0, 0, 1)  # Cor preta para o fundo
            Rectangle(pos=self.pos, size=self.size)  # Retângulo preto para preencher o fundo

            for line in self.lines:
                if len(line.points) >= 2:
                    Color(*line.line_color)  # Usa a cor atribuída à linha
                    Line(points=line.points, width=self.line_width)

# Exemplo de uso
if __name__ == "__main__":
    from kivy.app import App

    class LineGraphApp(App):
        def build(self):
            return LineGraphWidget()

    LineGraphApp().run()
