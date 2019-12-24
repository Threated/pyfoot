import pyfoot
from pyfoot import World, Actor

class MyActor(Actor):

    def act(self):
        if pyfoot.isKeyDown("w"):
            self.y -= 1
        if pyfoot.isKeyDown("s"):
            self.y += 1
        if pyfoot.isKeyDown("a"):
            self.x -= 1
        if pyfoot.isKeyDown("d"):
            self.x += 1

def main():
    my_world = World(600, 400)
    my_actor = MyActor()
    my_world.add_Object(my_actor, 200, 200)
    pyfoot.set_title("My Game")
    pyfoot.start()

main()