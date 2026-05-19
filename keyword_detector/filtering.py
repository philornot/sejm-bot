import json
import pathlib

from config import get_the_great_filter
from scraper.config import TERM


def read_speech_from_json(proceeding_number, date, transcript_number):
    repo_root = pathlib.Path(__file__).parent.parent
    file_path = repo_root / f'speeches_term{TERM}' / f'proceeding{proceeding_number}' / f'{date}' / f'transcript{transcript_number}.json'
    with open(file_path, 'r') as json_file:
        speech = json.load(json_file)
    return speech


def determine_funniness(speeche):
    great_filter = get_the_great_filter()
    funniness = 0
    for category, keywords in great_filter.items():
        for keyword in keywords:
            if keyword in speeche.lower():
                #print(keyword, category)
                funniness += category
    return funniness


def add_to_funny_database(proceeding_number, date, transcript_number, funniness):
    speech_dict = read_speech_from_json(proceeding_number, date, transcript_number)
    repo_root = pathlib.Path(__file__).parent.parent
    if funniness <= 10:
        file_path = repo_root / f'funny_term{TERM}' / f'proceeding{proceeding_number}' / 'funny_transcripts.json'
        dir_path = repo_root / f'funny_term{TERM}' / f'proceeding{proceeding_number}'
    else:
        file_path = repo_root / f'funny_term{TERM}' / 'elite.json'
        dir_path = repo_root / f'funny_term{TERM}'
    for speaker, speech in speech_dict.items():
        speech_data = {
            "speaker": speaker,
            "speech": speech,
            "funniness": funniness,
            "date": date,
            "proceeding number": proceeding_number,
            "transcript_number": transcript_number
        }

        if not file_path.exists():
            dir_path.mkdir(exist_ok=True, parents=True)
            funny_speeches = [speech_data]
            json_str = json.dumps(funny_speeches, indent=4, ensure_ascii=False)
            with open(file_path, 'w') as file:
                file.write(json_str)
        else:
            if file_path.stat().st_size == 0:
                with open(file_path, 'w') as file:
                    file.write('[]')
            with open(file_path, 'r') as file:
                funny_speeches = json.load(file)
            if speech_data in funny_speeches:
                break
            funny_speeches.append(speech_data)
            json_str = json.dumps(funny_speeches, indent=4, ensure_ascii=False)
            with open(file_path, 'w') as file:
                file.write(json_str)


# speeches_term9/proceeding2/2019-12-12/transcript3.json
# test_speech = "Szanowna Pani Marszałek! Wysoka Izbo! Składam wniosek formalny o przerwanie posiedzenia i zwołanie Konwentu Seniorów w celu rozszerzenia porządku obrad o punkt dotyczący informacji ministra sprawiedliwości na temat nieprawidłowości w realizacji programu ˝Praca dla więźniów˝ i nadzorze nad nim. (Oklaski)\nSzanowni Państwo! Mamy do czynienia z wynikami, które są bezprecedensowe. NIK skierował 16 zawiadomień do prokuratury w sprawie realizacji tego programu. Chodzi o nieprawidłowości, które mogą dotyczyć 27 postępowań, które zostały przeprowadzone ze złamaniem ustawy o zamówieniach publicznych, co mogło narazić na stratę 115 mln zł - źle wydatkowanych.\nSzanowni Państwo! Ta sprawa powoduje, i o tym mówi NIK, powstawanie mechanizmów korupcyjnych. Wysoka Izba powinna mieć informację (Dzwonek) na temat tej sytuacji i minister Ziobro powinien przed Wysoką Izbą się z tego wytłumaczyć. Dziękuję bardzo."
# print(determine_funniness(test_speech))
# add_to_funny_database(2, '2019-12-12', 3)

def main(term):
    repo_root = pathlib.Path(__file__).parent.parent
    base_path = repo_root / f'speeches_term{term}'
    max_fun = 0
    for proceeding_dir in base_path.iterdir():
        if not proceeding_dir.is_dir():
            continue
        for date_dir in proceeding_dir.iterdir():
            if not date_dir.is_dir():
                continue
            for transcript_file in date_dir.glob("transcript*.json"):
                proceeding_number = int(str(proceeding_dir.stem).replace('proceeding', ''))
                transcript_number = int(str(transcript_file.stem).replace('transcript', ''))
                speech_dict = read_speech_from_json(proceeding_number, date_dir.name, transcript_number)
                for speaker, speech in speech_dict.items():
                    funniness = determine_funniness(speech)
                    if funniness > 2:
                        # print(speaker)
                        add_to_funny_database(proceeding_number, date_dir.name, transcript_number, funniness)
                        if funniness > max_fun:
                            max_fun = funniness
                    if funniness > 10:
                        print(speech)
    return max_fun
if __name__ == "__main__":
    print(main(TERM))

