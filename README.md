Michel is your friendly mate that helps you managing your todo list. It
can push/pull flat text files to google tasks.

Usage
=====

Commands
--------

Michel keeps it stupid simple. It only has two commands:

    michel pull
which prints the default todo list on the standard output

    michel push <TODO.txt>
which replaces the default todo list with the content of TODO.txt

Non features
------------

Michel aims at being simple: it does not handle due dates nor notes.

Syntax
------

One line is one task. Indented lines are subtasks of the "parent" line.

Suggestion
----------

Here is how michel can be used. A crontask pulls every 15 minutes the
default TODO list:

    */30 * * * * michel pull > ${HOME}/.TODO

The following script is used to display a notification during 10 seconds every
hour (requires notify-send - usually in a package called libnotify - and some
notification-daemon - provided with most desktops)

    #!/usr/bin/env bash
    DISPLAY=:0.0
    #params
    todofile=$HOME/.TODO
    icon='/usr/share/icons/gnome/32x32/status/dialog-information.png'
    popupTime=10000
    urgency='low'
    if test -f $todofile; then
        notification=`cat $todofile`
        notify-send -u $urgency -t $popupTime -i "$icon" TODO "$notification"
    fi

Also called in a cron task, every hour:

    1 * * * * todo.sh

After you modify your TODO list, don't forget to push it!

    michel push .TODO

Installing
==========

install python-xdg, then run

    easy_install michel

or

    pip install michel

About
=====

Author/License
--------------

- License: Public Domain
- Original author: Christophe-Marie Duquesne ([blog post](http://blog.chmd.fr/releasing-michel-a-flat-text-file-to-google-tasks-uploader.html))

Contributing
------------

As usual, patches are welcome.
