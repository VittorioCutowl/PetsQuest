# PetsQuest - Specifiche MVP e Stato Implementazione

## Gameplay Target

PetsQuest e' un RPG pixel-art con razze animali, classi fantasy e combattimento a turni in tempo reale. Il giocatore sceglie razza/classe, avanza su una campagna a quadri, combatte nemici e sblocca progressione fino alle modalita' endgame.

## Razze e Classi

| Razza | Classi previste | Risorse |
|-------|-----------------|---------|
| Cani | Guerriero, Paladino, Prete, Cacciatore | Rabbia, Fede, Energia |
| Topi | Guerriero, Ladro, Prete | Rabbia, Energia, Fede |
| Gatti | Ladro, Negromante, Mago, Prete | Energia, Mana, Fede |

## Combat MVP

Ogni turno ha due fasi:

1. Azione player: `ARMA`, `ABILITA` o `OGGETTO`.
2. Difesa player: lettura del segnale nemico e scelta della direzione di difesa.

### Implementato Ora

- `ARMA`: attacco fisico direzionale con quattro direzioni.
- Hit/miss reale:
  - direzione bloccata: il colpo viene parato e il danno e' `0`;
  - direzione sfavorevole: danno ridotto;
  - direzione favorevole: danno pieno.
- `ABILITA`: danno garantito con consumo risorsa.
- `OGGETTO`: pozione curativa con contatore reale.
- Difesa semi-telegrafata:
  - niente testo esplicito "difendi destra";
  - indizio leggibile nel pannello azione;
  - D-pad evidenziato in modalita' difesa.
- Risorse reali:
  - Energia: usata dall'arma, rigenera a ogni turno;
  - Mana: usato dall'abilita';
  - Rabbia: risorsa alternativa per abilita' quando il Mana non basta;
  - Pozioni: consumabili finite.
- Stati vittoria/sconfitta con animazioni e feedback ricompensa.

### Ancora Da Implementare

- Sequenza magica a 4 punti per caster.
- Cura con selezione bersaglio per Prete/Paladino.
- Inventario completo con piu' oggetti.
- Loot reale post-combat e aggiornamento progressione.
- Persistenza scelta razza/classe nelle schermate successive.
- Progressione EXP/livelli/talenti.
- Dialoghi e cutscene campagna.
- Multiplayer, matchmaking e ranking endgame.

## Campagna

La campagna e' strutturata a quadri con nodi:

- combattimento;
- tesoro;
- riposo;
- negozio;
- miniboss;
- boss finale.

Nel prototipo la mappa e' navigabile visivamente e i nodi di combattimento aprono la schermata combat.

## Endgame

Modalita' previste:

- Hero Dungeon;
- Raid;
- Ranked;
- Arena;
- Stagioni competitive;
- Party e ruoli.

Nel prototipo e' implementato l'hub visuale endgame, senza gameplay endgame reale.
