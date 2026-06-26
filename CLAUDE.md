# PetsQuest — Agent Context

## Repo e avvio rapido
- **GitHub**: https://github.com/VittorioCutowl/PetsQuest
- **Dev server**: `python3 -m http.server 8080` dalla root del progetto
- **Entry point**: `index.html` (tutto il codice è in questo file — PixiJS, JS, CSS)
- **Apri**: http://localhost:8080

---

## Cos'è questo progetto
PetsQuest è un gioco RPG pixel art con combattimento a turni in tempo reale. Il gameplay ruota attorno a mini-giochi interattivi durante il combattimento (attacco direzionale con frecce, sequenza magica con 4 punti, difesa). Vedi `SPECS.md` per le regole complete estratte dall'infografica originale.

---

## Stato attuale dell'implementazione

### ✅ Fatto
- Combat system completo a 6 fasi (`action → dir_attack | magic_attack → def_physical | def_magic → resolution`)
- Timer 15s (azione) e 5s (difesa) con countdown visivo
- Attacco direzionale: D-pad cliccabile + supporto tastiera (frecce / WASD)
- Sequenza magica: 4 cristalli cliccabili + supporto tastiera (1-4)
- Difesa fisica e magica funzionanti
- Risoluzione danni con floating numbers animati e shake on hit
- Sprite animati (idle, 6 frame) per player (cane) e nemico (scheletro)
- HP bars, Rabbia bar, panel UI, background con luna/stelle/montagne
- Scaling responsivo del canvas via CSS transform

### ❌ Non ancora fatto (in ordine di priorità)
1. **Animazioni attacco** — frame one-shot per attack/hit (prossimo step)
2. **Character selection** — schermata scelta razza + classe prima del combat
3. **Effetti visivi** — flash bianco sul colpito, particelle magiche
4. **Mappa campagna** — board a quadri (Quadro → Combat → Miniboss → Rewards)
5. **Multiplayer** — WebSocket / Colyseus (fase avanzata)

---

## Stack tecnico
- **Renderer**: PixiJS v7.4.2 (`https://pixijs.download/v7.4.2/pixi.min.js`)
- **Font**: Press Start 2P (Google Fonts) — atteso con `document.fonts.load()` prima di init
- **Asset loading**: `new Image()` + `PIXI.Texture.from(img)` (funziona con `file://` e HTTP)
- **No bundler** — single HTML file, zero dipendenze locali (si migra a Vite quando il file supera ~1500 righe)

---

## Assets: struttura e convenzione CRITICA

```
assets/sprites/
├── main_character/
│   ├── idle/            ← cane guarda a SINISTRA ← usato per nemico se fosse cane
│   └── idle_left/       ← cane guarda a DESTRA → usato per PLAYER (sinistra schermo)
└── enemy_skeleton/
    ├── idle/            ← scheletro guarda a SINISTRA → usato per ENEMY (destra schermo)
    └── idle_left/       ← scheletro guarda a DESTRA
```

**Naming controintuitivo**: `idle` = guarda sinistra, `idle_left` = guarda destra.  
Regola: il personaggio a SINISTRA usa `idle_left`, quello a DESTRA usa `idle`.

**Dimensioni**: 362×724 px RGBA, 6 frame per animazione, scala in-game: 0.21

L'oggetto `frames` in JS:
```javascript
frames.player.idle  // array 6 PIXI.Texture — cane guarda sinistra
frames.player.left  // array 6 PIXI.Texture — cane guarda destra (usato per player)
frames.enemy.idle   // array 6 PIXI.Texture — scheletro guarda sinistra (usato per enemy)
frames.enemy.left   // array 6 PIXI.Texture — scheletro guarda destra
```

**Nuove animazioni**: quando l'artista consegna nuovi frame (es. `attack`, `hit`), aggiungere:
1. Cartella `assets/sprites/{personaggio}/{animazione}/`
2. Estendere `loadAllAssets()` con `loadFrames(path, count)`
3. Aggiungere alla struttura `frames`

---

## Architettura index.html

### Layer PixiJS (ordine di draw)
```javascript
L.bg      // sfondo statico — disegnato una volta sola al boot
L.chars   // AnimatedSprite player e nemico — float animation su ticker
L.effects // floating damage, flash — ogni elemento si auto-rimuove (ticker)
L.ui      // HP bars, timer, bottoni — svuotato e ridisegnato ad ogni setPhase()
```

