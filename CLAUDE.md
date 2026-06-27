# PetsQuest — Agent Context

## Regola grafica
Ogni volta che serve un asset grafico non ancora presente nella cartella `assets/`, fermarsi e chiedere all'utente di crearlo prima di procedere con l'implementazione. Non usare placeholder geometrici se esiste già uno stile visivo definito nel progetto.

---

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
- **Animazioni attacco/hit/death** — catena a 4 step in `resolveRound()`: player attack → enemy hit → enemy attack → player hit → resolution
- **Bilanciamento combat** — formule danno usano ATK/DEF/MATK reali; guard anti-doppio-click su tutti i handler; UI magia spiega la meccanica; sequenza incantesimo mostrata nel log
- HP bars, Rabbia bar, panel UI, background con luna/stelle/montagne
- Scaling responsivo del canvas via CSS transform

### ❌ Non ancora fatto (in ordine di priorità)
1. **Character selection** — schermata scelta razza + classe prima del combat ← **PROSSIMO STEP, GRAFICA DISPONIBILE**
2. **Effetti visivi** — flash bianco sul colpito, particelle magiche
3. **Mappa campagna** — board a quadri (Quadro → Combat → Miniboss → Rewards)
4. **Multiplayer** — WebSocket / Colyseus (fase avanzata)

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

**Naming controintuitivo per `idle`**: `idle` = guarda sinistra, `idle_left` = guarda destra.  
Regola: il personaggio a SINISTRA usa `idle_left`, quello a DESTRA usa `idle`.

**⚠️ ATTENZIONE — la convenzione è NON UNIFORME tra i set:**

| Set | no-suffix | `_left` |
|-----|-----------|---------|
| `idle` | guarda **SINISTRA** | guarda **DESTRA** |
| `attack` | guarda **DESTRA** ← invertito! | guarda **SINISTRA** |
| `hit` | guarda **SINISTRA** | guarda **DESTRA** |
| `death` | guarda **SINISTRA** | guarda **DESTRA** |

Solo `attack` ha la convenzione invertita rispetto a `idle`. `hit` e `death` seguono la stessa di `idle`.

Quindi, per direzione coerente:
- **Player** (sinistra schermo, guarda destra): `idle`→`left`; `attack`→`attack` (no-suffix); `hit`→`hitLeft`; `death`→`deathLeft`
- **Enemy** (destra schermo, guarda sinistra): `idle`→`idle` (no-suffix); `attack`→`attackLeft`; `hit`→`hit` (no-suffix); `death`→`death` (no-suffix)

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
| `playAnim(sprite, frames, speed, cb)` | Animazione one-shot + callback via setTimeout (background-tab safe) |
| `returnToIdle(sprite, idleFrames)` | Ripristina sprite a looping idle dopo animazione one-shot |

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

## Animazioni: note tecniche

`frames` ha 8 chiavi per personaggio: `idle, left, attack, attackLeft, hit, hitLeft, death, deathLeft`.

`playAnim(sprite, frameList, speed, cb)` — usa `setTimeout(cb, ms)` dove `ms = Math.round(frameList.length / speed / 60 * 1000)`. Non usa ticker per il callback, quindi funziona anche con tab in background.

**IMPORTANTE**: `requestAnimationFrame` è throttled nei tab in background (Chrome), quindi le animazioni PixiJS non girano visivamente se il tab non è in focus. Ma il callback e la logica di gioco si completano correttamente grazie a `setTimeout`.

---

## Grafica disponibile in `art_input/`

Cartella sorgente degli asset prodotti dall'artista. Tutto il necessario per il prossimo step è già presente.

### Sprite personaggi giocabili (solo `idle` per ora, 6 frame × 2 direzioni)
| Personaggio | Razza | Classe |
|-------------|-------|--------|
| `main_character` | Cane | Guerriero |
| `dog_paladin` | Cane | Paladino |
| `cat_mage` | Gatto | Mago |
| `cat_necromancer` | Gatto | Negromante |
| `mouse_warrior` | Topo | Guerriero |
| `mouse_thief` | Topo | Ladro |
| `mouse_priest` | Topo | Prete |

### Altri asset presenti
- `backgrounds/battle/` — sfondi battaglia per razza (dog_forest_night, cat_dark_dungeon, mouse_ruined_city, pvp_arena)
- `campaign/` — mappe campagna, tiles percorso, icone eventi (combat/rest/shop/treasure)
- `ui/abilities/` — icone abilità per tutte le classi
- `ui/resources/` — icone Rabbia/Mana/Fede/Energia
- `ui/buttons/` — bottoni con stati normal/hover/pressed
- `inventory/` — armi, armature, pozioni, loot
- `endgame/` — sfondi raid/dungeon, icone rank (bronze→diamond)
- `tools/` — script Python per processare sprite dall'artista

### Convenzione direzioni (da `art_input/README.md`)
> Personaggi giocabili (cani/gatti/topi): la direzione principale **senza suffisso** va da sinistra → destra.  
> Nemici (scheletro): la direzione principale **senza suffisso** va da destra → sinistra.  
> Le varianti `_left` sono le versioni specchiate.

Nota: per `idle` questa regola è **invertita per errore storico** (idle no-suffix guarda sinistra). La convenzione corretta vale solo per `attack`, `hit`, `death`. Vedi tabella in "Assets: struttura e convenzione CRITICA".

---

## Documenti del progetto
| File | Contenuto |
|------|-----------|
| `SPECS.md` | Regole di gameplay complete (razze, classi, combat, campagna, endgame) |
| `TECH.md` | Decisioni tecniche, scelte architetturali, domande aperte |
| `art_input/README.md` | Regole grafiche, workflow artista, convenzione naming sprite |
| `CLAUDE.md` | Questo file — punto di partenza per agenti |
