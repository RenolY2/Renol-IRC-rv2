

import socket
import threading
import queue
import traceback

class Networking(object):
    def __init__(self, host, port,
                 bindIP = "", bindPort = 0,
                 timeOut = 180):

        server_conn = socket.create_connection((host, port), timeOut,
                                            source_address=(bindIP, bindPort))



class _socketThread(threading.Thread):
    def __init__(self, socket):
        self._socket = socket
        self._buffer = queue.Queue()

        self._stop = False
        self.exception = None


    def run(self):
        pass


class RecvSocket(_socketThread):
    def __init__(self, *args, **kwargs):
        super(RecvSocket, self).__init__(*args, **kwargs)

    def run(self):
        line_buffer = ""

        while not self._stop:
            try:
                data = self._socket.read(1024)
            except Exception as error:
                # We will store the traceback so that it can be looked at from the main program.
                self.exception = traceback.format_exc()
                #self.exception_appeared = True
            else:
                # The data we received needs to be broken up at every \n character
                # into different messages.
                # This can be done by adding the data to the line buffer, and then
                # trying to split the line buffer at \n characters.
                line_buffer += data
                lines = line_buffer.split("\n")

                # The last line in the list does not end with a \n, so we will remove it
                # and set the line buffer to it. This also removes the lines that we have processed so far.
                #
                # Because socket reading is a blocking operation, the lines list should never be empty,
                # so the pop() function should never raise an exception due to an empty list.
                # If there is a way it might raise an exception, please add a github issue about it.
                line_buffer = lines.pop()


                for line in lines:
                    # Because we specifically split lines at \n, there can be \r characters
                    # left over in the lines. By stripping away whitespace to the right,
                    # we can remove them.
                    line = line.rstrip()

                    if line:
                        prefix, command, arguments = self._split_msg(line)
                    else:
                        pass #do nothing


    # Every IRC message is made of, at most, three components:
    # The prefix, the command and the arguments. We need to split
    # the incoming messages into these components.
    def _split_msg(self, msg):

        if msg.startswith(":"):
            prefix, cmd, args = msg.split(" ", 2)
        else:
            prefix = None
            cmd, args = msg.split(" ", 1)







class SendSocket(_socketThread):
    def __init__(self, *args, **kwargs):
        super(SendSocket, self).__init__(*args, **kwargs)

    def run(self):
        while not self._stop:
            pass






if __name__ == "__main__":
    string = ""
    string2 = "abc"

    if string:
        print("herp")
    if not string:
        print("durp")
    if string2:
        print("herp")
    if not string2:
        print("durp")