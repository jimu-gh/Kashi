
<h1 align="center">KASHI · 歌詞 · かし</h1>

![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)
![love](http://forthebadge.com/images/badges/built-with-love.svg)

![build](https://img.shields.io/badge/build-passing-brightgreen.svg?style=for-the-badge)  ![license](https://img.shields.io/badge/license-GPLv3-blue.svg?style=for-the-badge) ![license](https://img.shields.io/badge/PRs-welcome-yellow.svg?style=for-the-badge)

Kashi is a custom preset for [BetterTouchTool](https://folivora.ai/) that displays the current song's lyrics on the Macbook Pro's Touch Bar. It works with [Spotify](https://www.spotify.com/us/download/other/) and [iTunes](https://www.apple.com/itunes/download/).

Kashi has three main functions:
1. It gets the current song playing via AppleScript.
2. It searches the [Genius API](https://docs.genius.com/) and looks for the best match within the hits.
3. It scrapes lyrics from the raw HTML, formats, and outputs them onto the Touch Bar.

## Installation

### Step 1: Install BetterTouchTool

Kashi is a plugin for BTT, so first you will need to download and install [BetterTouchTool](https://folivora.ai/).

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

Open BetterTouch Tool preferences.
![pref](/screens/1.png)
Click "Manage Presets", then "Import".

![import](/screens/2.png)

Import [`kashi.json`](/kashi.json).

![json](/screens/3.png)
 
You should see Kashi appear as a new widget.
![kashi](/screens/4.png)
Lyrics should now appear on the Touch Bar when a song is playing. Enjoy never forgetting the lyrics again! 🎉

## Planned Features
  - Scrolling lyrics (in progress)
  - Browser support: Youtube, Soundcloud, etc.
  - Support for non-English languages.

## Contact

[LinkedIn](https://www.linkedin.com/in/hojim)

[Medium](https://www.medium.com/_jim)
