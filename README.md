# Taiko Bot

A simple chat bot for [osu!](https://osu.ppy.sh) in Python. Calculates the PP for an osu!taiko map sent over private message (``/np``). Works very similarly to [Tillerino](https://github.com/Tillerino/Tillerinobot), but a lot of features are still missing.

Note: This is my first project in Python, so a lot will be unefficient or unelegant. Feel free to make as many suggestions (or even pull requests!) as you want! I'm always happy to listen and learn!

A special thanks goes to the osu! user numbermaniac, who wrote an [excellent forum post](https://osu.ppy.sh/community/forums/topics/472288) on how to calculate PP for osu!taiko. Another crucial resource was the [osu!api wiki](https://github.com/ppy/osu-api/wiki).

## TODO

- Documentation! (WIP)
- Further cleanup (Also WIP)
- Difficulty selection when no difficulty is chosen. (Doing ``/np`` in the beatmap selection menu)
- Convert support
- In-console queries?
- Recent play analysis
- The possibility to query other player's plays (dependent on the point above)
- Support for other modes?

## The config file

If you want to run this on your own account, great! You do need an [API key](https://osu.ppy.sh/p/api) and your [IRC password](https://osu.ppy.sh/p/irc) for osu!. Just put those two into the config file and run the bot!

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