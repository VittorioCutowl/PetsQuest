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
- Persistenza scelta razza/classe via `localStorage`, propagata tra selezione, campagna e combat.
- Mappatura abilita' per classe: icone, nome abilita', arma, costo risorsa e danno cambiano in base alla classe selezionata.
- Loot/progressione prototipale:
  - oro, EXP, talent point e pozioni vengono aggiornati nello stato player;
  - vittoria combat assegna ricompense reali del nodo selezionato;
  - nodi non-combat base come Quadro/Riposo/Tesoro/Negozio applicano reward/recupero direttamente dalla campagna.
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
- Cura con selezione bersaglio per Prete/Paladino. Ora esiste solo una cura self semplificata su abilita' dedicate.
- Inventario completo con piu' oggetti.
- Progressione EXP/livelli/talenti finale. Ora esiste una progressione prototipale salvata con level up e talent point.
- Mappatura finale di tutte le abilita' disponibili in UI: ora ogni classe selezionabile ha una primaria, ma manca ancora un pannello abilita' completo.
- Completamento definitivo loot/equip: ora alcune ricompense entrano nello stato, ma manca inventario ispezionabile/equipaggiabile.
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
