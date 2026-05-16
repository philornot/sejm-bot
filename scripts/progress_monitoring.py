import json
import pathlib

TERM = 10


def save_progress_to_json(term):
    progress_file = f'term{term}_progress.json'
    repo_root = pathlib.Path(__file__).parent.parent
    base_path = repo_root / f'speeches_term{term}'
    path = pathlib.Path(base_path)

    proceedings = sorted(path.iterdir(), key=lambda p: int(p.name.replace('proceeding', '')))
    last_proceeding = proceedings[-1].name
    last_proceeding_path = pathlib.Path(f'{base_path}/{last_proceeding}')
    last_proceeding_number = int(last_proceeding.replace('proceeding', ''))

    dates = sorted(last_proceeding_path.iterdir())
    last_date = dates[-1].name
    last_date_path = pathlib.Path(f'{base_path}/{last_proceeding}/{last_date}')

    transcripts = sorted(last_date_path.iterdir(),
                         key=lambda p: int(p.name.replace('transcript', '').replace('.json', '')))
    last_transcript = transcripts[-1].name
    last_transcript_number = int(last_transcript.replace('transcript', '').replace('.json', '')) - 1
    last_transcript_path = str((base_path / last_proceeding / last_date / last_transcript).relative_to(repo_root))

    progress = {
        'last_proceeding': last_proceeding_number,
        'last_date': last_date,
        'last_transcript': last_transcript_number,
        'full_path': last_transcript_path
    }

    json_str = json.dumps(progress, indent=4)

    with open(progress_file, 'w') as json_file:
        json_file.write(json_str)


def read_progress_from_json(term):
    progress_file = f'term{term}_progress.json'
    with open(progress_file, 'r') as json_file:
        progress = json.load(json_file)
    # last_proceeding = progress['last_proceeding']
    # last_date = progress['last_date']
    # last_transcript = progress['last_transcript']
    # full_path = progress['full_path']
    return progress


if __name__ == "__main__":
    save_progress_to_json(TERM)
