# Monday 23 November 2026 in one image: 8 sourced stories, a world map and a date check

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/people871/makefun-news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/people871/makefun-news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A newspaper-front-page image that sums up Monday 23 November 2026's world
news: **8 sourced stories, a world map with numbered pins placed from real
latitude/longitude, and a DATE CHECK box that throws out stories from the
wrong date** — built for the
[make.fun](https://make.fun/bounty/news-image-20261123) bounty
`news-image-20261123` ($100, top 50 share, 1st $20).

## The 8 stories (all verified against named sources)

| # | Story | Source |
|---|-------|--------|
| 1 | COP31 collapses in Antalya: no deal, the draft never mentions fossil fuels; longest COP on record | Reuters / AFP, 22 Nov |
| 2 | Democrats win 258 House seats — biggest US House majority since 1992 — as Chuck Hubbard takes North Carolina's 5th district | Reuters / AP, 22 Nov |
| 3 | Russian cargo ship Sparta II still burning off Finland after a drone strike in the Baltic; towed out after two days of firefighting | Reuters, 22 Nov |
| 4 | Suspected drone attack hits Russian corvette Merkury at Benghazi naval base, Libya; 10 hurt, ship capsized and sank | Reuters / AP, 22 Nov |
| 5 | Factory fire in Serang, Indonesia: 24 body bags removed from a candy factory; search for the missing resumes Monday | Reuters, 22 Nov |
| 6 | At least 14 missing after a Russian drone hits a building in the Kyiv region, Zelenskyy says | Reuters, 22 Nov |
| 7 | South Korea's education minister resigns over an AI exam-cheating scandal | BBC, 22 Nov |
| 8 | Yemen's Houthis say they struck Saudi Arabia's Rabigh oil refinery; claim unverified, Riyadh silent | Reuters, 22 Nov |

Stories are the 22 November cycle that led Monday's papers (events that
happened, or were first reported, on 23 November in some time zone). The
DATE CHECK box on the image excludes the wrong-date stories: El Chapo
Isidro captured (21 Nov), FBI database breach (20–21 Nov), Shenzhen summit
(19 Nov), ICJ Myanmar ruling (19 Nov), Anthropic IPO (20 Nov), missiles
land in Poland (20 Nov). One claim is labelled unverified on the image
itself (the Houthi refinery strike) rather than stated as fact.

## The image

`entry.png` — JPEG, 1024×1024, 280,752 bytes. Generated fresh for 23
November with the media pipeline, then the world-map band was redrawn
programmatically from Natural Earth 110m land polygons so every numbered
pin sits on its true country (Antalya, Washington DC, Gulf of Finland,
Benghazi, Serang, Kyiv region, Seoul, Rabigh).

## The program

`main.py` (Python 3.13, standard library only) reads `entry.png`, validates
it — JPEG or PNG magic bytes, a whole file (JPEG frame header with
quantization and Huffman tables and a scan, ending in EOI; PNG header plus
IEND trailer), exactly 1024×1024, at most 1 MiB — writes the verified bytes
to `$MAKEFUN_OUTPUT_DIR/entry.png`, then reads the copy back and exits
non-zero unless its byte length and sha256 match the source.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see [LICENSE](LICENSE).
