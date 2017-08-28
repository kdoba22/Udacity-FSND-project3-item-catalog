from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item, User, engine

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

#create Categories
categorySchool = Category(name="School")
categoryElectronics = Category(name="Electronics")
categoryDogs = Category(name="Dogs")
categoryFoods = Category(name="Foods")
categoryHalloween = Category(name="Halloween")

session.add(categorySchool)
session.commit()
session.add(categoryElectronics)
session.commit()
session.add(categoryDogs)
session.commit()
session.add(categoryFoods)
session.commit()
session.add(categoryHalloween)
session.commit()


# Items for School

item = Item(name="Pencil", description="wooden tool for writing",category=categorySchool)
session.add(item)
session.commit()

item = Item(name="Eraser", description="used to remove lead from paper", category=categorySchool)
session.add(item)
session.commit()

item = Item(name="Paper", description="used to write on", category=categorySchool)
session.add(item)
session.commit()

item = Item(name="Books", description="used to read", category=categorySchool)
session.add(item)
session.commit()

item = Item(name="chalk", description="used to write on blackboard", category=categorySchool)
session.add(item)
session.commit()

#Items used in electronics

item = Item(name="Resistor", description="used to restrict current flow",category=categoryElectronics)

session.add(item)
session.commit()

item = Item(name="Capasitor", description="used to hold a charge", category=categoryElectronics)

session.add(item)
session.commit()

item = Item(name="Ohm's Law", description="used to explain how Resistance, Voltage, and Current relate to one another", category=categoryElectronics)

session.add(item)
session.commit()

item = Item(name="Multi-Meter", description="used to measure voltage, current, and resistance", category=categoryElectronics)

session.add(item)
session.commit()

item = Item(name="Operational amplifier", description="One of many types of amplifieres used", category=categoryElectronics)

session.add(item)
session.commit()

# types of dogs


item = Item(name="Norwegion Elkhound", description="Given credit for chasing wolves from the scandivavian Mountain Range",category=categoryDogs)

session.add(item)
session.commit()

item = Item(name="German Shepard", description="Fearless Police Dog", category=categoryDogs)

session.add(item)
session.commit()

item = Item(name="Jack Russel Terrior", description="Frasier's dog", category=categoryDogs)

session.add(item)
session.commit()

item = Item(name="shih tzu ", description="gazuntite", category=categoryDogs)

session.add(item)
session.commit()

item = Item(name="English Bulldog", description="Let's Drool", category=categoryDogs)

session.add(item)
session.commit()

# my favorite foods


item = Item(name="Pizza", description="mmm Peperoni mmm",category=categoryFoods)

session.add(item)
session.commit()

item = Item(name="Hamburgers", description="Two all beef patti's, special sauce, lettuce, cheese, pickles, onions on a sesame seed bun", category=categoryFoods)

session.add(item)
session.commit()

item = Item(name="Saurkraut", description="A German favorite", category=categoryFoods)

session.add(item)
session.commit()

item = Item(name="Salad", description="when your feeling peckage", category=categoryFoods)

session.add(item)
session.commit()

item = Item(name="Soup", description="No soup for you!", category=categoryFoods)

session.add(item)
session.commit()

# its Halloween


item = Item(name="Ghost", description="Scary creatures in sheets",category=categoryHalloween)

session.add(item)
session.commit()

item = Item(name="Goblins", description="Gooble Gooble Gooble", category=categoryHalloween)

session.add(item)
session.commit()

item = Item(name="Witch", description="A big black hat", category=categoryHalloween)

session.add(item)
session.commit()

item = Item(name="Mummy", description="All wrapped up", category=categoryHalloween)

session.add(item)
session.commit()

item = Item(name="cats", description="meow", category=categoryHalloween)

session.add(item)
session.commit()




print ("added menu items!")
