Radio
=====

Radio is a very, very simple GTK+ client for radio streams.

Create a config file in `~/.config/radio/config`:

    [Radio Name 1]
    url=http://mystream.com/stream1.mp3

    [Radio Name 2]
    url=http://mystream.com/stream2.mp3

You can even add a square icon called `Radio Name 1.ext` in `~/.config/radio`.

Radio requires:

* Python 3.3+
* GTK+ 3.10+ with introspection
* Gstreamer 1.0+ with introspection
