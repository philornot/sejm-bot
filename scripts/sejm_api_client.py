import json
import pathlib

import requests
from bs4 import BeautifulSoup

from scripts.progress_monitoring import read_progress_from_json, save_progress_to_json
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
        # print(f'something went wrong?? url:{url}')
        return response.status_code

    html_transcript = response.text
    parsed_transcript = BeautifulSoup(html_transcript, 'html.parser')

    speakers = parsed_transcript.find_all('h2', class_='mowca')
    if len(speakers) != 1:
        print(f'found multiple speakers in one transcript!')
        raise ValueError

    speaker = speakers[0]
    return format_paragraphs(speaker)


def write_speech_to_json(proceeding_number, date, transcript_number):
    base_dir = f'../speeches_term{TERM}/proceeding{proceeding_number}/{date}'
    file_path = f'{base_dir}/transcript{transcript_number}.json'

    speeches = get_speech_transcripts(proceeding_number, date, transcript_number)
    if isinstance(speeches, int):
        raise RuntimeError(f'Request failed with status: {speeches}')

    pathlib.Path(base_dir).mkdir(parents=True, exist_ok=True)
    json_content = json.dumps(speeches, indent=4, ensure_ascii=False)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(json_content)


def read_speeches_from_json(proceeding_number, date, transcript_number):
    file_path = f'../speeches_term{TERM}/proceeding{proceeding_number}/{date}/transcript{transcript_number}.json'
    with open(file_path, 'r') as json_file:
        speeches = json.load(json_file)
    return speeches


if __name__ == "__main__":
    progress_data = read_progress_from_json(TERM)
    last_proceeding = progress_data['last_proceeding']
    last_date = progress_data['last_date']
    last_transcript = progress_data['last_transcript']
    # full_path = progress_data['full_path']
    proceeding_dates = read_proceeding_dates_from_file(TERM)
    print(f'found last saved transcript: proceeding {last_proceeding}, {last_date}, transcript {last_transcript}')
    for proceeding_number, dates in proceeding_dates.items():
        if int(proceeding_number) < last_proceeding:
            continue
        for date in dates:
            if date < last_date:
                continue
            print(f'trying date {date}')
            transcript_number = 1
            while True:
                if transcript_number < last_transcript:
                    transcript_number += 1
                    continue
                try:
                    print(f'writing transcript {transcript_number} from proceeding {proceeding_number} from date {date}')
                    write_speech_to_json(proceeding_number, date, transcript_number)
                    transcript_number += 1
                except RuntimeError:
                    save_progress_to_json(TERM)
                    print(f'no more transcripts for date {date} (last: {transcript_number})\n')
                    break
                except KeyboardInterrupt:
                    save_progress_to_json(TERM)
                    print(f'Saving progress...')
                except Exception as e:
                    save_progress_to_json(TERM)
                    print(f'sth went wrong with writing transcript from {date} (proceeding {proceeding_number}):\n{e}\n')
                    break
