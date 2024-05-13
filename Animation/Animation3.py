from typing import Union
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

DURATION = 10
NUM_FRAMES = 100
GRAVITY = 9.81


class ProjectileAnimation:
    def __init__(self, v0: Union[int, float] = None, angle: Union[int, float] = None):
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
        print(vy0, 'velocidad en y')
        xdata = vx0 * self.t
        ydata = vy0 * self.t - 0.5 * self.g * self.t ** 2
        y_max = (vy0**2 / 2 * self.g)
        print(y_max, 'y max ')

        return xdata, ydata

    def run_animation(self):
        xdata, ydata = self.calculate_position()
        max_height_index = np.argmax(ydata)
        max_height_time = self.t[max_height_index]
        max_height = ydata[max_height_index]

        fig, ax = plt.subplots()

        # Add background image
        ax.imshow(plt.imread('images/bg3.jpeg'), extent=[0, xdata[-1] + 30, 0, max_height + 30])
        canon_ball = plt.imread('images/canonball.png')
        ballon = ax.imshow(canon_ball, extent=[0, 1, 0, 1], animated=True)

        ax.set_xlabel('Eje (x) - distancia en metros')
        ax.set_ylabel('Eje y - distancia en metros')
        ax.set_xlim(0, xdata[-1] + 30)
        ax.set_ylim(0, max_height + 30)
        line, = ax.plot([], [], 'ro', animated=True)

        # Add labels with additional information
        label_x = 0.5 * (xdata[-1] + 30)
        label_y = max_height + 50
        ax.text(label_x, label_y,
                f"Altura maxima alcanzada: {max_height:.2f} metros\nTiempo en alcanzar altura maxima: {max_height_time:.2f} segundos",
                horizontalalignment='center', fontsize=12)

        # Adjust the interval to match the total time in the air
        interval = self.total_time_in_air / self.num_frames * 1000

        def update_line(num, xdata, ydata, line):
            line.set_data(xdata[:num], ydata[:num])
            return line,

        the_anim = animation.FuncAnimation(fig, update_line, frames=len(self.t),
                                           fargs=(xdata, ydata, line),
                                           interval=interval, blit=True)
        plt.show()


# Usage
# projectile_anim = ProjectileAnimation(v0=200, angle=45)
# projectile_anim.run_animation()

    # def run_animation(self):
    #     xdata, ydata = self.calculate_position()
    #     max_height_index = np.argmax(ydata)
    #     max_height_time = self.t[max_height_index]
    #     max_height = ydata[max_height_index]
    #
    #     fig, ax = plt.subplots()
    #
    #     # Add background image
    #     ax.imshow(plt.imread('images/bg3.jpeg'), extent=[0, xdata[-1] + 30, 0, max_height + 30])
    #     cannon_ball = plt.imread('images/canonball1.png')
    #
    #     # Plot the cannonball image
    #     ballon = ax.imshow(cannon_ball, extent=[0, 1, 0, 1], animated=True)
    #
    #     ax.set_xlabel('Eje (x) - distancia en metros')
    #     ax.set_ylabel('Eje y - distancia en metros')
    #     ax.set_xlim(0, xdata[-1] + 30)
    #     ax.set_ylim(0, max_height + 30)
    #
    #     # Adjust the interval to match the total time in the air
    #     interval = self.total_time_in_air / self.num_frames * 1000
    #
    #     def update_line(num, xdata, ydata, ballon):
    #         ballon.set_extent([xdata[num] - 0.1, xdata[num] + 0.1, ydata[num] - 0.1,
    #                            ydata[num] + 0.1])  # Update position of the cannonball
    #         return ballon,
    #
    #     the_anim = animation.FuncAnimation(fig, update_line, frames=len(self.t),
    #                                        fargs=(xdata, ydata, ballon),
    #                                        interval=interval, blit=True)
    #     plt.show()
    # ! Changes here