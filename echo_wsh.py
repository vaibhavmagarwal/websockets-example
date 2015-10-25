import os
import time


def web_socket_do_extra_handshake(request):
    # This example handler accepts any request. See origin_check_wsh.py for how
    # to reject access from untrusted scripts based on origin value.

    pass  # Always accept.


def web_socket_transfer_data(request):

    # open the specified file
    pt = open("/Users/vagrawal/python-test/a.txt", "r")
    total_lines = pt.readlines()
    lines = total_lines[-10:]

    for line in lines:
        request.ws_stream.send_message(str(line))

    last_modified = time.ctime(os.path.getmtime("/Users/vagrawal/python-test/a.txt"))
    pt.close()

    # have a continuous loop
    while True:
        pt = open("/Users/vagrawal/python-test/a.txt", "r")
        new_modified = time.ctime(os.path.getmtime("/Users/vagrawal/python-test/a.txt"))

        # Check if the file is modified than last read.
        if new_modified != last_modified:
            new_total_lines = pt.readlines()

            # loop through the lines and return the lines which have changed.
            for index in range(0, len(new_total_lines)):
                if index > len(total_lines)-1 or new_total_lines[index] != total_lines[index]:
                    request.ws_stream.send_message(str(new_total_lines[index]))

            # reset the variables for next iteration.
            total_lines = new_total_lines
            last_modified = new_modified
