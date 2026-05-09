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
        return f"coś poszło nie tak: {response.status_code}, url:{url}"

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


speeches = get_speech_transcripts(1, '2023-11-13', 1, )
for speeche in speeches:
    for speaker, transcript in speeche.items():
        print(f'speaker: {speaker}\n\n'
              f'{transcript}')
