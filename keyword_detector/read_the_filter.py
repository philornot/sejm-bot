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
                # print(keyword, category)
                if funniness < category:
                    funniness = category
    return funniness


def add_to_funny_database(proceeding_number, date, transcript_number):
    speech_dict = read_speech_from_json(proceeding_number, str(date_dir), transcript_number)


# speeches_term9/proceeding2/2019-12-12/transcript3.json
# test_speech = "Szanowna Pani Marszałek! Wysoka Izbo! Składam wniosek formalny o przerwanie posiedzenia i zwołanie Konwentu Seniorów w celu rozszerzenia porządku obrad o punkt dotyczący informacji ministra sprawiedliwości na temat nieprawidłowości w realizacji programu ˝Praca dla więźniów˝ i nadzorze nad nim. (Oklaski)\nSzanowni Państwo! Mamy do czynienia z wynikami, które są bezprecedensowe. NIK skierował 16 zawiadomień do prokuratury w sprawie realizacji tego programu. Chodzi o nieprawidłowości, które mogą dotyczyć 27 postępowań, które zostały przeprowadzone ze złamaniem ustawy o zamówieniach publicznych, co mogło narazić na stratę 115 mln zł - źle wydatkowanych.\nSzanowni Państwo! Ta sprawa powoduje, i o tym mówi NIK, powstawanie mechanizmów korupcyjnych. Wysoka Izba powinna mieć informację (Dzwonek) na temat tej sytuacji i minister Ziobro powinien przed Wysoką Izbą się z tego wytłumaczyć. Dziękuję bardzo."
# print(determine_funniness(test_speech))

def main(term):
    repo_root = pathlib.Path(__file__).parent.parent
    base_path = repo_root / f'speeches_term{term}'
    for proceeding_dir in base_path.iterdir():
        if not proceeding_dir.is_dir():
            continue
        for date_dir in proceeding_dir.iterdir():
            if not date_dir.is_dir():
                continue
            for transcript_file in date_dir.glob("transcript*.json"):
                proceeding_number = int(str(proceeding_dir.stem).replace('proceeding', ''))
                transcript_number = int(str(transcript_file.stem).replace('transcript', ''))
                speech_dict = read_speech_from_json(proceeding_number, str(date_dir), transcript_number)
                for speaker, speech in speech_dict.items():
                    funniness = determine_funniness(speech)
                    if funniness > 2:
                        print(speaker)
                        return speech
    return None


if __name__ == "__main__":
    funny = main(TERM)
    print(funny)
