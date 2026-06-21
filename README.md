# Proyección Mundial 2026 — auto-actualizable ⚽

Sitio estático que proyecta el Mundial 2026 (avance de grupos, cuadro de eliminatorias y favoritos al título) con un modelo Elo + Poisson + Montecarlo, **condicionado a los resultados reales** y mezclado con las cuotas del mercado. Una vez configurado, **se actualiza solo cada día**: un GitHub Action descarga los resultados, vuelve a correr el modelo y publica; la página relee los datos sola.

## Qué hay en el repositorio

| Archivo | Para qué |
|---|---|
| `index.html` | El tablero (generado). Se sirve por GitHub Pages. |
| `wcdata.json` | Datos del modelo (generado). La página lo relee cada 10 min. |
| `Proyeccion-Mundial-2026-MAESTRO.xlsx` | Libro Excel con todo (generado). |
| `fetch_results.py` | Descarga resultados reales de **openfootball** (JSON público, sin API key) → `results.json`. |
| `gen_html.py` | Corre el modelo (Elo + xG + 20.000 simulaciones) → `wcdata.json`. |
| `master.py` | Construye el Excel. |
| `write_html.py` | Inyecta los datos en `index.html`. |
| `results.json` | Resultados reales (lo reescribe `fetch_results.py`). |
| `xg.json`, `odds.json` | xG y cuotas de campeón — **manuales** (ver abajo). |
| `elo.json`, `sched.json`, `fixtures.json` | Ratings Elo, horarios/sedes y fixtures (datos base). |
| `.github/workflows/actualizar.yml` | El GitHub Action que automatiza todo. |

## Puesta en marcha (una sola vez)

1. **Crea un repositorio público** y sube todos estos archivos (incluida la carpeta oculta `.github`).
2. **Activa GitHub Pages:** Settings → Pages → Source: *Deploy from a branch* → rama `main`, carpeta `/(root)` → Save. Tu sitio quedará en `https://TU-USUARIO.github.io/TU-REPO/`.
3. **Activa el Action:** ve a la pestaña *Actions*, acepta habilitar los workflows. El Action ya tiene permiso de escritura (`contents: write`) para publicar los cambios.
4. Listo. El Action corre **todos los días** (por defecto 14:00 UTC) y también puedes lanzarlo a mano desde *Actions → Actualizar proyección Mundial 2026 → Run workflow*.

## Cómo funciona el ciclo automático

```
cron diario  →  fetch_results.py (baja resultados reales, sin API key)
             →  gen_html.py  (re-simula el torneo con los resultados)
             →  master.py    (rehace el Excel)
             →  write_html.py (rehace index.html)
             →  commit + push →  GitHub Pages publica
             →  la página relee wcdata.json sola → se ve actualizada
```

No tienes que tocar nada para que los **resultados** se reflejen.

## Lo que es automático y lo que no (importante)

- **Automático:** resultados → y con ellos las tablas de grupo, el avance, el cuadro y la probabilidad de campeón *del modelo*.
- **Manual:** el **xG** (`xg.json`) y las **cuotas de campeón** (`odds.json`). No existe un feed gratuito y fiable de esos dos datos, así que se quedan en sus últimos valores hasta que los edites a mano. La mezcla de favoritos pesa 70% mercado / 30% modelo; mientras no actualices `odds.json`, esa parte queda congelada.

Para refrescarlos: edita `xg.json` (clave `"Local|Visitante": [xg_local, xg_visitante]`) y `odds.json` (clave `"Equipo": cuota_americana`), haz commit, y el Action los tomará en la siguiente corrida.

## La fuente de resultados

`fetch_results.py` usa [openfootball/worldcup.json](https://github.com/openfootball/worldcup.json): dominio público, sin API key, sin límites. Su único matiz es que **se actualiza a mano una vez al día**, así que la proyección va con hasta ~1 día de retraso respecto al minuto a minuto. Para la cadencia diaria recomendada, es suficiente.

Si algún día quieres una fuente con menos retraso, el adaptador es fácil de cambiar por football-data.org o API-Football (requieren una API key gratuita y guardarla como *secret* del repositorio).

## Correrlo en tu computadora

```bash
pip install numpy openpyxl
python fetch_results.py    # baja resultados reales
python gen_html.py         # corre el modelo
python master.py           # rehace el Excel
python write_html.py       # rehace index.html
```

Abre `index.html` en el navegador (al abrirlo localmente usa los datos incrustados; publicado, relee `wcdata.json`).

## Aviso

Proyecto de aficionado, independiente, sin afiliación con FIFA. Es una estimación probabilística: ignora lesiones, alineaciones y forma; no es un pronóstico fiable.
