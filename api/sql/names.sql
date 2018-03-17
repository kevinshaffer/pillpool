insert into pp.room_names(name)
select d.name
from (
	      select lower('Aardvark')::text as name
	union select lower('Abyssinian')::text as name
	union select lower('Affenpinscher')::text as name
	union select lower('Akbash')::text as name
	union select lower('Akita')::text as name
	union select lower('Albatross')::text as name
	union select lower('Alligator')::text as name
	union select lower('Alpaca')::text as name
	union select lower('Angelfish')::text as name
	union select lower('Ant')::text as name
	union select lower('Anteater')::text as name
	union select lower('Antelope')::text as name
	union select lower('Ape')::text as name
	union select lower('Armadillo')::text as name
	union select lower('Ass')::text as name
	union select lower('Avocet')::text as name
	union select lower('Axolotl')::text as name
	union select lower('Baboon')::text as name
	union select lower('Badger')::text as name
	union select lower('Balinese')::text as name
	union select lower('Bandicoot')::text as name
	union select lower('Barb')::text as name
	union select lower('Barnacle')::text as name
	union select lower('Barracuda')::text as name
	union select lower('Bat')::text as name
	union select lower('Beagle')::text as name
	union select lower('Bear')::text as name
	union select lower('Beaver')::text as name
	union select lower('Bee')::text as name
	union select lower('Beetle')::text as name
	union select lower('Binturong')::text as name
	union select lower('Bird')::text as name
	union select lower('Birman')::text as name
	union select lower('Bison')::text as name
	union select lower('Bloodhound')::text as name
	union select lower('Boar')::text as name
	union select lower('Bobcat')::text as name
	union select lower('Bombay')::text as name
	union select lower('Bongo')::text as name
	union select lower('Bonobo')::text as name
	union select lower('Booby')::text as name
	union select lower('Budgerigar')::text as name
	union select lower('Buffalo')::text as name
	union select lower('Bulldog')::text as name
	union select lower('Bullfrog')::text as name
	union select lower('Burmese')::text as name
	union select lower('Butterfly')::text as name
	union select lower('Caiman')::text as name
	union select lower('Camel')::text as name
	union select lower('Capybara')::text as name
	union select lower('Caracal')::text as name
	union select lower('Caribou')::text as name
	union select lower('Cassowary')::text as name
	union select lower('Cat')::text as name
	union select lower('Caterpillar')::text as name
	union select lower('Catfish')::text as name
	union select lower('Cattle')::text as name
	union select lower('Centipede')::text as name
	union select lower('Chameleon')::text as name
	union select lower('Chamois')::text as name
	union select lower('Cheetah')::text as name
	union select lower('Chicken')::text as name
	union select lower('Chihuahua')::text as name
	union select lower('Chimpanzee')::text as name
	union select lower('Chinchilla')::text as name
	union select lower('Chinook')::text as name
	union select lower('Chipmunk')::text as name
	union select lower('Chough')::text as name
	union select lower('Cichlid')::text as name
	union select lower('Clam')::text as name
	union select lower('Coati')::text as name
	union select lower('Cobra')::text as name
	union select lower('Cockroach')::text as name
	union select lower('Cod')::text as name
	union select lower('Collie')::text as name
	union select lower('Coral')::text as name
	union select lower('Cormorant')::text as name
	union select lower('Cougar')::text as name
	union select lower('Cow')::text as name
	union select lower('Coyote')::text as name
	union select lower('Crab')::text as name
	union select lower('Crane')::text as name
	union select lower('Crocodile')::text as name
	union select lower('Crow')::text as name
	union select lower('Curlew')::text as name
	union select lower('Cuscus')::text as name
	union select lower('Cuttlefish')::text as name
	union select lower('Dachshund')::text as name
	union select lower('Dalmatian')::text as name
	union select lower('Deer')::text as name
	union select lower('Dhole')::text as name
	union select lower('Dingo')::text as name
	union select lower('Dinosaur')::text as name
	union select lower('Discus')::text as name
	union select lower('Dodo')::text as name
	union select lower('Dog')::text as name
	union select lower('Dogfish')::text as name
	union select lower('Dolphin')::text as name
	union select lower('Donkey')::text as name
	union select lower('Dormouse')::text as name
	union select lower('Dotterel')::text as name
	union select lower('Dove')::text as name
	union select lower('Dragonfly')::text as name
	union select lower('Drever')::text as name
	union select lower('Duck')::text as name
	union select lower('Dugong')::text as name
	union select lower('Dunker')::text as name
	union select lower('Dunlin')::text as name
	union select lower('Eagle')::text as name
	union select lower('Earwig')::text as name
	union select lower('Echidna')::text as name
	union select lower('Eel')::text as name
	union select lower('Eland')::text as name
	union select lower('Elephant')::text as name
	union select lower('Elephant seal')::text as name
	union select lower('Elk')::text as name
	union select lower('Emu')::text as name
	union select lower('Falcon')::text as name
	union select lower('Ferret')::text as name
	union select lower('Finch')::text as name
	union select lower('Fish')::text as name
	union select lower('Flamingo')::text as name
	union select lower('Flounder')::text as name
	union select lower('Fly')::text as name
	union select lower('Fossa')::text as name
	union select lower('Fox')::text as name
	union select lower('Frigatebird')::text as name
	union select lower('Frog')::text as name
	union select lower('Galago')::text as name
	union select lower('Gar')::text as name
	union select lower('Gaur')::text as name
	union select lower('Gazelle')::text as name
	union select lower('Gecko')::text as name
	union select lower('Gerbil')::text as name
	union select lower('Gharial')::text as name
	union select lower('Giant Panda')::text as name
	union select lower('Gibbon')::text as name
	union select lower('Giraffe')::text as name
	union select lower('Gnat')::text as name
	union select lower('Gnu')::text as name
	union select lower('Goat')::text as name
	union select lower('Goldfinch')::text as name
	union select lower('Goldfish')::text as name
	union select lower('Goose')::text as name
	union select lower('Gopher')::text as name
	union select lower('Gorilla')::text as name
	union select lower('Goshawk')::text as name
	union select lower('Grasshopper')::text as name
	union select lower('Greyhound')::text as name
	union select lower('Grouse')::text as name
	union select lower('Guanaco')::text as name
	union select lower('Guinea fowl')::text as name
	union select lower('Guinea pig')::text as name
	union select lower('Gull')::text as name
	union select lower('Guppy')::text as name
	union select lower('Hamster')::text as name
	union select lower('Hare')::text as name
	union select lower('Harrier')::text as name
	union select lower('Havanese')::text as name
	union select lower('Hawk')::text as name
	union select lower('Hedgehog')::text as name
	union select lower('Heron')::text as name
	union select lower('Herring')::text as name
	union select lower('Himalayan')::text as name
	union select lower('Hippopotamus')::text as name
	union select lower('Hornet')::text as name
	union select lower('Horse')::text as name
	union select lower('Human')::text as name
	union select lower('Hummingbird')::text as name
	union select lower('Hyena')::text as name
	union select lower('Ibis')::text as name
	union select lower('Iguana')::text as name
	union select lower('Impala')::text as name
	union select lower('Indri')::text as name
	union select lower('Insect')::text as name
	union select lower('Jackal')::text as name
	union select lower('Jaguar')::text as name
	union select lower('Javanese')::text as name
	union select lower('Jay')::text as name
	union select lower('Jellyfish')::text as name
	union select lower('Kakapo')::text as name
	union select lower('Kangaroo')::text as name
	union select lower('Kingfisher')::text as name
	union select lower('Kiwi')::text as name
	union select lower('Koala')::text as name
	union select lower('Komodo dragon')::text as name
	union select lower('Kouprey')::text as name
	union select lower('Kudu')::text as name
	union select lower('Labradoodle')::text as name
	union select lower('Ladybird')::text as name
	union select lower('Lapwing')::text as name
	union select lower('Lark')::text as name
	union select lower('Lemming')::text as name
	union select lower('Lemur')::text as name
	union select lower('Leopard')::text as name
	union select lower('Liger')::text as name
	union select lower('Lion')::text as name
	union select lower('Lionfish')::text as name
	union select lower('Lizard')::text as name
	union select lower('Llama')::text as name
	union select lower('Lobster')::text as name
	union select lower('Locust')::text as name
	union select lower('Loris')::text as name
	union select lower('Louse')::text as name
	union select lower('Lynx')::text as name
	union select lower('Lyrebird')::text as name
	union select lower('Macaw')::text as name
	union select lower('Magpie')::text as name
	union select lower('Mallard')::text as name
	union select lower('Maltese')::text as name
	union select lower('Manatee')::text as name
	union select lower('Mandrill')::text as name
	union select lower('Markhor')::text as name
	union select lower('Marten')::text as name
	union select lower('Mastiff')::text as name
	union select lower('Mayfly')::text as name
	union select lower('Meerkat')::text as name
	union select lower('Millipede')::text as name
	union select lower('Mink')::text as name
	union select lower('Mole')::text as name
	union select lower('Molly')::text as name
	union select lower('Mongoose')::text as name
	union select lower('Mongrel')::text as name
	union select lower('Monkey')::text as name
	union select lower('Moorhen')::text as name
	union select lower('Moose')::text as name
	union select lower('Mosquito')::text as name
	union select lower('Moth')::text as name
	union select lower('Mouse')::text as name
	union select lower('Mule')::text as name
	union select lower('Narwhal')::text as name
	union select lower('Neanderthal')::text as name
	union select lower('Newfoundland')::text as name
	union select lower('Newt')::text as name
	union select lower('Nightingale')::text as name
	union select lower('Numbat')::text as name
	union select lower('Ocelot')::text as name
	union select lower('Octopus')::text as name
	union select lower('Okapi')::text as name
	union select lower('Olm')::text as name
	union select lower('Opossum')::text as name
	union select lower('Orang-utan')::text as name
	union select lower('Oryx')::text as name
	union select lower('Ostrich')::text as name
	union select lower('Otter')::text as name
	union select lower('Owl')::text as name
	union select lower('Ox')::text as name
	union select lower('Oyster')::text as name
	union select lower('Pademelon')::text as name
	union select lower('Panther')::text as name
	union select lower('Parrot')::text as name
	union select lower('Partridge')::text as name
	union select lower('Peacock')::text as name
	union select lower('Peafowl')::text as name
	union select lower('Pekingese')::text as name
	union select lower('Pelican')::text as name
	union select lower('Penguin')::text as name
	union select lower('Persian')::text as name
	union select lower('Pheasant')::text as name
	union select lower('Pig')::text as name
	union select lower('Pigeon')::text as name
	union select lower('Pika')::text as name
	union select lower('Pike')::text as name
	union select lower('Piranha')::text as name
	union select lower('Platypus')::text as name
	union select lower('Pointer')::text as name
	union select lower('Pony')::text as name
	union select lower('Poodle')::text as name
	union select lower('Porcupine')::text as name
	union select lower('Porpoise')::text as name
	union select lower('Possum')::text as name
	union select lower('Prairie Dog')::text as name
	union select lower('Prawn')::text as name
	union select lower('Puffin')::text as name
	union select lower('Pug')::text as name
	union select lower('Puma')::text as name
	union select lower('Quail')::text as name
	union select lower('Quelea')::text as name
	union select lower('Quetzal')::text as name
	union select lower('Quokka')::text as name
	union select lower('Quoll')::text as name
	union select lower('Rabbit')::text as name
	union select lower('Raccoon')::text as name
	union select lower('Ragdoll')::text as name
	union select lower('Rail')::text as name
	union select lower('Ram')::text as name
	union select lower('Rat')::text as name
	union select lower('Rattlesnake')::text as name
	union select lower('Raven')::text as name
	union select lower('Red deer')::text as name
	union select lower('Red panda')::text as name
	union select lower('Reindeer')::text as name
	union select lower('Rhinoceros')::text as name
	union select lower('Robin')::text as name
	union select lower('Rook')::text as name
	union select lower('Rottweiler')::text as name
	union select lower('Ruff')::text as name
	union select lower('Salamander')::text as name
	union select lower('Salmon')::text as name
	union select lower('Sand Dollar')::text as name
	union select lower('Sandpiper')::text as name
	union select lower('Saola')::text as name
	union select lower('Sardine')::text as name
	union select lower('Scorpion')::text as name
	union select lower('Sea lion')::text as name
	union select lower('Sea Urchin')::text as name
	union select lower('Seahorse')::text as name
	union select lower('Seal')::text as name
	union select lower('Serval')::text as name
	union select lower('Shark')::text as name
	union select lower('Sheep')::text as name
	union select lower('Shrew')::text as name
	union select lower('Shrimp')::text as name
	union select lower('Siamese')::text as name
	union select lower('Siberian')::text as name
	union select lower('Skunk')::text as name
	union select lower('Sloth')::text as name
	union select lower('Snail')::text as name
	union select lower('Snake')::text as name
	union select lower('Snowshoe')::text as name
	union select lower('Somali')::text as name
	union select lower('Sparrow')::text as name
	union select lower('Spider')::text as name
	union select lower('Sponge')::text as name
	union select lower('Squid')::text as name
	union select lower('Squirrel')::text as name
	union select lower('Starfish')::text as name
	union select lower('Starling')::text as name
	union select lower('Stingray')::text as name
	union select lower('Stinkbug')::text as name
	union select lower('Stoat')::text as name
	union select lower('Stork')::text as name
	union select lower('Swallow')::text as name
	union select lower('Swan')::text as name
	union select lower('Tang')::text as name
	union select lower('Tapir')::text as name
	union select lower('Tarsier')::text as name
	union select lower('Termite')::text as name
	union select lower('Tetra')::text as name
	union select lower('Tiffany')::text as name
	union select lower('Tiger')::text as name
	union select lower('Toad')::text as name
	union select lower('Tortoise')::text as name
	union select lower('Toucan')::text as name
	union select lower('Tropicbird')::text as name
	union select lower('Trout')::text as name
	union select lower('Tuatara')::text as name
	union select lower('Turkey')::text as name
	union select lower('Turtle')::text as name
	union select lower('Uakari')::text as name
	union select lower('Uguisu')::text as name
	union select lower('Umbrellabird')::text as name
	union select lower('Vicuña')::text as name
	union select lower('Viper')::text as name
	union select lower('Vulture')::text as name
	union select lower('Wallaby')::text as name
	union select lower('Walrus')::text as name
	union select lower('Warthog')::text as name
	union select lower('Wasp')::text as name
	union select lower('Water buffalo')::text as name
	union select lower('Weasel')::text as name
	union select lower('Whale')::text as name
	union select lower('Whippet')::text as name
	union select lower('Wildebeest')::text as name
	union select lower('Wolf')::text as name
	union select lower('Wolverine')::text as name
	union select lower('Wombat')::text as name
	union select lower('Woodcock')::text as name
	union select lower('Woodlouse')::text as name
	union select lower('Woodpecker')::text as name
	union select lower('Worm')::text as name
	union select lower('Wrasse')::text as name
	union select lower('Wren')::text as name
	union select lower('Yak')::text as name
	union select lower('Zebra')::text as name
	union select lower('Zebu')::text as name
	union select lower('Zonkey')::text as name
	union select lower('Zorse')::text as name
) d
left join pp.room_names t
	on t.name = d.name
where t.name is null
