# -*- coding: utf-8 -*-
from __future__ import annotations
from pathlib import Path
import json, re

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ARTIST_DIR = PROJECT_ROOT / "artist"
DATA_FILE = PROJECT_ROOT / "data" / "artists.json"
ARTIST_DIR.mkdir(parents=True, exist_ok=True)

TR_MAP = str.maketrans({
    "ç":"c","ğ":"g","ı":"i","ö":"o","ş":"s","ü":"u",
    "Ç":"c","Ğ":"g","İ":"i","I":"i","Ö":"o","Ş":"s","Ü":"u",
})

def slugify(text: str) -> str:
    s = text.translate(TR_MAP).lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-{2,}", "-", s)
    return s

# Genres listende ne varsa burası da aynı kalsın
GENRES: dict[str, list[str]] = {
    "Rock": ["Duman", "Mor ve Ötesi", "Manga", "Queen", "Nirvana", "Pink Floyd", "Red Hot Chili Peppers"],
    "Pop": ["Tarkan", "Sezen Aksu", "Sertab Erener", "Michael Jackson", "Madonna", "Taylor Swift", "Dua Lipa"],
    "Hip-Hop / Rap": ["Ceza", "Sagopa Kajmer", "Ezhel", "Eminem", "Kendrick Lamar", "Tupac", "Drake"],
    "Jazz": ["Kerem Görsev", "İlhan Erşahin", "Miles Davis", "John Coltrane", "Louis Armstrong", "Ella Fitzgerald"],
    "Elektronik (EDM)": ["Mahmut Orhan", "Burak Yeter", "Mercan Dede", "Daft Punk", "Avicii", "Calvin Harris", "David Guetta"],
    "Metal": ["Pentagram (Mezarkabul)", "Kurban", "Hayko Cepkin", "Metallica", "Iron Maiden", "Slipknot"],
    "Anadolu Rock": ["Barış Manço", "Cem Karaca", "Erkin Koray", "Moğollar"],
    "Türk Halk Müziği": ["Neşet Ertaş", "Musa Eroğlu", "Arif Sağ", "Zara"],
    "Türk Sanat Müziği": ["Zeki Müren", "Müzeyyen Senar", "Bülent Ersoy"],
    "Indie / Alternative": ["Yüzyüzeyken Konuşuruz", "Adamlar", "Arctic Monkeys", "Radiohead"],
    "Blues": ["Yavuz Çetin", "B.B. King", "Eric Clapton"],
    "Klasik Müzik": ["Fazıl Say", "İdil Biret", "Mozart", "Beethoven"],
}

def render_timeline(albums: list[dict]) -> str:
    if not albums:
        return "<li><span class='year'>—</span> Albüm bilgisi ekleyebilirsiniz.</li>"
    items = []
    for a in albums:
        year = a.get("year", "—")
        title = a.get("title", "Albüm")
        items.append(f"<li><span class='year'>{year}</span> {title}</li>")
    return "\n        ".join(items)

def render_compare(me: str, other: str, rows: list[dict]) -> str:
    # rows: [{"feature":"Tempo", "me":"Orta", "other":"Yavaş"}]
    default_rows = [
        {"feature":"Söz Teması", "me":"—", "other":"—"},
        {"feature":"Tempo", "me":"—", "other":"—"},
        {"feature":"Tarz", "me":"—", "other":"—"},
        {"feature":"Sahne Havası", "me":"—", "other":"—"},
    ]
    rows = rows or default_rows
    trs = []
    for r in rows:
        trs.append(
            f"<tr><td>{r.get('feature','Özellik')}</td>"
            f"<td>{r.get('me','—')}</td>"
            f"<td>{r.get('other','—')}</td></tr>"
        )
    return f"""
  <div class="table-wrap">
    <table class="compare">
      <tr>
        <th>Özellik</th>
        <th>{me}</th>
        <th>{other}</th>
      </tr>
      {''.join(trs)}
    </table>
  </div>
"""

