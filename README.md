# 2026 World Cup — Group & Knockout Projection ⚽

**🌐 Idioma / Language:** [Español](#español) · [English](#english)

> **Página en vivo / Live page:** `https://vixbee.github.io/mundial-2026/`
> *(reemplaza con tu propia URL cuando actives GitHub Pages / replace with your own URL once GitHub Pages is enabled)*

---

## Español

Una proyección basada en datos del Mundial 2026, desde la fase de grupos hasta el título. Convierte el ranking FIFA de cada selección en probabilidades por partido y simula el torneo completo 20.000 veces para estimar quién avanza, quién llega a cada ronda de eliminatorias y quién tiene más opciones de levantar la copa.

El resultado es un tablero web autónomo (sin servidores, sin bases de datos, sin compilación) más una hoja de cálculo maestra con todos los números detrás.

### Contenido

| Archivo | Qué es |
|---------|--------|
| `index.html` | El tablero interactivo. Ábrelo en cualquier navegador, no hay nada que instalar. |
| `Proyeccion-Mundial-2026-MAESTRO.xlsx` | Hoja de cálculo maestra con cada número detrás de la página, en 7 pestañas. |

El tablero tiene cuatro pestañas, con selector español / inglés (ES / EN):

- **Partidos** — los 72 juegos de grupos con probabilidad de victoria/empate/derrota, el marcador más probable y un color (verde = favorito del modelo, amarillo = partido parejo / empate probable).
- **Avance** — la probabilidad de cada selección de ganar su grupo y de clasificar a eliminatorias.
- **Eliminatorias** — el cuadro de dieciseisavos (Round of 32) con los clasificados más probables.
- **Favoritos** — el ranking de candidatos al título según sus probabilidades.

La hoja de cálculo incluye además las probabilidades por partido, una tabla de avance grupo por grupo, el cuadro y las probabilidades ronda por ronda (octavos → campeón).

### Cómo funciona el modelo

La proyección se construye en cuatro pasos:

1. **Ranking → puntos.** La posición de cada selección en el ranking FIFA masculino (edición del 11 de junio de 2026) se convierte en puntos aproximados.
2. **Puntos → probabilidades.** La diferencia de puntos entre dos equipos pasa por una fórmula tipo Elo (la misma familia que usa la FIFA) para obtener probabilidades de victoria/empate/derrota.
3. **Probabilidades → goles.** De ese desbalance se derivan goles esperados para cada lado y se modela el marcador con una distribución de Poisson (media del torneo ≈ 2.6 goles por partido).
4. **Simulación.** Se juegan 20.000 torneos completos: fase de grupos con puntos reales 3/1/0 y desempates oficiales, y luego eliminatorias a una sola partida (los empates se deciden con penales sesgados hacia el equipo más fuerte). El promedio de todos da probabilidades estables en lugar de un único cuadro frágil.

Se aplica una pequeña ventaja de local (+60 puntos de ranking) **solo** a los tres anfitriones —México, Estados Unidos y Canadá— en sus propios partidos, ya que el resto juega en cancha neutral.

### Importante: es una estimación, no un pronóstico

Léelo antes de sacar conclusiones:

- **Ninguna proyección puede ser "verdadera".** El fútbol es muy aleatorio; hasta el favorito más claro pierde a menudo. Estos números son probabilidades, no certezas.
- **Solo conoce el ranking.** El modelo no sabe de lesiones, forma actual, suspensiones, cambios de plantilla ni motivación.
- **Los marcadores son ilustrativos.** Un "2–0" proyectado es un resultado plausible, no siempre el más probable.
- **El cuadro es un escenario.** La estructura del Round of 32 es la oficial de FIFA, pero los cruces desde octavos usan el orden estándar del bracket, y el cuadro único más probable tiene una probabilidad mínima de cumplirse tal cual.

Tómalo como una base informada y reproducible: una referencia para divertirse, no una guía de apuestas.

### Verlo en local

No requiere herramientas. Descarga ambos archivos en la misma carpeta y haz doble clic en `index.html`. El botón "Descargar Excel" funciona mientras la hoja de cálculo esté junto a la página.

### Publicarlo (gratis)

Es un sitio estático, así que sirve cualquier hosting gratuito: GitHub Pages, Cloudflare Pages, Netlify o Vercel. Para GitHub Pages: sube ambos archivos a un repositorio público, ve a **Settings → Pages**, elige **Deploy from a branch**, selecciona **main / (root)** y guarda. Tu URL aparece un minuto después.

### Actualizar la proyección

Cuando se publique un nuevo ranking FIFA, cambia las posiciones, regenera la página y vuelve a subir `index.html`. La columna de diferencia de ranking de la hoja de cálculo es una fórmula viva, así que editar las posiciones la recalcula sola.

### Notas técnicas

- HTML, CSS y JavaScript puro — **sin dependencias externas**, funciona sin conexión.
- Todos los datos están precalculados y embebidos en la página, así que carga al instante.
- Construido con un modelo propio Elo + Poisson + Montecarlo.

### Fuente de datos

Ranking FIFA Masculino oficial, edición del 11 de junio de 2026 — la última actualización antes del torneo.

### Aviso

Proyecto de aficionado, independiente y sin fines comerciales. No está afiliado, avalado ni conectado con la FIFA. Los nombres de selecciones y el ranking pertenecen a sus respectivos dueños.

---

## English

A data-driven projection of the 2026 FIFA World Cup, from the group stage all the way to the title. It turns each team's FIFA ranking into match probabilities and simulates the whole tournament 20,000 times to estimate who advances, who reaches each knockout round, and who is most likely to lift the trophy.

The result is a single, self-contained web dashboard (no servers, no databases, no build step) plus a master spreadsheet with all the underlying numbers.

### What's inside

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

### How the model works

The projection is built in four steps:

1. **Ranking → points.** Each team's position in the official FIFA Men's ranking (June 11, 2026 edition) is converted into approximate ranking points.
2. **Points → match odds.** The points gap between two teams is run through an Elo-style formula (the same family FIFA uses) to get win/draw/loss probabilities.
3. **Odds → goals.** From that imbalance the model derives expected goals for each side and models the scoreline with a Poisson distribution (tournament average ≈ 2.6 goals per game).
4. **Simulation.** 20,000 full tournaments are played out — group stage with real 3/1/0 points and official tiebreakers, then single-elimination knockouts (ties decided by a penalty draw weighted to the stronger side). Averaging across all of them gives stable probabilities instead of one fragile "single outcome" bracket.

A small home advantage (+60 ranking points) is applied **only** to the three host nations — Mexico, the USA, and Canada — in their own matches, since everyone else plays on neutral ground.

### Important: this is an estimate, not a prediction

Please read this before drawing conclusions:

- **No projection can be "true."** Football is highly random; even the strongest favourite loses often. The numbers here are probabilities, not certainties.
- **It only knows the ranking.** The model has no information about injuries, current form, suspensions, squad changes, or motivation.
- **Scorelines are illustrative.** A projected "2–0" is a plausible result, not the single most-likely one in every case.
- **The bracket is one scenario.** The Round of 32 structure is FIFA's official one, but the pairings from the Round of 16 onward use the standard bracket order, and the single most-likely bracket has a tiny chance of occurring exactly as shown.

Treat it as an informed, reproducible baseline — a fun reference, not a betting guide.

### View it locally

No tools required. Just download both files into the same folder and double-click `index.html`. The "Download Excel" button works as long as the spreadsheet sits next to the page.

### Publish it (free)

It's a static site, so any free static host works — GitHub Pages, Cloudflare Pages, Netlify, or Vercel. For GitHub Pages: upload both files to a public repository, then go to **Settings → Pages**, choose **Deploy from a branch**, select **main / (root)**, and save. Your URL appears a minute later.

### Updating the projection

When a new FIFA ranking is published, swap in the new positions, regenerate the page, and re-upload `index.html`. The spreadsheet's ranking-difference column is a live formula, so editing the positions there recalculates it automatically.

### Tech notes

- Pure HTML, CSS, and vanilla JavaScript — **zero external dependencies**, works offline.
- All data is precomputed and embedded in the page, so it loads instantly.
- Built with a custom Elo + Poisson + Monte Carlo model.

### Data source

Official FIFA Men's World Ranking, June 11, 2026 edition — the last update before the tournament.

### Disclaimer

This is an independent, non-commercial fan project. It is not affiliated with, endorsed by, or connected to FIFA. All team names and rankings belong to their respective owners.
