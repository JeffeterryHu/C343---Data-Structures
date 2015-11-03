#! /usr/bin/env python

import sys, time, random
import pygame
from macpath import curdir

start_time = time.clock()


e_aplh = "abcdefghijklmnopqrstuvwxyz"
dna_alph = "ACGT"

# generate random string drawn from the given alphabet and of a given length
def gen_random_string(alphabet, length):
    a_len = len(alphabet)
    ret = ""
    for n in range(length):
        ret += alphabet[random.randint(0, a_len-1)]
    return ret

# print gen_random_string(e_aplh, 5)

SPACE_CHAR = '_'
SPACE_PENALTY = -1

# the scoring function
def s(x, y):
    if x == SPACE_CHAR or y == SPACE_CHAR:
        return SPACE_PENALTY
    elif x == y:
        return 2
    else:
        return -2

TILE_SIZE = 40
tile_color = (255, 255, 255)
highlight_color = (120, 129, 250)

def init_board(m, n):
    screen = pygame.display.set_mode(((m+2)*TILE_SIZE, (n+2)*TILE_SIZE))
    screen.fill((0, 0, 0))
    pygame.display.set_caption('Dot Board')
    pygame.font.init()
    font = pygame.font.Font(None, 15)
    return screen, font

def create_tile(font, text, color):
    tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
    tile.fill(color)
    b1 = font.render(text, 1, (0, 0, 0))
    tile.blit(b1, (TILE_SIZE/2, TILE_SIZE/2))
    return tile

def render_board(board, font, s1, s2, F):
    for i in range(len(s1)):
        tile = create_tile(font, s1[i], tile_color)
        board.blit(tile, ((i+2)*TILE_SIZE, 0))
    tile = create_tile(font, '', tile_color); board.blit(tile, (0, 0))
    tile = create_tile(font, '', tile_color); board.blit(tile, (TILE_SIZE, 0))
    for j in range(len(s2)):
        tile = create_tile(font, s2[j], tile_color)
        board.blit(tile, (0, (j+2)*TILE_SIZE))
    tile = create_tile(font, '', tile_color); board.blit(tile, (0, TILE_SIZE))
    for (x,y) in sorted(F.keys()):
        tile = create_tile(font, str(F[(x,y)]), tile_color)
        board.blit(tile, ((x+1)*TILE_SIZE, (y+1)*TILE_SIZE))
        
#################################################################################
def lcs(a,b):
    # lcs is longest common subsequence
    a = []
    b = []
    if a == [] or b == []:
        return []
    l = len(a) + len(b) - 1
    sa = a + (len(b) - 1) * ['']
    sb = (len(a) - 1) * [''] + b
    longest = []
    for i in range(l):
        cur = []
        for j in range(l):
            if sa[j] != '' and sb[j] != '' and sa[j] == sb[j]:
                cur.append(sa[j])
            else:
                if len(cur) > len(longest):
                    longest = cur    
                cur = []
        if len(cur) > len(longest):
            longest = cur
        if sa[len(sa) - 1] == '':
            sa = [''] + sa[: len(sa) - 1]
        else:
            sb = sb[1:] + ['']
    return longest



def findSubList(l=[], sub=[]):
    if len(sub) > len(l):
        return -1
    for i in range(len(l) - len(sub) + 1):
        j = 0
        eq = True
        for s in sub:
            if l[i + j] != s:
                eq = False
                break
            j += 1
        if eq:
            return i
    return -1


