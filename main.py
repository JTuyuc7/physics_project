import tkinter as tk
from tkinter import messagebox
from UI import Labels
from Animation import Animation
import re
import PIL


def start_animation():
    # * Get the velocity
    value_velocity = input_velocity.get()
    value_angle = angle_slider.get()

    if value_velocity:
        reset_button.configure(state='active')
        reset_button.configure(state='active', cursor='arrow')
        pattern = r"\."
        casted_value = None
        if re.search(pattern, value_velocity):
            casted_value = float(value_velocity)
        else:
            casted_value = int(value_velocity)
        draw_parabola = Animation.ProjectileAnimation(casted_value, value_angle)
        draw_parabola.run_animation()
    else:
        messagebox.showwarning("Alerta", "Ingrese la velocidad inicial")


def restart_animation():
    input_velocity.delete(0, tk.END)
    angle_slider.set(0)


root = tk.Tk()
root.geometry("400x400")
root.title("Tiro parabolico")

# @ Mostrar datos iniciales
label_title = Labels.LabelsUi(text='Ingrese los datos minimos para calcular.', font=('Arial', 18),
                              grid={'row': 0, 'column': 0, 'padx': 10, 'pady': 10, 'sticky': 'nsew'})
label_title.pack_data()

# @ label para la velocidad
label_velocity_ms = Labels.LabelsUi(text='Ingrese la velocidad inicial',
                                    grid={'row': 3, 'column': 0, 'padx': (10, 0), 'pady': 2, 'sticky': 'w'})
label_velocity_ms.pack_data()

label_velocity_ms = Labels.LabelsUi(text='m/s', grid={'row': 4, 'column': 1, 'pady': 5, 'padx': 5, 'sticky': 'w'})
label_velocity_ms.pack_data()

# @ Angle label
angle_label = Labels.LabelsUi(text='Angulo de salida: 0', grid={'row': 7, 'column': 0, 'columnspan': 2, 'pady': 10})
angle_label.pack_data()

# @ Angle selector
angle_slider = tk.Scale(root, from_=0, to=90, orient="horizontal",
                        command=lambda value: angle_label.update_text(f"Angulo: {value} ° grados"))
angle_slider.grid(row=6, column=0, padx=2, pady=2, columnspan=2)

# Text input for velocity
input_velocity = tk.Entry(root)
input_velocity.grid(row=4, column=0, pady=0, padx=(10, 0), sticky='nsew')

# Button to start animation
start_button = tk.Button(root, text="CALCULAR", command=start_animation, width=15, height=2, foreground="green",
                         font=("Arial", 14, 'bold'))
start_button.grid(row=10, column=0, pady=(100, 0), padx=10, sticky='e', columnspan=2)
# start_button.configure(state='disabled', cursor='circle')

# @ Button to cancel or reset the animation
reset_button = tk.Button(root, text="RESETEAR", width=15, height=2, bg='white', foreground="red",
                         font=("Arial", 14, "bold"), command=restart_animation)
reset_button.grid(row=10, column=0, padx=10, pady=(100, 0), sticky='w', columnspan=2)
reset_button.configure(state='disabled', cursor='circle')

root.mainloop()
