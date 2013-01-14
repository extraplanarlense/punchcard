import argparse
import pickle

from datetime import datetime, timedelta


class Task():
    #start_time: datetime
    #stop_time: datetime
    #status: bool
    #name: str

    def __init__(self, name):
        self.name = name
        self.times = []
        self.start_time = None

    def start(self):
        if self.start_time is None:
            time = datetime.now().replace(microsecond=0)
            self.start_time = time
        else:
            raise Exception('Task is already active')

    def stop(self):
        if self.start_time is None:
            raise Exception('Task isn\'t currently active')
        else:
            time = datetime.now().replace(microsecond=0)
            self.times.append([self.start_time, time])
            self.start_time = None


class Punchcard():
    RUNNING = "running"
    STOPPED = "stopped"
    NONEXISTENT = "nonexistent"

    def __init__(self, filename='Tasks.data'):

        self.filename = filename
        self.load()
        self.liste = [(u, v) for u, v in enumerate(self.tasks.keys())]

    def start(self, name):
        self.load()
        if name in self.tasks:
            self.tasks[name].start()
        else:
            new_task = Task(name)
            self.tasks[name] = new_task
            self.tasks[name].start()
        print("Task '{0}' successfully started'".format(name))
        self.liste = [(u, v) for u, v in enumerate(self.tasks.keys())]
        self.save()

    def stop(self, name):
        self.load()
        if name in self.tasks:
            self.tasks[name].stop()
            print("Task '{0}' successfully stopped'".format(name))
        else:
            print("Task can't be stopped since it\
            isn't active at the moment")
        self.liste = [(u, v) for u, v in enumerate(self.tasks.keys())]
        self.save()

    def show_task(self, name):
        if name in self.tasks:
            if self.tasks[name].start_time == None:
                print("Task: '{0}'".format(name),
                      '(inactive)', '\n', '-' * 20)
            else:
                print("Task: '{0}'".format(name), '(active)', '\n', '-' * 20)
            for task in self.tasks[name].times:
                print('started: {0} stopped: {1} duration: {2:10}'
                      .format(task[0], task[1], task[1] - task[0]))
            print(20 * '-', '\n', 'total time: ',
                  self.time_elapsed(name), '\n')
        else:
            print("Task isn't known")

    def show_task_list(self):
        print('List of all tasks:\n', 20 * '-')
        for task in enumerate(self.tasks.keys(), 1):
            if self.tasks[task[1]].start_time == None:
                print('{0:2}: {1:10} (inactive)   total time: {2}'
                      .format(task[0], task[1], self.time_elapsed(task[1])))
            else:
                print('{0:2}: {1:10} (active)     total time: {2}'
                      .format(task[0], task[1], self.time_elapsed(task[1]) + \
                        (datetime.now().replace(microsecond=0) - \
                         self.tasks[task[1]].start_time)))
        if self.tasks == None:
            print('(empty)')

    def status(self, name):
        pass

    def elapsed(self, name, started, until):
        pass

    def time_elapsed(self, name):
        time_elapsed = timedelta()
        for (start, stop) in self.tasks[name].times:
            time_elapsed += stop - start
        return time_elapsed

    def save(self):
        with open(self.filename, 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
            pickle.dump(self, f)

    def load(self):
        try:
            with open(self.filename, 'rb') as f:
                data = pickle.load(f)
                self.tasks = data.tasks
        except IOError:
            self.tasks = {}

    def remove_task(self, name):
        if name in self.tasks:
            del self.tasks[name]
            self.liste = [(u, v) for u, v in enumerate(self.tasks.keys())]
            print("Task has been successfully removed")
        else:
            print("Task can't be removed since it isn't known")
        self.save()

    def status_task(self, name):
        if name in self.tasks:
            if self.tasks[name].start_time == None:
                print('Task is (inactice)')
            else:
                print('Task is (actice)')
        else:
            print("Can't grab status of the\
            task since it isn't known")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A Punchcard which can manage different tasks")
    parser.add_argument("-s", "--start", metavar='task', type=str, help="starts the timer for the task")
    parser.add_argument("-p", "--pause", metavar='task / number', type=str, help="stops the timer for the task")
    parser.add_argument("-v", "--view", metavar='task / number', type=str, help="view the detailed informations of a task")
    parser.add_argument("-r", "--remove", metavar='task / number', type=str, help="removes a task from the list")
    parser.add_argument("-t", "--time", metavar='task / number', type=str, help="total time of a task")
    parser.add_argument("-x", "--status", metavar='task / number', type=str, help="status of the task")
    parser.add_argument("-l", "--list", action="store_true", help="show a list of all tasks")
    args = parser.parse_args()
    p = Punchcard()
    if args.start:
        if args.start.isdigit():
            for x in p.liste:
                if x[0] + 1 == int(args.start):
                    p.start(x[1])
                    break
        else:
            p.start(args.start)
    elif args.pause:
        if args.pause.isdigit():
            for x in p.liste:
                if x[0] + 1 == int(args.pause):
                    p.stop(x[1])
                    break
        else:
            p.stop(args.pause)
    elif args.view:
        if args.view.isdigit():
            for x in p.liste:
                if x[0] + 1 == int(args.view):
                    p.show_task(x[1])
                    break
        else:
            p.show_task(args.view)
    elif args.remove:
        if args.remove.isdigit():
            for x in p.liste:
                if x[0] + 1 == int(args.remove):
                    p.remove_task(x[1])
        else:
            p.remove_task(args.remove)
    elif args.list:
        p.show_task_list()
    elif args.time:
        if args.time.isdigit():
            for x in p.liste:
                if x[0] + 1 == int(args.time):
                    print("Task '{0}' total time: {1}".
                          format(p.tasks[x[1]].name, p.time_elapsed(x[1])))
        else:
            print("Task '{0}' total time: {1}".
                format(p.tasks[args.time].name, p.time_elapsed(x[args.time])))
    elif args.status:
        if args.status.isdigit():
            for x in p.liste:
                if x[0] + 1 == int(args.status):
                    p.status_task(x[1])
        else:
            p.status_task(args.status)
    else:
        print('please use -h for help')
