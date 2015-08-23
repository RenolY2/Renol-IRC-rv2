from timeit import default_timer as timer

from time import time
from math import ceil

"""
Here is a rundown of how the delayer for sending messages works:
 - It is initiated with a dict of various key:value pairs, where the key
   is the amount of bytes sent in a second, and the value specifies the delay,
   i.e. how long the program needs to sleep in between two messages sent once
   the current average amount of bytes sent per second is bigger than the key value.
   The keys will also be referred to as "delay groups" or "delay categories"
 -
 - The dict needs to contain an entry for 0, which is the base delay when no messages
   have been sent yet. This also needs to be the smallest entry, so no negative entries allowed.

 - Example: We feed the dict {0: 1, 10: 2, 50: 3} into the delayer.
   As long as we send less than 10 bytes per second, our delay will always be 1. This also
   means that we can send less than 100 bytes every 10 seconds and still have a delay of 1.
   If we send 10 bytes or more, but less than 50 bytes per second, then we will fall into
   the second category and have a delay of 2. If we send >= 50 bytes per second, we will have
   a delay of 3.

 - If we end up in a higher delay category and send very little data, the average amount of
   bytes sent will drop and the delay will change accordingly.


"""


class DelayMessages(object):
    def __init__(self, delays):
        self.delay = 0

        self.delay_groups = [key for key in delays.keys()]
        self.delay_groups.sort()

        if self.delay_groups[0] != 0:
            raise RuntimeError("The smallest delay category needs to be 0!")

        self.delays = delays
        self.delay_level = 0

        # The base delay should be the first entry in the list of delay groups
        self.delay = delays[self.delay_groups[0]]

        self.max = len(delays)

        self.last_time = 0
        self.last_average = None

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


if __name__ == "__main__":
    delayer = DelayMessages({0: 0, 10: 40, 40: 80, 100: 100})
    print( )

    for i in range(10):
        msg = "a"*10
        delayer.send_message(msg, delta=1)
        print("Sent", msg, ", delay is now", delayer.delay,
              ", we are sending >=", delayer.delay_groups[delayer.delay_level], "characters per second")
        print("current average:",delayer.last_average)

    for i in range(10):
        msg = "bb"
        delayer.send_message(msg, delta=1)
        print("Sent", msg, ", delay is now", delayer.delay,
              ", we are sending >=", delayer.delay_groups[delayer.delay_level], "characters per second")
        print("current average:",delayer.last_average)