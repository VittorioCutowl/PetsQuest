# PetsQuest — Specifiche di Gameplay (MVP)

---

## 1. RAZZE E CLASSI

Ogni razza ha accesso a classi esclusive. La combinazione razza/classe determina le abilità disponibili e la risorsa usata in combattimento.

| Razza | Classi disponibili | Risorsa |
|-------|-------------------|---------|
| **Cani** | Guerriero, Paladino, Prete, Cacciatore | Rabbia / Fede / Energia |
| **Gatti** | Ladro, Negromante, Mago, Prete | Energia / Mana / Fede |
| **Topi** | Guerriero, Ladro, Prete | Rabbia / Energia / Fede |

### Risorsa per tipo di classe
- **Guerrieri / Cacciatori** → Rabbia (si accumula colpendo)
- **Ladri** → Energia (si rigenera ogni turno)
- **Caster (Mago, Negromante)** → Mana (pool fisso, si esaurisce)
- **Preti / Paladini** → Fede (bilanciata tra attacco e cura)

---

## 2. SISTEMA DI COMBATTIMENTO

Combattimento a **turni in tempo reale**. Ogni turno ha due fasi sequenziali.

### FASE 1 — AZIONE (15 secondi)

Il giocatore sceglie **una** azione tra:

#### A. Attacca con Arma
- Sceglie la **direzione** dell'attacco: ↑ ↓ ← →
- Tipo: attacco fisico

#### B. Usa Abilità
Dipende dalla classe:
- **Guerrieri / Fisici**: scelgono una direzione (usa Rabbia/Energia)
- **Caster (Mago, Negromante)**: collegano **4 punti** in un ordine a scelta (usa Mana)
- **Guaritori (Prete, Paladino)**: selezionano un bersaglio da curare (usa Fede)

#### C. Usa Oggetto
- Seleziona pozione, buff o altro oggetto dall'inventario
- Non consuma il turno di difesa (si difende comunque)

---

### FASE 2 — DIFESA (5 secondi)

Il nemico ha già deciso la sua azione nella Fase 1. Il giocatore deve:

#### Contro Attacco Fisico
- Sceglie da **quale lato** aspettarsi il colpo: ↑ ↓ ← →
- Se indovina: danno ridotto (~85%)
- Se sbaglia: danno pieno

#### Contro Attacco Magico
- Replica la **stessa sequenza di 4 punti** usata dall'attaccante
- Se corretta: danno ridotto (~90%)
- Se sbagliata: danno pieno
- Il giocatore vede la sequenza nemica da replicare

---

### RISOLUZIONE

| Situazione | Risultato |
|-----------|----------|
| Attacco fisico + direzione corretta | Colpisce |
| Attacco fisico + direzione sbagliata | Manca |
| Magia + sequenza corretta | Colpisce |
| Magia + sequenza sbagliata | Manca |
| Difesa fisica corretta | Danno ridotto |
| Difesa fisica sbagliata | Danno pieno |
| Difesa magica corretta (sequenza uguale) | Danno ridotto |
| Difesa magica sbagliata | Danno pieno |
| Difendi fisico ma ricevi magia (e viceversa) | Danno pieno |

---

## 3. PROGRESSIONE DEL PERSONAGGIO

### Tabella livelli (MVP)

| Range livello | Quadri campagna per salire |
|--------------|--------------------------|
| 1 → 3 | Ogni 2 quadri |
| 3 → 5 | Ogni 2 quadri |
| 5 → 6 | Ogni 2 quadri |
| 6 → 10 | Ogni 3 quadri |
| 10 → 15 | Ogni 4 quadri |
| 15 → 20 | Ogni 5 quadri |
| 20 → 25 | Ogni 6 quadri |
| 25 → 30 | Ogni 7 quadri |

### Come si ottiene EXP
- Uccidere mostri nei combattimenti
- Completare quadri della campagna
- Completare missioni secondarie

### Cosa porta il livello
- Miglioramento delle statistiche base
- Sblocco nuove abilità di classe
- **Punti Talento**: ogni livello guadagnato concede punti per la talent tree della classe

