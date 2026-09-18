## Squad Definitions

Squads Active:
1. ArtillerySquad (ID 1)
2. FrontAttackSquad (ID 2)
3. AttritionSquad (ID 3)
4. DropshipSquad (ID 4)
5. PathfindBoostSquad (ID 5)
6. DelayAttackSquad (ID 6)
7. BodyCoverSquad (ID 7)
20. Midboss (ID 20)
21. Endboss (ID 21)


## Unit Definitions
### Dagger
    Cannot lead
    Can Join: 1, 2, 6
    1 -> Meatshield
    2 -> Meatshield
    6 -> Meatshield

    Always OBAI

### Mace
    Can Lead: 2
    Can Join: 2, 6
    6 -> AttackUnit

    Easy -> KAI

### Fortress
    Can Lead: 1
    Can Join: 1
    1 -> ArtilleryUnit

    Always OBAI

### Sceptre
    Can Lead: 3
    Can Join: 3, 1

    1 -> ArtilleryUnit
    3 -> AttritionUnit

    Medium -> KAI

-----

### Nova
    Cannot lead:
    Can join: 1, 5

    1 -> Meatshield
    5 -> AttackUnit

    Always OBAI

### Pulsar
    Can Lead: 5
    Can Join: 5

    Always Creates new Squad

    Easy -> KAI

### Quasar
    Cannot Lead
    Can Join: 4, 5, 2

    4 -> ShieldUnit
    5 -> AttackUnit
    2 -> ShieldUnit

    Always OBAI

### Vela
    Can Lead: 3
    Can Join: 3

    As HealerUnit

    _IS GUARDIAN?_

-----

### Crawler
    Cannot Lead
    Can Join: 2, 6

    2 -> AttackUnit
    6 -> Meatshield

    Easy -> KAI

### Atrax
    Cannot Lead
    Can Join: 2, 3

    2 -> AttackUnit
    3 -> AttackUnit

    Always OBAI

### Spiroct
    Can Lead: 3
    Can Join: 3, 6

    3 -> AttackUnit
    6 -> AttackUnit

    Always OBAI

-----

### Flare
    Cannot Lead
    Can Join: 1, 3, 4, 5

    Always as InterceptorUnit
    
    Easy -> KAI

### Horizon
    ALWAYS VAI

### Zenith
    Cannot Lead
    Can Join: 1, 3, 4, 5

    Always as InterceptorUnit
    
    Medium -> KAI

-----

### Mega
    Can Lead: 4
    Can Join: 4

    Always as DropshipUnit

    Always OBAI

-----

### Stell
    Cannot Lead
    Can Join: 2, 3

    2 -> MeatshieldUnit
    3 -> AttackUnit

    Easy -> KAI

### Locus
    Can Lead: 3
    Can Join: 3

    3 -> AttackUnit

    Medium -> KAI

### Merui
    Cannot Lead

    Can join: 1, 6

    1 as Meatshield
    6 as Meatshield

    Easy -> KAI

-----

### Cleroi
    Cannot Lead

    Can join: 1

    1 as PDS

    Medium -> KAI

### Anthicus

    Can lead 1
    Can join 1

    1 as ArtilleryUnit

    Easy -> KAI

    