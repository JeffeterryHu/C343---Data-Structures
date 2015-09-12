from utilities import *

# got help from Yitian Zhang, my partner just left earlier in lab and we didn't collaborate together

def flood(color_of_tile, flooded_list, screen_size):
    for i in flooded_list:
        for j in up(i), down(i), left(i), right(i):
            if in_bounds(j, screen_size) and j not in flooded_list and color_of_tile[j] == color_of_tile[flooded_list[0]]:
                flooded_list.append(j)
                
