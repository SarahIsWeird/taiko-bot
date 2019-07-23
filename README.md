# Taiko Bot

A simple chat bot for [osu!](https://osu.ppy.sh) written in Python. Calculates the PP for an osu!taiko map sent over private message (``/np``). Works very similarly to [Tillerino](https://github.com/Tillerino/Tillerinobot), but a lot of features are still missing.

Note: This is my first project in Python, so a lot will be unefficient or unelegant. Feel free to make as many suggestions (or even pull requests!) as you want! I'm always happy to listen and learn!

A special thanks goes to the osu! user numbermaniac, who wrote an [excellent forum post](https://osu.ppy.sh/community/forums/topics/472288) on how to calculate PP for osu!taiko. Another crucial resource was the [osu!api wiki](https://github.com/ppy/osu-api/wiki).

## TODO

- Difficulty selection when no difficulty is chosen. (Doing ``/np`` in the beatmap selection menu)
- Convert support
- Recent play analysis
- The possibility to query other player's plays (dependent on the point above)
- Support for other modes?

## Running the bot

After filling out the config file, the only thing left to do is starting the bot and you're good to go! You need [Python](https://python.org) to run it.

On Windows, you can just double-click the ``main.py`` file! If you want to start it from console, you simply type

```bash
main.py
```

or

```bash
python main.py
```

On Linux and OSX you open a terminal in the directory of the bot and type

```bash
python3 main.py
```

The bot should start without any problems, listening to any incoming ``/np``s!

## The config file

The [config file system](config.py) is written by me and is very rudimentary. Right now it supports strings and integers, but if the need arises, other data types might be added in the future. Comments are also possible, but only whole-line comments. Empty lines, as well as lines only containing a ``=`` are ignored.
If a line either looks like this

```
key=
```

or like this,

```
=value
```

the bot won't start. This was implemented because it indicates that you forgot to put something into the file. A line number as well as the key/value which was given is shown to help you find the problem.

### Currently used config entries

Entry|What is this?|Data type
-|-|-
ircServer|The URL of Bancho (the IRC server).|string
port|The port of the IRC server.|int
username|The IRC username (aka your in-game name).|string
pw|The IRC password.|string
recv_buf|The size of the received IRC data.|int
rate_limit|The delay of messages sent over IRC.msg().|int
burst_time|The time a user has to wait between calls.|int
minute_count|The number of calls allowed per minute.|int
api_key|The API key for the osu!api.|string