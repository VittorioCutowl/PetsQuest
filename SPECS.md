# PetsQuest - Specifiche MVP e Stato Implementazione

## Gameplay Target

PetsQuest e' un RPG pixel-art con razze animali, classi fantasy e combattimento a turni in tempo reale. Il giocatore sceglie razza/classe, avanza su una campagna a quadri, combatte nemici e sblocca progressione fino alle modalita' endgame.

## Razze e Classi

| Razza | Classi previste | Risorse |
|-------|-----------------|---------|
| Cani | Guerriero, Paladino, Prete, Cacciatore | Rabbia, Fede, Energia |
| Topi | Guerriero, Ladro, Prete | Rabbia, Energia, Fede |
| Gatti | Ladro, Negromante, Mago, Prete | Energia, Mana, Fede |

## Selezione Razza e Classe

La selezione razza/classe e' una schermata giocabile, non solo visuale.

### Implementato Ora

- Le razze disponibili sono `Cani`, `Topi` e `Gatti`.
- Ogni card razza mostra un solo personaggio alla volta.
- Selezionando una classe, lo sprite preview cambia in base alla classe scelta.
- La preview usa gli sprite coerenti con la razza selezionata:
  - Cani: Guerriero, Paladino, Prete, Cacciatore;
  - Topi: Guerriero, Ladro, Prete;
  - Gatti: Ladro, Negromante, Mago, Prete.
- I punti `Rabbia`, `Energia`, `Mana` e `Fede` sotto la selezione cambiano in base alla classe e scalano con il livello corrente.
- La scelta razza/classe viene salvata in `localStorage` e propagata a campagna e combat.

### Nota Risorse Selezione

I quattro valori sotto la selezione sono una preview di identita' e crescita classe. Nel combat, al momento, le risorse operative sono `Energia`, `Mana`, `Rabbia` e `Pozioni`; `Fede` non e' ancora una barra combat autonoma.

## Combat MVP

Ogni turno combat ha una sequenza interattiva:

1. Azione player: `ARMA`, `ABILITA` o `OGGETTO`.
2. Eventuale mira direzionale per `ARMA`.
3. Eventuale sequenza magica a 4 cristalli per caster.
4. Eventuale scelta target per abilita' curative.
5. Difesa player: lettura del segnale nemico e scelta della direzione di difesa.

### Implementato Ora

- `ARMA`: attacco fisico direzionale con quattro direzioni.
- Hit/miss reale:
  - direzione bloccata: il colpo viene parato e il danno e' `0`;
  - direzione sfavorevole: danno ridotto;
  - direzione favorevole: danno pieno.
- `ABILITA`: abilita' primaria di classe con consumo risorsa.
  - classi fisiche: risoluzione immediata;
  - classi caster: sequenza magica a 4 cristalli prima della risoluzione;
  - Prete e Paladino: dopo la sequenza scelgono il target della cura.
- `OGGETTO`: pozione curativa con contatore reale.
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

### Profili Classe Prototipali

| Classe | Ruolo previsto | Risorsa abilita' attuale | Sequenza magica | Cura target |
|--------|----------------|--------------------------|-----------------|-------------|
| Guerriero | melee resistente | Rabbia | No | No |
| Paladino | ibrido tank/cura | Mana + Rabbia | Si | Si |
| Prete | healer/supporto | Mana | Si | Si |
| Cacciatore | ranged fisico | Energia | No | No |
| Ladro | fisico rapido | Energia | No | No |
| Negromante | caster oscuro | Mana | Si | No |
| Mago | caster danno | Mana | Si | No |

Nota: le regole classe sono condivise tra razze quando la stessa classe esiste su piu' razze. Per esempio Prete cane, Prete topo e Prete gatto usano lo stesso profilo numerico, ma sprite diversi.

### Ancora Da Implementare

- Sequenza magica finale per caster: ora esiste una versione prototipale a 4 cristalli, manca bilanciamento finale e varianti per abilita' multiple.
- Cura con selezione bersaglio finale: ora esiste un target prototipale eroe/alleato, manca integrazione con party reale e abilita' multiple.
- Inventario completo con piu' oggetti.
- Progressione EXP/livelli/talenti finale. Ora esiste una progressione prototipale salvata con level up e talent point.
- Mappatura finale di tutte le abilita' disponibili in UI: ora ogni classe selezionabile ha una primaria e profilo stat base, ma manca ancora un pannello abilita' completo.
- Completamento definitivo loot/equip: ora alcune ricompense entrano nello stato, ma manca inventario ispezionabile/equipaggiabile.
- Dialoghi e cutscene campagna.
- Multiplayer, matchmaking e ranking endgame.

## Ambiguita' Aperte Da Risolvere

Questi punti sono esplicitati per evitare decisioni implicite durante i prossimi blocchi.

1. `Fede` vs `Mana`
   - La UI selezione mostra `Fede`, ma il combat usa ancora `Mana` come risorsa tecnica anche per Prete/Paladino.
   - Decisione richiesta: `Fede` deve diventare una barra combat separata o restare solo una fantasy label della risorsa magica sacra?

2. Classi condivise tra razze
   - Ora una classe ha lo stesso bilanciamento numerico su ogni razza.
   - Decisione richiesta: una classe deve cambiare stat in base alla razza, oppure la razza e' solo estetica/lineup?

3. Party reale
   - La cura target usa un `ALLEATO` prototipale con HP propri, ma non esiste ancora una lista party reale.
   - Decisione richiesta: in campagna si controlla un solo eroe con alleati astratti, o un party ispezionabile con piu' membri?

4. Inventario ed equip
   - Le ricompense entrano nello stato come oro, EXP, pozioni e stringhe item, ma non esiste ancora un inventario navigabile.
   - Decisione richiesta: equip deve modificare stat combat subito o solo dopo una schermata inventario/equip?

5. Progressione classe
   - Il livello scala alcuni valori preview e il prototipo assegna talent point, ma non esiste ancora un albero talenti.
   - Decisione richiesta: i talenti sbloccano abilita', modificatori passivi o entrambi?

6. Sequenza magica
   - La sequenza a 4 cristalli e' unica e deterministica per turno/classe.
   - Decisione richiesta: ogni abilita' caster deve avere pattern propri, pattern casuali o pattern leggibili da icone?

7. Direzioni combat
   - Arma e difesa usano direzioni con regole prototipali di guardia, opposto e danno pieno.
   - Decisione richiesta: queste direzioni rappresentano lato fisico del bersaglio, timing, lane/posizione o semplicemente minigame input?

8. Endgame
   - Hub endgame e modalita' esistono visivamente, ma senza gameplay.
   - Decisione richiesta: quale modalita' endgame deve diventare giocabile per prima: Hero Dungeon, Raid, Ranked o Arena?

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
