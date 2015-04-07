
import os
import time

from time import mktime
from calendar import timegm
from logging.handlers import BaseRotatingHandler

# Seconds in a day
DAY = 60*60*24

class DailyRotationHandler(BaseRotatingHandler):
    def __init__(self,
                 pathformat="%Y/%m/%Y-%m-%d.log", utc=False,
                 encoding=None, delay=False):

        self.pathformat = pathformat
        self.utc = utc

        # Placeholder function for the info function of the
        # logging module.
        self.logging_writeinfo = lambda *args: None

        current_time = self._get_time()
        current_file = self._format_time(current_time)


        self._current_day = self._get_days_since_epoch(current_time)
        self._create_dirs(os.path.abspath(current_file))

        BaseRotatingHandler.__init__(self,
                                     filename=current_file, mode="a",
                                     encoding=encoding, delay=delay)

    # This function will be used to write information
    # about the rollover, e.g. the new file name that will be
    # written to.
    def set_logging_info_func(self, func):
        self.logging_writeinfo = func

    def shouldRollover(self, record):
        now = self._get_time()
        day = self._get_days_since_epoch(now)

        # The no_rollover attribute can be set when writing a log entry
        # so that no rollover happens. This can be used to keep
        # a set of log entries in the same file.
        if hasattr(record, "no_rollover") and record.no_rollover:
            return False
        elif self._current_day != day:
            self._current_day = day

            return True
        else:
            return False

    def doRollover(self):
        new_filename = os.path.abspath(self._format_time())

        # To prevent the function from going into an infinite recursive
        # loop, the rollover will be disabled using the extra argument.
        self.logging_writeinfo("Rollover is happening! New filename is %s",
                               new_filename, extra={"no_rollover": True})

        if self.stream:
            self.stream.close()
            self.stream = None

        self._create_dirs(new_filename)

        timeoffset, timezone = local_time_offset()

        old_name = self.baseFilename
        self.baseFilename = new_filename
        self.stream = self._open()


        self.logging_writeinfo("Rollover happened! Old filename was %s",
                               old_name,
                               extra={"no_rollover": True})
        self.logging_writeinfo("New filename is %s", new_filename,
                               extra={"no_rollover": True})

        # We want to have a timeoffset string formatted as
        # "+<num>" or "-<num>". If the time offset is 0 or bigger,
        # we need to add the + sign to the string.
        timeoffset_str = str(timeoffset)
        if timeoffset >= 0:
            timeoffset_str = "+"+timeoffset_str

        self.logging_writeinfo("Current time offset: %s (%s)", timeoffset_str, timezone,
                               extra={"no_rollover": True})

    def _create_dirs(self, filepath):
        directories, filename = os.path.split(filepath)
        os.makedirs(directories, exist_ok=True)

    def _get_time(self):
        if self.utc:
            return time.gmtime()
        else:
            return time.localtime()

    def _format_time(self, struct_time=None):
        if struct_time is None:
            struct_time = self._get_time()

        return time.strftime(self.pathformat, struct_time)

    def _get_days_since_epoch(self, struct_time):
        if self.utc:
            return timegm(struct_time) // DAY
        else:
            return mktime(struct_time) // DAY

class TestDatedDailyRotationHandler(DailyRotationHandler):
    def __init__(self, timefunc, *args, **kwargs):
        print("woohoo")
        self._timefunc = timefunc
        DailyRotationHandler.__init__(self, *args, **kwargs)

    def _get_time(self):
        if self.utc:
            return time.gmtime(self._timefunc())
        else:
            return time.localtime(self._timefunc())


# Returns UTC offset and name of time zone at current time
# Based on http://stackoverflow.com/a/13406277
def local_time_offset():
    t = time.time()

    if time.localtime(t).tm_isdst and time.daylight:
        return -time.altzone/3600, time.tzname[1]
    else:
        return -time.timezone/3600, time.tzname[0]

if __name__ == "__main__":
    import logging

    # testfixtures needs to be installed separately,
    # but it is only used for testing the handler.
    from testfixtures import test_time

    #pathfmt = "%Y/%m-%b/%Y-%m-%d.log"
    pathfmt = "%Y/%Y-%m-%b_Week-%W.log"
    my_time = test_time(*time.localtime()[0:5], delta=1, delta_type="hours")

    handler = TestDatedDailyRotationHandler(pathformat=pathfmt, timefunc=my_time, utc=True)#DailyRotationHandler(utc=True)#
    print(handler._format_time())

    logger = logging.getLogger("main")

    handler.set_logging_info_func(logger.info)

    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)


    logger.info("Testing, testing, please work!")

    for i in range(300):
        logger.info("Testing %s", i)