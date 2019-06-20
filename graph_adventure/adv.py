from room import Room
from player import Player
from world import World
from util import Stack, Queue
from data import roomGraph, roomGraph_M, roomGraph_S, roomGraph_XS, roomGraph_XXS

# Load world
world = World()
world.loadGraph(roomGraph)
world.printRooms()
player = Player("Name", world.startingRoom)


# HOW TO SOLVE THIS
# start at player.currentRoom

# run DFT until you hit dead end (room with no unvisited neighbours) OR you have visited every room

# on every move, add room to traversalPath
# mark every visited room as visited

# if you find a room with no more unvisited neighbours (dead end)

# run BFT to find SHORTEST PATH to first room that is unvisited
# on every move to that room save path
# then run this path with the player so you get to that room

# continute DFT loop (until you find another dead end, then repeat BFT again)

# FILL THIS IN WITH ROOM IDs
traversalPath = []


def dft(player):

    visited = []
    s = Stack()
    s.push(player.currentRoom)

    while s.size() > 0:
        current_room = s.pop()

        if current_room.id not in visited:
            visited.append(current_room.id)

            # keep track of stack size
            # to see if you add any new room into it
            stack_before = len(s.stack)

            """
            # This part optimizes the order of rooms
            # in which they are added to the Stack
            # it will check the number of rooms after neighbouring rooms
            # and adds the one with least amount of rooms (possible dead end)
            # as first to be processed in the stack (last in stack)
            # this will prevent long paths back
            # and make sure dead ends rooms are delt with first
            """
            obj = {'n': None, 'w': None, 's': None, 'e': None}

            # direction == one of 'n', 'w', 's', 'e'
            for direction in current_room.getExits():
                # get room in direction
                room = current_room.getRoomInDirection(direction)
                obj[direction] = room

            # make the obj with rooms a list of tuples
            # for directions that do have a room (value of direction is not None)
            obj_no_none = [i for i in obj.items() if i[1] != None]

            # sort the list based on length of exits from the room
            # the room with least amount of exits (1) will be added to stack last
            # and visited first
            sorted_obj = sorted(
                obj_no_none, key=lambda room: len(room[1].getExits()), reverse=True)

            for room in sorted_obj:
                # do not add already visited rooms into stack
                if room[1].id not in visited:
                    s.push(room[1])

            stack_after = len(s.stack)

            # if we dont push any rooms to the stack, we hit dead end => start BFT
            # check length of stack before and after the for loop
            # if it has the same length, run BFT
            if stack_before == stack_after:
                # BFT will return shortest PATH to the next non-visited room
                shortest_path = []
                try:
                    # if current_room.id == s.stack[-1].id (you hit a dead end in looped nodes(cyclic graph))
                    # take s.stack[-2].id as TARGET if it exist
                    # if it doesnt (means the stack is empty) you are finished
                    if current_room.id == s.stack[-1].id:
                        # BFS entry and target nodes:
                        # FROM = current_room
                        # TARGET = s.stack[-2].id
                        shortest_path = bfs(
                            current_room, s.stack[-2])

                    else:
                        # BFS entry and target nodes:
                        # FROM = current_room
                        # TARGET = s.stack[-1].id
                        shortest_path = bfs(
                            current_room, s.stack[-1])

                    # append paths traversed with BFS to visited list
                    # except the first and the last node
                    # as they are added to the traversed path with DFT (unvisited nodes at this point)
                    for i in range(1, len(shortest_path)-1):
                        visited.append(shortest_path[i])

                except IndexError:
                    print('We are done!')

    return visited


def bfs(start, target):
    que = Queue()
    que.enqueue({"node": start, "path": []})
    bfs_visited = set()

    while que.size() > 0:
        current_room = que.queue[0]

        if current_room["node"].id not in bfs_visited:
            bfs_visited.add(current_room["node"].id)

            if current_room["node"].id == target.id:
                current_room["path"].append(current_room["node"].id)
                return current_room["path"]

            # add all neighbouring nodes to queue
            for direction in current_room["node"].getExits():
                room = current_room["node"].getRoomInDirection(direction)

                # Make a COPY of the PATH set from current node to neighbour nodes
                path_to_neighbour = current_room["path"].copy()
                path_to_neighbour.append(current_room["node"].id)

                que.enqueue(
                    {"node": room, "path": path_to_neighbour})

        que.dequeue()
    return None


traversalPath = dft(player)

print(f'path: {traversalPath}')
print(f'path length: {len(traversalPath)}')


# TRAVERSAL TEST
# commented out parts of code that took direction
# as my resulting path gives room IDs
visited_rooms = set()
# player.currentRoom = world.startingRoom
# visited_rooms.add(player.currentRoom)
for move in traversalPath:
    # player.travel(move)
    visited_rooms.add(move)


if len(visited_rooms) == len(roomGraph):
    print(
        f"TESTS PASSED: {len(traversalPath)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(roomGraph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.currentRoom.printRoomDescription(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     else:
#         print("I did not understand that command.")
