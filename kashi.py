import re
import requests
import json
import osascript
import hashlib
from bs4 import BeautifulSoup
from io import open


def main():
    # Get browser and player data via AppleScript
    code, output, err = getBrowserAndPlayerData()
    # print(output,err)
    current_data = output.split(', ')
    # Separate output
    player_data = current_data[0:4]
    browser_data = current_data[4:]
    # Process player and browser data
    player_type, player_artist, player_song, player_state = processPlayerData(
        player_data)
    browser_type, browser_artist, browser_song, browser_state = processBrowserData(
        browser_data)
    # Determine priority, player or browser
    priority = (playerOrBrowser(
        player_type, player_state, browser_type, browser_state))
    # print(priority)
    if priority == "player":
        artist = player_artist
        song = player_song
    elif priority == "browser":
        artist = browser_artist
        song = browser_song
    else:
        return
    # Remove extra information from title
    song = cleanSong(song)
    artist_1, artist_2 = multipleArtistCheck(artist)
    # Prepare array of artists
    artist_array = [artist, artist_1, artist_2]
    # print('\nPlayer Full Artist: ' + player_artist + '\nPlayer Artist 1: ' + player_artist_1 + '\nPlayer Artist 2: ' + player_artist_2 + '\nPlayer Song: ' + player_song)
    # Access Genius API 'https://docs.genius.com'
    accesstoken = 'ORYExHGED-rUDNu6wEqCt42NCg9nFuBiCiVKAYkjSrS6aQ1RHdyyjp5gl7GlpXZH'
    headers = {'Authorization': 'Bearer ' + accesstoken, 'User-Agent': 'Kashi',
               'Accept': 'application/json', 'Host': 'api.genius.com'}
    params = {'q': artist + ' ' + song}
    hits = requests.get('https://api.genius.com/search',
                        params=params, headers=headers).json()['response']['hits']
    # for hit in hits:
    #     print ("Artist: " + hit['result']['primary_artist']['name'] + "\nSong: " + hit['result']['full_title'])
    hitcount = 0
    if len(hits) > 0:
        # Get info from top search hit that contains player artist
        while hitcount < len(hits) - 1 and not any([x in hits[hitcount]['result']['primary_artist']['name'].lower() for x in artist_array]):
            hitcount += 1                                           # Go to next hit
        genius_artist = hits[hitcount]['result']['primary_artist']['name'].lower(
        )
        genius_song = hits[hitcount]['result']['full_title'].lower()
        genius_url = hits[hitcount]['result']['url']
        # print('\nGenius Artist: ' + genius_artist + '\nGenius Song: ' + genius_song + '\nGenius URL: ' + genius_url + '\n')
        if any([y in genius_artist for y in artist_array]):
            # Parse Genius HTML with BeautifulSoup and format lyrics
            lyrics = parseAndFormat(genius_url)
            # FINAL STEP: Print to touch bar
            print(lyrics)
        else:
            # Print music quote if lyrics not found
            printWisdom(song)
    else:
        printWisdom(song)
    return


def getBrowserAndPlayerData():
    return osascript.run('''
    on run
        set playerData to {"none", "none", "none", "none"}
        set browserData to {"none", "none"}
        if application "Spotify" is running then
            tell application "Spotify"
                set playerData to {"Spotify", artist of current track, name of current track, player state}
            end tell
        else if application "iTunes" is running then
        	tell application "iTunes"
                set playerData to {"iTunes", artist of current track, name of current track, player state}
            end tell
        else
            set playerData to {"none", "none", "none", "none"}
        end if

        if (application "Google Chrome" is running) and (exists (front window of application "Google Chrome")) then 
            tell application "Google Chrome"
                set browserData to {"Chrome", title of active tab of front window}
            end tell
        else if (application "Safari" is running) and (exists (front window of application "Safari")) then
            tell application "Safari"
                set browserData to {"Safari", name of current tab of front window}
            end tell
        else
            set browserData to {"none", "none"}
        end if

        set currentData to {playerData, browserData}
        return currentData
    end run
    ''', background=False)


