Michel is a bridge between google tasks and plain text files.

Usage
=====

Typical usage
-------------

First, we save our tasks in a file:

    michel pull > ~/.TODO

The file `~/.TODO` now contains our tasks, as a tab-indented list:

    shopping
    	milk
    	cheese
    	butter
    work
    	call Joe
    	prepare presentation

We will then edit our tasks. Let's add "coffee" in the shopping list. The
syntax is to use one line per item, and in order to make an item part of a
sublist, one needs to put a tab caracter in front of it:

    shopping
    	coffee
    	milk
    	cheese
    	butter
    work
    	call Joe
    	prepare presentation

We can now upload our new task list to gtasks:

    michel push ~/.TODO

Configuration
-------------

At the first run, you will be prompted an url. Click it, authorize michel.
You're done! Michel will save the authorization token as
$XDG_DATA_HOME/michel/oauth.dat. No other data about your account is
stored, and this token is the only information michel needs to access your
tasks.

Commands
--------

Michel keeps it stupid simple. It only has the two previously mentionned
commands:

    michel pull
Print the default todo list on the standard output

    michel push <TODO.txt>
Replace the default todo list with the content of TODO.txt

Usage suggestion
----------------

Here is how the author uses michel. A crontask pulls every 15 minutes the
default TODO list, and another one displays a notification during 10
seconds every hour (requires notify-send).

    */15 * * * * michel pull > /tmp/TODO && mv /tmp/TODO ~/.TODO
    0 * * * * DISPLAY=":0.0" notify-send -t 10000 TODO "$(cat ~/.TODO)"

After you modify your TODO list, don't forget to push it!

    michel push .TODO

If this trick is not working, it is probably because the variable PATH
does not contains /usr/local/bin in crontab. You might want to set it
manually. See 'man 5 crontab'.


Non features
------------

Michel aims at being simple: it does not handle due dates nor notes. Do
NOT use michel on your tasks list if it contains such information: it will
wipe it.

Installing
==========

install python-xdg, then run

    pip install michel

About
=====

Author/License
--------------

- License: Public Domain
- Original author: Christophe-Marie Duquesne ([blog post](http://blog.chmd.fr/releasing-michel-a-flat-text-file-to-google-tasks-uploader.html))

Contributing
------------
Patches are welcome, as long as they keep the source simple and short.

Neat forks
----------

- If you are an emacs orgmode user, you should have a look at
  [michel-orgmode](https://bitbucket.org/edgimar/michel-orgmode).
- There's also a fork of michel that supports
  [due-dates](https://github.com/WillForan/michel)

