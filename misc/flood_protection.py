import abc

from math import ceil
from timeit import default_timer as timer


class WrongModeException(Exception):
    def __init__(self, incorrect_mode, mode_list):
        self.mode = incorrect_mode
        self.mode_list = mode_list

    def __str__(self):
        return "Received '{0}', but mode of operation must be one of {1}".format(
            self.mode, self.mode_list
        )


class FloodController:
    __metaclass__ = abc.ABCMeta

    def __init__(self, config):
        self.delay = 0
        self.last_time = 0
        self.last_average = None

    @abc.abstractmethod
    def calculate_delay(self, msg):
        pass


class MessageCountController(FloodController):
    def __init__(self, config):
        super().__init__(config)

        self.burst = config["burst_count_per_10_seconds"]
        self.msg_queue = []
        self.time_limit = 10
        self.base_delay = config["base_delay"]
        self.max_delay = config["max_delay"]

    def calculate_delay(self, msg):
        now = timer()
        time_limit = self.time_limit

        new_queue = [filtered_time for filtered_time in filter(lambda x: (now-x) <= time_limit,
                                                               self.msg_queue)]
        new_queue.append(now)

        self.msg_queue = new_queue

        if len(new_queue) > self.burst:
            return self.max_delay
        else:
            return self.base_delay


class ByteCountController(FloodController):
    def __init__(self, config):
        super().__init__(config)

        delays = config

        self.delay_groups = [key for key in delays.keys()]
        self.delay_groups.sort()

        if self.delay_groups[0] != 0:
            raise RuntimeError("The smallest delay category needs to be 0!")

        self.delays = delays
        self.delay_level = 0

        # The base delay should be the first entry in the list of delay groups
        self.delay = delays[self.delay_groups[0]]

        self.max = len(delays)

    def calculate_delay(self, msg):
        return self.send_message(msg, delta=None)

    def send_message(self, msg, delta=None):
        self.delay = 0

        # Calculate the time delta
        now = timer()
        if delta is None:
            diff = now - self.last_time
        else:
            diff = delta

        # If the time difference between two messages is 1, then the
        # average bytes sent will go up instead of going down or staying
        # the same. For that reason we will add 1 to the diff. This also
        # prevents division by 0 errors (as long as the difference isn't negative)
        if self.last_average is None:
            average_bytes_sent = len(msg)
        else:
            average_bytes_sent = (self.last_average + len(msg)) // (diff+1)

        # Now we know which delay group the value belongs to, and the position of that group
        # in the delay_groups list.
        delay_group, group_pos = self.get_limit(average_bytes_sent)

        self.last_average = average_bytes_sent
        self.last_time = now
        self.delay_level = group_pos
        self.delay = self.delays[delay_group]

        return self.delay

    # Given a specific value, check which limit group the value belongs to.
    # When the value lies between two limit groups, the lower group is chosen.
    # Bonus: We use binary search, so the time complexity is log(n)
    def get_limit(self, val):
        delay_groups = self.delay_groups

        start = 0
        end = len(delay_groups)-1

        while start < end:
            middle = ceil((start+end) / 2)
            #print(middle, start, end)

            if val < delay_groups[middle]:
                end = middle-1
            elif val > delay_groups[middle]:
                start = middle
            else:
                return delay_groups[middle], middle

        return delay_groups[end], end


class FloodControlManager(object):
    CONTROLLERS = {"msg_count": MessageCountController,
                   "byte_count": ByteCountController}

    def __init__(self, mode, config):
        if mode not in self.CONTROLLERS:
            raise WrongModeException(mode, self.CONTROLLERS.values())

        self.controller = self.CONTROLLERS[mode](config)

    def calculate_delay(self, msg):
        return self.controller.calculate_delay(msg)


if __name__ == "__main__":
    """
    from time import sleep

    #controller = FloodControlManager("msg_count", config={"burst_count_per_10_seconds": 5,
    #                                                      "base_delay": 0})

    controller = FloodControlManager("byte_count", config={0: 0, 10: 5})

    for i in range(15):
        print(controller.calculate_delay("hello!"))
        #sleep(1.9)"""

