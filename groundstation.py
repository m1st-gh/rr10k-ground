import serial
import serial.tools.list_ports
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import struct
import PySimpleGUI as sg
import threading
ser = None
found = False
data = [[] for _ in range(14)]

def listen_input():
    global ser
    global found
    data_in = ser.read(56)  # Read 52 bytes from the serial port
    if data_in:  # If data_in is not empty
        found = True
        exit(0)


def initialize_serial(port, baud_rate):
    global ser
    try:
        ser = serial.Serial(port, baud_rate)
    except serial.SerialException:
        exit(1)


def animate(frame, ser: serial.Serial, axs, fig):
    lines = []
    text = []
    for ax in axs:
        for sub_ax in ax:
            sub_ax.clear()
    global data
    ser.flushInput()
    data_in = [round(value, 2) for value in struct.unpack('f'*14, ser.read(56))]
    if round(data_in[-1],0) == round(sum(data_in[:13]),0):
        for i in range(13):
            data[i].append(data_in[i])
    def get_last_element(lst):
        if lst:  # Check if the list is not empty
            return lst[-1]
        else:
            return 0  # Or any default value

    if len(data[9]) > 0:  # Check if data[9] is not empty
        if data[9][-1] - data[9][0] > 20:
            for i in range(13):
                data[i].pop(0)    
    lines.extend(axs[0, 0].plot(data[9], data[0], label="x deg's", color="red"))
    lines.extend(axs[0, 0].plot(data[9], data[1], label="y deg's", color="blue"))
    axs[0, 0].set_xlim(data[9][0], data[9][-1])
    axs[0, 0].legend(loc="upper left")
    text.append(axs[0, 0].text(
        0.9825,
        0.95,
        "\n".join(str(get_last_element(data[i])) for i in range(2)),
        ha="right",
        va="top",
        transform=axs[0, 0].transAxes,
        bbox=dict(facecolor="white", alpha=0.5),
    ))
    lines.extend(axs[1, 0].plot(data[9], data[2], label="x g's", color="red"))
    lines.extend(axs[1, 0].plot(data[9], data[3], label="y g's", color="blue"))
    lines.extend(axs[1, 0].plot(data[9], data[4], label="z g's", color="green"))
    axs[1, 0].set_xlim(data[9][0], data[9][-1])
    axs[1, 0].legend(loc="upper left")
    text.append(axs[1, 0].text(
        0.9825,
        0.95,
        "\n".join(str(get_last_element(data[i])) for i in range(2, 5)),
        ha="right",
        va="top",
        transform=axs[1, 0].transAxes,
        bbox=dict(facecolor="white", alpha=0.5),
    ))
    lines.extend(axs[2, 0].plot(data[9], data[5], label="Atm", color="blue"))
    axs[2, 0].set_xlim(data[9][0], data[9][-1])
    axs[2, 0].legend(loc="upper left")
    text.append(axs[2, 0].text(
        0.9825,
        0.95,
        str(get_last_element(data[5])),
        ha="right",
        va="top",
        transform=axs[2, 0].transAxes,
        bbox=dict(facecolor="white", alpha=0.5),
    ))
    lines.extend(axs[0, 1].plot(data[9], data[6], label="Temp C", color="black"))
    axs[0, 1].set_xlim(data[9][0], data[9][-1])
    axs[0, 1].legend(loc="upper left")
    text.append(axs[0, 1].text(
        0.9825,
        0.95,
        str(get_last_element(data[6])),
        ha="right",
        va="top",
        transform=axs[0, 1].transAxes,
        bbox=dict(facecolor="white", alpha=0.5),
    ))
    lines.extend(axs[1, 1].plot(data[9], data[7], label="Alt M", color="black"))
    axs[1, 1].set_xlim(data[9][0], data[9][-1])
    axs[1, 1].legend(loc="upper left")
    text.append(axs[1, 1].text(
        0.9825,
        0.95,
        str(get_last_element(data[7])),
        ha="right",
        va="top",
        transform=axs[1, 1].transAxes,
        bbox=dict(facecolor="white", alpha=0.5),
    ))
    lines.extend(axs[2, 1].plot(data[9], data[8], label="Head", color="black"))
    axs[2, 1].set_xlim(data[9][0], data[9][-1])
    axs[2, 1].legend(loc="upper left")
    text.append(axs[2, 1].text(
        0.9825,
        0.95,
        str(get_last_element(data[8])),
        ha="right",
        va="top",
        transform=axs[2, 1].transAxes,
        bbox=dict(facecolor="white", alpha=0.5),
    ))
    lines.extend(axs[3, 0].plot(data[9], data[10], label="x g's", color="red"))
    lines.extend(axs[3, 0].plot(data[9], data[11], label="y g's", color="blue"))
    lines.extend(axs[3, 0].plot(data[9], data[12], label="z g's", color="green"))
    axs[3, 0].set_xlim(data[9][0], data[9][-1])
    axs[3, 0].legend(loc="upper left")
    text.append(axs[3, 0].text(
        0.9825,
        0.95,
        "\n".join(str(get_last_element(data[i])) for i in range(10, 13)),
        ha="right",
        va="top",
        transform=axs[3, 0].transAxes,
        bbox=dict(facecolor="white", alpha=0.5),
    ))
    fig.canvas.draw()
    return lines + text
    
def init_gui():
    ports = serial.tools.list_ports.comports()
    layout = [
        [sg.Text("Serial Port"), sg.Combo(ports, key="port", default_value = ports[0])],
        [sg.Text("Baud Rate"), sg.InputText(key="baud_rate", default_text="115200")],
        [sg.Button("Connect"), sg.Button("Exit")],
    ]
    window = sg.Window("Ground Station", layout)
    while True:
        event, values = window.read()
        if event == "Connect":
            initialize_serial(values["port"].name, values["baud_rate"])
            window.close()
            break
        elif event == "Exit" or event == sg.WIN_CLOSED:
            window.close()
            exit(0)

def connect_gui():
    global found
    layout = [
        [sg.Text("Looking for incoming data...")],
    ]
    window = sg.Window("Ground Station", layout)
    thread = threading.Thread(target=listen_input)
    thread.start()
    while True:
        event, values = window.read(100)
        if event == sg.WIN_CLOSED or found is True:
            thread.join()
            window.close()
            break

def plot_gui():
    global ser
    fig, axs = plt.subplots(4, 2)
    axs[0, 0].set_ylim(-190, 190)
    axs[0, 0].set_ylim(-190, 190)
    axs[1, 0].set_ylim(-16, 16)
    axs[1, 0].set_ylim(-16, 16)
    axs[1, 0].set_ylim(-16, 16)
    axs[2, 0].set_ylim(0, 1.5)
    axs[0, 1].set_ylim(-40, 60)
    axs[1, 1].set_ylim(-100, 4000)
    axs[2, 1].set_ylim(0, 360)
    axs[3, 0].set_ylim(-16, 16)
    axs[3, 1].set_visible(False)
    plt.style.use('ggplot')
    update = FuncAnimation(
        fig, animate, fargs=(ser, axs, fig), interval=1, save_count=600, blit=True
    )
    plt.show()
    
def main():
    init_gui()
    connect_gui()
    plot_gui()

if __name__ == "__main__":
    main()
