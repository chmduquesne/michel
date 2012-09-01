Michel is your friendly mate that helps you managing your todo list. It
can push/pull flat text files to google tasks.

Usage
=====

Configuration
-------------

At the first run, you will be prompted an url. Click it, authorize michel.
You're done!

The authorization token is stored in $XDG_DATA_HOME/michel/oauth.dat. This
is the only information stored.

Commands
--------

Michel keeps it stupid simple. It only has two commands:

    michel pull
Print the default todo list on the standard output

    michel push <TODO.txt>
Replace the default todo list with the content of TODO.txt

Non features
------------

Michel aims at being simple: it does not handle due dates nor notes.

Syntax
------

One line is one task. tab-indented lines (with the real tab character)
are subtasks of the "parent" line.

How to
------

Here is how michel can be used. A crontask pulls every 15 minutes the
default TODO list, and another one displays a notification during 10
seconds every hour (requires notify-send).

    */15 * * * * michel pull > /tmp/TODO && mv /tmp/TODO ~/.TODO
    0 * * * * DISPLAY=":0.0" notify-send -t 10000 TODO "$(cat ~/.TODO)"

After you modify your TODO list, don't forget to push it!

    michel push .TODO

If this trick is not working, it is probably because the variable PATH
does not contains /usr/local/bin in crontab. You might want to set it
manually. See 'man 5 crontab'.

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
