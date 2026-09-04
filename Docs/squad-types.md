## Basic Squad Bitmask

BITMASKED VALUE (LSB)
0 - Artillery
1 - Shield
2 - Drop
3 - Pathfind
4 - DelayAttack
5 - Attrition
6 - PathfindBoost
7 - BodyCover
20+ - SPECIAL SQUADS


### 0 - Artillery
Leaders/Sergeants will try to stay at range and pelt targets from afar.
Meatshield units will always be the ones in front and do not actively cover the group.
PDS will stay close in front of the Artilleries and will take the hits instead.
Max 1 Squad
#### Command 1 Meatshield
    Units in Meatshield Command will put themselves in front of the Leader, but will actively engage the turrets and still pathfind towards them. ù
    Example: Dagger, Mace, Atrax, Stell
#### Command 2 Cover
    Units in Cover Command will put themselves in front of the Leader and STAY THERE, providing body cover for long ranged enemies. They'll absorb long range turrets before they hit the artillery.
    Example: Cleroi, Locus, Quasar


### 1 - Shield
Created by units that have shield emitters.
Units can join as AttackUnit (Command 1), SupportUnit (Command 2)
AttackUnit will leave the shield to attack when ordered.
SupportUnit will always try to stay inside the shield.
Max 1 Squad
#### Command 1 AttackUnit
    Units in AttackUnit command will resume normal logic when given the command, with the possibility of leaving the shield.
    Example Unit: Crawler, Atrax, Horizon
#### Command 2 SupportUnit
    Units in SupportUnit command will always try to stay inside the shield and will not leave to attack.
    Example Unit: Stell, Nova, Fortress

### 2 - Drop
Created by units that can carry Payloads.
Units can join as Interceptor (Command 1), Dropshippers (Command 2), PDS (Command 3)
The Leader will take care of pathfinding and ensuring a valid floor for dropping is found.
Dropshippers will follow closely together and drop together.
PDS Units try to always stay in front of the dropshippers.
Interceptors will actively engage units near the dropshippers.
Max 1 Squad
#### Command 1 Interceptors
    Units in Interceptor Command will actively look for UNITS to target near the leader. They will focus on Units first and foremost.
    Example: Flare, Zenith.
#### Command 2 Dropshippers
    Units in Dropshippers command will follow the leader closely and drop together. They cannot get far from the Leader.
    Example: Mega, Quad
#### Command 3
    Units in PDS command will always try to put themselves between the dropshippers and the closes turret, absorbing enemy fire.
    Example: Flare, Horizon.

### 3 - Pathfind
Created by specific unit types, usually custom via DataPack
Units can join as AttackUnit (Command 1), Interceptor (Command 2)
Leader has powerful pathfinding and target selection logic.
Units will follow leader and actively attack target.
Interceptors will actively engage units near the Leader
Every Leader creates his own squad.
#### Command 1 AttackUnit
    Units in AttackUnit command will stay with the leader and cannot go far unless ordered. When ordered, they stop following the pathfind logic and start attacking as normal.
    Example: Mace, Quasar.
#### Command 2 Interceptors
    Units in Interceptor Command will actively look for UNITS to target near the leader. They will focus on Units first and foremost.
    Example: Flare, Zenith.

### 4 - DelayAttack
Created by specific unit types, usually custom via DataPack.
Units can join as MeatShield (Command 1), AttackUnit (Command 2)
Meatshields will be sent in a staggered formation, designed to consume extra ammunition.
AttackUnit will be the last wave of units sent.
Max 1 Squad

### 5 - Attrition
Created by specific unit types, usually custom via DataPack.
Units can join as AttackUnit (Command 1), HealerUnit (Command 2), PDS (Command 3)
AttackUnits will actively try to avoid damage and retreat to repair.
HealerUnits will try to stay outside of any turret range.
PDS units will actively target enemy units that approach the squad.
Max 1 Squad

### 6 - Pathfind Boost
As Pathfind, but only boosting units can join this squad (and have preference for this)
Every Leader creates his own squad.

### 7 - BodyCover
The opposite of Artillery, a bigger units will go in first and smaller units will stay behind it for cover.
Units can join as AttackUnit (Command 1), Interceptor (Command 2)
AttackUnit will always try to stay behind Leaders.
Max 1 Squad.

### 20+ - SPECIAL SQUADS
Used for stuff like guardian logic, WorldEvents and similarly special squads. Changes depending on the map.

