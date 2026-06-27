# PetsQuest - Agent Context

## Regola Grafica

Usare gli asset gia' presenti nel progetto. Non introdurre placeholder geometrici se esiste un asset coerente nello stile PetsQuest.

## Skill Codex Di Riferimento

Per qualunque lavoro su asset raster PetsQuest usare:

```text
/Users/vittoriocutolo/.codex/skills/petsquest-character-sprites
```

La skill copre sprite personaggi/nemici, animazioni combat, mappe campagna, sfondi battaglia, icone UI/inventario/endgame, badge rank, naming, dimensioni, direzioni, validazione PNG e regole git sugli asset generati.

## Memoria Sprite

Non dedurre mai l'orientamento di uno sprite dal nome file o dal suffisso `_left`. Prima di cambiare uno stem sprite nel codice, controllare l'audit:

```text
SPRITE_ORIENTATION_AUDIT.md
```

Stato verificato: `main_character` e' un'eccezione, perche' usa `idle_left` per guardare a destra ma `attack`, `hit` e `death` senza suffisso per guardare a destra. Gli altri giocabili verificati usano `idle` per guardare a destra. Lo scheletro nemico usa `idle`, `attack`, `hit`, `death` per guardare a sinistra.

## Repo e Avvio

- Entry point: `index.html`.
- Dev server locale: `python3 -m http.server 8080`.
- URL: `http://localhost:8080/index.html`.
- Progetto locale di lavoro: `/Users/vittoriocutolo/Documents/PetsQuest`.
- Repo GitHub sorgente: `/Users/vittoriocutolo/Claude/PetsQuest Game`.

## Stato Attuale

Implementato nel prototipo:

- schermata selezione razza/classe;
- mappa campagna visuale;
- combat screen con sprite, HUD, risorse e azioni;
- endgame hub visuale;
- combat loop giocabile con arma, abilita', oggetto e difesa;
- risorse reali Energia/Mana/Rabbia e pozione consumabile;
- hit/miss reale su attacco direzionale;
- segnale nemico semi-telegrafato in difesa.

Non ancora implementato:

- sequenza magica a 4 punti;
- cura con target;
- loot/progressione reale;
- persistenza scelta razza/classe;
- multiplayer/endgame gameplay.

## Attenzione Path Asset

Nel progetto locale `index.html` usa path:

```text
assets/...
```

Nel repo GitHub molte sorgenti asset vivono sotto:

```text
art_input/assets/...
```

Prima di committare sul repo GitHub, trasformare i path non `assets/generated_ui/` da `assets/...` a `art_input/assets/...`.

## File Documentazione

- `README.md`: panoramica, stato prototipo e asset.
- `SPECS.md`: specifiche MVP e stato gameplay.
- `TECH.md`: architettura tecnica corrente.
- `GENERATED_UI_ASSETS.md`: manifest asset UI generati.
- `CLAUDE.md`: note operative per agenti.
