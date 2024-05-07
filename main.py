import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox

window = Tk()
window.title("Symulator ze sterownikiem PD")
window.minsize(width=1200, height=800)
window.config(padx=20, pady=20, bg="seashell")

gs = Canvas(width=365, height=300, bg="seashell", highlightthickness=0)
xxx = PhotoImage(file="img.png")
gs.create_image(0, 80, anchor=SW, image=xxx)
gs.place(x=0,y=660)

# Tworzenie obszaru do rysowania wykresów
figure = plt.Figure(figsize=(9, 5.2), dpi=130)
canvas = FigureCanvasTkAgg(figure, master=window)
canvas.get_tk_widget().place(x=370, y=70)

title_label = Label(
    text="Program symulujący układ ze sterownikiem PD w konfiguracji z ujemnym sprzężeniem zwrotnym dla wybranych parametrow.",
    font=("Arial", 14), bg="seashell")
title_label.place(y=10)

wspol = Label(text="Wpisz wspolczynniki transmitancji:", font=14, bg="seashell")
wspol.place(y=60, x=45)

a1 = Label(text="a1:", font=16, bg="seashell")
a1.place(y=90, x=130)
a1_entry = Entry(width=10)
a1_entry.place(y=95, x=165)

a0 = Label(text="a0:", font=16, bg="seashell")
a0.place(y=120, x=130)
a0_entry = Entry(width=10)
a0_entry.place(y=125, x=165)

b2 = Label(text="b2:", font=16, bg="seashell")
b2.place(y=150, x=130)
b2_entry = Entry(width=10)
b2_entry.place(y=155, x=165)

b1 = Label(text="b1:", font=16, bg="seashell")
b1.place(y=180, x=130)
b1_entry = Entry(width=10)
b1_entry.place(y=185, x=165)

b0 = Label(text="b0:", font=16, bg="seashell")
b0.place(y=210, x=130)
b0_entry = Entry(width=10)
b0_entry.place(y=215, x=165)

wyb_para = Label(text=" Wpisz parametry:", font=20, bg="seashell")
wyb_para.place(y=240, x=45)

kp_label = Label(text="Kp:", font=20, bg="seashell")
kp_label.place(y=270, x=45)
kp_entry = Entry(width=10)
kp_entry.place(y=275, x=80)

kd_label = Label(text="Kd:", font=20, bg="seashell")
kd_label.place(y=270, x=165)
kd_entry = Entry(width=10)
kd_entry.place(y=275, x=200)

t1_label = Label(text="Tp:", font=20, bg="seashell")
t1_label.place(y=310, x=45)
t1_entry = Entry(width=10)
t1_entry.place(y=315, x=80)

t2_label = Label(text="Td:", font=20, bg="seashell")
t2_label.place(y=310, x=165)
t2_entry = Entry(width=10)
t2_entry.place(y=315, x=200)

amplituda_label = Label(text=" Amplituda:", font=20, bg="seashell")
amplituda_label.place(y=480, x=150)
amplituda_entry = Entry(width=10)
amplituda_entry.place(y=515, x=170)

pobudzenie_label = Label(text=" Wybierz pobudzenie:", font=20, bg="seashell")
pobudzenie_label.place(y=340, x=45)


def radio_used():
    print(radio_state.get())


# Variable to hold on to which radio button value is checked.
radio_state = IntVar()
radiobutton1 = Radiobutton(text=" pobudzenie sygnlem prostokatnym ", value=1, variable=radio_state, command=radio_used,
                           bg="seashell")
radiobutton2 = Radiobutton(text=" pobudzenie sygnlem trojkatnym ", value=2, variable=radio_state, command=radio_used,
                           bg="seashell")
radiobutton3 = Radiobutton(text=" pobudzenie sygnlem harmonicznym ", value=3, variable=radio_state, command=radio_used,
                           bg="seashell")
radiobutton1.place(y=390, x=40)
radiobutton2.place(y=420, x=40)
radiobutton3.place(y=450, x=40)

okres = Label(text=" Okres(s):", font=20, bg="seashell")
okres.place(y=480, x=45)
okres_entry = Entry(width=10)
okres_entry.place(y=515, x=65)


def symulacja(a0, a1, b0, b1, b2, Kp_val, Kd_val, input_signal, input_time):
    dt = input_time[1] - input_time[0]
    output = np.zeros_like(input_signal)
    poprzedni_uchyb = 0.0

    for i in range(len(input_signal)):
        uchyb = input_signal[i] - output[i]

        # Regulator PD
        proportional = uchyb
        derivative = (uchyb - poprzedni_uchyb) / dt

        # Obliczanie sterowania
        control_signal = Kp_val * proportional + Kd_val * derivative

        # Obliczanie odpowiedzi układu
        output[i] = control_signal / (b2 * dt ** 2 + b1 * dt + b0)

        # Aktualizacja błędu dla regulatora PD
        poprzedni_uchyb = uchyb

    return output

