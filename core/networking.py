

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

        #self.



class _socketThread(threading.Thread):
    encoding = "utf-8"
    def __init__(self, socket):
        self._socket = socket
        self._buffer = queue.Queue()

        self._stop = False
        self.exception = None

        # We will set the network threads as daemons so that we don't
        # have to put additional effort into stopping the threads manually.
        self.daemon = True


    def run(self):
        pass


class ReadSocket(_socketThread):
    encoding = "utf-8"
    def __init__(self, *args, **kwargs):
        super(ReadSocket, self).__init__(*args, **kwargs)

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


    # Every IRC message is made of three main components:
    # The prefix, the command and the arguments. We need to split
    # the incoming messages into these components.
    def _split_msg(self, msg):
        # An IRC message can contain an optional argument prefixed with ':'.
        # It is unique because it can contain spaces, unlike the normal arguments.
        msg_rest, sep, string_arg = msg.partition(" :")

        if not sep:
            string_arg = None


        msg_rest_list = msg_rest.split()

        # An IRC message can start with a prefix,
        # the first character of which must be ':'
        if msg_rest_list[0].startswith(":"):
            prefix = msg_rest_list.pop(0)
            prefix = prefix.lstrip(":")
        else:
            prefix = None

        # An IRC message must contain a command that comes after
        # the prefix
        command = msg_rest_list.pop(0)

        # An IRC message can contain arguments that follow after the command.
        args_list = msg_rest_list

        return prefix, command, args_list, string_arg







class SendSocket(_socketThread):
    def __init__(self, *args, **kwargs):
        super(SendSocket, self).__init__(*args, **kwargs)

    def run(self):
        while not self._stop:
            msg = self._buffer.get()








if __name__ == "__main__":
    raw = ":prefix command   arg1   arg2   :asdasjd aw daw   wadhwawajh "
    #raw = "command   arg1   arg2   :asdasjd aw daw   wadhwawajh "
    #raw = "comand arg1"
    #raw = "command"

    print(ReadSocket._split_msg(None, raw))
