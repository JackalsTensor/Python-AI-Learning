from Animal_demo import Animal
from Dog_demo import Dog
from Cat_demo import Cat
def make_speak(animal):
    animal.speak()
dog=Dog()
cat=Cat()
make_speak(dog)
make_speak(cat)