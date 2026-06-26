# PetsQuest — Agent Context

## Cos'è questo progetto
PetsQuest è un gioco RPG pixel art a turni in tempo reale. Il gameplay ruota attorno a un sistema di combattimento con mini-giochi interattivi (direzione attacco, sequenza magica, difesa). Il progetto è in fase di demo HTML/CSS/JS con PixiJS v7.

## Stack tecnico
- **Renderer**: PixiJS v7 (`https://pixijs.download/v7.4.2/pixi.min.js`)
- **Font**: Press Start 2P (Google Fonts)
- **Dev server**: `python3 -m http.server 8080` dalla root del progetto
- **Entry point**: `index.html`
- **Assets**: `assets/sprites/` — PNG RGBA 362×724px, 6 frame per animazione

## Struttura file
```
PetsQuest Game/
├── index.html              ← gioco completo (PixiJS, tutto in un file)
├── SPECS.md                ← specifiche complete del gameplay
├── CLAUDE.md               ← questo file
└── assets/
    └── sprites/
        ├── main_character/
        │   ├── idle/               ← cane guarda a SINISTRA (usa per nemico)
        │   ├── idle_left/          ← cane guarda a DESTRA (usa per player)
        │   └── *.png               ← spritesheet e chromakey
        └── enemy_skeleton/
            ├── idle/               ← scheletro guarda a SINISTRA (usa per nemico)
            ├── idle_left/          ← scheletro guarda a DESTRA
            └── *.png
```

## Convenzione sprite — CRITICA
Il naming degli sprite è controintuitivo:
- `idle` → il personaggio guarda a **sinistra**
- `idle_left` → il personaggio guarda a **destra**

Regola per il combat:
- **Player** (sinistra dello schermo) → usa `idle_left` (guarda a destra, verso il nemico)
- **Enemy** (destra dello schermo) → usa `idle` (guarda a sinistra, verso il player)

## Architettura index.html
Il gioco è una state machine con queste fasi (`GS.phase`):
```
'action' → 'dir_attack' | 'magic_attack' → 'def_physical' | 'def_magic' → 'resolution' → 'action'
```

Layer PixiJS (in ordine di draw):
1. `L.bg` — sfondo statico (cielo, luna, stelle, montagne, terreno)
2. `L.chars` — sprite animati (player e nemico con float animation)
3. `L.effects` — floating damage numbers, effetti temporanei
4. `L.ui` — tutto il UI (HP bars, timer, panel, pulsanti)

Funzioni chiave:
- `setPhase(phase)` — switcha fase, pulisce UI, ridisegna
- `drawStaticUI()` — HP bars, nome personaggi, pannello di sfondo
- `drawTimerUI(remaining, total, label)` — timer bar (chiamata ogni 100ms)
- `resolveRound()` — calcola danni, applica, mostra floating numbers
- `startTimer(duration, onTick, onDone)` — timer con clearInterval
- `floatDmg(x, y, txt, color)` — numero danno fluttuante animato
- `shake(sprite, intensity, duration)` — shake animation su hit

## Costanti layout
```javascript
const W = 820, H = 640;
const BATTLE_H = 400;   // altezza area di battaglia
const PANEL_H = 240;    // altezza pannello azioni (H - BATTLE_H)
const PY = BATTLE_H + 48; // Y start contenuto pannello (sotto timer bar)
const GROUND_Y = BATTLE_H * 0.72; // linea del terreno
```

## Personaggi attuali (demo)
- **Player**: Biscotto, Guerriero Cane, Lv7 — risorsa: Rabbia (rossa)
- **Enemy**: Rattleclaw, Scheletro, Lv8

## Gameplay specs
Vedi `SPECS.md` per le specifiche complete di gameplay estratte dall'infografica.

## Cose da implementare (roadmap)
1. **Animazioni attacco** — frame separati per hit, flash sul colpo
2. **Character selection** — schermata scelta razza + classe
3. **Effetti visivi** — particelle magiche, glow
4. **Mappa campagna** — board a quadri
5. **Multiplayer / endgame** — dopo MVP

## Come avviare
```bash
cd "/Users/vittoriocutolo/Claude/PetsQuest Game"
python3 -m http.server 8080
# apri http://localhost:8080
```
