
<h1 align="center">KASHI · 歌詞 · かし</h1>

![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)
![love](http://forthebadge.com/images/badges/built-with-love.svg)

![build](https://img.shields.io/badge/build-passing-brightgreen.svg?style=for-the-badge)  ![license](https://img.shields.io/badge/license-GPLv3-blue.svg?style=for-the-badge) ![license](https://img.shields.io/badge/PRs-welcome-yellow.svg?style=for-the-badge)

## About Kashi

Kashi is a custom [BetterTouchTool](https://folivora.ai/) widget that displays the current song lyrics on the Macbook Pro's Touch Bar.

Kashi works with [Spotify](https://www.spotify.com/us/download/other/), [Music](https://www.apple.com/music/), and [Youtube](https://www.youtube.com) (Chrome or Safari).

Kashi has three main functions:
1. It retrieves data about the current song playing in Spotify, Music, or YouTube via AppleScript.
2. It calls [Genius](https://docs.genius.com/) and checks for a good match in the search hits, accounting for variations such as remixes.
3. It scrapes the lyrics from the raw HTML of the Genius URL, prettifies, and outputs them onto the Touch Bar.

Regarding YouTube:
1. YouTube must be playing on the active tab on Chrome or Safari, with window focus.
2. If both browser and player are open, Kashi will prioritize the player if it is playing.

## Installation

### Step 1: Install BetterTouchTool

BetterTouchTool can be downloaded [here](https://folivora.ai/downloads). To install, unzip the download file and move the application file to your Applications folder.

### Step 2: Install Python 3 and Packages

Install [Python 3](https://www.python.org/downloads/release/python-371/) and the Python packages below.<br>
For help with package installation, please refer to the [Python Packaging User Guide](https://packaging.python.org/tutorials/installing-packages/).

  - [OSAscript](https://pypi.org/project/osascript/)<br>
  `pip install osascript` or `pip3 install osascript`
  - [Requests](https://pypi.org/project/requests/)<br>
  `pip install requests` or `pip3 install requests`
  - [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)<br>
  `pip install beautifulsoup4` or `pip3 install beautifulsoup4`
  
### Step 3: Import Kashi.json into BetterTouchTool

Open BetterTouchTool Configuration, accessible via the top menu bar.

<img src="screens/1.png" alt="Open BTT Configuration" width="425">

Confirm that you are in the Touch Bar Settings.

<img src="screens/2.png" alt="Touch Bar Settings" width="400">

Open [`kashi.json`](/kashi.json) in a text editor. Select all (⌘A) and copy (⌘C).

<img src="screens/3.png" alt="Select / Copy JSON" width="650">

Click somewhere on the trigger list (left column, striped), and Paste (⌘V) directly into the BetterTouchTool Configuration window. The new widget will appear in your list.

<img src="screens/4.png" alt="Paste JSON Into BTT Configuration Window" width="650">

Depending on how your Python is installed, the widget may already be working. If not, do Step 4 below to configure the widget's parameters.

### Step 4: Set Widget Parameters

The Launch Path parameter must direct to your Python 3 install. [PATH](https://bic-berkeley.github.io/psych-214-fall-2016/using_pythonpath.html) will also work.

&nbsp;&nbsp;&nbsp;Default - "/Library/Frameworks/Python.framework/Versions/3.7/bin/python3.7"

The second parameter must refer to Python's "site-packages" folder containing Python modules.

&nbsp;&nbsp;&nbsp;Default - "/Library/Frameworks/Python.Framework/Versions/3.7/lib/Python3.7/site-packages"

Lyrics for the currently playing song should now appear on the Touch Bar. Enjoy! 🎉

## History

&nbsp;&nbsp;&nbsp;11.30.19 Updated for macOS Catalina

&nbsp;&nbsp;&nbsp;6.23.19 YouTube and browser support added

&nbsp;&nbsp;&nbsp;12.03.18 Initial release

## Resources

For detailed information about Touch Bar customization, please refer to the official [BTT Documentation](https://docs.bettertouchtool.net/docs/402_touch_bar_basics.html).

More awesome Touch Bar presets can be found on the [BTT Community](https://community.folivora.ai/).

ChengHaoMou's [Touchbar-Lyric](https://github.com/ChenghaoMou/touchbar-lyric) is a similarly inspired widget accessing NetEase's API for real-time lyrics display.

## Contact

[LinkedIn](https://www.linkedin.com/in/hojim)
[Homepage](https://www.jimho.us)
