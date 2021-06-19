'''
=== Play TOP100 of Zing MP3 by exlab ===
=== version 1.1 13/02/2019 ===
--------
# Config in configuration.yaml file for Home Assistant
zing_mp3:

# Code in script
play_zing_mp3:
  sequence:
    - service: zing_mp3.play
      data:
        entity_id: media_player.room_player
        music_type: 'Pop'
        # optional, default: 'Pop' #list music_type: Pop, Country, Rock, Dance, R&B, Rap, Soundtrack, Nhac tre, Tru tinh, Que huong, Cach mang, Rock Viet, Rap Viet, Dance Viet
        repeat: on
        # optional, default: 'off'
        shuffle: on
        # optional, default: 'off'
--------        
'''

# Declare variables
DOMAIN = 'zing_mp3'
SERVICE_ZING_PLAY = 'play'

# data service
CONF_PLAYER_ID = 'entity_id'
CONF_MUSIC_TYPE= 'music_type'
CONF_REPEAT = 'repeat'
CONF_SHUFFLE = 'shuffle'

# const data
TOP100 = {'pop':'ZWZB96AB', 'country': 'ZWZB96AE', 'rock': 'ZWZB96AC', 'dance': 'ZWZB96C7', 'r&b': 'ZWZB96C8', 'rap': 'ZWZB96AD', 'soundtrack': 'ZWZB96C9',
          'nhac tre':'ZWZB969E', 'tru tinh': 'ZWZB969F', 'que huong': 'ZWZB96AU', 'cach mang': 'ZWZB96AO', 'rock viet': 'ZWZB96A0', 'rap viet': 'ZWZB96AI', 'dance viet': 'ZWZB96AW'}
url_list = 'https://mp3.zing.vn/xhr/media/get-list?op=top100&start=0&length=20&id='
url_audio = 'https://mp3.zing.vn/xhr/media/get-source?type=audio&key='
prefix_url = 'https:'

import requests, time, random
def get_codes(type_TOP):
    type_TOP = type_TOP.lower()
    uri = url_list + TOP100.get(type_TOP)
    re = requests.get(uri).json()
    items = re['data']['items']
    audio_codes = []
    for item in items:
        code = item['code']
        audio_codes.append(code)
    return audio_codes

def get_audio_links(type_TOP):
    audio_links = {}
    codes = get_codes(type_TOP)
    for code in codes:
        uri = url_audio + code
        re = requests.get(uri).json()['data']
        link = prefix_url + re['source']['128']
        duration =  int(re['duration'])
        audio_links[link] = duration
    return audio_links
                   
def setup(hass, config):
    # play handler
    def play_zing(data_call):
        # Get data service
        media_id = data_call.data.get(CONF_PLAYER_ID)
        music_type  = data_call.data.get(CONF_MUSIC_TYPE, 'Pop')
        repeat = data_call.data.get(CONF_REPEAT, 'off')
        shuffle = data_call.data.get(CONF_SHUFFLE, 'off')
        # get link of audio
        mp3_links = get_audio_links(music_type)
        # force turn off media player
        hass.services.call('media_player', 'turn_off', {'entity_id': media_id})
        time.sleep(0.2)
        ''' play '''
        flag = True
        while (flag == True):
            if (shuffle == 'off'):
                for uri in mp3_links:
                    # service data for 'CALL SERVICE' in Home Assistant
                    service_data = {'entity_id': media_id, 'media_content_id': uri, 'media_content_type': 'music'}
                    # Call service from Home Assistant
                    hass.services.call('media_player', 'play_media', service_data)
                    # sleep while media_player is playing
                    time_sleep = mp3_links.get(uri)
                    time.sleep(time_sleep)
            elif (shuffle == 'on'):
                for idez in range(0, len(mp3_links)):
                    uri, time_sleep = random.choice(list(mp3_links.items()))
                    # service data for 'CALL SERVICE' in Home Assistant
                    service_data = {'entity_id': media_id, 'media_content_id': uri, 'media_content_type': 'music'}
                    # Call service from Home Assistant
                    hass.services.call('media_player', 'play_media', service_data)
                    # sleep while media_player is playing
                    time.sleep(time_sleep)
            if (repeat == 'off'): 
                flag = False
        
    hass.services.register(DOMAIN, SERVICE_ZING_PLAY, play_zing)
    return True
