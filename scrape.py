import re
import json
from urllib.request import ulopen, Request

URL = "https://shortq.org/JADWAL-DAN-PREDIKSI-BOLA2026"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "identity",
    "Connection": "keep-alive"
}
ELITE = [
    "argentina", "brazil", "france", "germany", "spain", "england",
    "portugal", "netherlands", "italy", "belgium", "uruguay", "croatia",
    "japan", "south korea", "usa", "mexico", "canada", "colombia",
    "switzerland", "denmark", "austria", "morocco", "senegal",
    "australia", "poland", "chelsea", "manchester city", "manchester united",
    "liverpool", "arsenal", "tottenham", "newcastle united", "aston villa",
    "real madrid", "barcelona", "bayern munich", "inter milan", "ac milan",
    "juventus", "paris saint-germain", "benfica", "porto", "galatasaray",
    "palmeiras", "river plate", "crystal palace", "nottingham forest",
    "sunderland"
]
MONTHS = {
    "01": "Jan", "02": "Feb", "03": "Mar", "04": "apt",
    "05": "Mei", "06": "Jun", "07": "Jul", "08": "Agu",
    "09": "Sep", "10": "Okt", "11": "Nov", "12": "Des"
}
def is_elite(home, away):
    h = home.lower().strip()
    a = away.lower().strip()
    for e in ELITE:
        if e in h or e in a:
            return True
    return False
def clean_team(name):
    name = re.sub(r'\[\d+\]', '', name)
    name = re.sub(r'\[n\]', '', name)
    return name.strip()
def parse_line(line):
    line = line.strip()
    if not line or '<br' in line or '/' not in line[:6]:
        return None
    pattern = r'(\d{2})/(\d{2})\s+(\d{2})[.:](\d{2})\s+WIB\s+(.+?)\s+VS\s+(.+?)\s+(\d+[-]\d+|\d+)$'
    m = re.match(pattern, line)
    if not m:
        return None
    day, month, hour, minute, home_raw, away_raw, score = m.groups()
    home = clean_team(home_raw)
    away = clean_team(away_raw)
    if not is_elite(home, away):
        return None
    tanggal = day + " " + MONTHS.get(month, month) + " 2026"
    waktu = hour + ":" + minute
    return {
        "tanggal": tanggal,
        "waktu": waktu,
        "home": home,
        "away": away,
        "prediksi": home + " " + score + " " + away,
        "tip": "Prediksi Skor",
        "link": "https://shortlyx.link/smrk4d"
    }
def main():
    req = Request(URL, headers=HEADERS)
    html = urlopen(req, timeout=30).read().decode('utf-8', errors='ignore')
    start = html.find('PREDIKSI BOLA')
    if start == -1:
        print("SECTION_NOT_FOUND")
        return
    end = html.find('</div>\n            </div>\n        </div>', start)
    if end == -1:
        end = len(html)
    section = html[start:end]
    lines = section.split('\n')
    results = []
    seen = set()
    for line in lines:
        parsed = parse_line(line)
        if parsed:
            key = parsed["home"] + "|" + parsed["away"] + "|" + parsed["waktu"]
            if key not in seen:
                seen.add(key)
                results.append(parsed)
    results.sort(key=lambda x: (x["tanggal"], x["waktu"]))
    with open('prediksi.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("OK: " + str(len(results)) + " pertandingan")
if __name__ == '__main__':
    main()