def seq_align(s1, s2, enable_graphics=True):
    
    value_table = {}
    direction_table = {}
    for x in range(len(s1) + 1):
        for y in range(len(s2) + 1):
            value_table[(x,y)] = None
            direction_table[(x,y)] = None
    value_table[(0,0)] = 0
    s1_work = SPACE_CHAR + s1
    s2_work = SPACE_CHAR + s2
    #using while loops to make it easier to access older tables
    for i in range(len(s1_work)): #y
        for j in range(len(s2_work)): #x
            #setup blocks so we can use the previous cells as values
            if not(i == 0 and j == 0):
                if (i > 0 and j > 0):
                    diagonal = value_table[(i-1,j-1)]
                    up = value_table[(i-1,j)]
                    left = value_table[(i,j-1)]
                elif (i > 0):
                    diagonal = None
                    up = value_table[(i-1,j)]
                    left = None
                else:
                    diagonal = None
                    up = None
                    left = value_table[(i,j-1)]

                if s(s1_work[i],s2_work[j]) == 2:
                    score = 2 + diagonal
                    value_table[(i,j)] = score
                    direction_table[(i,j)] = "M"
                else:
                    direction = None
                    direction_text = None
                    if max(up,left) == left:
                        direction = left
                        direction_text = "L"
                    else:
                        direction = up
                        direction_text = "U"
                    value_table[(i,j)] = direction - 1
                    direction_table[(i,j)] = direction_text
    i = len(s1)
    j = len(s2)
    ans = [direction_table[(i,j)]]
    # print str(i) + ", " + str(j)
    # print table[i][j]
    # print table[i][j][1]
    while i > 0 and j >0:
        if direction_table[(i,j)] == 'M':
            i = i-1
            j = j-1
        elif direction_table[(i,j)] == 'L':
            j = j-1
        elif direction_table[(i,j)] == 'U':
            i = i-1
        if direction_table[(i,j)] != None:
            ans.append(direction_table[(i,j)])
    print 'ans, ', ans
    # # L's are gaps on s1, U's are gaps on s2
    s1_final = ""
    s2_final = ""
    s1_count = 0
    s2_count = 0
    for i in range(len(ans)-1,-1,-1):
        if ans[i] == "L":
            s1_final = s1_final + SPACE_CHAR
            s2_final = s2_final + s2[s2_count]
            s2_count = s2_count + 1
        if ans[i] == "U":
            s1_final = s1_final + s1[s1_count]
            s2_final = s2_final + SPACE_CHAR
            s1_count = s1_count + 1
        if ans[i] == "M":
            s1_final = s1_final + s1[s1_count]
            s2_final = s2_final + s2[s2_count]
            s1_count = s1_count + 1
            s2_count = s2_count + 1
    print s1_final
    print s2_final
    #prints table
    print "tables"
    for i in range(len(s1_work)):
        for j in range(len(s2_work)):
            print '{:3}'.format(value_table[(i,j)]),
        print
    print "directions"
    for i in range(len(s1_work)):
        for j in range(len(s2_work)):
            print '{:4}'.format(direction_table[(i,j)]),
        print
        
    if enable_graphics:
        F = value_table
        board = init_board(len(s1),len(s2))
        screen = board[0]
        font = board[1]
        render_board(screen, font, s1, s2, F)
        pygame.display.flip()
        time.sleep(2)
    
    return s1_final, s2_final

def bestSoln(orig_a1, orig_a2, ret_a1, ret_a2, a1, a2):
    if len(ret_a1) != len(ret_a2):
        return False

    ansScore = 0
    for ctr in range(len(a1)):
        ansScore += s(a1[ctr], a2[ctr])

    retScore = 0
    for ctr in range(len(ret_a1)):
        retScore += s(ret_a1[ctr], ret_a2[ctr])

    if retScore > ansScore:
        return False

    orig_ctr = 0
    for ctr in range(len(ret_a1)):
        if ret_a1[ctr] != "_":
            if ret_a1[ctr] != orig_a1[orig_ctr]:
                return False
            orig_ctr += 1

    orig_ctr = 0
    for ctr in range(len(ret_a2)):
        if ret_a2[ctr] != "_":
            if ret_a2[ctr] != orig_a2[orig_ctr]:
                return False
            orig_ctr += 1
        
    return True

#################################################################################

if len(sys.argv) == 2 and sys.argv[1] == 'test':
    f=open('tests.txt', 'r');tests= eval(f.read());f.close()
    cnt = 0; passed = True
    for ((s1, s2), (a1, a2)) in tests:
        (ret_a1, ret_a2) = seq_align(s1, s2, False)
        #if (ret_a1 != a1) or (ret_a2 != a2):
        if( not bestSoln(s1, s2, ret_a1, ret_a2, a1, a2) ):
            print s1, s2 
            print a1, a2
            print ret_a1, ret_a2
            print("test#" + str(cnt) + " failed...")
            passed = False
        cnt += 1
    if passed: print("All tests passed!")
elif len(sys.argv) == 2 and sys.argv[1] == 'gentests':
    tests = []
    for n in range(25):
        m = random.randint(8, 70); n = random.randint(8, 70)
        (s1, s2) = (gen_random_string(dna_alph, m), gen_random_string(dna_alph, n))
        (a1, a2) = seq_align(s1, s2, False)
        tests.append(((s1, s2), (a1, a2)))
    f=open('tests.txt', 'w');f.write(str(tests));f.close()
else:
    l = [('ACACACTA', 'AGCACACA'), ('IMISSMISSISSIPI', 'MYMISSISAHIPPIE')]
    enable_graphics = True
    if enable_graphics: pygame.init()
    for (s1, s2) in l:
        print 'sequences:'
        print (s1, s2)
        
        m = len(s1)
        n = len(s2)
        
        print 'alignment: '
        print seq_align(s1, s2, enable_graphics)
    
    if enable_graphics: pygame.quit()
    
#####################################################
print time.clock() - start_time, "seconds"