def artist_page_html(slug: str, name: str, genre: str, about: str, works: list[str],
                     albums: list[dict], compare_with: str, compare_rows: list[dict],
                     moods: list[str], why: str) -> str:

    works_html = "\n".join([f"        <li>{w}</li>" for w in works]) if works else "        <li>Ödev için eser ekleyebilirsiniz.</li>"
    timeline_html = render_timeline(albums)
    compare_html = render_compare(name, compare_with, compare_rows)

    moods = moods or ["🎧 Düşünceli", "🔥 Enerjik", "🌙 Gece"]
    tags_html = "\n          ".join([f"<span class='tag'>{m}</span>" for m in moods])

    why_text = why or "Gitar/ritim yapısı, üretim tarzı ve genel atmosfer bu sanatçıyı bu türle ilişkilendirir."

    return f"""<!doctype html>
<html lang="tr">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{name} • Sanatçı</title>
  <link rel="stylesheet" href="../css/style.css" />
</head>
<body>

<header class="site-header small">
  <nav class="nav container">
    <a class="logo" href="../index.html">
      <img src="../img/picture.webp" alt="MusicGenres Logo">
      <span>MusicGenres</span>
    </a>
    <ul class="nav-links">
      <li><a href="../index.html">Ana Sayfa</a></li>
      <li><a class="active" href="../genres.html">Türler</a></li>
      <li><a href="../contact.html">İletişim</a></li>
    </ul>
  </nav>

  <div class="hero container">
    <h1>{name}</h1>
    <p>{genre} türü ile ilişkilendirilen sanatçı/grup.</p>
  </div>
</header>

<main class="container">

  <section class="section">
    <h2>Hakkında</h2>
    <p class="muted">{about}</p>
  </section>

  <section class="section info">
    <div class="info-box">
      <h3>Müzik Türü</h3>
      <p>{genre}</p>
    </div>
    <div class="info-box">
      <h3>Öne Çıkan Eserler</h3>
      <ul class="mini-list">
{works_html}
      </ul>
    </div>
  </section>

  <!-- 2️⃣ Albüm Zaman Çizelgesi -->
  <section class="section">
    <h2>Albüm Zaman Çizelgesi</h2>
    <ul class="timeline">
        {timeline_html}
    </ul>
  </section>

  <!-- 4️⃣ Karşılaştırma -->
  <section class="section">
    <h2>Karşılaştırma</h2>
    <p class="muted">Aynı türde iki sanatçının bazı özelliklerinin karşılaştırılması.</p>
    {compare_html}
  </section>

  <!-- 6️⃣ Etkileşim -->
  <section class="section">
    <h2>Etkileşimli Bilgi</h2>
    <div class="accordion">
      <button class="acc-btn" type="button">Bu sanatçı neden {genre}?</button>
      <div class="acc-content">
        <p>{why_text}</p>
        <p><strong>Uygun Ruh Halleri:</strong></p>
        <div class="tags">
          {tags_html}
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <a class="btn" href="../genres.html">← Türlere Geri Dön</a>
  </section>

</main>

<footer class="footer">
  <div class="container footer-inner">
    <p>©️ 2025 MusicGenres</p>
    <p class="muted">Sanatçı Bilgi Sayfası</p>
  </div>
</footer>

<script src="../js/app.js"></script>
</body>
</html>
"""

def main():
    data = json.loads(DATA_FILE.read_text(encoding="utf-8")) if DATA_FILE.exists() else {}

    # Her türde “kiminle karşılaştırılsın” otomatik: aynı türdeki bir sonraki kişi
    for genre, names in GENRES.items():
        for i, name in enumerate(names):
            slug = slugify(name)
            rec = data.get(slug, {})

            about = rec.get("about", f"{name} hakkında kısa bilgi ekleyebilirsiniz (2–4 cümle).")
            works = rec.get("works", ["Örnek eser 1", "Örnek eser 2"])

            # 2️⃣ timeline: JSON’da albums varsa onu kullan, yoksa boş
            albums = rec.get("albums", [])

            # 4️⃣ compare: JSON’da compare varsa onu kullan, yoksa otomatik eşleştir
            compare_with = rec.get("compare_with")
            if not compare_with:
                other_name = names[(i + 1) % len(names)] if len(names) > 1 else name
                compare_with = other_name
            compare_rows = rec.get("compare_rows", [])

            # 6️⃣ etkileşim: moods + why
            moods = rec.get("moods", [])
            why = rec.get("why", "")

            html = artist_page_html(
                slug=slug,
                name=rec.get("name", name),
                genre=rec.get("genre", genre),
                about=about,
                works=works,
                albums=albums,
                compare_with=compare_with,
                compare_rows=compare_rows,
                moods=moods,
                why=why
            )

            (ARTIST_DIR / f"{slug}.html").write_text(html, encoding="utf-8")

    print("✅ Tüm sanatçı sayfalarına 2️⃣ 4️⃣ 6️⃣ otomatik eklendi.")

if __name__ == "__main__":
    main()