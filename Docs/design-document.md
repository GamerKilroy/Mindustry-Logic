## KLR-AI-EXPANDED DESIGN DOCUMENT

1. Goals and considerations
    a. The Different Levels of AI
    b. The Units
    c. The Squads
2. The OpenBus - Async Atomic Memory Map
    a. The RAMProcs & ROMProcs
    b. The RAMACCESS Processor
    c. Dynamic Memory Allocation
    d. Garbage Collection
3. The Unit Modules
4. The Squad Modules
    a. How a squad is made
    b. What are the goals of squads
5. The Gamemaster
6. World Events
7. General Unit Overview
8. General Squad Overview


### 1. Goals and considerations.
The main goal is to use Content Packs, Data Packs and World Processors to provide an enriched Survival experience with improved enemy AIs. unit collaboration and new tactics.

The first attempt involved using only simple world processors and memory cells to share data between the units. However, the INT only limitation quickly proved it the wrong way to go. It's a great way for units to manage themselves, but when it comes to managing squads, the available tools proved lacking.

The need to share entire unit, building or complex waypoint data necessitates a more complex way to store data, ideally in a completely asyncronous and multithreadable system.
This is where the KLR-OpenBus system comes in. By using wProcessor's capability to house 6k arbitrary variables and writing/reading to remote processors, we can use a series of wProcs properly programmed to act as a Open Bus.

We now have an easy way to store any amount of data we wish, we no type limitation. Sure, this includes an execution time penalty due to the extra operations needed to write/read to memory, but due to multiple processors being able to read/write at the same time, the problem can be solved with intelligent design.

#### a. The Different Levels of AI
When originally creating the system, it relied on an advanced targetting and pathfinding logic relying on local ulocate and uradar commands. While it works great for simpler units, more advanced groups require more attention. This is where the AI has been subdiveded in 3 categories:
- The Vanilla AI (VAI)
- The klr-pathfind AI (KAI)
- The OpenBus AI (OBAI)

The Vanilla AI, VAI for short, is Vanilla. No wProcessor that manages that unit type exists. That doesn't mean the unit is fully Vanilla, it could easily come from a DataPack. However, it still uses Vanilla Mindustry AI logic.

The klr-pathfind AI, KAI for short, is the base version of advanced AIs. A wProcessor exists for this unit type, but either the OpenBus system is not active, or the unit's logic has been deactived via configuration. 
This level of AI is still an improvement over default AI, and usually written on a unit-to-unit basis. It's not complex and doesn't allow coordination with other units, but several unit types do not need heavy coordination anyway. Preffered for anything that doesn't want to subrscibe to the Squad system.

The OpenBus AI, OBAI for short, is the max level of intelligence a Unit can ask for. When a unit is initially bound and is allowed to allocate memory, it will request it's manager for 16 variables of RAM.
By using the RAM space the unit now has available it is able to calculate complex waypoints, remember units and formation, track enemy turret positions and the state of it's own logic.
Most of the OBAIs are designed to work in tandem via the Squad System. More on that below.

#### b. The Units
While some of the units will be vanilla, most are not. Units are added via the Content Pack / Data Pack system, by remixing Vanilla content into personalized enemies and bosses for KLR maps.
The DP system also allows for duplication of unit data, so we can have identical units subscribing to wholly different AIs.

When first spawned and bound, a unit looks for OpenBus availability on the map (marked by a specific flag set on the core). If the OpenBus is found, the unit will now check the Logic Enabled table to see if it's type shows up. If it doesn't (or OpenBus is not found), it will mark itself as a klr-pathfind target and start working with that logic.

If instead the Unit sees it's enabled for advanced logic in the OpenBus, it will proceed to request RAM to the memory space and save it's own reference there first and foremost. It will then proceed on a completely different branch of logic, flagging it's own address to always have access to the space.

After the unit has been mapped properly (and it has run all of the necessary setups) it will proceed to either create/check for a Squad, or start working alone with even more advanced pathfinding and target selection than the default klr-pathfinding logic.

#### c. The Squads
Unit Coordination works on a Squad System. Some units can create squads, while other can join squads.

