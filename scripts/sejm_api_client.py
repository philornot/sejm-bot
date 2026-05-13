import json
import pathlib
import random
import string

import requests
from bs4 import BeautifulSoup

TERM = 10
BASE_API_URL = 'https://api.sejm.gov.pl/sejm'


def format_paragraphs(speaker):
    speaker_clean = speaker.text.strip(':')
    transcript = []
    transcript_part = speaker.find_next_sibling()
    while transcript_part and transcript_part.name != 'br':
        if transcript_part.name == 'p':
            transcript.append(transcript_part.get_text(strip=True).replace('\r\n', ''))
        transcript_part = transcript_part.find_next_sibling()

    transcript = '\n'.join(transcript)
    return {speaker_clean: transcript}


def get_speech_transcripts(proceeding_number, date, transcript_number):
    url = f'{BASE_API_URL}/term{TERM}/proceedings/{proceeding_number}/{date}/transcripts/{transcript_number}'
    response = requests.get(url)
    if not response.ok:
        print(f'something went wrong?? url:{url}')
        return response.status_code

    html_transcript = response.text
    parsed_transcript = BeautifulSoup(html_transcript, 'html.parser')

    speakers = parsed_transcript.find_all('h2', class_='mowca')
    if len(speakers) == 1:
        speaker = speakers[0]
        transcript = []
        transcript_part = speaker.find_next_sibling()
        while transcript_part and transcript_part.name != 'br':
            if transcript_part.name == 'p':
                transcript.append(transcript_part.get_text(" ", strip=True))
            transcript_part = transcript_part.find_next_sibling()

        transcripts = [format_paragraphs(speaker)]
    else:
        transcripts = [format_paragraphs(speaker) for speaker in speakers]
    return transcripts


def write_speech_to_json(proceeding_number, date, transcript_number, salted_filename=False):
    base_dir = f'../speeches/{date}/proceeding{proceeding_number}'
    base_file_path = f'{base_dir}/transcript{transcript_number}'
    pathlib.Path(base_dir).mkdir(parents=True, exist_ok=True)
    speeches = get_speech_transcripts(proceeding_number, date, transcript_number)
    if type(speeches) == int:
        raise Exception(f'something went wrong, error: {speeches}')
    for speech in speeches:
        json_content = json.dumps(speech, indent=4, ensure_ascii=False)
        random_string = ''.join(random.choice(string.ascii_lowercase) for _ in range(4))
        file_path = base_file_path + f'_{random_string}.json' if salted_filename else base_file_path + '.json'
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(json_content)


if __name__ == "__main__":
    try:
        write_speech_to_json(1, '2023-11-13', 1)
    except Exception as e:
        print(f'something went wrong: {e}')
