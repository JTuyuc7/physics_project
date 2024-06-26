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

        # Add background image
        # ax.imshow(plt.imread('images/bg3.jpeg'), extent=[0, xdata[-1] + max_distance_x, 0, max_height + y_max])
        ax.imshow(plt.imread('images/bg3.jpeg'), extent=[0, xdata[-1] + 10, 0, max_height + 10])

        # Add canon ball image
        ball_image = plt.imread('images/canonball.png')
        # ax.imshow(ball_image, extent=[0, 1, 0, 1], animated=True)

        # Set labels and title
        ax.set_xlabel('Eje (x) - distancia en metros')
        ax.set_ylabel('Eje y - distancia en metros')
        ax.set_xlim(0, xdata[-1] + 10)
        ax.set_ylim(0, max_height + 10 )
        # ax.set_title('Projectile Motion Animation')

        # Add labels with additional information
        label_x = 0.5 * (xdata[-1] + 30)
        label_y = max_height + 30
        ax.text(label_x, label_y,
                f"Altura maxima alcanzada: {max_height:.2f} metros\n"
                f"Tiempo en alcanzar altura maxima: {max_height_time:.2f} segundos\n"
                f"Tiempo total de vuelo: {total_time_in_air:.2f} segundos\n"
                f"Distancia maxima alcanzada {max_distance_x:.2f}",
                horizontalalignment='center', fontsize=12)

        # img_left_bottom = plt.imread('images/canon1.jpeg')  # Replace with your image
        img_path = 'images/canon3.svg'  # Replace with your image
        img = Image.open(img_path)

        # Resize the image
        new_img_height = 10  # New height of the image (adjust as needed)
        img = img.resize((img.width * new_img_height // img.height, new_img_height))

        # Rotate the image (clockwise)
        rotation_angle = 45  # Angle of rotation (in degrees)
        img = img.rotate(rotation_angle, expand=True)

        # Convert the PIL image back to a NumPy array
        rotated_img = np.array(img)

        # Position the image where the line animation starts (at the first point)
        x_start, y_start = xdata[0], ydata[0]
        img_width = rotated_img.shape[1]  # Width of the image
        img_height = rotated_img.shape[0]  # Height of the image
        ax.imshow(rotated_img, extent=[x_start, x_start + img_width, y_start, y_start + img_height])

        # Adjust the interval to match the total time in the air
        interval = self.total_time_in_air / self.num_frames * 1000

        # Define animation update function
        def update_line(num, xdata, ydata, line):
            line.set_data(xdata[:num], ydata[:num])
            return line,

        # Create animation
        # line, = ax.plot([], [], 'ro', animated=True)
        line, = ax.plot([], [], color='purple', marker='o', markersize=3, linestyle='None', animated=True)

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