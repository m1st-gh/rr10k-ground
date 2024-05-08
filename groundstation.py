import serial
import threading
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

found = False
data = [[] for _ in range(10)]



def listen_input(ser):
    global found
    while True:
        response = ser.readline().decode().strip()
        if response == "STARTING":
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
    except:
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


def animate(frame, ser, axs):
    for ax in axs:
        for sub_ax in ax:
            sub_ax.clear()
    indata = ser.readline().decode().strip()
    indata = indata.split(",")
    print (indata)
    if len(indata) == 10:
        for i in range(10):
            data[i].append(float(indata[i]))
        if data[9][-1] - data[9][0] > 20:
            for i in range(10):
                data[i].pop(0)
        for ax in axs:
            for sub_ax in ax:
                sub_ax.set_xlim(data[9][0], data[9][-1])
    
    axs[0, 0].plot(data[9], data[0], label="x deg's", color="red")
    axs[0, 0].plot(data[9], data[1], label="y deg's", color="blue")
    axs[1, 0].plot(data[9], data[2], label="x g's", color="red")
    axs[1, 0].plot(data[9], data[3], label="y g's", color="blue")
    axs[1, 0].plot(data[9], data[4], label="z g's", color="green")
    axs[2, 0].plot(data[9], data[5], label="Atm", color="blue")
    axs[0, 1].plot(data[9], data[6], label="Temp C", color="black")
    axs[1, 1].plot(data[9], data[7], label="Alt M", color="black")
    axs[2, 1].plot(data[9], data[8], label="Head", color="black")
    axs[0, 0].set_ylim(-190, 190)
    axs[0, 0].set_ylim(-190, 190)
    axs[1, 0].set_ylim(-16, 16)
    axs[1, 0].set_ylim(-16, 16)
    axs[1, 0].set_ylim(-16, 16)
    axs[2, 0].set_ylim(0, 1.5)
    axs[0, 1].set_ylim(-40, 60)
    axs[1, 1].set_ylim(-100, 4000)
    axs[2, 1].set_ylim(0, 360)
    for ax in axs:
        for sub_ax in ax:
            sub_ax.legend(loc = "upper left")
    axs[0, 0].text(0.9825, 0.95, ('\n'.join((str(data[0][-1]), str(data[1][-1])))), ha='right', va='top', transform=axs[0, 0].transAxes, bbox=dict(facecolor='red', alpha=0.5))
    axs[1, 0].text(0.9825, 0.95, ('\n'.join((str(data[2][-1]), str(data[3][-1]), str(data[4][-1])))), ha='right', va='top', transform=axs[1, 0].transAxes, bbox=dict(facecolor='red', alpha=0.5))
    axs[2, 0].text(0.9825, 0.95, str(data[5][-1]), ha='right', va='top', transform=axs[2, 0].transAxes, bbox=dict(facecolor='red', alpha=0.5))
    axs[0, 1].text(0.9825, 0.95, str(data[6][-1]), ha='right', va='top', transform=axs[0, 1].transAxes, bbox=dict(facecolor='red', alpha=0.5))
    axs[1, 1].text(0.9825, 0.95, str(data[7][-1]), ha='right', va='top', transform=axs[1, 1].transAxes, bbox=dict(facecolor='red', alpha=0.5))
    axs[2, 1].text(0.9825, 0.95, str(data[8][-1]), ha='right', va='top', transform=axs[2, 1].transAxes, bbox=dict(facecolor='red', alpha=0.5))

def main():
    ser = connect_serial()
    start_reading(ser)
    fig, axs = plt.subplots(3, 2)
    ani = FuncAnimation(fig, animate, fargs=(ser, axs), interval=250, save_count=20)
    plt.show()
    


if __name__ == "__main__":
    main()
