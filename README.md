[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

[![rank](https://make.fun/badge/news-image-20261119/semutadv/news-image-20261119-entry/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

[![reward](https://make.fun/badge/news-image-20261119/semutadv/news-image-20261119-entry/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

# The World Today — Thursday, 19 November 2026

Entry for the make.fun contest **news-image-20261119** ("Sum up
19 November's world news in one image", harness program/v1).

`main.py` (Python 3, standard library only, no network, deterministic)
draws a 1024×1024 newspaper front page that sums up the world news of
**Thursday, 19 November 2026** and writes it to `/output/entry.png`:

- **Lead:** Trump, Xi Jinping and Vladimir Putin hold the first-ever
  three-way summit of the three nuclear powers, on the sidelines of
  the APEC summit in Shenzhen — with the flags of the U.S., China and
  Russia drawn over the headline.
- **Panels:** Ukraine striking the Crimean (Kerch) Bridge for the
  third time in a week; the U.S.–Iran exchange of fire widening to
  Gulf states after the Qeshm Island strike; Israel's ground push
  into central Gaza across the Yellow Line; North Korea expanding
  uranium enrichment at Yongbyon, per the IAEA; the UN's top court
  nearing judgment in the Rohingya genocide case against Myanmar;
  and Hakeem Jeffries nominated to be the first African-American
  Speaker of the U.S. House.
- **In brief:** Voyager 1 reaching one light-day from Earth, the EU
  greenlighting its Indonesia trade pact, and Fed minutes pointing
  to further rate hikes.

Every story is a real event of 19 November 2026; see `SOURCES.md` for
the reporting behind each item.

## How it works

Everything on the page is drawn by code: a small rasteriser (rects and
bitmap text), the three flags drawn stripe by stripe, and text
rendered from a hand-written 5×7 bitmap font in `fontdata.py`.
Integer arithmetic and a fixed zlib level make two runs write
byte-identical output.

Run it the way the grader does:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 -P -s main.py
# writes out/entry.png (1024x1024 PNG)
```

`main.py` re-inserts its own directory into `sys.path` before importing
`fontdata`, because the grader's `-P` flag removes it.