def sprawdz_stabilnosc(a0, a1, b0, b1, b2, Kp_val, Kd_val):
    if b2 > 0 and b1 > 0 and b0 > 0:
        roots = np.roots([b2, b1, b0 + Kp_val, Kd_val])
        real_parts = np.real(roots)
        if all(real_parts < 0):
            return True
    messagebox.showwarning("Niestabilny układ", "Wprowadź inne współczynniki.")
    return False

def generuj_sygnal(signal_type, duration, dt, amplitude):
    time = np.arange(0, duration, dt)
    if signal_type == 'square':
        frequency = 0.5  # Hz
        input_signal = amplitude * np.where(np.sin(2 * np.pi * frequency * time) > 0, 1, -1)
    elif signal_type == 'triangle':
        frequency = 0.5  # Hz
        input_signal = amplitude *2 * np.abs(2 * (time * frequency - np.floor(0.5 + time * frequency))) - 1
    elif signal_type == 'harmonic':
        frequency = 0.5  # Hz
        input_signal = amplitude * np.sin(2 * np.pi * frequency * time)
    else:
        raise ValueError('Invalid signal type.')
    return input_signal


def plot_response(input_signal, output_signal, input_time):
    figure.clear()
    ax = figure.add_subplot(111)
    ax.plot(input_time, input_signal, label='Input Signal')
    ax.plot(input_time, output_signal, label='Output Signal')
    ax.set_xlabel('Time')
    ax.set_ylabel('Amplitude')
    ax.legend()
    ax.grid(True)
    canvas.draw()


def transmitance(a0, a1, b0, b1, b2, Kp_val, Kd_val, frequencies, T1, T2, ):
    transfer_function = np.zeros_like(frequencies, dtype=np.complex128)

    for i, f in enumerate(frequencies):
        s = 1j * 2 * np.pi * f
        numerator = (Kd_val * s + Kp_val) * (a1 * s + a0) * np.exp(-T1 * s)
        denominator = (
            (b2 * s ** 2 + (b1 + Kd_val * s) * s + (b0 + Kp_val))
            * (T2 * s + 1)
        )
        transfer_function[i] = numerator / denominator

    return transfer_function


def draw_transmitance():
    a0_val = float(a0_entry.get())
    a1_val = float(a1_entry.get())
    b0_val = float(b0_entry.get())
    b1_val = float(b1_entry.get())
    b2_val = float(b2_entry.get())
    Kp_val = float(kp_entry.get())
    Kd_val = float(kd_entry.get())
    T1_val = float(t1_entry.get())
    T2_val = float(t2_entry.get())
    frequencies = np.logspace(-2, 2, num=1000)
    transfer_function = transmitance(a0_val, a1_val, b0_val, b1_val, b2_val, Kp_val, Kd_val, frequencies, T1_val, T2_val)

    figure.clear()
    ax = figure.add_subplot(111)
    ax.plot(frequencies, np.abs(transfer_function))
    ax.set_xlabel('Frequency')
    ax.set_ylabel('Magnitude')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.grid(True)
    canvas.draw()


def draw_response():
    a0_val = float(a0_entry.get())
    a1_val = float(a1_entry.get())
    b0_val = float(b0_entry.get())
    b1_val = float(b1_entry.get())
    b2_val = float(b2_entry.get())
    Kp_val = float(kp_entry.get())
    Kd_val = float(kd_entry.get())
    Duration_val = float(okres_entry.get())
    Amp_val = float(amplituda_entry.get())
    signal_type = get_signal_type()
    duration = Duration_val
    dt = 0.001
    if not sprawdz_stabilnosc(a0_val, a1_val, b0_val, b1_val, b2_val, Kp_val, Kd_val):
        return
    input_signal = generuj_sygnal(signal_type, duration, dt, Amp_val)
    input_time = np.arange(0, duration, dt)
    output_signal = symulacja(a0_val, a1_val, b0_val, b1_val, b2_val, Kp_val, Kd_val, input_signal, input_time)

    figure.clear()
    ax = figure.add_subplot(111)
    ax.plot(input_time, input_signal, label='Input Signal')
    ax.plot(input_time, output_signal, label='Output Signal')
    ax.set_xlabel('Time')
    ax.set_ylabel('Amplitude')
    ax.legend()
    ax.grid(True)
    canvas.draw()


def get_signal_type():
    if radio_state.get() == 1:
        return 'square'
    elif radio_state.get() == 2:
        return 'triangle'
    elif radio_state.get() == 3:
        return 'harmonic'


gs_button = Button(text="Rysuj transmitancje", command=draw_transmitance)
gs_button.place(y=550, x=65)
gs_button = Button(text="Rysuj odpowiedz na pobudzenie", command=draw_response)
gs_button.place(y=600, x=65)

window.mainloop()