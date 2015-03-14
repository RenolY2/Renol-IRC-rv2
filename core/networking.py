


import socket
import threading
import queue
import traceback

from time import sleep

class Networking(object):
    def __init__(self, host, port,
                 bind_ip = "", bind_port = 0,
                 timeout = 180):

        server_conn = socket.create_connection((host, port), timeout,
                                            source_address=(bind_ip, bind_port))

        self.ReadThread = ReadSocket(server_conn)
        self.SendThread = SendSocket(server_conn)

    def start_threads(self):
        self.ReadThread.start()
        self.SendThread.start()

    def set_encoding(self, encoding):
        self.ReadThread.encoding = encoding
        self.SendThread.encoding = encoding

    def send_msg(self, *args, **kwargs):
        self.SendThread.send_msg(*args, **kwargs)
    def read_msg(self, *args, **kwargs):
        return self.ReadThread.read_msg(*args, **kwargs)

class _socketThread(threading.Thread):
    encoding = "utf-8"

    def __init__(self, socket):
        super(_socketThread, self).__init__()

        self._socket = socket
        self._buffer = queue.Queue()

        self._stop = False
        self.exception = None

        # We will set the network threads as daemons so that we don't
        # have to put additional effort into stopping the threads manually.
        self.daemon = True

    def set_encoding(self, encoding):
        self.encoding = encoding

    def run(self):
        pass


class ReadSocket(_socketThread):
    def __init__(self, *args, **kwargs):
        super(ReadSocket, self).__init__(*args, **kwargs)

    def run(self):
        line_buffer = ""

        while not self._stop:
            try:
                data = self._socket.recv(1024)
            except Exception as error:

                # We will store the traceback so that it can be looked at from the main program.
                self.exception = traceback.format_exc()
                print(self.exception)
                self._stop = True
                #self.exception_appeared = True
            else:
                # The data we received needs to be broken up at every \n character
                # into different messages.
                # This can be done by adding the data to the line buffer, and then
                # trying to split the line buffer at \n characters.
                line_buffer += data.decode(self.encoding)
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
                        prefix, command, arguments, message = self._split_msg(line)
                        self._buffer.put((prefix, command, arguments, message))
                    else:
                        pass #do nothing

    def read_msg(self):
        try:
            value = self._buffer.get_nowait()
        except queue.Empty:
            value = None
        return value

    # Every IRC message is made of three main components:
    # The prefix, the command and the arguments. We need to split
    # the incoming messages into these components.
    @staticmethod
    def _split_msg(msg):
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
            prefix, command, args, message = self._buffer.get()
            msg = self._pack_msg(prefix, command, args, message) + "\r\n"

            print("Sent away:",msg)
            self._socket.send(msg.encode("utf-8"))
            sleep(2)

    @staticmethod
    def _pack_msg(prefix, command, arguments, message):
        msg_assembly = []

        if prefix is not None:
            msg_assembly.append(":"+prefix)
        msg_assembly.append(command)

        msg_assembly.extend(arguments)

        if message is not None:
            msg_assembly.append(":"+message)

        msg = " ".join(msg_assembly)
        return msg


    def send_msg(self, command, arguments = [], message = None, prefix = None):
        for arg in arguments:
            # Arguments cannot contain space characters. To prevent the irc server
            # from interpreting our message incorrectly, we will raise an exception
            # right here.
            if " " in arg:
                raise RuntimeError( "Illegal space inside Argument: '{0}'"
                                    "from arguments '{1}'".format(arg, arguments))

        self._buffer.put((prefix, command, arguments, message))








if __name__ == "__main__":
    test_messages = [
        (None, "command", [], None),
        (None, "command", ["arg1"], None),
        ("prefix", "command", [], None),
        ("prefix", "command", ["arg1"], None),

        (None, "command", [], "test message"),
        (None, "command", ["arg1"], "test message"),
        ("prefix", "command", [], "test message"),
        ("prefix", "command", ["arg1"], "test message"),
    ]

    for msg in test_messages:
        msg = ("someprefix", "somecommand", ["arg1", "arg2"], None)
        packed = SendSocket._pack_msg(*msg)
        unpacked = ReadSocket._split_msg(packed)
        re_packed = SendSocket._pack_msg(*unpacked)

        assert msg == unpacked
        assert packed == re_packed
        print("Test successful for message:", msg)

    print("All tests were successful!")