Squads have types, which are ways to group what the goal of the squad is. Example Squad are Meatshield Squads (Smallers units being cannon fodder for more important units) - Pathfinding Squads (Using a unit's advanced pathfinding to allow other units to follow) - Active Cover squads (A unit asks for interceptor/anti-unit cover)

A Squad Manager is a wProc dedicated to a squad type that will run all maintenance and join requests for that type of squad.

When a Leader (A unit that can create a squad) spawns and gets it's RAM allocation, it will check into the squad list if a Squad of it's correct type exists. If it does, it will append to that as a co-leader. Otherwise, it will create one. Some units cannot co-lead and will always create a new squad if possible.

Every second, Soldiers (A unit that can join a squad) will check for available squads to join. If one is found, it will request that Squad type Manager for a request to join. If the join was successful, the unit will now work with the Leader's order instead of its default OBAI/KAI logic.

### 2. The OpenBus - Async Atomic Memory Map
The OpenBus system is the core of all OBAI units in the map. It's a completely asyncronous, atomic memory space that provides random memory access to any address in a fast and easily-synchonizable manner.
It works on a base design by user 6f6626 & 1ue999 from the Mindustry Discord, modified to better suit my needs (multiple asyncronous access points and background processes)
Due to the ability of wProcs to hold 6k arbitrary variables and Mindustry's innate ability to Lookup names from the block list, it is possible to create a processor that holds those 6000 variables and a way to reliably access and index those variables via the assistance of a ROM lookup.
It works very similarly to real life RAM, except made out of completely different parts.
The OpenBus system is designed to work with up to 261 Memory wProcessors, maxing out at around 1.5 million available variables in the memory space. However, this is more often than not overkill - 18k variables have proven plenty for all uses.

#### a. The RAMProcs & ROMProcs

The core of the system are 2 types of World Processors: The RAM processors and the ROM processors.

The RAM processors are nothing but a massive array of "draw triangle" operations, compiled via a Python Script (Thanks 6f6626!) to have a defined and guaranteed list of names.
The ROM processors are a list of "set var" operations, where the name of every block in mindustry (Sorted ascending by ID) is paired to a value corresponding to the list made above for RAM, variable to variable.

Basically, if the variable number 33 in the RAMproc is called "potato", in the ROMprocessor Block ID 33 you will find the value "potato".
Same for all other variable numbers in memory. To save all 6k possible variable names from a RAMprocessor, a total of 23 ROM processors are needed. Each cover 261 possible variable names, so 23 cover all possible names for a single RAMprocessor.

During Lookup, a Processor can divide the address by 6000 to obtain the number of the RAMprocessor, module by 6000 to obtain the location.
By then diving the location by 261 again, we know which ROMprocessor holds that specific variable name.
Get the Modulo of the location by 261, and you'll find the ID number of the block that contains that variable in ROM.

By reading the obtained variable name from the calculated RAMprocessor number, you will obtain exactly the value you wish.

#### b. The RAMACCESS Processor.
Writing and reading to memory directly is slow and code-heavy, and as such it won't be a good idea to fit all of the necessary functions directly on a Unit.
As such, the RAMACCESS processor was born. The RAMACCESS processor has utility function for reading, writing, lookup, clear, malloc and many more. It has a Busy flag to avoid requests overlapping each other.
The RAMACCESS processors in the main way all other modules access the memory banks. A single RAMACCESS can manage a few modules, but particularly heavy processors may have a dedicated RAMACCESS processor to cooperate with RAM better.

ALL RAMACCESS processors are always connected to a singular, unique MEMPOINTER cell. The MEMPOINTER cell always keep the current reference for the first free spot in the Unit or Squad list updated.
Since Dynamic Memory allocation exists, all RAMACCESS processors have to ensure they are not overwriting each other's data in memory. As such, before any write operation in RAM is performed, the current pointer will be read and then immediately set (even before writing!) to ensure that all wProcessors running Dynamic Memory Allocation will be in sync when it comes to which resources are for what units.

The MEMPOINTER holds little data:
The first data cell is the "UnitReady" flag. If this is false, then the processor is not ready to allocate memory.
Then you have the "UnitPointer", which is the pointer to the current HEAD in memory for Unit allocation.
The data is then repeated for the "SquadReady" and "SquadPointer" fields, but for squads instead.

Data further down is used for Squad lookups, which is much faster than ram. More details regarding that in the "4. The Squad Modules" section.

#### c. Dynamic Memory Allocation
Units and Squads have the ability to ask for Memory Allocation. By requesting their RAMACCESS processor for a malloc, they will receive back the base address of their own memory space.

Said memory space is provided by having a predefined size and start position in memory space. When a unit asks for memory allocation, the wProc will check for MEMPOINTER readyness and, if ready, start using it. It will immediately set the ready flag to false, read the unit pointer, write it back updated and then free to MEMPOINTER cell. Only after this is done it will proceed with proper memory allocation for the unit/squad.

The memory space is predefined at 16 vars for Units and 128 vars for Squads. In the code, Constants define both the length and the start of the memory space used for Dynamic allocation.
Between each wave, the MEMPOINTER is reset to it's default values, allowing the table to be filled from the start again.
At default configuration, the OPENBUS can manage up to 128 OBAI units and up to 32 OBAI squads.

#### d. Garbage Collection
Due to the asyncronous nature of unit command, it is highly likely that some OBAI units may die without their wProc being notified (for instance, currently bound to a different unit). As such, the memory space will get dirty with stale references to units or squads.

Due to units needing to lookup both the Unit Dynamic Space and the Squad Dynamic Space, a system of garbage collectors is needed. There are 2 garbage collectors of OBAI units - One for Units and one for Squads.

The Unit GC will keep scanning the Unit Dynamic Space, looking at all heads (populated or not!). Since Heads are always a Unique Unit Reference, the GC will try binding to that unit. When a NULL reference is returned (or sensor @unit @dead == true), the GC knows the unit is no longer alive and, as such, will clean that memory space by removing HEAD.

The Squad GC works in a similar way, but instead of checking for singular units, it will check for all units present in the Leaders list. For each leader, try to bind as for the unit garbage collector. If failed, remove the unit from the squad. When there are 0 leaders left, disband the squad.

### 3. The Unit Modules
Unit Command is divided in modules, each managing a specific unit type. A module always has a RAMACCESS processor linked to it as processor1.
Several Unit Modules may share the same RAMACCESS, albeit consideration for use time is to be accounted for (Do not use the same RAMACCESS for 100 units!)

The Unit Module itself is just a wProcessor that binds to a specific unit type on a loop. The Unit Module manages ALL units of the same type, and decides whether the linked type is VAI, KAI, or OBAI.

The Unit Module is composed mainly of 3 parts.
1. The Memory Check
2. The KAI
3. The OBAI

The Memory Check is the code that controls for the existance of OBAI networks. If OBAI is found, the unit will then check if OBAI is enabled for that type. If OBAI is enabled, then use the OBAI code block. Otherwise, if OBAI is not available or this logic module is marked as not OBAI, then KAI will be used.

VAI is only used IF AND ONLY IF no logic module is installed at all. Even without OBAI, the Unit Module will still run KAI logic on the unit!
If you wish to have both VAI and KAI (Or even all 3 types) units of the same type, you will have to create a fake duplicate via Content Pack.

The Unit Module never accesses OB memory space directly. Every Unit Module relies on it's linked RAMACCESS processor, leaving more lines of code and IPT available for unit control and movement.

Unit modules are the main way to add a specific custom logic to the Map. All Units are always managed by their own wProcessors, even when they are part of a squad. As such, in the Unit Module you will find all information regarding pathfinding, target weights, movement logics, squad coordination and many more. Most of this information will be saved in RAM for easy access from the other Unit Modules (or Squad Modules).

### 4. The Squad Modules
Similarly to a Unit Module, a Squad Module manages specific Squad types. As above, it has it's own RAMACCESS processor1 that can be shared between multiple Squad Modules.

The Squad Module will be contacted by a Leader, requesting to create a squad. When this happens, the Squad Manager will ask RAMACCESS to allocate the squad memory, receives back a Squad ADDR in memory, and provides it to the units.

The Squad Modules all have access to the MEMPOINTER cell directly, as it is used for Squad Lookups. WMEM access is strong, but slow. Since a lot of units may need to check for squad availability every single second, reading directly from a memory cell provides a fast way to check if squads at least exist.

The Squad Modules are composed mainly of 2 parts:
1. The Squadmaking system
2. The Squad Calculations

The Squadmaking system is responsible for taking in all create squad or join squad requests for that type of squad. It will allocate the necessary memory to create a squad, as well as appending members that ask to join a squad to their relevant leaders.
The Squadmaking system knows how many squads of each type are available. As such, Soldiers will be properly sorted out into their relevant squads, allowing better unit cohesion.

The Squad Calculations are repeated for the units in squad, depending on the logic. The results will be made available for everyone in the Squad memory area. It's mostly used for target selection, order sharing such as boost or coordinated fire, and Waypoint navigation.

Squad Disbanding never happens naturally: Once a unit is a part of the squad it remains part of it. The GC will eventually find all leaders as dead and mark the squad as inactive, prompting all units to return to base OBAI or KAI logic. 

#### a. How a squad is made
Squads are composed of 3 main components:
- The Leader
- The Sergeants
- The Soldiers

The Leader is the one calling the shots. There is always, only one leader in a Squad. If the leader dies, then the first available Sergeant becomes the new Leader
The Sergeants are other leaders that did not create a squad because one exists already. They are placed into a special Sergeant List and will become new leaders as needed due to the squad thinning out.
The Soldiers are all the other units in the squad. They possess no capabilities of leadership and will simply follow orders. A Soldier can never become a Leader nor a Sergeant.

The first unit to create the squad become the Leader by default. It will immediately start processing squad information.
Every other leader that tries to create the same type of squad (with some exceptions) will be put into the Sergeant list instead.

Soldiers will look for available squads at RAM allocation and every second. This way, soldiers that are left without a valid squad will try to look for a new one to join.

#### b. What are the goals of Squads
Squads are a way to provide advanced unit cooperation without relying on manually deciding logic for each possible combination.
Due to squads being dynamically created, they can also contain completely different units every single wave, leading to completely different logic.

For instance, Crawlers can join either a Meatshield Squad, a Shield Assault Squad, or a Wait Aggro squad.
If a Quasar is present (Shield Assault Squad), it will use the Quasar's shield to make those Crawlers more likely to reach the walls.
If a Fortress is present (Meatshield Squad), it will use the Crawlers as a body shield while shooting your turrets from afar.
If a Sceptre is present (Wait Aggro Squad), the crawlers will wait for the Sceptre to take damage before rushing in from the second line.

Many more of those interactions can be programmed, and will natively happen as the waves mix and match their units depending on spawn.
The important part is keeping Squads for one goal and one goal only - This makes it possible to pre-set which units will behave in a particular way depending on squad type.

The Squad Management should be the most interesting part of the maps, as it will vary enemy tactics in an always dynamic manner - A way that even the map creator may be unable to properly predict.

### 5. The Gamemaster
The Gamemaster is the main world processor that makes the game run smoothly. Not only it's the initializer for all kinds of configuration (For instance, RAM init from ROM), but it's also the system to keep track of waves and game progression.

The Gamemaster is always active on game start, and is linked to the main control display for Game Control.
The Game Control display is the way for the user to set the AI difficulty (By enabling or disabling certain logic modules) and start the wave timer.

The Gamemaster is also responsible for changing parameters through the course of the game. For instance, certain OBAI units will look in memory for their parameters. Those can be set on a wave number or event basis by the Gamemaster. 

There is also a World Event system, which may make stuff happen depending on certain parameters. For instance, destroy part of the map, run cuscenes, spawn materials or blocks, or even more.
World Events are always started by the Gamemaster (and are in fact usually saved there). There are not many World Events per map.

### 6. World Events
Some gameplay actions may lead to what are commonly called World Events.
World Events are sequences of actions that, when triggered, will alter the gameplay somehow.
It could be the creation of new enemy pathways, the activation or deactivation of certain Unit or Squad modules, cutscenes and many more.

World Events are usually either Wave Based, or Unit Location Based.

Wave Based World Events happen when the Wave Number reaches a certain value for the first time. Examples of this include cutscenes, special enemy spawns, KLR logic changes and more.
Unit Location World Events are usually linked to "boss" units. For instance, Miniboss Guardians are a great source of Unit Location world events. Those events happen if/when the selected unit is within a certain range of a waypoint. Examples include units using weapons on "the world" (aka breaking blocks), the units building a certain structure, or even more advanced logic on a case-to-case basis. Those events can be completely prevented from happening... as long as their trigger never happens.

Discovering the various trigger for the World Events is meant to be part of the fun of my maps. Some resources may be completely blocked behind World Events, but some can also make the run even harder.

### 7. General Unit Overview
### 8. General Squad Overview