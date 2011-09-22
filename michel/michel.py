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

def get_service():
    """
    Handle oauth's shit (copy-pasta from
    http://code.google.com/apis/tasks/v1/using.html)
    """
    FLAGS = gflags.FLAGS
    FLOW = OAuth2WebServerFlow(
            client_id='617841371351.apps.googleusercontent.com',
            client_secret='i5hU5w1Frj4RuLFTFLT5dRZw',
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

def print_todolist():
    service = get_service()
    tasks = service.tasks().list(tasklist='@default').execute()
    levels = {}
    for task in tasks.get('items', []):
        parent_id = task.get('parent')
        if parent_id:
            level = levels[parent_id] + 1
        else:
            level = 0
        levels[task['id']] = level
        print('\t'.join(['' for i in range(level + 1)]) + task['title'])

def wipe_todolist():
    service = get_service()
    tasks = service.tasks().list(tasklist='@default').execute()
    for task in tasks.get('items', []):
        service.tasks().delete(tasklist='@default',
                task=task['id']).execute()

def push_todolist(path):
    wipe_todolist()
    service = get_service()
    with open(path) as f:
        last_inserted = None
        last_inserted_at_level = {}
        for line in f:
            if line[-1] == '\n':
                line = line[:-1]
            level = 0
            while line[0] == '\t':
                line = line[1:]
                level += 1
            args = {'tasklist':'@default', 'body':{ 'title' : line } }
            if level:
                args['parent'] = last_inserted_at_level[level - 1]
            if args.get('parent') != last_inserted:
                args['previous'] = last_inserted_at_level[level]
            result = service.tasks().insert(**args).execute()
            last_inserted = result['id']
            last_inserted_at_level[level] = result['id']

def main():
    if (len(sys.argv)) < 2:
        print(__doc__)
    elif sys.argv[1] == "pull":
        print_todolist()
    elif sys.argv[1] == "push":
        if not len(sys.argv) == 3:
            print("'push' expects exactly 1 argument")
            sys.exit(2)
        path = sys.argv[2]
        if not os.path.exists(path):
            print("The file you want to push does not exist.")
            sys.exit(2)
        push_todolist(path)
    else:
        print(__doc__)
        sys.exit(2)

if __name__ == "__main__":
    main()
