fdwatch
=======

A tool for watching a given file descriptor.

This program is intended for **Linux** users that would like to watch how fast
is a file being read or written to and - in case of a read - when will the
operation be completed. This can for example be useful during a compression of
a file, when there's no ETA shown (like in 7zip's case it was actually the
reason I wrote it).


Installation
============

The script should work immediately after downloading. It requires Python
installed. To try running it, type "python fdwatch.py". For convenience, you
might want to copy it to your /usr/bin or /usr/local directory and add it the
executable permissions, like this:

    cp fdwatch.py /usr/bin/fdwatch
    chmod +x /usr/bin/fdwatch

This usually has to be done using the administrator account (use `sudo -i` or
`su` to switch to it - in case of problems, seek help from your Linux
distrubution's provider (usually that means "RTFM" - Read The Fabulous
Manual). Once completed, your terminal should react to a new command -
"fdwatch". Sometimes before the first use you might need to re-run the command
line shell or reload the executable cache (the first should imply the second).

For usage hints, read on.

Usage
=====

To make fdwatch work, you must call it with two parameters - the process ID
which holds the file you want to watch and the file descriptor number. Once you
know these two numbers, just run the script like this (let's say 1234 is the
process ID and 3 is the file descriptor number):

    python fdwatch.py 1234 3

To find out the process ID of the program you're running, you can use `ps` and
`grep` programs. For example, to find out the process ID of a running `7z`
program:

    d33tah@d33tah-pc:/home/d33tah$ ps waux | grep 7z
    d33tah   20563  0.0  0.0   9528   988 pts/3    S+   23:28   0:00 /bin/sh /usr/bin/7z a traceroute.7z traceroute
    d33tah   20564  173  2.3 233560 183212 pts/3   Rl+  23:28   0:06 /usr/libexec/p7zip/7z a traceroute.7z traceroute
    d33tah   20598  0.0  0.0   9044   548 pts/7    S+   23:28   0:00 grep --color=auto 7z

Process ID's are in the second column. The last line is irrelevant, we should
probably look at processes number 20563 and 20564. To list the file descriptors
and the files they point to, we'll use `ls -l`, like this:

    d33tah@d33tah-pc:/home/d33tah$ ls -l /proc/20563/fd
    total 0
    lrwx------. 1 d33tah d33tah 64 Jul 28 23:31 0 -> /dev/pts/3
    lrwx------. 1 d33tah d33tah 64 Jul 28 23:31 1 -> /dev/pts/3
    lrwx------. 1 d33tah d33tah 64 Jul 28 23:30 2 -> /dev/pts/3
    lr-x------. 1 d33tah d33tah 64 Jul 28 23:31 255 -> /usr/bin/7z*
    d33tah@d33tah-pc:/home/d33tah$ ls -l /proc/20564/fd
    total 0
    lrwx------. 1 d33tah d33tah 64 Jul 28 23:31 0 -> /dev/pts/3
    lrwx------. 1 d33tah d33tah 64 Jul 28 23:31 1 -> /dev/pts/3
    lrwx------. 1 d33tah d33tah 64 Jul 28 23:30 2 -> /dev/pts/3
    l-wx------. 1 d33tah d33tah 64 Jul 28 23:31 3 -> /mnt/sda9/d33tah/traceroute.7z
    lr-x------. 1 d33tah d33tah 64 Jul 28 23:31 4 -> /mnt/sda9/d33tah/traceroute

The first command didn't yield any interesting results, but the second shows us
the two files we'd like to watch - /mnt/sda9/d33tah/traceroute and
`/mnt/sda9/d33tah/traceroute.7z. The `4 -> /mnt/sda9/d33tah/traceroute` line
means that the file is open with file descriptor number 4. Now, that's enough
to start fdwatch. To make it estimate how long will the compression take, run
it now (your current working directory must contain fdwatch.py - if it doesn't,
prepend the path to it to the command or install the script - see above).
Here's an example:

    d33tah@d33tah-pc:/home/d33tah$ python fdwatch.py 20564 4
    4.81%, 9.0 MB/s, ETA: ETA=31m 55s
    4.86%, 9.0 MB/s, ETA: ETA=31m 54s
    (and it goes on, until the process finishes its job...)
    Traceback (most recent call last):
      File "/bin/fdwatch", line 83, in <module>
        fd = open("/proc/%s/fdinfo/%s" % (pid,fdno))
    IOError: [Errno 2] No such file or directory: '/proc/20564/fdinfo/4'


How does it work?
=================

The script uses the /proc special Linux directory that contains info about
processes - a separate directory for each process. The script opens the
/proc/PID/fdinfo/FD-NUMBER file every second and compares the head position to
the last saving state, calculating all the values needed.

Bugs, problems
==============

The script's at the moment pretty poorly documented and I didn't go great
lengths to make it user-friendly; patches are welcome, though! As for the bugs,
if the file is being written to, you'll keep seeing 100% file read. There's
also no error checking and during testing, the script sometimes crashed
(actually, it's currently its way to notify the user that the process shut
down).

TO-DO list
==========

I'm thinking of rewriting this toy to C language or turn it into an extension
to "pv" program. Adding support for more platforms would be nice, too. It could
probably also use more output options and perhaps some localization for
non-English users. Also, maybe configurable polling intervals?

Please keep in mind, that it's you, dear user, that is most important here.
Should you have an idea for a specific feature that you could find useful, let
me know and I'll implement it if it fits my vision of the project.

Author, license
===============

This application was written by Jacek Wielemborek <d33tah@gmail.com>. My blog
can be found here:
[http://deetah.jogger.pl/kategoria/english/](http://deetah.jogger.pl/kategoria/english/)

If you're not a viagra vendor, feel free to write me an e-mail, I'd be happy to
hear that you use this program!

This program is Free Software and is protected by GNU General Public License
version 3. Basically, it gives you four freedoms:


Freedom 0: The freedom to run the program for any purpose.

Freedom 1: The freedom to study how the program works, and change it to make
    it do what you wish.

Freedom 2: The freedom to redistribute copies so you can help your neighbor.

Freedom 3: The freedom to improve the program, and release your improvements
    (and modified versions in general) to the public, so that the whole
     community benefits.

In order to protect that freedom, you must share any changes you did to the
program with me, under the same license. For details, read the LICENSE file
attached to the program.
