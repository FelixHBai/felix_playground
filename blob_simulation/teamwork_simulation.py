from matplotlib import pyplot as plt
import random
import time

start_time = time.perf_counter()

class Tree:
    def __init__(self):
        self.blobs = []

tree_amount = 500
world = []
for i in range(tree_amount):
    world.append(Tree())
world_index = {i for i in range(tree_amount)}

def world_reset():
    for tree_index in world_index:
        world[tree_index].blobs = []
    #print('World Reset')

blobs = []

class Blob:
    def __init__(self, blob_type):
        self.blob_type = blob_type
        self.tree = None
        
    def __str__(self):
        return self.blob_type.capitalize() + ' blob'

    def go_to_tree(self):
        while True:
            if len(available_tree_index) > 0:
                tree_index = random.choice(list(available_tree_index))
                #print(tree_attempt)
                if (len(world[tree_index].blobs) < 2):
                    self.tree = world[tree_index]
                    world[tree_index].blobs.append(self)
                    if world[tree_index].blobs == 2:
                        available_tree_index.remove(tree_index)
                    return world[tree_index]
                else:
                    available_tree_index.remove(tree_index)
            else:
                blobs.remove(self)
                return 'Blob removed'
                
    def reproduce(self, score):
        #print(score)
        whole = score // 1
        chance = score % 1
        new_blobs = [Blob(self.blob_type)] * int(whole)
        rand_num = random.random()
        #print(rand_num)
        if chance > rand_num:
            new_blobs.append(Blob(self.blob_type))
        #print(len(new_blobs))
        #print(len(blobs))
        blobs.extend(new_blobs)
        blobs.remove(self)
        #print('R', end=' ')

team_start_amt = 1
solo_start_amt = 1
team_blobs_amount = [team_start_amt]
solo_blobs_amount = [solo_start_amt]

for i in range(solo_start_amt):
    blobs.append(Blob('solo'))

for i in range(team_start_amt):
    blobs.append(Blob('team'))

### START SIMULATION ###

'''
Reward Chart
v Self  Opponent =======================>
-----------------------------------------
|      | Own Tree |   Solo   |   Team   |
-----------------------------------------
| Solo |   2.00   |   0.50   |   1.50   |
-----------------------------------------
| Team |   2.00   |   0.50   |   1.50   |
-----------------------------------------
'''

total_days = 100

for i in range(total_days):
    available_tree_index = set(list(world_index)[:])

    for blob in blobs:
        blob.go_to_tree()

    for tree in world:
        if len(tree.blobs) == 2:
            blob1 = tree.blobs[0]
            blob2 = tree.blobs[1]

            if blob1.blob_type == 'solo':
                if blob2.blob_type == 'solo':
                    blob1.reproduce(0.5)
                    blob2.reproduce(0.5)
                    #print('SS', end=' ')
                elif blob2.blob_type == 'team':
                    blob1.reproduce(1.5)
                    blob2.reproduce(0.5)
                    #print('ST', end=' ')
            
            if blob1.blob_type == 'team':
                if blob2.blob_type == 'solo':
                    blob1.reproduce(0.5)
                    blob2.reproduce(1.5)
                    #print('TS', end=' ')
                if blob2.blob_type == 'team':
                    blob1.reproduce(1.5)
                    blob2.reproduce(1.5)
                    #print('TT', end=' ')

        elif len(tree.blobs) == 1:
            blob1 = tree.blobs[0]
            blob1.reproduce(2)
            #print('OT', end=' ')
        
        #else:
            #print('NB', end=' ')
        
    #print()


    '''
    for tree in world:
        print(len(tree.blobs), end=' ')
        print()
    '''

    world_reset()

    solo_count = 0
    team_count = 0
    
    for blob in blobs:
        if blob.blob_type == 'solo':
            solo_count += 1
        elif blob.blob_type == 'team':
            team_count += 1

    solo_blobs_amount.append(solo_count)
    team_blobs_amount.append(team_count)

    #try: print('Solo: {}%, {} blobs\nTeam:{}%, {} blobs\n'.format(round(100*solo_count/len(blobs)), solo_count round(100*team_count/len(blobs)), team_count))
    #try: print('Solo: {}%, {} blobs\nTeam:{}%, {} blobs\n'.format(round(100*solo_count/len(blobs)), solo_count, round(100*team_count/len(blobs)), team_count))
    #except: print('Solo: 0%, 0 blobs\nTeam: 0%, 0 blobs\n')

### START CREATING GRAPH ###

end_time = time.perf_counter()
print('Total time: {} s'.format(end_time - start_time))
print('Trees: {}, Days: {}'.format(tree_amount, total_days))

plt.stackplot([i for i in range(len(solo_blobs_amount))], solo_blobs_amount, team_blobs_amount, colors=[(1, 0.4, 0.4), (0.4, 0.5, 1)])
plt.legend(['Solo Blobs', 'Team Blobs'])
plt.title('Frequency of Solo & Team Blobs')
plt.xlabel('Day')
plt.ylabel('# of Solo Blobs')
plt.show()