def processBrowserData(browser_data):
    browser_artist = browser_song = ""
    # Check that tab is a Youtube video
    if " - YouTube" in browser_data[1]:
        # Remove  "Youtube" from title
        browser_data[1] = browser_data[1][0:-10]
        # Check for music video
        if " - " in browser_data[1]:
            # Music video likely. Parse for Artist/Song
            browser_artist = re.search(
                r'^([^\-]+)', browser_data[1]).group(0).strip().lower()
            browser_song = re.search(
                r'([^\-]+)$', browser_data[1]).group(0).strip().lower()
            browser_state = 'playing'
        else:
            # Music video not likely
            browser_state = 'paused'
    else:
        # Not a Youtube video page
        browser_state = 'paused'
    return browser_data[0], browser_artist, browser_song, browser_state


def processPlayerData(player_data):
    player_type = player_data[0]
    # Recombine artist or title that may have been split up if commas in title
    player_data = normalizeCommas(player_type, player_data)
    player_artist = player_data[1].lower()
    player_song = player_data[2].lower()
    player_state = player_data[3].lower()
    return player_type, player_artist, player_song, player_state


def playerOrBrowser(player_type, player_state, browser_type, browser_state):
    if player_state == "playing":
        return "player"
    elif browser_state == "playing":
        return "browser"
    else:
        return


def normalizeCommas(engine, player_data):
    while len(player_data) > 5:
        if engine == 'iTunes':                 # iTunes: Combine artists split by comma
            player_data[1] = player_data[1] + ', ' + player_data[2]
            player_data.pop(2)
        else:                                       # Spotify: Combine songs split by comma
            player_data[2] = player_data[2] + ', ' + player_data[3]
            player_data.pop(3)
    return player_data


def cleanSong(songtitle):
    # Remove everything after dash
    songtitle = re.sub(r' -.*$', '', songtitle)
    songtitle = re.sub(r' \(.*\)', '', songtitle)   # Remove parentheses
    songtitle = re.sub(r' \[.*\]', '', songtitle)   # Remove brackets
    return songtitle


def multipleArtistCheck(artist):
    if '&' in artist:
        artist_1 = re.sub(r' \&.*$', '', artist)
        artist_2 = re.sub(r'^.*\& ', '', artist)
    else:
        artist_1 = 'n/a'
        artist_2 = 'n/a'
    return artist_1, artist_2


def parseAndFormat(url):
    source_soup = BeautifulSoup(requests.get(
        url).text, 'html.parser')  # Parse HTML
    # Get text from the lyrics <div>
    lyricstext = source_soup.find('div', class_='lyrics').get_text()
    # Remove song sections in brackets
    lyricstext = re.sub(r'\[.*\n*.*\]', '', lyricstext).strip()
    # Remove parentheticals
    lyricstext = re.sub(r'\(.*\n*.*\)', '', lyricstext).strip()
    while '\n\n' in lyricstext:                                         # Line breaks, flatten, and replace
        lyricstext = lyricstext.replace('\n\n', '\n')
    lyricstext = lyricstext.replace('\n', ', ').replace('?,', '?').replace('!,', '!').replace(' ,', ',').replace(
        ' .', '.').replace('.,', '.').replace(',.', '.').replace('...', '..').replace('...', '..').replace('  ', ' ')
    return lyricstext


def printWisdom(player_song):
    wisdom = [
        '\"Music expresses that which cannot be said and on which it is impossible to be silent.\" - Victor Hugo ',
        '\"If music be the food of love, play on.\" - William Shakespeare ',
        '\"Where words fail, music speaks.\" - Hans Christian Anderson ',
        '\"One good thing about music, when it hits you, you feel no pain.\" - Bob Marley ',
        '\"And those who were seen dancing were thought to be insane by those who could not hear the music.\" - Nietzsche ',
        '\"There is geometry in the humming of the strings, there is music in the spacing of the spheres.\" - Pythagoras ',
        '\"You are the music while the music lasts.\" - T. S. Eliot ',
        '\"After silence, that which comes nearest to expressing the inexpressible is music.\" - Aldous Huxley '
    ]
    # Hash songname for constant quote when script refires
    songhash = hashlib.sha224(player_song.encode('utf-8')).hexdigest()
    songhash_int = int(songhash, base=16)
    # Reduce hash to within array length
    print(wisdom[(songhash_int % (len(wisdom) + 1)) - 1])


if __name__ == '__main__':
    main()
