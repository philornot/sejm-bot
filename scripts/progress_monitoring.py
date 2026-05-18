import json
import pathlib

from config import TERM


def save_progress_to_json(term):
    progress_file = f'term{term}_progress.json'
    repo_root = pathlib.Path(__file__).parent.parent
    base_path = repo_root / f'speeches_term{term}'
    path = pathlib.Path(base_path)
    path.mkdir(exist_ok=True)

    all_proceedings = path.iterdir()
    non_empty_proceedings = [p for p in all_proceedings if any(p.iterdir())]
    proceedings = sorted(non_empty_proceedings, key=lambda p: int(p.name.replace('proceeding', '')))
    if not proceedings:
        return None

    last_proceeding = proceedings[-1].name
    last_proceeding_path = pathlib.Path(f'{base_path}/{last_proceeding}')
    last_proceeding_number = int(last_proceeding.replace('proceeding', ''))

    all_dates = last_proceeding_path.iterdir()
    non_empty_dates = [d for d in all_dates if any(d.iterdir())]
    dates = sorted(non_empty_dates)
    if not dates:
        return None

    last_date = dates[-1].name
    last_date_path = pathlib.Path(f'{base_path}/{last_proceeding}/{last_date}')

    transcripts = sorted(last_date_path.iterdir(),
                         key=lambda p: int(p.name.replace('transcript', '').replace('.json', '')))
    if not transcripts:
        return None
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
    path = pathlib.Path(progress_file)
    if not path.exists() or path.stat().st_size == 0:
        empty_data = {
            "last_proceeding": 0,
            "last_date": "",
            "last_transcript": 0,
            "full_path": ""
        }
        return empty_data
    with open(progress_file, 'r') as json_file:
        progress = json.load(json_file)
    # last_proceeding = progress['last_proceeding']
    # last_date = progress['last_date']
    # last_transcript = progress['last_transcript']
    # full_path = progress['full_path']
    return progress


if __name__ == "__main__":
    save_progress_to_json(TERM)
