import serial
import time

# ID the serial ports that appear the same


def usb_id(name_list=['face'], usb_prefix="/dev/ttyACM", baud_rate=115200, timeout=1):
    # Set timeout while waiting for each port's response
    num_ports = len(name_list)
    ports = {}

    for name in name_list:
        ports[name] = None

    connections = 0

    for j in range(10):
        if connections >= num_ports:
            break
        try:
            port_name = "{}{}".format(usb_prefix, j)
            ser = serial.Serial(port_name, baud_rate)
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            connections += 1

            # Opening serial port reboots Arduino, wait a bit before trying to talk
            time.sleep(2)

            ser.write(b'i')

            handshake_done = False
            start = time.time()
            while True:
                if time.time()-start > timeout:
                    print("USB{} handshake timed out".format(j))
                    break
                line = ser.readline().decode("utf-8").rstrip("\r\n")
                if line != "":
                    for n in name_list:
                        if line == n:
                            ports[n] = serial.Serial(port_name, baud_rate)
                            ser.write(b'd')
                            ser.close()
                            print("USB{} is {}".format(j, n))
                            handshake_done = True
                    if not handshake_done:
                        print("USB{} did not have a matching name".format(j))
                    break

        except serial.SerialException:
            print("Can not open USB{}".format(j))

    return ports


def take_command(msg, ports, timeout=1):
    print("")

    finished = False

    parsed = msg.split(" ")
    cmd = parsed[0]
    if len(parsed) == 2:
        arg = parsed[1]
    else:
        arg = 0

    if cmd == "drive_forward":
        ports["drive"].write("<forward>".encode('utf-8'))
    elif cmd == "drive_backward":
        ports["drive"].write("<backward>".encode('utf-8'))
    elif cmd == "drive_right":
        ports["drive"].write("<right>".encode('utf-8'))
    elif cmd == "drive_left":
        ports["drive"].write("<left>".encode('utf-8'))

    if cmd == "head_up":
        ports["head"].write("<Nod Up>".encode('utf-8'))
    elif cmd == "head_down":
        ports["head"].write("<Nod Down>".encode('utf-8'))
    elif cmd == "head_left":
        ports["head"].write("<Turn Left>".encode('utf-8'))
    elif cmd == "head_right":
        ports["head"].write("<Turn Right>".encode('utf-8'))
    elif cmd == "head_up_stop" or cmd == "head_down_stop":
        ports["head"].write("<Stop Nodding>".encode('utf-8'))
    elif cmd == "head_left_stop" or cmd == "head_right_stop":
        ports["head"].write("<Stop Turning>".encode('utf-8'))

    if cmd == "payload_one":
        ports["payload"].write("<snack1>".encode('utf-8'))
    elif cmd == "payload_two":
        ports["payload"].write("<snack2>".encode('utf-8'))
    elif cmd == "payload_three":
        ports["payload"].write("<snack3>".encode('utf-8'))
    elif cmd == "payload_four":
        ports["payload"].write("<snack4>".encode('utf-8'))

    if cmd == "face_loading":
        ports["face"].write("<loading>".encode('utf-8'))
    elif cmd == "face_happy":
        ports["face"].write("<happy>".encode('utf-8'))
    elif cmd == "face_angry":
        ports["face"].write("<angry>".encode('utf-8'))
    elif cmd == "suprise":
        ports["face"].write("<suprise,{}>".format(arg).encode('utf-8'))
    elif cmd == "face_happy_emphasis":
        ports["face"].write("<happy_emphasis,{}>".format(arg).encode('utf-8'))
    elif cmd == "face_sad":
        ports["face"].write("<sad,{}>".format(arg).encode('utf-8'))
    elif cmd == "face_neutral":
        ports["face"].write("<neutral>".encode('utf-8'))
    elif cmd == "face_bounce":
        ports["face"].write("<bounce>".encode('utf-8'))

    return finished

# write commands to stop motions at each subsystem


def finish(ports):
    ports["motor"].write("<brake,0>".encode("utf-8"))


if __name__ == "__main__":

    name_list = ["motor", "sensors"]
    ports = usb_id(name_list=name_list, usb_prefix="/dev/ttyACM",
                   baud_rate=9600, timeout=1)

    finished = False
    while not finished:
        finished = take_command(ports)

    finish(ports)
    exit()
# drive, face, head, payload
