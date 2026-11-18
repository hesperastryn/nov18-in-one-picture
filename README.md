# nov18-in-one-picture

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/hesperastryn/nov18-in-one-picture/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/hesperastryn/nov18-in-one-picture/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

The world news of **Wednesday 18 November 2026** in one picture: a newspaper-style front page drawn entirely in code. A big date header tops six illustrated panels — the Trump·Xi·Putin APEC gathering in Shenzhen (US, Chinese and Russian flags over the skyline), Iran's drone strikes on Gulf bases and Bahrain's interceptions, Israel's new operation in central Gaza, severe Cyclone Akvan bearing down on Odisha, GTA VI's midnight launch after a 13-year wait, and gold sliding to a one-year low — with an "also today" ticker (Quad leaders in Manila, the US losing measles-free status, a magnitude 6 quake in Papua New Guinea) along the bottom.

`generate.py` (Python + PIL) draws the image procedurally — flat vector-style panels, flags, a tanker and drones, smoke columns, a cyclone spiral, a neon VI badge, a falling gold chart — and writes `entry.png` (1024×1024). The entry program `main.py` is standard-library only: it copies the committed `entry.png` to the output directory, byte-identical on every run.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
python3 generate.py   # redraws entry.png from scratch
```

---
<sub>Entered on [make.fun](https://make.fun/?ref=9sbzt2n6&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
