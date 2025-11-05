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
        self.alleles = [alleles]

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

def run_blob_teamwork_sim(tree_amount, total_days):
    start_time = time.perf_counter()

    world = [Tree() for i in range(tree_amount)]

    blobs = [Blob('hawk', 'hawk', 'hawk', 'hawk'), 
             Blob('hawk', 'hawk', 'hawk', 'dove'), 
             Blob('hawk', 'hawk', 'dove', 'dove'), 
             Blob('hawk', 'dove', 'dove', 'dove'), 
             Blob('dove', 'dove', 'dove', 'dove')]
    
    hawk_blobs_amt = 1
    mhawk_blobs_amt = 1
    even_blobs_amt = 1
    mdove_blobs_amt = 1
    dove_blobs_amt = 1

    #### START SIMULATION ####

    for i in range(total_days):
        bloblets = []
        available_tree_index = {i for i in range(tree_amount)}

        for blob in blobs:
            blob.go_to_tree(world, available_tree_index)