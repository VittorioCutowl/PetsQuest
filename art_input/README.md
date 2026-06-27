# PetsQuest

PetsQuest e' un giochino RPG alla giapponese con visuale isometrica, ispirato alla leggibilita' dei classici action RPG in stile Zelda. Lo stile visivo dei personaggi e' chibi fantasy, caldo, pulito e leggibile anche in piccolo.

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

## Asset Creati

- `assets/style/petsquest-main-board.jpeg`: tavola principale di stile da tenere in git.
- `assets/sprites/main_character/main_character_idle_sheet_chromakey.png`: sorgente generata con chroma-key.
- `assets/sprites/main_character/main_character_idle_sheet.png`: sprite sheet trasparente.
- `assets/sprites/main_character/idle/main_character_idle_01.png` ... `main_character_idle_06.png`: frame IDLE separati, trasparenti, con canvas uniforme `362x724`.

Gli sprite generati sotto `assets/sprites/` sono deliverable locali e non vanno versionati tutti su git, salvo scelta esplicita. Git deve contenere solo la documentazione, gli strumenti e gli asset principali di stile/riferimento.

## Workflow Consigliato

1. Generare i keyframe su sfondo chroma-key piatto `#00ff00`, evitando quel colore nel personaggio.
2. Rimuovere il chroma-key e produrre PNG RGBA trasparenti.
3. Dividere la sheet in frame singoli.
4. Ricentrare ogni frame su canvas identico.
5. Verificare dimensioni, canale alpha, angoli trasparenti e centro del bounding box.

Per lavori futuri usare la skill personale `petsquest-character-sprites`.
