Michel is your friendly mate that helps you managing your todo list. It
can push/pull flat text files to google tasks.

Keeping it stupid simple
========================

Michel has only two commands:

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

Installing
==========

install python-xdg, then run

    easy_install michel

About
=====

Author/License
--------------

- License: Public Domain
- Original author: Christophe-Marie Duquesne ([blog post](http://blog.chmd.fr/releasing-michel-a-flat-text-file-to-google-tasks-uploader.html))

Contributing
------------

As usual, patches are welcome.
