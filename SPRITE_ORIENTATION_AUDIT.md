# PetsQuest - Sprite Orientation Audit

Audit visivo eseguito sui primi frame PNG. Regola importante: il nome della cartella non e' sufficiente per capire l'orientamento; usare questa tabella come riferimento operativo.

## Giocabili - Idle

I giocabili stanno a sinistra nel combat e devono guardare verso destra.

| Personaggio | Verso destra | Verso sinistra | Note |
|-------------|--------------|----------------|------|
| `main_character` | `idle_left` | `idle` | Eccezione: idle invertito rispetto agli altri giocabili |
| `dog_paladin` | `idle` | `idle_left` | Verificato visivamente |
| `dog_priest` | `idle` | `idle_left` | Verificato visivamente |
| `dog_hunter` | `idle` | `idle_left` | Verificato visivamente |
| `mouse_warrior` | `idle` | `idle_left` | Verificato visivamente |
| `mouse_thief` | `idle` | `idle_left` | Verificato visivamente |
| `mouse_priest` | `idle` | `idle_left` | Verificato visivamente |
| `cat_thief` | `idle` | `idle_left` | Verificato visivamente |
| `cat_necromancer` | `idle` | `idle_left` | Verificato visivamente |
| `cat_mage` | `idle` | `idle_left` | Verificato visivamente |
| `cat_priest` | `idle` | `idle_left` | Verificato visivamente |

## Protagonista - Animazioni Combat

Il protagonista usa un mix non deducibile dal nome:

| Animazione | Verso destra | Verso sinistra |
|------------|--------------|----------------|
| Idle | `idle_left` | `idle` |
| Attack | `attack` | `attack_left` |
| Hit | `hit` | `hit_left` |
| Death | `death` | `death_left` |

## Scheletro Nemico

Lo scheletro sta a destra nel combat e deve guardare verso sinistra.

| Animazione | Verso sinistra | Verso destra |
|------------|----------------|--------------|
| Idle | `idle` | `idle_left` |
| Attack | `attack` | `attack_left` |
| Hit | `hit` | `hit_left` |
| Death | `death` | `death_left` |

## Regola Operativa

Prima di cambiare uno stem sprite nel codice:

1. aprire il primo frame dell'animazione;
2. verificare dove guarda il personaggio;
3. aggiornare il codice solo dopo la verifica visiva;
4. non dedurre mai l'orientamento dal suffisso `_left`.
