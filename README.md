# 2026 World Cup — Group & Knockout Projection ⚽

A data-driven projection of the 2026 FIFA World Cup, from the group stage all the way to the title. It turns each team's FIFA ranking into match probabilities and simulates the whole tournament 20,000 times to estimate who advances, who reaches each knockout round, and who is most likely to lift the trophy.

The result is a single, self-contained web dashboard (no servers, no databases, no build step) plus a master spreadsheet with all the underlying numbers.

> **Live page:** `https://vixbee.github.io/mundial-2026/`


---

## What's inside

| File | What it is |
|------|------------|
| `index.html` | The interactive dashboard. Open it in any browser — nothing to install. |
| `Proyeccion-Mundial-2026-MAESTRO.xlsx` | Master spreadsheet with every number behind the page, across 7 sheets. |

The dashboard has four tabs, with a Spanish / English toggle (ES / EN):

- **Matches** — all 72 group-stage games with win/draw/loss probabilities, the most likely scoreline, and a color tag (green = model favourite, yellow = tight match / likely draw).
- **Advancement** — each team's chance of winning its group and of reaching the knockout stage.
- **Knockouts** — the Round of 32 bracket filled in with the most likely qualifiers.
- **Favourites** — the title-odds ranking of the top contenders.

The spreadsheet additionally includes per-match probabilities, a full group-by-group advancement table, the bracket, and round-by-round odds (round of 16 → champion).

---

## How the model works

The projection is built in four steps:

1. **Ranking → points.** Each team's position in the official FIFA Men's ranking (June 11, 2026 edition) is converted into approximate ranking points.
2. **Points → match odds.** The points gap between two teams is run through an Elo-style formula (the same family FIFA uses) to get win/draw/loss probabilities.
3. **Odds → goals.** From that imbalance the model derives expected goals for each side and models the scoreline with a Poisson distribution (tournament average ≈ 2.6 goals per game).
4. **Simulation.** 20,000 full tournaments are played out — group stage with real 3/1/0 points and official tiebreakers, then single-elimination knockouts (ties decided by a penalty draw weighted to the stronger side). Averaging across all of them gives stable probabilities instead of one fragile "single outcome" bracket.

A small home advantage (+60 ranking points) is applied **only** to the three host nations — Mexico, the USA, and Canada — in their own matches, since everyone else plays on neutral ground.

---

## Important: this is an estimate, not a prediction

Please read this before drawing conclusions:

- **No projection can be "true."** Football is highly random; even the strongest favourite loses often. The numbers here are probabilities, not certainties.
- **It only knows the ranking.** The model has no information about injuries, current form, suspensions, squad changes, or motivation.
- **Scorelines are illustrative.** A projected "2–0" is a plausible result, not the single most-likely one in every case.
- **The bracket is one scenario.** The Round of 32 structure is FIFA's official one, but the pairings from the Round of 16 onward use the standard bracket order, and the single most-likely bracket has a tiny chance of occurring exactly as shown.

Treat it as an informed, reproducible baseline — a fun reference, not a betting guide.

---

## View it locally

No tools required. Just download both files into the same folder and double-click `index.html`. The "Download Excel" button works as long as the spreadsheet sits next to the page.

## Publish it (free)

It's a static site, so any free static host works — GitHub Pages, Cloudflare Pages, Netlify, or Vercel. For GitHub Pages: upload both files to a public repository, then go to **Settings → Pages**, choose **Deploy from a branch**, select **main / (root)**, and save. Your URL appears a minute later.

## Updating the projection

When a new FIFA ranking is published, swap in the new positions, regenerate the page, and re-upload `index.html`. The spreadsheet's ranking-difference column is a live formula, so editing the positions there recalculates it automatically.

---

## Tech notes

- Pure HTML, CSS, and vanilla JavaScript — **zero external dependencies**, works offline.
- All data is precomputed and embedded in the page, so it loads instantly.
- Built with a custom Elo + Poisson + Monte Carlo model.

## Data source

Official FIFA Men's World Ranking, June 11, 2026 edition — the last update before the tournament.

## Disclaimer

This is an independent, non-commercial fan project. It is not affiliated with, endorsed by, or connected to FIFA. All team names and rankings belong to their respective owners.