### State machine
```
'action' → 'dir_attack' ──────────┐
         → 'magic_attack' ────────┼→ 'def_physical' → 'resolution' → 'action'
         → item (salta attacco) ──┘  'def_magic'
```

### Funzioni chiave
| Funzione | Scopo |
|----------|-------|
| `setPhase(phase)` | Switcha stato, svuota L.ui, ridisegna tutto |
| `drawStaticUI()` | HP bars, nomi, panel background — chiamata da setPhase |
| `drawTimerUI(rem, tot, label)` | Aggiorna solo la timer bar ogni 100ms |
| `resolveRound()` | Calcola danni, applica a GS, trigger floatDmg + shake |
| `startTimer(dur, onTick, onDone)` | setInterval 100ms, si stoppa con stopTimer() |
| `floatDmg(x, y, txt, color)` | Numero danno che sale e svanisce via ticker |
| `shake(sprite, intensity, ms)` | Vibrazione orizzontale su hit |
| `makeAnimSprite(frameList)` | Crea PIXI.AnimatedSprite con scala e anchor già impostati |

### Game state (GS)
```javascript
GS.phase           // fase corrente della state machine
GS.turn            // numero turno corrente
GS.player          // { name, cls, hp, maxHP, res, maxRes, resName, resColor, lv, atk, def, matk }
GS.enemy           // { name, cls, hp, maxHP, lv, atk, def, matk }
GS.playerAction    // 'attack' | 'ability' | 'item'
GS.playerAtkType   // 'physical' | 'magic' | null
GS.playerDir       // 'up'|'down'|'left'|'right' | null
GS.playerSeq       // array [0-3] sequenza magica player
GS.enemyAtkType    // 'physical' | 'magic' — pre-rollaato all'inizio del turno
GS.enemyDir        // direzione attacco nemico — rivelata in risoluzione
GS.enemySeq        // sequenza magica nemica — mostrata nella difesa magica
GS.playerDefDir    // direzione difesa scelta dal player
GS.playerDefSeq    // sequenza difesa scelta dal player
GS.turnResult      // { pDmg, eDmg, msgs } — popolato da resolveRound()
```

### Costanti layout
```javascript
const W = 820, H = 640;
const BATTLE_H = 400;       // area di battaglia
const PANEL_H  = 240;       // pannello azioni (H - BATTLE_H)
const PY = BATTLE_H + 48;   // Y start contenuto panel (sotto timer bar)
const GROUND_Y = BATTLE_H * 0.72;  // linea del terreno
const CHAR_SCALE = 0.21;    // scala sprite (362px → ~76px)
```

### Posizioni personaggi
```javascript
playerSprite.x = 210   // cane — sinistra
enemySprite.x  = 620   // scheletro — destra
// y = GROUND_Y + oscillazione seno (float animation)
```

---

## Prossimo step concreto: Animazioni di Attacco

**Cosa fare**: quando il player o il nemico attacca, riprodurre un'animazione one-shot (non looping) prima di mostrare il floating damage.

**Approccio consigliato senza nuovi sprite** (nel frattempo):
1. Tween del personaggio in avanti (verso il nemico) e indietro — ~300ms
2. Flash bianco sul bersaglio colpito (overlay alpha su L.effects)
3. Poi shake + floatDmg come ora

**Approccio con nuovi sprite** (quando disponibili):
1. Aggiungere cartella `assets/sprites/{char}/attack/` con N frame
2. Caricare in `frames.player.attack` / `frames.enemy.attack`
3. In `resolveRound()`: switchare temporaneamente lo sprite all'animazione attack, poi tornare a idle

**Domande aperte** (vedere anche `TECH.md` sezione 7):
- Quanti frame per l'animazione attacco?
- Il personaggio avanza fisicamente verso il nemico durante l'attacco?
- Flash bianco sì/no sul colpito?

---

## Documenti del progetto
| File | Contenuto |
|------|-----------|
| `SPECS.md` | Regole di gameplay complete (razze, classi, combat, campagna, endgame) |
| `TECH.md` | Decisioni tecniche, scelte architetturali, domande aperte |
| `CLAUDE.md` | Questo file — punto di partenza per agenti |
