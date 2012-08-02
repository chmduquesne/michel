#!env python
"""
Pushes/pulls flat text files to google tasks

USAGE:
    michel pull                 prints the default tasklist on stdout
    michel push <textfile>      replace the default tasklist with the
                                content of <textfile>.
"""
from __future__ import with_statement
import gflags
import httplib2
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run
from xdg.BaseDirectory import save_config_path, save_data_path
import os.path
import sys

class TasksTree():
    """
    Tree for holding tasks

    A TasksTree:
    - is a task (except the root, which just holds the list)
    - has subtasks
    - may have a task_id
    - may have a title
    """

    def __init__(self, title=None, task_id=None):
        """init"""
        self.title = title
        self.task_id = task_id
        self.subtasks = []

    def get(self, task_id):
        """Returns the task of given id"""
        if self.task_id == task_id:
            return self
        else:
            for subtask in self.subtasks:
                if subtask.get(task_id) != None:
                    return subtask.get(task_id)

    def add_subtask(self, title, task_id = None, parent_id = None):
        """
        Adds a subtask to the tree
        - with the specified task_id
        - as a child of parent_id
        """
        if not parent_id:
            self.subtasks.append(TasksTree(title, task_id))
        else:
            if not self.get(parent_id):
                raise ValueError, "No element with suitable parent id"
            self.get(parent_id).add_subtask(title, task_id)

    def last(self, level):
        """Returns the last task added at a given level of the tree"""
        if level == 0:
            return self
        else:
            res = None
            for subtask in self.subtasks:
                res = subtask.last(level - 1) or res
            if res:
                return res

    def push(self, service, list_id, parent = None, root=True):
        """Pushes the task tree to the given list"""
        # We do not want to push the root node
        if not root:
            args = {'tasklist': list_id, 'body':{ 'title' : self.title } }
            if parent:
                args['parent'] = parent
            res = service.tasks().insert(**args).execute()
            self.task_id = res['id']
        # the API head inserts, so we insert in reverse.
        for subtask in reversed(self.subtasks):
            subtask.push(service, list_id, parent=self.task_id, root=False)

    def _lines(self, level):
        """Returns the sequence of lines of the string representation"""
        res = []
        for subtask in self.subtasks:
            indentations = '\t'.join(['' for i in range(level + 1)])
            res.append(indentations + subtask.title)
            subtasks_lines = subtask._lines(level + 1)
            res += subtasks_lines
        return res


    def __str__(self):
        """string representation of the tree"""
        return '\n'.join(self._lines(0))

def get_service():
    """
    Handle oauth's shit (copy-pasta from
    http://code.google.com/apis/tasks/v1/using.html)
    Yes I do publish a secret key here, apparently it is normal
    http://stackoverflow.com/questions/7274554/why-google-native-oauth2-flow-require-client-secret
    """
    FLAGS = gflags.FLAGS
    FLOW = OAuth2WebServerFlow(
            client_id='617841371351.apps.googleusercontent.com',
            client_secret='_HVmphe0rqwxqSR8523M6g_g',
            scope='https://www.googleapis.com/auth/tasks',
            user_agent='michel/0.0.1')
    FLAGS.auth_local_webserver = False
    storage = Storage(os.path.join(save_data_path("michel"), "oauth.dat"))
    credentials = storage.get()
    if credentials is None or credentials.invalid == True:
        credentials = run(FLOW, storage)
    http = httplib2.Http()
    http = credentials.authorize(http)
    return build(serviceName='tasks', version='v1', http=http)

def print_todolist(list_id):
    """Prints the todo list of given id"""
    service = get_service()
    tasks = service.tasks().list(tasklist=list_id).execute()
    tasks_tree = TasksTree()
    tasklist = [t for t in tasks.get('items', [])]
    fail_count = 0
    while tasklist != [] and fail_count < 1000 :
        t = tasklist.pop(0)
        try:
            tasks_tree.add_subtask(t['title'].encode('utf-8'), t['id'], t.get('parent'))
        except ValueError:
            fail_count += 1
            tasklist.append(t)
    print(tasks_tree)

def erase_todolist(list_id):
    """Erases the todo list of given id"""
    service = get_service()
    tasks = service.tasks().list(tasklist=list_id).execute()
    for task in tasks.get('items', []):
        service.tasks().delete(tasklist=list_id,
                task=task['id']).execute()

def parse(path):
    """Parses a todolist file and returns a tree"""
    tasks_tree = TasksTree()
    with open(path) as f:
        curr_indent_lvl = 0
        for n, line in enumerate(f):
            # trim trailing '\n'
            if line[-1] == '\n':
                line = line[:-1]
            # get the indent level
            indent_lvl = 0
            while line[0] == '\t':
                line = line[1:]
                indent_lvl += 1
            assert indent_lvl <= curr_indent_lvl + 1, ("line %d: "
                    "subtask has no parent task" % n)
            curr_indent_lvl = indent_lvl
            tasks_tree.last(indent_lvl).add_subtask(line)
    return tasks_tree

def push_todolist(path, list_id):
    """Pushes the specified file to the specified todolist"""
    tasks_tree = parse(path)
    erase_todolist(list_id)
    tasks_tree.push(get_service(), list_id)

def main():
    if (len(sys.argv)) < 2:
        print(__doc__)
    elif sys.argv[1] == "pull":
        print_todolist('@default')
    elif sys.argv[1] == "push":
        if not len(sys.argv) == 3:
            print("'push' expects exactly 1 argument")
            sys.exit(2)
        path = sys.argv[2]
        if not os.path.exists(path):
            print("The file you want to push does not exist.")
            sys.exit(2)
        push_todolist(path, '@default')
    else:
        print(__doc__)
        sys.exit(2)

if __name__ == "__main__":
    main()
