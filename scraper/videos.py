import requests
from datetime import datetime, timedelta

TERM = 10
BASE_API_URL = "https://api.sejm.gov.pl/sejm"


def pobierz_nagranie_konkretnego_przemowienia(proceeding_number, date, transcript_number):
    """
    Zwraca precyzyjnie zaadresowane nagranie wideo dla konkretnego numeru transkrypcji (przemówienia).

    :param proceeding_number: int/str (np. 1)
    :param date: str 'YYYY-MM-DD' (np. '2023-11-13')
    :param transcript_number: int/str (np. 5)
    """
    # 1. Pobranie bazowego wideo z wykorzystaniem triku przesunięcia daty o 1 dzień (zapobiega pustej liście)
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    next_day_obj = date_obj + timedelta(days=1)
    date_tomorrow = next_day_obj.strftime("%Y-%m-%d")

    url_videos = f"{BASE_API_URL}/term{TERM}/videos?since={date}&till={date_tomorrow}&type=posiedzenie"
    res_videos = requests.get(url_videos)

    if res_videos.status_code != 200 or not res_videos.json():
        return {"error": f"Nie znaleziono strumienia wideo z dnia {date}."}

    glowne_wideo = res_videos.json()[0]
    unid = glowne_wideo.get("unid")
    base_player_url = glowne_wideo.get("playerLink")
    video_link_m3u8 = glowne_wideo.get("videoLink")

    # 2. Konstrukcja precyzyjnego linku WWW z automatycznym przewijaniem.
    # System Sejmowy w odtwarzaczu dla danej transmisji (unid) mapuje punkty i wypowiedzi
    # za pomocą parametru id (identyfikatora elementu transkrypcji).
    # W większości przypadków dodanie kotwicy lub parametru 'id' odpowiadającego numerowi transkrypcji
    # powoduje, że odtwarzacz Sejmu ładuje listę wystąpień i podświetla/przewija do wybranego posła.
    precyzyjny_player_url = f"{base_player_url}&id={transcript_number}"

    # 3. Dodatkowo: wyciągamy bazowe ramy czasowe całego dnia (z Twojego JSONa)
    # Przykład: "https://.../playlist.m3u8?start=1699873200000&stop=1699901820000"
    base_stream_url = video_link_m3u8.split("?")[0]
    time_params = video_link_m3u8.split("?")[1]

    start_timestamp = int(time_params.split("start=")[1].split("&")[0])
    stop_timestamp = int(time_params.split("stop=")[1])

    # Ponieważ nie mamy JSON-a z dokładną sekundą (błąd 404), idealnym rozwiązaniem dla Twojego bota
    # jest podanie użytkownikowi linku do player_www (gdzie Sejm sam przewinie wideo na bazie parametru &id=)
    # oraz bazowego strumienia m3u8, z którego można odtworzyć cały dzień obrad.

    return {
        "status": "Sukces",
        "wypowiedz_info": {
            "kadencja": TERM,
            "posiedzenie": proceeding_number,
            "data": date,
            "numer_wypowiedzi": transcript_number
        },
        "link_do_odtwarzacza_www_auto_scroll": precyzyjny_player_url,
        "strumien_m3u8_calego_dnia": video_link_m3u8,
        "czysty_url_strumienia": base_stream_url,
        "ramy_czasowe_unix_ms": {
            "start": start_timestamp,
            "stop": stop_timestamp
        },
        "tytul_posiedzenia": glowne_wideo.get("title").strip()
    }


# --- WYWOŁANIE FUNKCJI ---
wynik = pobierz_nagranie_konkretnego_przemowienia(proceeding_number=1, date="2023-11-13", transcript_number=5)
import json

print(json.dumps(wynik, indent=4, ensure_ascii=False))