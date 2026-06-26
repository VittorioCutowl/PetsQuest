# PetsQuest — Decisioni Tecniche

## 1. Renderer: PixiJS v7

**Scelta**: PixiJS v7.4.2 via CDN  
**Alternativa scartata**: HTML/CSS/JS puro, Phaser.js, Kaboom.js

**Perché PixiJS**:
- WebGL-accelerated, ideale per pixel art con molti sprite
- AnimatedSprite nativo — gestisce spritesheet e frame sequences senza librerie aggiuntive
- Leggero rispetto a Phaser (nessun physics engine, tilemap engine, ecc. di cui non abbiamo bisogno)
- Controllo fine sul rendering layer-by-layer

**Perché non Phaser**:
- Overengineered per una demo: include physics, camera, tilemap, input system complessi
- Passeremo a Phaser se la campagna a quadri richiede tilemap complesse

**Versione bloccata a v7** (non v8) perché v8 ha API breaking changes e documentazione ancora immatura.

---

## 2. Struttura: Single HTML File (per ora)

**Scelta**: tutto in `index.html` — HTML + CSS + JS inline  
**Alternativa futura**: bundler (Vite) con file JS separati

**Perché single file adesso**:
- Zero setup, zero dipendenze locali
- Deploy immediato su qualsiasi static host
- Il progetto è ancora in fase di prototipo rapido
- Facile da condividere e testare

**Quando passare a Vite + moduli**:
- Quando `index.html` supera ~1500 righe
- Quando aggiungiamo più schermate (character selection, mappa campagna)
- Quando servirà un bundler per ottimizzare assets

---

## 3. Assets: PNG RGBA — Frame Singoli

**Scelta**: frame PNG singoli caricati via `new Image()` → `PIXI.Texture.from(img)`  
**Alternativa**: spritesheet JSON (TexturePacker) + `PIXI.Assets.load()`

**Perché frame singoli**:
- Già forniti così dall'artista
- Funzionano con `file://` senza server HTTP (CORS-safe)
- Più semplici da aggiungere/modificare animazione per animazione

**Quando passare a spritesheet**:
- In produzione, per ridurre le HTTP request (24+ immagini → 2-4 sheet)
- Quando l'artista esporterà in formato TexturePacker

**Formato sprite**:
- Dimensione frame: **362 × 724 px** RGBA
- Frame per animazione: **6**
- Scale in-game: **0.21** (≈ 76×152px a schermo)
- Naming: `{character}_{animation}_{nn}.png` (es. `main_character_idle_left_03.png`)

**Convenzione direzioni** ⚠️ controintuitiva:
- `idle` → guarda a **sinistra**
- `idle_left` → guarda a **destra**

---

## 4. State Machine del Combat

**Scelta**: state machine esplicita con `GS.phase` (stringa) + funzione `setPhase()`

```
'action' → 'dir_attack' ─────────┐
         → 'magic_attack' ───────┼→ 'def_physical' → 'resolution' → 'action'
         → (item, skip attack) ──┘  'def_magic'
```

**Perché non un framework di state machine**:
- Il combat ha ~6 stati ben definiti, non vale la dipendenza
- La transizione è sempre lineare (nessuna transizione parallela per ora)

**Timer**:
- `setInterval` a 100ms (0.1s granularità) per il countdown
- `stopTimer()` chiamato esplicitamente ad ogni transizione
- Keyboard listener pulito ad ogni cambio fase per evitare listener duplicati

---

## 5. Layer di Rendering

Quattro container PixiJS in ordine di draw:

| Layer | Contenuto | Si svuota? |
|-------|-----------|-----------|
| `L.bg` | Sfondo statico (cielo, luna, stelle, montagne) | Mai (disegnato una volta) |
| `L.chars` | Sprite animati player e nemico | Solo a reset/game over |
| `L.effects` | Floating damage, particelle, flash | Auto (ogni elemento si rimuove da solo) |
| `L.ui` | HP bars, timer, panel, bottoni | Ad ogni `setPhase()` |

**Perché separare effects da ui**:
- I floating numbers devono stare sopra i personaggi ma sotto i bottoni del panel
- Il layer effects si autogestisce (ticker rimuove ogni elemento quando alpha → 0)

---

## 6. Canvas e Layout

**Dimensioni**: `820 × 640 px`  
**Battle area**: `400 px` di altezza (BATTLE_H)  
**Panel azioni**: `240 px` di altezza (H - BATTLE_H)

**Scaling responsivo**: CSS `transform: scale()` sul wrapper, calcolato su `window.innerWidth`  
→ il canvas non cambia risoluzione, scala solo visivamente (pixel art rimane nitido)

**Font**: Press Start 2P (Google Fonts) — caricato e atteso (`document.fonts.load()`) prima di inizializzare PixiJS per evitare FOUT sui testi

---

## 7. Scelte di Gameplay da Tradurre in Codice

Decisioni aperte che impatteranno l'implementazione:

### Danni e Stats
- [ ] Definire formula danno base per classe (attacco fisico vs magico)
- [ ] Definire riduzione danno su parata (attuale: 85% fisico, 90% magico — da bilanciare)
- [ ] Definire scaling per livello (lineare? esponenziale?)

### Animazioni attacco (prossimo step)
- [ ] Quanti frame per animazione `attack`? (suggerito: 4-6 frame)
- [ ] L'attacco è un'animazione one-shot o loopping?
- [ ] Flash bianco sul personaggio colpito (1-2 frame)?
- [ ] Il personaggio avanza verso il nemico durante l'attacco o rimane fermo?

### Risorse (Rabbia, Energia, Mana)
- [ ] Rabbia: si accumula solo colpendo o anche ricevendo danno?
- [ ] Energia: quanto si rigenera per turno?
- [ ] Mana: si recupera fuori combattimento o solo con oggetti?

### Sequenza magica
- [ ] La sequenza nemica è visibile durante la fase azione o solo nella difesa?
- [ ] L'ordine scelto dal player cambia il tipo di effetto (es. 1→2→3→4 = fuoco, 4→3→2→1 = ghiaccio)?

---

## 8. Roadmap Tecnica

```
[✓] Fase 0 — Combat demo funzionante con sprite
[ ] Fase 1 — Animazioni attacco (frame hit + flash)
[ ] Fase 2 — Character selection screen
[ ] Fase 3 — Mappa campagna a quadri
[ ] Fase 4 — Refactor a Vite + moduli quando file cresce
[ ] Fase 5 — Multiplayer (WebSocket o Colyseus)
[ ] Fase 6 — Mobile responsive
```

---

*Documento aggiornato alla build iniziale del combat demo.*
