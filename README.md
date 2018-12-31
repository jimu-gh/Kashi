
<h1 align="center">KASHI · 歌詞 · かし</h1>

![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)
![love](http://forthebadge.com/images/badges/built-with-love.svg)

![build](https://img.shields.io/badge/build-passing-brightgreen.svg?style=for-the-badge)  ![license](https://img.shields.io/badge/license-GPLv3-blue.svg?style=for-the-badge) ![license](https://img.shields.io/badge/PRs-welcome-yellow.svg?style=for-the-badge)

Kashi is a custom widget for [BetterTouchTool](https://folivora.ai/) that displays the current song's lyrics on the Macbook Pro's Touch Bar. It works with [Spotify](https://www.spotify.com/us/download/other/) and [iTunes](https://www.apple.com/itunes/download/).

Kashi has three main functions:
1. It gets the current song playing via AppleScript.
2. It searches the [Genius API](https://docs.genius.com/) and looks for the best match within the hits.
3. It scrapes lyrics from the raw HTML, formats, and outputs them onto the Touch Bar.

## Installation

### Step 1: Install BetterTouchTool

Kashi was made for BTT, so first you will need to download and install [BetterTouchTool](https://folivora.ai/). The software is free to use (to an extent).

### Step 2: Install Python & Necessary Modules

Install [Python 3](https://www.python.org/downloads/release/python-371/) and the [PyPI](https://pypi.org/) modules below.<br>
To learn how to install a file from PyPI, visit the [installation tutorial](https://packaging.python.org/tutorials/installing-packages/#installing-from-pypi) on the Python Packaging User Guide.

  - [OSAscript](https://pypi.org/project/osascript/)<br>
  `pip install osascript` or `pip3 install osascript`
  - [Requests](https://pypi.org/project/requests/)<br>
  `pip install requests` or `pip3 install requests`
  - [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)<br>
  `pip install beautifulsoup4` or `pip3 install beautifulsoup4`
  
### Step 3: Import Kashi Into BetterTouchTool

Open BetterTouch Tool preferences. If the app is hidden in the dock, it may be visible in the top menu bar.
![pref](/screens/1.png)
Click "Manage Presets", then "Import".

![import](/screens/2.png)

Open [`kashi.json`](/kashi.json) to import the preset.
![json](/screens/3.png)
That's it! You should see Kashi appear as a new widget.
![kashi](/screens/4.png)
Lyrics for the currently playing song should appear on the Touch Bar. Enjoy! 🎉

## Planned Features
  - Scrolling lyrics (in progress)
  - Browser support: Youtube, Soundcloud, etc.
  - Support for non-English languages.

## Contact

[LinkedIn](https://www.linkedin.com/in/hojim)
