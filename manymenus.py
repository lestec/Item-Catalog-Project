from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Item, Category, User

engine = create_engine('sqlite:///kidsevents.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create Location of Events #not sure if ADD user_id=1 ????
category1 = Category(name="Library")
session.add(category1)
session.commit()

# Create Activites at above location
item1 = Item(
    name="Storytime",
    description='Storytimes for varies ages.',
    category=category1
    # user = user_id=1
    )
session.add(item1)
session.commit()

item2 = Item(
    name="Playtime",
    description='An hour playtime for ages 3-6.',
    category=category1
    # user = user_id=1
    )
session.add(item2)
session.commit()

item3 = Item(
    name="STEM Programs",
    description='Programs focused on Math, Science, Engineering, and Math',
    category=category1
    # user = user_id=1
    )
session.add(item3)
session.commit()

category2 = Category(name="Recreation Center")
session.add(category2)
session.commit()

item1 = Item(
    name="Events",
    description='Events for kids.',
    category=category2
    # user user_id=1
    )
session.add(item1)
session.commit()

item2 = Item(
    name="Classes",
    description='Classes for kids',
    category=category2
    # user user_id=1
    )
session.add(item2)
session.commit()

item3 = Item(
    name="Camps",
    description='Day camps for school breaks',
    category=category2
    # user user_id=1
    )
session.add(item3)
session.commit()


category3 = Category(name="Children's Amusement Centers")
session.add(category3)
session.commit()

item1 = Item(
    name="Kangamoo",
    description='Indoor playland and events.',
    category=category3
    # user user_id=1
    )
session.add(item1)
session.commit()

item2 = Item(
    name="Lost World Myth and Magic",
    description='Indoor playland and arcade.',
    category=category3
    # user user_id=1
    )
session.add(item2)
session.commit()

item3 = Item(
    name="Bouncy World Indoor Bounce Playland",
    description='Indoor bouncy playland',
    category=category3
    # user user_id=1
    )
session.add(item3)
session.commit()


print "added Location and Events!"
