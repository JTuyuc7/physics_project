import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

DURATION = 10
NUM_FRAMES = 100
GRAVITY = 9.81


class ProjectileAnimation:
    def __init__(self, v0: float, angle: float):
        if not isinstance(v0, (int, float)) or not isinstance(angle, (int, float)):
            raise TypeError("v0 and angle must be integers or floats")

        self.g = GRAVITY
        self.v0 = v0
        self.angle = angle
        self.num_frames = NUM_FRAMES
        self.duration = DURATION

        # Calculate the total time the object spends in the air
        self.total_time_in_air = (2 * self.v0 * np.sin(np.radians(self.angle))) / self.g

        # Adjust the number of frames and time range to match the total time in the air
        self.t = np.linspace(0, self.total_time_in_air, self.num_frames)

    def calculate_position(self):
        vx0 = self.v0 * np.cos(np.radians(self.angle))
        vy0 = self.v0 * np.sin(np.radians(self.angle))

        xdata = vx0 * self.t
        ydata = vy0 * self.t - 0.5 * self.g * self.t ** 2
        y_max = (vy0 ** 2 / (2 * self.g))
        time_to_go_up = vy0 / self.g
        total_time_in_air = 2 * time_to_go_up
        max_distance_x = vx0 * total_time_in_air

        return xdata, ydata, time_to_go_up, total_time_in_air, max_distance_x, y_max

    def run_animation(self):
        xdata, ydata, time_to_go_up, total_time_in_air, max_distance_x, y_max = self.calculate_position()
        max_height_index = np.argmax(ydata)
        max_height_time = self.t[max_height_index]
        max_height = ydata[max_height_index]

        fig, ax = plt.subplots()
        x_maring = 10
        y_margin = 20
        if self.angle > 80:
            x_maring = 300
        if self.angle > 60:
            y_margin = 60

        ax.imshow(plt.imread('images/bg3.jpeg'), extent=[0, xdata[-1] + x_maring, 0, max_height + 50])

        # Add canon ball image
        ball_image = plt.imread('images/canonball.png')
        # ax.imshow(ball_image, extent=[0, 1, 0, 1], animated=True)

        # Set labels and title
        ax.set_xlabel('Eje (x) - distancia en metros')
        ax.set_ylabel('Eje y - distancia en metros')
        ax.set_xlim(0, xdata[-1] + x_maring)
        ax.set_ylim(0, max_height + 50 )
        #@ ax.set_title('Projectile Motion Animation')

        info_text = (f"Altura maxima alcanzada: {max_height:.2f} metros\n"
                    f"Tiempo en alcanzar altura maxima: {max_height_time:.2f} segundos\n"
                    f"Tiempo total de vuelo: {total_time_in_air:.2f} segundos\n"
                    f"Distancia maxima alcanzada {max_distance_x:.2f} metros")
        props = dict(boxstyle='round,pad=0.5', facecolor='wheat', alpha=0.5)

        fig.text(0.95, 0.95, info_text, fontsize=12, verticalalignment='top', horizontalalignment='right', bbox=props)

        fig.canvas.manager.set_window_title('Animacion Tiro Vertical')

        interval = self.total_time_in_air / self.num_frames * 1000
        def update_line(num, xdata, ydata, line):
            line.set_data(xdata[:num], ydata[:num])
            return line,

        line, = ax.plot([], [], color='purple', marker='P', markersize=5, linestyle='None', animated=True)

        the_anim = animation.FuncAnimation(fig, update_line, frames=len(self.t),
                                           fargs=(xdata, ydata, line),
                                           interval=interval, blit=True)
        plt.show()
