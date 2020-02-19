import pyfoot
from pyfoot import World, Actor

class MyActor(Actor):

    def act(self):
        if pyfoot.is_key_down("w"):
            self.y -= 1
        if pyfoot.is_key_down("s"):
            self.y += 1
        if pyfoot.is_key_down("a"):
            self.x -= 1
        if pyfoot.is_key_down("d"):
            self.x += 1

def main():
    my_world = World(600, 400)
    my_actor = MyActor()
    my_world.add_Object(my_actor, 200, 200)
    pyfoot.set_title("My Game")
    pyfoot.start()

main()