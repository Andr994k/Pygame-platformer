import random


grassblock = "G"
grass = "g"
dirt = "D"


#The length and height of the world need to be divisible by 64, as it is the size of the individual tiles in the game
length = 3200
height = 1600
#world = []
externalrowlist = ""
def world_gen(l,h):
    #Generates an array with the length of the variables length and height divided by 64. 
    def create_empty_world():
        global world
        world = [["E" for i in range(int(l/64))] for j in range(int(h/64))]
    create_empty_world()

    #Generates one row of a variable name. 
    #Then converts it to a string, using the "join" method.
    #This is currently only used for making a dirt layer at the bottom of the world
    def create_row(tile, rowlist):
        rowlist = []
        global externalrowlist
        for empty in range(0,int(l/64)):
            empty = tile
            rowlist.append(empty)
        externalrowlist = rowlist
    #Create a row of dirt
    create_row(dirt,"dirtrow")

    #Add the row of dirt to the bottom of the list
    def add_dirt_layer(layers):
        index = -1
        while not index == -layers:
            world[index] = externalrowlist
            index -= 1
        if index == -layers:
            create_row(grassblock, "grassblockrow")
            world[index] = externalrowlist
    add_dirt_layer(6)

    #Adds a random amount of dirt blocks placed randomly throughout the map
    def add_dirt_blocks():
        amount_of_patches = random.randint(30,40)
        #print(f"The amount of dirt patches is:", amount_of_patches)
        x = 0
        #Loop for first placing a dirt block at a random location, and afterwards expanding upon it in both x and y
        while not x == amount_of_patches:
            dirt_location_x = random.randint(5,l/64-5)
            dirt_location_y = random.randint(0,h/64-8)
            #Expand a random amount between 0 and 5 on the x axis.
            def plot_dirt(x1,y1,dx,dy):
                for x in range(x1,x1+dx):
                    for y in range(y1,y1+dy):
                        if y == y1 and world[y-1][x] == "E":
                                world[y-1][x] = grassblock
                        world[y][x] = dirt
            plot_dirt(dirt_location_x,dirt_location_y,random.randint(0,5),random.randint(0,6))
            x += 1
    add_dirt_blocks()

    #sep="" makes a seperator between each element in the list. By using \n there will be a line break after each element.
    #This helps to view the list as a map.
    #world[17][24] = "P"
    world[0][0] = "P"
    for x in world:
        print(' '.join(map(str, x)))

world_gen(length,height)