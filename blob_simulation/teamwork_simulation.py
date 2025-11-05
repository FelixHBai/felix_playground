from matplotlib import pyplot as plt
import random
import time

class Tree:
    def __init__(self):
        self.blobs = []


def world_reset(world):
    for tree in world:
        tree.blobs = []
    #print('World Reset')


class Blob:
    def __init__(self, blob_type):
        self.blob_type = blob_type

    def go_to_tree(self, world, available_tree_index):
        if len(available_tree_index) > 0:
            tree_index = random.choice(list(available_tree_index))
            #print(tree_attempt)
            if (len(world[tree_index].blobs) < 2):
                world[tree_index].blobs.append(self)
                if world[tree_index].blobs == 2:
                    available_tree_index.remove(tree_index)
                return world[tree_index]
                            
    def reproduce(self, score, bloblets):
        #print(score)
        whole = score // 1
        chance = score % 1
        new_blobs = [Blob(self.blob_type)] * int(whole)
        rand_num = random.random()
        #print(rand_num)
        if rand_num < chance:
            new_blobs.append(Blob(self.blob_type))
        #print(len(new_blobs))
        #print(len(blobs))
        bloblets.extend(new_blobs)
        #print('R', end=' ')

#### DEFINING THE SIMULATION FUNCTION ####

def run_blob_teamwork_sim(tree_amount, total_days, team_start_amt=1, solo_start_amt=1):
    start_time = time.perf_counter()

    world = [Tree() for i in range(tree_amount)]

    team_blobs_amount = [team_start_amt]
    solo_blobs_amount = [solo_start_amt]

    blobs = [Blob('solo') for i in range(solo_start_amt)] + [Blob('team') for i in range(team_start_amt)]

    #### START SIMULATION ####

    for i in range(total_days):
        bloblets = [] # Blobs born / Next gen blobs
        available_tree_index = {i for i in range(tree_amount)}

        for blob in blobs:
            blob.go_to_tree(world, available_tree_index)

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

        for tree in world:
            if len(tree.blobs) == 2:
                blob1 = tree.blobs[0]
                blob2 = tree.blobs[1]

                if blob1.blob_type == 'solo':
                    if blob2.blob_type == 'solo':
                        blob1.reproduce(0.5, bloblets)
                        blob2.reproduce(0.5, bloblets)
                        #print('SS', end=' ')
                    elif blob2.blob_type == 'team':
                        blob1.reproduce(1.5, bloblets)
                        blob2.reproduce(0.5, bloblets)
                        #print('ST', end=' ')
                
                if blob1.blob_type == 'team':
                    if blob2.blob_type == 'solo':
                        blob1.reproduce(0.5, bloblets)
                        blob2.reproduce(1.5, bloblets)
                        #print('TS', end=' ')
                    if blob2.blob_type == 'team':
                        blob1.reproduce(1.5, bloblets)
                        blob2.reproduce(1.5, bloblets)
                        #print('TT', end=' ')

            elif len(tree.blobs) == 1:
                blob1 = tree.blobs[0]
                blob1.reproduce(2, bloblets)
                #print('OT', end=' ')
            
            #else:
                #print('NB', end=' ')
            
        #print()


        '''
        for tree in world:
            print(len(tree.blobs), end=' ')
            print()
        '''

        blobs = bloblets
        world_reset(world)

        #### COUNT THE BLOBS FOR THE GRAPH ####

        solo_count = 0
        team_count = 0
        
        for blob in blobs:
            if blob.blob_type == 'solo':
                solo_count += 1
            elif blob.blob_type == 'team':
                team_count += 1

        solo_blobs_amount.append(solo_count)
        team_blobs_amount.append(team_count)

    ### START CREATING GRAPH ###

    end_time = time.perf_counter()
    #return
    print('Total time: {} s'.format(end_time - start_time))
    print('Trees: {}, Days: {}'.format(tree_amount, total_days))

    plt.stackplot([i for i in range(len(solo_blobs_amount))], solo_blobs_amount, team_blobs_amount, colors=[(1, 0.4, 0.4), (0.4, 0.5, 1)])
    plt.legend(['Solo Blobs', 'Team Blobs'])
    plt.title('Frequency of Solo & Team Blobs')
    plt.xlabel('Day')
    plt.ylabel('# of Solo Blobs')
    plt.show()

if __name__ == '__main__':
    import cProfile
    import pstats
    cProfile.run('run_blob_teamwork_sim(tree_amount=500, total_days=100)', 'teamwork_evolve_cprofile.temp')
    stats = pstats.Stats('teamwork_evolve_cprofile.temp')
    stats.sort_stats('cumulative')
    stats.print_stats(200)
    #run_blob_teamwork_sim(tree_amount=500, total_days=100)
