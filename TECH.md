# PetsQuest - Note Tecniche

## Architettura Corrente

Il prototipo corrente e' un'app statica in un solo file:

- `index.html`: HTML, CSS e JavaScript inline.
- Nessun bundler.
- Nessuna dipendenza npm.
- Avvio locale: `python3 -m http.server 8080`.
- URL locale: `http://localhost:8080/index.html`.

Il layout usa una canvas logica HTML/CSS da `1640x920` scalata via `transform: scale(...)` per restare centrata nel viewport.

## Schermate

Le schermate sono sezioni `.screen` mostrate/nascoste via classe `.active`:

- `race-screen`;
- `campaign-screen`;
- `combat-screen`;
- `endgame-screen`.

La navigazione e' gestita con attributi `data-go`.

## Combat State

Lo stato combat vive nell'oggetto `combat`:

```js
{
  playerHp,
  playerMaxHp,
  enemyHp,
  enemyMaxHp,
  allyHp,
  allyMaxHp,
  rage,
  rageMax,
  mana,
  manaMax,
  energy,
  energyMax,
  potions,
  phase,
  turn,
  awaitingDirection,
  playerAction,
  enemyIntent,
  magicSequence,
  magicResults,
  magicIndex,
  magicHits,
  pendingAbility,
  timerFrame,
  timerToken,
  timerPhase
}
```

Fasi principali:

- `action`: scelta tra arma, abilita' e oggetto;
- `aim`: scelta direzione attacco arma;
- `magic`: sequenza a 4 cristalli direzionali per abilita' caster;
- `target`: scelta bersaglio per cure prototipali;
- `resolve-player`: risoluzione azione player;
- `defense`: lettura segnale nemico e scelta difesa;
- `resolve-enemy`: risoluzione attacco nemico;
- `won` / `lost`.

Le fasi interattive `action`, `aim` e `defense` usano un countdown live basato su `requestAnimationFrame`:

- `action`: 12 secondi; se scade, il player perde l'azione e parte la difesa;
- `aim`: 6 secondi; se scade, l'attacco arma manca il bersaglio;
- `defense`: 5 secondi; se scade, il nemico infligge danno pieno.
- `magic`: 8 secondi; se scade, la magia viene risolta con potenza ridotta.
- `target`: 6 secondi; se scade, la cura usa l'eroe come fallback.

## Regole Risorse

- Arma: costa Energia in base alla classe.
- Abilita': costa la risorsa definita dal profilo classe.
- Oggetto: consuma `1` pozione e cura `22 HP`.
Il prototipo usa profili classe in `classRules[*].stats`:

- `maxHp`, `energyMax`, `manaMax`, `rageMax`;
- risorse iniziali `startHp`, `startEnergy`, `startMana`, `startRage`;
- `weaponCost` e tabella direzionale `weaponDamage`;
- rigenerazione `regen.energy`, `regen.mana`, `regen.rage`;
- riduzione danno in difesa `guardRate`.

I pulsanti azione vengono disabilitati quando la risorsa richiesta non e' disponibile. Le risorse correnti vengono salvate in `playerState` e riallineate quando cambia la classe selezionata.

## Direzioni Combat

Nota importante: il nome file non e' una fonte affidabile per dedurre l'orientamento dello sprite. Prima di cambiare uno stem `idle`, `idle_left`, `attack`, `attack_left`, ecc. bisogna verificare visivamente i frame. La tabella completa e' in `SPRITE_ORIENTATION_AUDIT.md`.

Stato verificato per il cane guerriero:

- idle verso destra: `assets/sprites/main_character/idle_left/main_character_idle_left`;
- attack verso destra: `assets/sprites/main_character/attack/main_character_attack`;
- hit verso destra: `assets/sprites/main_character/hit/main_character_hit`;
- death verso destra: `assets/sprites/main_character/death/main_character_death`.

Attacco player:

- direzione bloccata dal nemico: danno `0`, feedback parata;
- direzione opposta alla guardia: danno ridotto;
- altra direzione: danno pieno.

Difesa player:

- il nemico usa pattern fisici con direzione e segnale testuale;
- la UI mostra un indizio semi-telegrafato e una freccia evidenziata;
- difesa corretta: danno ridotto;
- difesa errata: danno pieno.

Sequenza magia:

- le classi con `magicSequence: true` usano 4 input direzionali prima della risoluzione abilita';
- la sequenza usa `assets/generated_ui/endgame/matchmaking_crystal.png` e le frecce `assets/generated_ui/combat_fx/control_arrow_*`;
- ogni input corretto aumenta il moltiplicatore di danno/cura;
- timeout o input errati risolvono comunque la magia, ma con efficacia ridotta.

Cura e target:

- Paladino e Prete usano la fase `target` quando l'abilita' ha cura associata;
- la cura puo' andare su `EROE` o su un `ALLEATO` prototipale con HP separati;
- l'alleato usa asset endgame esistenti e i suoi HP sono salvati in `playerState`.

## Asset

Il prototipo legge gli asset da:

- `assets/generated_ui/`: frame UI, D-pad, FX, rewards, endgame, campaign;
- `assets/sprites/`: animazioni personaggio e nemico;
- `assets/backgrounds/`: sfondi;
- `assets/ui/`: icone risorsa e abilita';
- `assets/inventory/`: armi e pozioni.

Nel repository GitHub gli asset sorgente sono disponibili sotto `art_input/assets/`; per questo, quando si sincronizza `index.html` dal progetto locale al repo GitHub, i path `assets/...` non generati devono puntare ad `art_input/assets/...`.

## Verifica Manuale Corrente

Eseguita nel browser locale:

- caricamento senza immagini mancanti;
- nessun errore console;
- `ARMA` consuma Energia;
- `ABILITA` consuma la risorsa definita dal profilo classe;
- `OGGETTO` consuma la pozione e poi resta disabilitato;
- hit pieno, danno ridotto e parata/miss funzionano;
- difesa semi-telegrafata senza testo esplicito della direzione.
- sequenza magica, target cura e fallback timeout sono presenti come prototipo;
- selezione razza/classe aggiorna preview sprite singola e punti risorsa classe/livello.

## Roadmap Tecnica

- Separare JS/CSS da `index.html` quando il prototipo smette di essere mock/demo.
- Introdurre un piccolo state manager per combat e campagna.
- Estrarre dati bilanciamento in JSON.
- Rendere `Fede` una risorsa combat autonoma oppure definirla come label di Mana sacra.
- Collegare target cura a un party reale.
- Implementare inventario/equip ispezionabile.
- Preparazione a Vite o altro bundler solo quando serve build reale.
