import re
import json
from urllib.request import urlopen

URL = "https://shortq.org/JADWAL-DAN-PREDIKSI-BOLA2026"

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
    "01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr",
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
    tanggal = f"{day} {MONTHS.get(month, month)} 2026"
    waktu = f"{hour}:{minute}"
    return {
        "tanggal": tanggal,
        "waktu": waktu,
        "home": home,
        "away": away,
        "prediksi": f"{home} {score} {away}",
        "tip": "Prediksi Skor",
        "link": "https://shortlyx.link/smrk4d"
    }

def main():
    html = urlopen(URL, timeout=30).read().decode('utf-8', errors='ignore')
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
            key = f"{parsed['home']}|{parsed['away']}|{parsed['waktu']}"
            if key not in seen:
                seen.add(key)
                results.append(parsed)
    results.sort(key=lambda x: (x['tanggal'], x['waktu']))
    with open('prediksi.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"OK: {len(results)} pertandingan")

if __name__ == '__main__':
    main()
