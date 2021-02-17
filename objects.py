from classes import Character, Area, Consumable, Totem
import questions as q
from story import geography_story, hallway_story, history_story, gym_story, music_room_story, science_room_story, office_story

# CREATE CONSUMABLES
lucozade = Consumable(name='lucozade', value=30)
poison = Consumable("poison", -99)
whiskey = Consumable("whiskey", 5)
apple = Consumable("apple", 30)
haribo = Consumable("haribo", 10)
banana = Consumable("banana", 40)
pint = Consumable("pint of ale", 15)
chewing_gum = Consumable("chewing gum", 1)

# CREATE TOTEMS
magical_compass = Totem(name="magical compass")
strange_coin = Totem("strange coin")
dusty_old_manuscript = Totem("dusty manuscript")
triangle = Totem("silver triangle")
wonder_whistle = Totem("wonder whistle")
test_tube = Totem("glowing test tube")
school_crest = Totem("school crest")


# CREATE AREAS
geography_class = Area(name="Geography Class", items_to_collect=[apple], connections=[], characters=[], story=geography_story,
    message="One door.\nOld Mr Smith stands over his desk.\nJuicy Granny Smith on the table.")
humanities_hallway = Area(name="Hallway", items_to_collect=[haribo, strange_coin], connections=[], characters=[], story=hallway_story,
    message="Long and bright.\nLots of doors.\nWhere to go?")
history_class = Area(name="History Class", items_to_collect=[whiskey], connections=[], characters=[], story=history_story,
    message="Lots of fancy old books.\nDark and eerie...")
gym = Area(name="Gymnasium", items_to_collect=[lucozade, poison], connections=[], characters=[], story=gym_story,
    message="Really pink!\n3 doors total.\nSome items scattered around...")
music_room = Area(name="Music Room", items_to_collect=[banana], connections=[], characters=[], story=music_room_story,
    message="Various instruments.\nGood vibes in here.")
science_room = Area(name="Science Lab", items_to_collect=[pint], connections=[], characters=[], story=science_room_story,
    message="Test tubes and lab benches.\nMore hi-tech than you recall!")
headmasters_office = Area(name="Head's Office", items_to_collect=[chewing_gum], connections=[], characters=[], story=office_story,
    message="Imposing desk.\nBeautiful view.")

# ADD CONNECTIONS TO CREATE A NAVIGATABLE MAP
geography_class.connections = [humanities_hallway]
humanities_hallway.connections = [geography_class, history_class, gym]
history_class.connections = [humanities_hallway]
music_room.connections = [humanities_hallway]
gym.connections = [music_room, science_room, humanities_hallway]
science_room.connections = [gym, headmasters_office]
headmasters_office.connections = [science_room]

# CREATE CHARACTERS
geography_teacher = Character(name="Mr Smith", items=[magical_compass], questions=q.geography, weapon="desk globe")
history_teacher = Character(name="Miss Adams", items=[dusty_old_manuscript], questions=q.history, weapon="Magna Carta")
music_teacher = Character(name="Mr Lord", items=[triangle], questions=q.music, weapon="recorder")
gym_teacher = Character(name="Mr Wenn", items=[wonder_whistle], questions=q.sport, weapon="tennis racket")
science_teacher = Character(name="Dr Brown", items=[test_tube], questions=q.science, weapon="bunsen burner")
headmaster = Character(name="Headmaster", items=[school_crest], questions=q.general_knowledge, weapon="headmasters cane")

# PLACE CHARACTERS IN ROOMS
geography_class.characters = [geography_teacher]
history_class.characters = [history_teacher]
music_room.characters = [music_teacher]
gym.characters = [gym_teacher]
science_room.characters = [science_teacher]
headmasters_office.characters = [headmaster]
