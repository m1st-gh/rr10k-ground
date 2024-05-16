import serial
import threading
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
import re
ser = None
found = False
data = [[] for _ in range(10)]

def listen_input(ser):
    global found
    running = False
    pattern = re.compile(r"^-?\d+(\.\d+)?(,-?\d+(\.\d+)?)*$", re.IGNORECASE)
    while True:
        response = ser.readline().decode().strip()
        running = pattern.match(response)
        if response == "STARTING" or running is not None:
            found = True
            time.sleep(0.5)
            print("Found connection!")
            break

def send_start(ser):
    global found
    while True:
        if found is True:
            exit(0)
        ser.write(b"START\n")
        print("Looking for Connection...")
        time.sleep(2)


def initialize_serial(port, baud_rate):
    try:
        ser = serial.Serial(port, baud_rate)
        return ser
    except serial.SerialException:
        print("Device Not detected.")
        exit(1)


def connect_serial():
    port = input("Enter the port: ")
    baud_rate = int(input("Enter the baud rate: "))
    ser = initialize_serial(port, baud_rate)
    return ser


def start_reading(ser):
    send_thread = threading.Thread(target=send_start, args=(ser,))
    listen_thread = threading.Thread(target=listen_input, args=(ser,))
    send_thread.start()
    listen_thread.start()
    listen_thread.join()
    send_thread.join()


def animate(frame, ser, axs, fig):
    lines = []
    text = []
    for ax in axs:
        for sub_ax in ax:
            sub_ax.clear()
    ser.reset_input_buffer()
    indata = ser.readline().decode().strip()
    indata = indata.split(",")
    print(indata)
    if len(indata) == 10:
        for i in range(10):
            try:
                data[i].append(float(indata[i]))
            except ValueError:
                data[i].append(-1)
    def get_last_element(lst):
        if lst:  # Check if the list is not empty
            return lst[-1]
        else:
            return 0  # Or any default value
    
    def draw_deg():
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

    def draw_g():
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

    def draw_atm():
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

    def draw_temp():
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

    def draw_alt():
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

    def draw_head():
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
    threads = []
    t1 = threading.Thread(target=draw_deg)
    t2 = threading.Thread(target=draw_g)
    t3 = threading.Thread(target=draw_atm)
    t4 = threading.Thread(target=draw_temp)
    t5 = threading.Thread(target=draw_alt)
    t6 = threading.Thread(target=draw_head)
    threads.extend([t1, t2, t3, t4, t5, t6])
    

    for t in threads:
        t.start()

    for t in threads:
        t.join()
    fig.canvas.draw()
    return lines + text

def main():
    global ser
    ser = connect_serial()
    start_reading(ser)
    fig, axs = plt.subplots(3, 2)
    axs[0, 0].set_ylim(-190, 190)
    axs[0, 0].set_ylim(-190, 190)
    axs[1, 0].set_ylim(-16, 16)
    axs[1, 0].set_ylim(-16, 16)
    axs[1, 0].set_ylim(-16, 16)
    axs[2, 0].set_ylim(0, 1.5)
    axs[0, 1].set_ylim(-40, 60)
    axs[1, 1].set_ylim(-100, 4000)
    axs[2, 1].set_ylim(0, 360)
    plt.style.use('ggplot')
    update = FuncAnimation(
        fig, animate, fargs=(ser, axs, fig), interval=50, save_count=20, blit=True
    )
    plt.show()


if __name__ == "__main__":
    main()