### Unlock endgame
- Dal **livello 15**: accesso a Dungeon (2-3 giocatori) e Arene (2-3 giocatori)
- **Miniboss** ogni X quadri con loot migliorato

---

## 4. LA CAMPAGNA

Tre storie separate, una per razza. Si giocano in modo indipendente.

### Storia Cani
Il Re dei Cani parte per un viaggio alla ricerca di alleati. Il giocatore lo affianca combattendo per proteggere il proprio popolo.

### Storia Topi
Ricostruisci la città soggiogata dai gatti. Incontra il Re dei Cani e unisce le forze per la libertà.

### Storia Gatti
Agisci nell'ombra, rapisce e conquista le terre dei cani. Insegui il Re dei Cani e affrontalo nello scontro finale.

### Struttura di un Quadro
```
Quadro → Combattimento → Miniboss (ogni X quadri) → Ricompense → Prossimo Quadro
```
- Ogni quadro offre ricompense e possibilità di loot dai mostri sconfitti
- I quadri avanzano la storia tramite dialoghi e cutscene

---

## 5. MODALITÀ ENDGAME (dal livello 15)

### 1. Raid — 5 giocatori
- Composizione: 1 Tank + 1 Healer + 3 DPS
- Versione avanzata dei dungeon
- Nemici e boss più forti
- Droppa il massimo livello equipaggiamento per quel dungeon
- Boss epici con meccaniche avanzate
- Loot esclusivo, equipaggiamento PvE di altissimo livello

### 2. Hero Dungeons
- Versione avanzata dei dungeon normali
- Nemici e boss più forti
- Droppa il massimo livello equipaggiamento per quel dungeon
- Meccaniche avanzate sui boss
- Loot di alta qualità

### 3. Ranked Dungeons
- Difficoltà crescente
- Cronometrati
- Classifiche stagionali
- Nuovo gear ogni stagione
- Ricompense estetiche (skin, mount, titoli, banner, ecc.)

### 4. Arene (2v2 / 3v3)
- PvP bilanciato
- Guadagni Punti Arena
- Acquista equipaggiamento estetico PvP dal shop arena
- Equipaggiamento Arena utilizzabile solo nelle Arene
- Nessun vantaggio in termini di potenza

### 5. Ranked Arenas
- Partite rankate
- Stagioni competitive
- Ricompense estetiche (skin, mount, titoli, emote, effetti, ecc.)
- Nessun vantaggio in termini di potenza

> Tutte le modalità endgame supportano **matchmaking automatico** e possono essere affrontate in solo o in gruppo premade.

---

## 6. ATTREZZATURA E PROGRESSIONE

### Sistemi
- **Inventario & Equipaggiamento**: raccoglie potenziamenti, armi, armature, accessori
- **Crafting Base**: crea oggetti utili per l'avventura dai materiali raccolti
- **Gilda & Cooperazione**: unisciti a una gilda e partecipa a eventi speciali
- **Classifiche**: scala le classifiche nelle arene e nelle sfide competitive

### Filosofia del bilanciamento

**PvE e PvP sono completamente separati.**

```
Progressione PvE:
Campagna → Dungeon → Hero Dungeon → Raid → Miglior equipaggiamento PvE

Progressione PvP:
Arena → Equip PvP → Ranked Arena → Classifiche → Ricompense estetiche

Progressione Competitiva:
Dungeon → Ranked Dungeon → Classifiche → Ricompense estetiche
```

---

## 7. CARATTERISTICHE PRINCIPALI MVP

| Feature | Descrizione |
|---------|-------------|
| **Combattimento** | Turni in tempo reale, dinamico e strategico |
| **Classi** | Abilità uniche e risorse specifiche per razza |
| **Campagna** | Storia ramificata per razza con quadri |
| **Cooperazione** | Co-op con matchmaking automatico |
| **Endgame** | Ricco e bilanciato tra PvE e PvP |

---

*Documento basato sull'infografica PetsQuest — "L'avventura ti aspetta. Insieme, siamo più forti."*
