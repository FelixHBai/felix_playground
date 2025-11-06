from matplotlib import pyplot as plt
import random
import time

class Tree:
    def __init__(self):
        self.blobs = []

def world_reset(world):
    for tree in world:
        tree.blobs = []

class Blob:
    def __init__(self, alleles):
        self.alleles = alleles

    def go_to_tree(self, world, available_tree_index):
        if len(available_tree_index) > 0:
            tree_index = random.choice(list(available_tree_index))
            if len(world[tree_index].blobs) < 2:
                world[tree_index].blobs.append(self)
                if world[tree_index].blobs == 2:
                    available_tree_index.remove(tree_index)
                return world[tree_index]
    
    def reproduce(self, score, bloblets):
        whole = score // 1
        chance = score % 1
        new_blobs = [Blob(self.alleles)] * int(whole)
        rand_num = random.random()
        if rand_num < chance:
            new_blobs.append(Blob(self.alleles))
        bloblets.extend(new_blobs)

#### DEFINING THE SIMULATION FUNCTION ####

def run_blob_aggresion_sim(tree_amount, total_days, hblobs, mhblobs, eblobs, mdblobs, dblobs):
    start_time = time.perf_counter()

    world = [Tree() for i in range(tree_amount)]

    hblobs_amt = [hblobs]
    mhblobs_amt = [mhblobs]
    eblobs_amt = [eblobs]
    mdblobs_amt = [mdblobs]
    dblobs_amt = [dblobs]

    blobs = [Blob(['hawk', 'hawk', 'hawk', 'hawk']) for i in range(hblobs)] +\
            [Blob(['hawk', 'hawk', 'hawk', 'dove']) for i in range(mhblobs)] +\
            [Blob(['hawk', 'hawk', 'dove', 'dove']) for i in range(eblobs)] +\
            [Blob(['hawk', 'dove', 'dove', 'dove']) for i in range(mdblobs)] +\
            [Blob(['dove', 'dove', 'dove', 'dove']) for i in range(dblobs)]

    #### START SIMULATION ####

    for i in range(total_days):
        bloblets = []
        available_tree_index = {i for i in range(tree_amount)}

        for blob in blobs:
            blob.go_to_tree(world, available_tree_index)
        
        '''
        Reward Chart
        v Self  Opponent =======================>
        -----------------------------------------
        |      | Own Tree |   Hawk   |   Dove   |
        -----------------------------------------
        | Hawk |   2.00   |   0.00   |   1.50   |
        -----------------------------------------
        | Dove |   2.00   |   0.50   |   1.00   |
        -----------------------------------------
        '''

        for tree in world:
            if len(tree.blobs) > 2:
                blob1 = tree.blobs[0]
                blob2 = tree.blobs[1]
                blob1choice = random.choice(blob1.alleles)
                blob2choice = random.choice(blob2.alleles)

                if blob1choice == 'hawk':
                    if blob2choice == 'hawk':
                        blob1.reproduce(0, bloblets)
                        blob2.reproduce(0, bloblets)
                    elif blob2choice == 'dove':
                        blob1.reproduce(1.5, bloblets)
                        blob2.reproduce(0.5, bloblets)
                
                if blob1choice == 'dove':
                    if blob2choice == 'hawk':
                        blob1.reproduce(0.5, bloblets)
                        blob2.reproduce(1.5, bloblets)
                    elif blob2choice == 'dove':
                        blob1.reproduce(1, bloblets)
                        blob2.reproduce(1, bloblets)

            elif len(tree.blobs) == 1:
                    blob1 = tree.blobs[0]
                    blob1.reproduce(2, bloblets)
                    #print('OT', end=' ')

        blobs = bloblets
        world_reset(world)

        #### COUNT THE BLOBS FOR THE GRAPH ####

        hawk_count = 0
        mhawk_count = 0
        even_count = 0
        mdove_count = 0
        dove_count = 0

        for blob in blobs:
            if blob.alleles == ['hawk', 'hawk', 'hawk', 'hawk']:
                hawk_count += 1
            elif blob.alleles == ['hawk', 'hawk', 'hawk', 'dove']:
                mhawk_count += 1
            elif blob.alleles == ['hawk', 'hawk', 'dove', 'dove']:
                even_count += 1
            elif blob.alleles == ['hawk', 'dove', 'dove', 'dove']:
                mdove_count += 1
            elif blob.alleles == ['dove', 'dove', 'dove', 'dove']:
                dove_count += 1

        hblobs_amt.append(hawk_count)
        mhblobs_amt.append(mhawk_count)
        eblobs_amt.append(even_count)
        mdblobs_amt.append(mdove_count)
        dblobs_amt.append(dove_count)

    #### START CREATING GRAPH ####

    end_time = time.perf_counter()
    print('Total time: {} s'.format(end_time - start_time))
    print('Trees: {}, Days: {}'.format(tree_amount, total_days))

    plt.stackplot([i for i in range(len(hblobs_amt))], hblobs_amt, mhblobs_amt, eblobs_amt, mdblobs_amt, dblobs_amt,\
                  colors=[(1, 0, 0), (0.75, 0, 0.25), (0.5, 0, 0.5), (0.25, 0, 0.75), (0, 0, 1)])
    plt.legend(['Hawk Blobs', 'Mostly Hawk Blobs', 'Even Blobs', 'Mosty Dove Blobs', 'Dove Blobs'])
    plt.title('Frequency of Hawk & Dove Blobs')
    plt.xlabel('Day')
    plt.ylabel('# of Blobs')
    plt.show()

if __name__ == '__main__':
    import cProfile
    import pstats
    cProfile.run('run_blob_aggresion_sim(tree_amount=500, total_days=200, ' \
    'hblobs=1, mhblobs=1, eblobs=1, mdblobs=1, dblobs=1)', 'aggresion_evolve_cprofile.temp')
    stats = pstats.Stats('aggresion_evolve_cprofile.temp')
    stats.sort_stats('cumulative')
    stats.print_stats(200)
