import re, requests, json, osascript, hashlib
from bs4 import BeautifulSoup
from io import open

def main():
    # Get player state via AppleScript
    code,output,err = getPlayerInfo()
    # Parse data by comma
    player_data = output.split(', ')
    # print(player_data)
    player_type = player_data[0]
    # Recombine artist or title split in parse step due to commas
    player_data = normalizeCommas(player_type, player_data)
    player_artist = player_data[1].lower()          # Player artist post-normalization
    player_song = player_data[2].lower()            # Player song post-normalization
    player_position = int(float(player_data[3]))    # Position in song
    player_state = player_data[4].lower()           # Playing or paused?
    if '&' in player_artist:                        # Check for multiple artists
        player_artist_1 = re.sub(r' \&.*$', '', player_artist)
        player_artist_2 = re.sub(r'^.*\& ', '', player_artist)
    else:
        player_artist_1 = 'n/a'
        player_artist_2 = 'n/a'
    player_artist_array = [player_artist, player_artist_1, player_artist_2]
    # Remove extra information from title
    player_song = cleanSong(player_song)
    # print('\nPlayer Full Artist: ' + player_artist + '\nPlayer Artist 1: ' + player_artist_1 + '\nPlayer Artist 2: ' + player_artist_2 + '\nPlayer Song: ' + player_song)
    if player_state != 'playing':
        return
    else:
        # Access Genius API
        accesstoken = 'PQoWxI5pVo20hSd4OI1Y3kaV1qqZfqnmZACjvXGSJeRv6-gOCaKrVWRUpzKJTor-'
        headers = {'Authorization': 'Bearer ' + accesstoken, 'User-Agent': 'Kashi', 'Accept': 'application/json', 'Host':'api.genius.com'}
        params = {'q': player_artist + ' ' + player_song}
        hits = requests.get('https://api.genius.com/search', params = params, headers = headers).json()['response']['hits']
        # print("\nHits:", hits)
        hitcount = 0
        if len(hits) > 0:
            # Get info from top search hit that contains player artist
            while hitcount < len(hits) - 1 and not any([x in hits[hitcount]['result']['primary_artist']['name'].lower() for x in player_artist_array]):
                hitcount += 1                                           # Go to next hit
            genius_artist = hits[hitcount]['result']['primary_artist']['name'].lower()
            genius_song = hits[hitcount]['result']['full_title'].lower()
            genius_url = hits[hitcount]['result']['url']
            # print('\nGenius Artist: ' + genius_artist + '\nGenius Song: ' + genius_song + '\nGenius URL: ' + genius_url + '\n')
            if any([y in genius_artist for y in player_artist_array]):
                # Parse Genius HTML with BeautifulSoup and format lyrics
                lyrics = parseAndFormat(genius_url)
                # Print to touch bar
                print(lyrics)
            else:
                # Print music quote if lyrics not found
                printWisdom(player_song)
        else:
            printWisdom(player_song)
        return

def getPlayerInfo():
    return osascript.run('''
    on run
        if application "iTunes" is running then
            tell application "iTunes"
                set currentInfo to {"iTunes", artist of current track, name of current track, player position, player state}
            end tell
        else if application "Spotify" is running then
        	tell application "Spotify"
                set currentInfo to {"Spotify", artist of current track, name of current track, player position, player state}
            end tell
        end if
        return currentInfo
    end run
    ''', background = False)

def normalizeCommas(player_type, player_data):
    while len(player_data) > 5:
        if player_type == 'iTunes':                 # iTunes: Combine artists split by comma
            player_data[1] = player_data[1] + ', ' + player_data[2]
            player_data.pop(2)
        else:                                       # Spotify: Combine songs split by comma
            player_data[2] = player_data[2] + ', ' + player_data[3]
            player_data.pop(3)
    return player_data

def cleanSong(songtitle):
    songtitle = re.sub(r' -.*$', '', songtitle)     # Remove everything after dash
    songtitle = re.sub(r' \(.*\)', '', songtitle)   # Remove parenthetical
    return songtitle

def parseAndFormat(url):
    source_soup = BeautifulSoup(requests.get(url).text, 'html.parser')  # Parse HTML
    lyricstext = source_soup.find('div', class_ = 'lyrics').get_text()  # Get text from the Lyrics <div>
    lyricstext = re.sub(r'\[.*\]', '', lyricstext).strip()              # Remove song sections in brackets
    lyricstext = re.sub(r'\(.*\n*.*\)', '', lyricstext).strip()         # Remove parentheticals from lyrics
    while '\n\n' in lyricstext:                                         # Remove double line breaks, then flatten and replace
        lyricstext = lyricstext.replace('\n\n', '\n')
    lyricstext = lyricstext.replace('\n', ', ').replace('?,', '?').replace('!,', '!').replace(' ,', ',').replace(' .', '.').replace('.,', '.').replace(',.', '.').replace('...', '..').replace('...', '..').replace('  ', ' ')
    return lyricstext

def printWisdom(player_song):
    wisdom = [
    '\"Music expresses that which cannot be said and on which it is impossible to be silent.\" - Victor Hugo ',
    '\"If music be the food of love, play on.\" - William Shakespeare ',
    '\"Music is the movement of sound to reach the soul for the education of its virtue.\" - Plato ',
    '\"Where words fail, music speaks.\" - Hans Christian Anderson ',
    '\"One good thing about music, when it hits you, you feel no pain.\" - Bob Marley ',
    '\"Words make you think a thought. Music makes you feel a feeling. A song makes you feel a thought.\" - E. Y. Harburg ',
    '\"I haven\'t understood a bar of music in my life, but I have felt it.\" - Igor Stravinsky ',
    '\"And those who were seen dancing were thought to be insane by those who could not hear the music.\" - Nietzsche ',
    '\"Without music to decorate it, time is just a bunch of boring production deadlines or dates by which bills must be paid.\" - Frank Zappa ',
    '\"Music doesn\'t lie. If there is something to be changed in this world, then it can only happen through music.\" - Jimi Hendrix ',
    '\"There is geometry in the humming of the strings, there is music in the spacing of the spheres.\" - Pythagoras ',
    '\"You are the music while the music lasts.\" - T. S. Eliot ',
    '\"After silence, that which comes nearest to expressing the inexpressible is music.\" - Aldous Huxley '
    ]
    # Hash songname for constant quote when script refires
    songhash = hashlib.sha224(player_song.encode('utf-8')).hexdigest()
    songhash_int = int(songhash, base = 16)
    # Reduce hash to within array length
    print(wisdom[(songhash_int % (len(wisdom) + 1)) - 1])

if __name__ == '__main__':
    main()
