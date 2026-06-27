# PetsQuest

PetsQuest e' un giochino RPG alla giapponese con visuale isometrica, ispirato alla leggibilita' dei classici action RPG in stile Zelda. Lo stile visivo dei personaggi e' chibi fantasy, caldo, pulito e leggibile anche in piccolo.

## Stato Implementazione Prototipo

Entry point corrente: `index.html`, prototipo statico HTML/CSS/JS senza build step.

Schermate principali implementate:

- Selezione razza/classe con card Cani, Topi e Gatti.
- Mappa campagna con nodi cliccabili e accesso al combat da combattimento/miniboss/boss.
- Combat screen con sfondo, HUD, sprite animati, pannello risorse e azioni.
- Endgame hub con modalita' Hero Dungeon, Raid, Ranked e Arena.

Gameplay combat implementato:

- Loop a turni: scelta azione -> eventuale direzione attacco -> difesa -> turno successivo.
- `ARMA`: consuma `12 Energia`, richiede direzione e puo' fare colpo pieno, danno ridotto o miss/parata.
- `ABILITA`: consuma `18 Mana`, oppure `24 Rabbia` se il Mana non basta, e infligge danno garantito.
- `OGGETTO`: consuma una pozione reale (`x1 -> x0`) e cura il personaggio.
- Risorse reali: Rabbia, Mana ed Energia hanno valori numerici, segmenti visivi e rigenerazione a ogni nuovo turno.
- Difesa semi-telegrafata: il nemico non mostra piu' un testo esplicito tipo "difendi destra", ma un segnale leggibile e una direzione evidenziata sul D-pad.
- Stati vittoria/sconfitta con animazioni death e feedback ricompensa.

Verifica locale eseguita:

- Consumo energia, mana/rabbia e pozione.
- Danno pieno, danno ridotto e parata/miss.
- Disabilitazione pulsanti quando un'azione non e' disponibile.
- Nessuna immagine mancante e nessun errore console nel browser locale.

Prossimi punti gameplay:

- Sequenza magica a 4 punti per caster.
- Selezione bersaglio cura per Prete/Paladino.
- Ricompense reali e progressione dopo la vittoria.
- Persistenza scelta razza/classe tra selezione, campagna e combat.
- Bilanciamento numerico finale per classi, nemici e progressione.

## Direzione Sprite

- I personaggi sono animali fantasy antropomorfi, con proporzioni chibi, silhouette chiara e dettagli leggibili.
- Il personaggio principale parte da un cane avventuriero: pelo marrone e crema, occhi espressivi, mantello corto, tunica in pelle, cintura, piccola spada e scudo tondo.
- La vista base e' isometrica 3/4, con il personaggio orientato verso down-right.
- Lo stile deve restare coerente con il riferimento principale di PetsQuest: pixel-art ispirata, bordi puliti, fantasy giapponese, colori caldi e accessori leggibili.

## Regole Di Output

- Ogni keyframe deve essere consegnato come PNG singolo, non solo come sprite sheet.
- Tutti i PNG della stessa animazione devono avere esattamente le stesse dimensioni del quadro/canvas.
- Il personaggio deve essere sempre centrato nello stesso punto del canvas.
- I file devono essere scontornati: PNG RGBA con sfondo trasparente.
- Non usare ombre portate, sfondi, numeri, griglie, testo o watermark negli sprite finali.
- Se si genera su chroma-key, conservare opzionalmente la sorgente `_chromakey.png`, ma il file finale deve essere trasparente.

## Convenzione Direzioni Combat

- Tutti i personaggi giocabili, quindi cani, gatti e topi, stanno a sinistra e puntano verso destra.
- Per i giocabili, la direzione principale senza suffisso deve muoversi/attaccare da sinistra verso destra.
- Scheletro nemico: la direzione principale senza suffisso deve muoversi/attaccare da destra verso sinistra.
- Le varianti `_left` sono le versioni specchiate della rispettiva direzione principale e vanno usate solo quando serve il verso opposto.
- Prima di generare nuove animazioni di combat, controllare che i due lati si guardino: giocabili verso destra, nemici verso sinistra.

## Naming

Usare questa struttura:

```text
assets/sprites/<character>/<animation>/<character>_<animation>_<frame>.png
```

Esempio:

```text
assets/sprites/main_character/idle/main_character_idle_01.png
assets/sprites/main_character/idle/main_character_idle_02.png
```

## Asset Prodotti Localmente

