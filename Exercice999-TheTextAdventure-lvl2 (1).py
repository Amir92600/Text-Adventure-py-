# lors des premières heures du jeu vidéo (1970), en l'abscence de graphisme, les aventures textuelles étaient légion !
# (en français : fiction interactive : https://fr.wikipedia.org/wiki/Fiction_interactive)
# Ces jeux simple, inspiré des livres dont vous êtes le héros contenaient une liste de lieux avec une description.
# chaque lieu donnait lieu a plusieurs option (entrer dans une pièce; frapper un ennemi...)
# Une fois l'option sélectionnée, elle pointait vers un autre lieu. Et ainsi de suite.
# bien souvent il s'agissait simplement d'un donjon à explorer pour trouver un trésor.
# Le genre est un peu vieillot mais il est revenu récemment sur le devant de la scène avec https://fr.wikipedia.org/wiki/AI_Dungeon_2

# hey bien avec les connaissances actuelles, boucles, listes et dictionnaire il est parfaitement possible de réaliser une micro aventure textuelle !
# ce mini projet représente un défi 

# cette seconde implémentation fait appel à tout ce que nous avons vu depuis le début avec quelques fonctions supplémentaires trouvable sur internet ;)

# CONSTANTS
EXIT_COMMAND = "exit"
# room info
ID="id"
DESCRIPTION = "description"
CHOICES = "choices"
DESTINATION= "destination"
ENDGAME = "endgame"
# inventory management
INVENTORY = "inventory"
ADD = "add"
REMOVE = "remove"
# inventory check
TEST = "test"
HAS = "has"
HASNOT = "hasnot"


#global var
user_input = ""
current_room_id = 0
inventory = set()

rooms = [
    {
        ID:0,
        DESCRIPTION:"Une pièce vide aux murs froids couvert de mousse, une porte en bois est entrouverte au fond",
        ENDGAME:False,
        CHOICES: [
            {
                DESCRIPTION:"ouvrir la porte",
                DESTINATION : 1
            }
        ]
    },
    {
        ID:1,
        DESCRIPTION:"Une bibliothèque étrange : tout les livres ont des pages vierges ! Sur le coté, une porte fermée à clef",
        ENDGAME:False,
        CHOICES: [
            {
                DESCRIPTION:"Prendre un livre",
                DESTINATION : 1,
                TEST:[HASNOT,"book"],
                INVENTORY: [ADD,"book"]
            },
            {
                DESCRIPTION:"lire un livre",
                DESTINATION : 2,
            },
            {
                DESCRIPTION:"fouiller les rayonnages",
                DESTINATION : 3,
                INVENTORY: [ADD,"clef"]
            },
            {
                DESCRIPTION:"revenir dans la pièce aux murs couvert de mousse",
                DESTINATION : 0
            },
            {
                DESCRIPTION:"Ouvrir la porte avec la clef",
                DESTINATION : 4,
                TEST:[HAS,"clef"],
                INVENTORY: [REMOVE,"clef"]
            }
        ]
    },
    {
        ID:2,
        DESCRIPTION:"Les livres permettent de s'évader, vous êtes libre, dans votre esprit du moins...",
        ENDGAME: True
    },
     {
        ID:3,
        DESCRIPTION:"Vous trouvez une clef caché sous un livre",
        ENDGAME: False,
        CHOICES: [
            {
                DESCRIPTION:"revenir dans bibliothèque",
                DESTINATION : 1
            }
        ]
    },
     {
        ID:4,
        DESCRIPTION:"La porte s'ouvre une salle avec un puit qui s'enfonce dans les ténèbres...",
        ENDGAME: False,
        CHOICES: [
            {
                DESCRIPTION:"Marcher dans le vide, vous avez la foi !",
                DESTINATION : 5
            },
            {
                DESCRIPTION:"revenir dans bibliothèque",
                DESTINATION : 1
            },
            {
                DESCRIPTION:"Jeter le livre dans le puit pour voir...",
                DESTINATION : 6,
                TEST:[HAS,"book"],
                INVENTORY: [REMOVE,"book"]
            }
        ]
    },
    {
        ID:5,
        DESCRIPTION:"Contre toute attente, il y a un sol, peint en noir au travers du gouffre que vous pouvez traverser ! Vous êtes libre",
        ENDGAME: True
    },
    {
        ID:6,
        DESCRIPTION:"Contre toute attente, le livre tombe et s'arrète au niveau du sol, dans le noir, comme s'il était retenu par quelque chose",
        ENDGAME: False,
        CHOICES: [
            {
                DESCRIPTION:"Rester le long du puit",
                DESTINATION : 4
            },
            {
                DESCRIPTION:"Marcher dans le vide, vous avez la foi !",
                DESTINATION : 5
            },
        ]
    },
]

while user_input != EXIT_COMMAND: # allows the player to leave
    room = rooms[current_room_id]
    # check for endgame
    if room[ENDGAME]: 
         print(room[DESCRIPTION])
         exit()
    # manage user input
    if user_input.isnumeric() :
        # guard
        if int(user_input) not in range(0,len(room[CHOICES])):
            continue # cette instruction est le contraire d'un break. On "continue" la boucle (mais en sautant à la boucle suivante)
        #display choices according to the inventory
        choice = room[CHOICES][int(user_input)]
        current_room_id = choice[DESTINATION]
        if INVENTORY in choice:
            inventory_event = choice[INVENTORY]
            if inventory_event[0] == ADD:
                inventory.add(inventory_event[1])
            elif inventory_event[0] == REMOVE:
                inventory.remove(inventory_event[1])
        user_input = ""
        continue
    #display the room
    if user_input == "":
        print(room[DESCRIPTION])
        print("Vous avez : "+" ".join(inventory))
        i = 0
        for options in room[CHOICES]:
            to_print = True
            if TEST in options:
                item_to_test = options[TEST][1]
                to_print = (options[TEST][0] == HAS and item_to_test in inventory) or (options[TEST][0] == HASNOT and item_to_test not in inventory)
            if to_print:
                print(f"{i}) {options[DESCRIPTION]}")
            i+=1
        user_input =""
    user_input = input(">")