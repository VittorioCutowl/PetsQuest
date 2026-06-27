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
- Profili classe prototipali:
  - HP massimi, Energia, Mana e Rabbia massimi cambiano per classe;
  - costo e danno arma cambiano per classe;
  - rigenerazione turno e riduzione difesa cambiano per classe;
  - risorse correnti vengono salvate e ricalcolate al cambio classe.
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
- Combat timing reale:
  - countdown live per scelta azione, mira e difesa;
  - azione non scelta: turno perso e passaggio alla difesa;
  - direzione attacco non scelta: colpo mancato;
  - difesa non scelta: danno pieno dal nemico.
- Sequenza magica prototipale:
  - Paladino, Prete, Negromante e Mago risolvono `ABILITA` con 4 cristalli direzionali;
  - input corretti aumentano danno e cura;
  - timeout o errori producono una magia piu' debole.
- Cura con target prototipale:
  - Paladino e Prete scelgono il bersaglio dopo la sequenza magica;
  - `EROE` cura il player, `ALLEATO` cura un compagno prototipale con HP propri;
  - timeout sulla scelta target applica fallback sull'eroe.

### Ancora Da Implementare

- Sequenza magica finale per caster: ora esiste una versione prototipale a 4 cristalli, manca bilanciamento finale e varianti per abilita' multiple.
- Cura con selezione bersaglio finale: ora esiste un target prototipale eroe/alleato, manca integrazione con party reale e abilita' multiple.
- Inventario completo con piu' oggetti.
- Progressione EXP/livelli/talenti finale. Ora esiste una progressione prototipale salvata con level up e talent point.
- Mappatura finale di tutte le abilita' disponibili in UI: ora ogni classe selezionabile ha una primaria e profilo stat base, ma manca ancora un pannello abilita' completo.
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
