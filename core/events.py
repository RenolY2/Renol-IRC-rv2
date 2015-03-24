

class EventNameAlreadyExists(Exception):
    pass

class Events(object):
    def __init__(self):
        self._events = {}

    def add_event(self, eventname, func):
        if not callable(func):
            raise RuntimeError("func argument must be a function!")
        elif eventname in self._events_:
            raise EventNameAlreadyExists("Event name already exists: "+eventname)
        else:
            self._events[eventname] = func

    def remove_event(self, eventname):
        del self._events[eventname]

    def execute_event(self, eventname, *args, **kwargs):
        if eventname not in self._events_:
            raise RuntimeError("No such Event name '{0}'".format(eventname))
        else:
            self._events_[eventname](*args, **kwargs)

    def execute_all_events(self):
        for eventname, eventfunc in self._events.items():
            pass


class PriorityEvents(Events):
    def __init__(self):
        super(PriorityEvents, self).__init__()
        self._priority_list = []

    # The root flag is for events that are much more important than others,
    # e.g. events used by the internal bot code.
    def add_event(self, eventname, func, priority=0, root=False):
        assert priority >= 0
        if not root:
            priority += 255

        super(PriorityEvents, self).add_event(eventname, func)

        self._priority_list.append((eventname, priority))
        self._priority_list.sort(key=lambda x: x[1])

    def remove_event(self, eventname):
        super(PriorityEvents, self).remove_event(eventname)

        index = None
        for i, event, priority in enumerate(self._priority_list):
            if event == eventname:
                index = i
        deleted_event, priority = self._priority_list.pop(i)
        assert deleted_event == eventname

    def execute_event(self, eventname):
        pass






