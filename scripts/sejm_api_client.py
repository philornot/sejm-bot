import json
import pathlib

import requests
from bs4 import BeautifulSoup

from scripts.save_and_read_proceeding_dates import read_proceeding_dates_from_file

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


def write_speech_to_json(proceeding_number, date, transcript_number):
    base_dir = f'../speeches/{date}/proceeding{proceeding_number}'
    file_path = f'{base_dir}/transcript{transcript_number}.json'
    pathlib.Path(base_dir).mkdir(parents=True, exist_ok=True)

    speeches = get_speech_transcripts(proceeding_number, date, transcript_number)
    if isinstance(speeches, int):
        raise Exception(f'Request failed with status: {speeches}')

    json_content = json.dumps(speeches, indent=4, ensure_ascii=False)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(json_content)


def read_speeches_from_json(proceeding_number, date, transcript_number):
    file_path = f'../speeches/{date}/proceeding{proceeding_number}/transcript{transcript_number}.json'
    with open(file_path, 'r') as json_file:
        speeches = json.load(json_file)
    return speeches


if __name__ == "__main__":
    proceeding_dates = read_proceeding_dates_from_file(TERM)
    for proceeding_number, dates in proceeding_dates.items():
        for date in dates:
            print(f'trying date {date}')
            try:
                transcript_number = 1
                while True:
                    print(f'writing transcript {transcript_number} from proceeding {proceeding_number} from date {date} ')
                    write_speech_to_json(proceeding_number, date, transcript_number)
                    transcript_number += 1
            except Exception as e:
                print(f'sth went wrong with writing transcript from {date} (proceeding {proceeding_number}):\n{e}\n')
                continue