- `assets/style/petsquest-main-board.jpeg`: tavola principale di stile da tenere in git.
- `assets/sprites/`: personaggi, nemici e animazioni.
- `assets/backgrounds/battle/`: sfondi battaglia campagna `820x400`.
- `assets/campaign/`: tile percorso, icone evento e mappe campagna.
- `assets/ui/`: HP bar, risorse, abilita' e cornici bottoni.
- `assets/inventory/`: pozioni, armi, equipaggiamento, accessori e loot.
- `assets/endgame/`: sfondi endgame e icone rank.
- `assets/generated_ui/`: pacchetto UI generato per schermate principali, documentato in `GENERATED_UI_ASSETS.md`.

Nota path repository GitHub: nel progetto locale il prototipo usa `assets/...`; nel repository GitHub molte sorgenti artistiche sono raccolte sotto `art_input/assets/...`. Per questo, l'`index.html` sincronizzato sul repo GitHub usa `art_input/assets/...` per sprite, sfondi, inventario e UI sorgente, mantenendo `assets/generated_ui/...` per il pacchetto UI versionato.

Gli asset generati sotto `assets/sprites/`, `assets/backgrounds/`, `assets/campaign/`, `assets/ui/`, `assets/inventory/` e `assets/endgame/` sono deliverable locali e non vanno versionati tutti su git, salvo scelta esplicita. Il pacchetto `assets/generated_ui/` e' stato invece selezionato per essere versionato come set UI riutilizzabile. Git deve contenere solo la documentazione, gli strumenti, gli asset principali di stile/riferimento e i pacchetti esplicitamente selezionati.

## Pacchetti Asset

### Combat Demo

- `main_character`: `idle`, `idle_left`, `attack`, `attack_left`, `hit`, `hit_left`, `death`, `death_left`.
- `enemy_skeleton`: `idle`, `idle_left`, `attack`, `attack_left`, `hit`, `hit_left`, `death`, `death_left`.
- Formato frame personaggi: PNG `RGBA`, `362x724`, 6 frame per animazione.

### Character Selection

Solo `idle` e `idle_left`, 6 frame per set:

- Cani: `dog_paladin`, `dog_priest`, `dog_hunter`.
- Gatti: `cat_thief`, `cat_necromancer`, `cat_mage`, `cat_priest`.
- Topi: `mouse_warrior`, `mouse_thief`, `mouse_priest`.

### Campagna

- Battle background `820x400`: foresta notturna cani, citta' in rovina topi, dungeon/castello gatti, arena PvP.
- Tile percorso `256x256` trasparenti: normale, miniboss, boss finale, checkpoint.
- Icone evento `192x192` trasparenti: combattimento, tesoro, riposo, negozio.
- Mappe campagna `1024x1024`: cani, topi, gatti.

### UI, Inventario, Endgame

- UI: frame HP bar, risorse Rabbia/Energia/Mana/Fede, 16 icone abilita', bottoni panel `normal`, `hover`, `pressed`.
- Inventario: pozioni HP/MP/buff, armi, armature, accessori, loot comune/raro/epico.
- Endgame: sfondi Hero Dungeon, Raid, Ranked PvP Arena; rank bronzo, argento, oro, platino, diamante.

### Generated UI Pack

- `assets/generated_ui/`: 88 PNG trasparenti per schermate selezione, campagna, combat, ricompense ed endgame.
- `assets/generated_ui/_generated_ui_contact_sheet.png`: anteprima completa del pacchetto.
- `GENERATED_UI_ASSETS.md`: lista esatta dei file e uso previsto per categoria.

## File Versionati

Questa repository versiona:

- `index.html`: prototipo giocabile statico con UI e combat loop corrente.
- `README.md`: direzione artistica, convenzioni e inventario asset.
- `.gitignore`: regole per tenere fuori gli asset generati massivi.
- `assets/style/petsquest-main-board.jpeg`: tavola principale di stile.
- `assets/generated_ui/`: pacchetto UI generato e selezionato per il gioco.
- `GENERATED_UI_ASSETS.md`: manifest del pacchetto UI generato.
- `tools/process_generated_sprite.py`: helper per scontornare, dividere, centrare e specchiare sprite sheet.
- `tools/process_latest_image_asset.py`: helper per normalizzare sfondi, sheet icone e asset generati.

Gli altri asset PNG generati restano nella workspace locale e sono esclusi da git.

## Workflow Consigliato

1. Generare i keyframe su sfondo chroma-key piatto `#00ff00`, evitando quel colore nel personaggio.
2. Rimuovere il chroma-key e produrre PNG RGBA trasparenti.
3. Dividere la sheet in frame singoli.
4. Ricentrare ogni frame su canvas identico.
5. Verificare dimensioni, canale alpha, angoli trasparenti e centro del bounding box.

Per lavori futuri usare la skill personale `petsquest-character-sprites`.
