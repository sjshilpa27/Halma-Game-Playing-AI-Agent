import math
import heapq
import sys,time
from copy import copy
from getdist import *

class board:
    # start_time = time.time()
    filter_time = 0.0
    priority_time = 0.0
    sort_time = 0.0
    next_valid = 0.0
    def __init__(self,black_pos,white_pos,empty):

        self.black_pos = black_pos
        self.white_pos = white_pos
        self.empty = empty
        self.score = 0
        self.actions = [[0,1],[1,0],[0,-1],[-1,0],[-1,1],[1,-1],[-1,-1],[1,1]]
        self.black_home = {(0,0),(0,1),(0,2),(0,3),(0,4),(1,0),(1,1),(1,2),(1,3),(1,4),(2,0),(2,1),(2,2),(2,3),(3,0),(3,1),(3,2),(4,0),(4,1)}
        self.white_home = {(15,15),(15,14),(15,13),(15,12),(15,11),(14,15),(14,14),(14,13),(14,12),(14,11),(13,15),(13,14),(13,13),(13,12),(12,15),(12,14),(12,13),(11,15),(11,14)}
        self.eval = 0.0;

    def __str__(self):
        # s = time.time()
        matrix = [['.'] * 16 for i in range(16)]
        stri = ""
        for i in self.black_pos:
            #print(i)
            matrix[i[1]][i[0]] = 'B'
        for i in self.white_pos:
            matrix[i[1]][i[0]] = 'W'
        for each in matrix:
            stri+=''.join(each)+"\n"
        # print("__STR__" + str(time.time() - s))
        return stri



    def score_cal(self):
        # s = time.time()
        sum_black = 0
        sum_white = 0

        for each in self.black_pos:
            sum_black = sum_black + self.distance((15,15), each)
        for each in self.white_pos:
            sum_white = sum_white + self.distance((0, 0), each)

        self.eval = sum_black - sum_white
        # print("__Score_cal__" + str(time.time() - s))
        return self.eval

    def get_next_valid(self,player_turn):
        s = time.time()
        d = {}
        if player_turn == 'B':
            for x in self.black_pos:
                d[x] = self.adjacent_move(x)
                d[x] = d[x].union(self.jump_move(x))
        if player_turn == 'W':
            for x in self.white_pos:
                d[x] = self.adjacent_move(x)
                d[x] = d[x].union(self.jump_move(x))
        board.next_valid += time.time() - s
        # print(d)
        # print("\n")
        updated_list = self.filterr(d,player_turn)

        # while len(updated_list) != 0:
        #     print(heapq.heappop(updated_list))

        return updated_list

        # sorted_moves = self.priority(updated_dict,player_turn)
        # print(sorted_moves)
        # print("__getnextvalid__" + str(time.time() - s))
        # return sorted_moves


    def adjacent_move(self,x):
        # s = time.time()
        adj = set()
        for action in self.actions:
            if (x[0] + action[0],x[1] + action[1]) in self.empty:
                adj.add(('E',x, (x[0] + action[0],x[1] + action[1]),0))
        # print("__adj__" + str(time.time() - s))
        return adj



    def jump_move(self,y):
        # s = time.time()
        jumpqueue = []
        visited = set()
        ret = set()
        y = ('J',None,y,0)
        #jumpqueue.append(y)
        c = 0
        heapq.heappush(jumpqueue,(c,y))
        visited.add(y[2])
        while len(jumpqueue) != 0:
            x = heapq.heappop(jumpqueue)[1]
            print(x)

            ret.add(x)
            #del jumpqueue[0]

            for action in self.actions:
                if (x[2][0] + action[0], x[2][1] + action[1]) not in self.empty and (x[2][0] + 2 * action[0], x[2][1] + 2 * action[1]) in self.empty and (x[2][0] + 2 * action[0], x[2][1] + 2 * action[1]) not in visited:
                    c += 1
                    heapq.heappush(jumpqueue,(c,('J',x,(x[2][0] + 2 * action[0], x[2][1] + 2 * action[1]),x[3]+1)))
                    visited.add((x[2][0] + 2 * action[0], x[2][1] + 2 * action[1]))
        ret.remove(y)
        # print("__jump__" + str(time.time() - s))
        return ret


    def filterr(self,d,player_turn):
        s = time.time()
        if player_turn == "W":
            home = self.white_home
            opp_home = self.black_home
        elif player_turn == "B":
            home = self.black_home
            opp_home = self.white_home
        out = {0:[],1:[],2:[],3:[]}
        counter = 0
        # filter_out = {}
        # checkinhome = False
        # checkouthome = False
        for src in d:
            moves = d[src]
            flag = 0
            # if src in home:
            #     checkinhome = True
            # if checkinhome and src not in home:
            #     filter_out[src] = set()
            # if checkouthome and src in home:
            #     filter_out[src] = set()
            # out[1][src] = set()
            # out[2][src] = set()
            # out[3][src] = set()
            # filter_out[src] = set()
            for move in moves:
                # print("----------------")
                # print(move)
                # print("----------------")
                dest = move[2]
                # if (not checkinhome) and checkouthome and src in home and dest in home:
                #     filter_out[src].add(move)
                #     # print("-------10--------")
                #     # print(move)
                #     # print("----------------")
                # if checkinhome and src not in home:
                #     # continue
                #     # print("-------7--------")
                #     # print(move)
                #     # print("----------------")
                #     filter_out[src].add(move)
                direction = 0
                if player_turn == 'W':
                    corner = (0, 0)
                    if ((src[0] - dest[0] > 0) and (src[1] - dest[1] > 0)):
                        direction = 0
                        # counter1 += 1

                    elif ((src[0] - dest[0] == 0) or (src[1] - dest[1] == 0)):
                        direction = 1
                    else:
                        direction = 2
                else:
                    corner = (15, 15)
                    if (dest[0] - src[0] > 0 and dest[1] - src[1] > 0):
                        direction = 0
                    elif (dest[0] - src[0] == 0 or dest[1] - src[1] == 0):
                        direction =1
                    else:
                        direction = 2
                        # counter2 -= 1
                if src not in home and dest in home:
                    # d[src].remove(move)
                    # print("------6---------")
                    # print(move)
                    # print("----------------")
                    continue
                    # print("ASAAAAAAAA")

                elif src in opp_home and dest not in opp_home:
                    # print("-----5----------")
                    # print(move)
                    # print("----------------")
                    continue
                elif src not in opp_home and dest in opp_home:
                    heapq.heappush(out[0], (direction, self.distance(corner, dest), -move[3], counter, move))
                    counter += 1
                elif src in home and dest not in home:
                    # out[src].add(move)
                    # print("------1---------")
                    # print(move)
                    # print("----------------")
                    # flag = 1
                    # if src not in out[1]:
                    #     out[1][src]=set()
                    # out[1][src].add(move)
                    # checkouthome = True
                    heapq.heappush(out[1],(direction,self.distance(corner,dest),-move[3],counter,move))
                    counter += 1


                # elif flag == 1 and src in home and dest in home:
                #     # print("------2---------")
                #     # print(move)
                #     # print("----------------")
                #     out[2][src].add()
                #     continue
                elif src in home and dest in home:
                    if player_turn == 'W' and (src[0] - dest[0] < 0 or src[1] - dest[1] < 0) or dest == src:
                        # print("-----3----------")
                        # print(move)
                        # print("----------------")
                        continue
                    elif player_turn == 'B' and (dest[0] - src[0] < 0 or dest[1] - src[1] < 0) or dest == src:
                        # print("-----4----------")
                        # print(move)
                        # print("----------------")
                        continue
                    else:
                        # print("--------9-------")
                        # print(move)
                        # print("----------------")
                        # if src not in out[2]:
                        #     out[2][src] = set()
                        # out[2][src].add(move)
                        heapq.heappush(out[2], (direction, self.distance(corner, dest), -move[3], counter, move))
                        counter += 1
                else:
                    # print("--------8-------")
                    # print(move)
                    # print("----------------")
                    # if src not in out[3]:
                    #     out[3][src]=set()
                    # out[3][src].add(move)
                    heapq.heappush(out[3], (direction,  self.distance(corner, dest), -move[3], counter, move))
                    counter += 1
        # empty = False
        # print("\nout\n")
        # print(out)
        # for each in out:
        #     if len(out[each]) == 0:
        #         empty = True
        #     else:
        #         empty = False
        #         break
        # print(empty)
        # if empty:
        #     # print("Adding")
        #     for each in filter_out:
        #         out[each] = filter_out[each]
        # print("\nfilter_out\n")
        # print(filter_out)
        # print("\nout\n")
        # print(out[1])

        # print("__filter__" + str(time.time() - s))
        board.filter_time += time.time() - s
        if len(out[1]) > 0:
            return out[1]
        elif len(out[2]) > 0:
            return out[2]
        elif len(out[0]) > 0:
            return out[0]
        else:
            return out[3]


    def distance(self,corner,coord):
        return math.sqrt((corner[0]-coord[0])**2 + (corner[1]-coord[1])**2)
        # return get_dist(corner,coord)
        # return max(abs(corner[0]-coord[0]),abs(corner[1]-coord[1]))

    def priority(self, d,player_turn):
        s = time.time()
        if player_turn == 'W':
            corner = (0,0)
        elif player_turn == 'B':
            corner = (15,15)
        jump_d = []
        adj_d = []

        for key in d:
            for each in d[key]:
                if each[0] == 'J':
                    jump_d.append((key,each))
                elif each[0] == 'E':
                    adj_d.append((key,each))

        # print("\nJUMPD")
        # print(jump_d)
        # print("\nADJ_d")
        # print(adj_d)

        # jump_sort= self.all_sort(jump_d,player_turn,corner)
        # adj_sort = self.all_sort(adj_d,player_turn,corner)
        # print("\nall_sort")
        all_sort = self.all_sort(jump_d + adj_d , player_turn, corner)
        # print(all_sort)
        # print("\naall_sort")
        # aall_sort = self.all_sort(adj_d + jump_d, player_turn, corner)
        # print(aall_sort)
        # print("__priority__" + str(time.time() - s))
        board.priority_time += time.time() - s
        return all_sort


    def all_sort(self,list,player_turn,corner):
        s = time.time()
        l = []
        # counter1 = 0
        # counter2 = len(list)
        for each in list:
            src = each[0]
            dest = each[1][2]
            #print(src,dest)
            if player_turn == 'W':
                if((src[0] - dest[0] > 0) and (src[1] - dest[1] > 0)) :
                    l.append((0, -each[1][3], self.distance(corner,dest), each[1]))
                    # counter1 += 1

                else:
                    l.append((1,-each[1][3], self.distance(corner,dest), each[1]))
                    # counter2 -=1

            elif player_turn == 'B':
                if (src[0] - dest[0] > 0 and src[1] - dest[1] > 0):
                    l.append((1, -each[1][3], self.distance(corner, dest), each[1]))
                    # counter1 += 1

                else:
                    l.append((0, -each[1][3], self.distance(corner, dest), each[1]))
                    # counter2 -= 1


        l.sort(key=lambda t:(t[0],t[1],t[2]))

        # print("l\n"+str(l))
        # print("__allsort__" + str(time.time() - s))
        board.sort_time += time.time() - s
        return l

    # #def isvalid_jump(self,x):
    #
    # def isvalid(self,i,j):
    #     if (i,j) in self.empty and 0 <= i < 16 and 0 <= j < 16:
    #         return True
    #     return False


    def goal_check(self):
        if self.black_pos == self.white_home:
            return 'B'
        elif self.white_pos == self.black_home:
            return 'W'
        else:
            return 'E'

class halma:
    minimax_time = 0.0
    w = 0.0
    countt = 0
    limit = 2
    def __init__(self):
        self.initialboard = None
        self.mode = ""
        self.player = ""
        self.time = 0.0
        self.moves = 76

    def playgame(self):
        s = time.time()
        if self.mode == "SINGLE":
            self.single_mode()
            # print("__playgame__" + str(time.time() - s))
        elif self.mode == "GAME":
            self.game_mode()
        # print("__playgame__" + str(time.time() - s))
        # print("Filter:"+str(board.filter_time))
        # print("Priority:" + str(board.priority_time))
        # print("Sort:" + str(board.sort_time))
        # print("Next Valid:" + str(board.next_valid))
        # print("Minimax_time:" + str(halma.minimax_time))
        # print("copy_time:" + str(halma.w))

    def minimax(self,b,depth,player_turn,alpha,beta):
        s = time.time()
        g = b.goal_check()

        if depth == halma.limit or g != 'E':
            if g == 'W':
                return b.score_cal() + 50
            elif g == 'B':
                return b.score_cal() - 50
            return b.score_cal()

        if player_turn == 'W':
            best_val = - sys.maxsize
            moves = b.get_next_valid('W')
            c = 0
            while len(moves) != 0:
                c += 1
                if c == 30:
                    break
                each = heapq.heappop(moves)
                if each[4][0] == 'J':
                    src = self.src_find(each[4])
                else:
                    src = each[4][1]
                dest = each[4][2]
                t = time.time()
                new_white = copy(b.white_pos)
                new_white.remove(src)
                new_white.add(dest)
                new_empty = copy(b.empty)

                new_empty.remove(dest)
                new_empty.add(src)
                # halma.countt += 1
                # print(time.time() - t,halma.countt)

                halma.w += time.time() - t

                newboard = board(b.black_pos,new_white,new_empty)

                val = self.minimax(newboard,depth+1,'B',alpha,beta)
                best_val = max(best_val,val)
                alpha = max(best_val,alpha)

                if alpha >= beta:
                    break
            # print("__minimaxW__" + str(time.time() - s))
            halma.minimax_time += time.time() - s
            return best_val
        else:
            best_val = sys.maxsize
            moves = b.get_next_valid('B')
            c = 0
            while len(moves) != 0:
                c += 1
                if c == 30:
                    break
                each = heapq.heappop(moves)
                if each[4][0] == 'J':
                    src = self.src_find(each[4])
                else:
                    src = each[4][1]
                dest = each[4][2]
                new_black = copy(b.black_pos)
                new_black.remove(src)
                new_black.add(dest)
                new_empty = copy(b.empty)
                new_empty.remove(dest)
                new_empty.add(src)

                newboard = board(new_black, b.white_pos, new_empty)

                val = self.minimax(newboard, depth + 1, 'W',alpha,beta)

                best_val = min(best_val, val)
                beta = min(best_val,beta)

                if alpha >= beta:
                    break
            # print("__minimaxB__" + str(time.time() - s))
            halma.minimax_time += time.time() - s
            return best_val


    def minimax_driver(self,b,player_turn):
        s = time.time()
        #print(halma.limit)
        #print("---------------------------------")
        if player_turn == 'W':
            best_val = - sys.maxsize
            best_move = None
            best_board = None
            moves = b.get_next_valid('W')
            print(moves)
            if halma.limit == 0:
                #print(halma.limit)
                #print(moves[0][4])
                return moves[0][4],best_board
            #print("White Branching:"+str(len(moves)))
            c = 0
            while len(moves) != 0:
                c += 1
                if c==30:
                    break
                each = heapq.heappop(moves)
                s = time.time()
                # print(each)
                if each[4][0] == 'J':
                    src = self.src_find(each[4])
                else:
                    src = each[4][1]
                dest = each[4][2]
                new_white = copy(b.white_pos)
                new_white.remove(src)
                new_white.add(dest)
                new_empty = copy(b.empty)
                new_empty.remove(dest)
                new_empty.add(src)

                newboard = board(b.black_pos,new_white,new_empty)
                s1 = time.time()
                val = self.minimax(newboard,0,'B',-sys.maxsize,sys.maxsize)
                # print("Val:"+str(val))
                # print(time.time()-s1)
                if val > best_val:
                    best_move = each[4]
                    best_val=val
                    best_board = newboard
                # print("__DriverminimaxW__" + str(time.time() - s))
                # print("Filter:" + str(board.filter_time))
                # print("Priority:" + str(board.priority_time))
                # print("Sort:" + str(board.sort_time))
                # print("Next Valid:" + str(board.next_valid))
                # print("Minimax_time:" + str(halma.minimax_time))
            print(best_board)
            #print("__DriverminimaxW__" + str(time.time() - s))
            # print(best_val)
            return best_move,best_board

        else:
            best_val = sys.maxsize
            best_move = None
            moves = b.get_next_valid('B')
            #print("Black Branching:" + str(len(moves)))
            best_board = None
            if halma.limit == 0:
                return moves[0][4], best_board
            c = 0
            while len(moves) != 0:
                c += 1
                if c == 30:
                    break
                each = heapq.heappop(moves)
                if each[4][0] == 'J':
                    src = self.src_find(each[4])
                else:
                    src = each[4][1]
                dest = each[4][2]
                new_black = copy(b.black_pos)
                new_black.remove(src)
                new_black.add(dest)
                new_empty = copy(b.empty)
                new_empty.remove(dest)
                new_empty.add(src)

                newboard = board(new_black, b.white_pos, new_empty)

                val = self.minimax(newboard, 0, 'W',-sys.maxsize,sys.maxsize)
                if val < best_val:
                    best_move = each[4]
                    best_val = val
                    best_board = newboard
            #print(best_board)
            #print("__DriverminimaxB__" + str(time.time() - s))
            return best_move,best_board

    def src_find(self,move):
        # print(move)
        while move[1] != None:
            move = move[1]
        return move[2]

    def input(self,input_file):
        s = time.time()
        f = open(input_file)
        l = f.readlines()
        self.mode = l[0].strip()
        self.player = l[1][0]
        self.time = float(l[2].strip())
        black = set()
        white = set()
        empty = set()
        """
        input logic
        """
        for i in range(3,3+16,1):
            temp = l[i].strip()
            for j in range(len(temp)):
                if temp[j] == 'B':
                    black.add((j,i-3))
                elif temp[j] =='W':
                    white.add((j,i-3))
                else:
                    empty.add((j,i-3))

        self.initialboard = board(black,white,empty)
        print(self.initialboard)
        self.initialboard.score_cal()
        #print(self.initialboard.eval)
        # print("__input__" + str(time.time() - s))

    def single_mode(self):
        # self.initialboard.get_next_valid(self.player)
        # print(self.minimax_driver(self.initialboard, self.player))
        x = self.minimax_driver(self.initialboard, self.player)[0]
        self.output(x)


    def getdepth(self):
        ti = self.time
        if(self.moves>0):
            ti/=self.moves
        #print(ti)
        if(ti<5):
            return 0
        elif(ti<10):
            return 1
        return 2

    def game_mode(self):

        try:
            f = open('playdata.txt','r')
            self.moves=int(f.readlines()[0])
        except:
            pass
        halma.limit = self.getdepth()
        self.single_mode()
        self.moves -= 1
        f = open('playdata.txt', 'w')
        f.write(str(self.moves))
        f.close()
        # board_= self.initialboard
        # w_cnt = 0
        # b_cnt = 0
        # while board_.goal_check() == 'E':
        #     w_cnt +=1
        #     move,board_ = self.minimax_driver(board_,'B')
        #     print("White moves completed:"+str(w_cnt))
        #     b_cnt +=1
        #     move, board_ = self.minimax_driver(board_,'W')
        #     print("BLack moves completed:" + str(b_cnt))
        # pass

    def output(self, move):
        print(move)
        f = open("output.txt", "w")
        s = ""
        if move[0] == 'J':
            l = []
            while(move[1]!=None):
                l.append(move[0] + " " + str(move[1][2][0]) + "," + str(move[1][2][1]) + " " + str(move[2][0]) + "," + str(move[2][1]))
                move = move[1]
            l.reverse()
            s = "\n".join(l)
            #print(l)
        elif move[0] == 'E':
            s = move[0] + " " + str(move[1][0]) + "," + str(move[1][1]) + " " + str(move[2][0]) + "," + str(move[2][1])
        f.write(s)
        f.close()

if __name__ == '__main__':
    t = time.time()
    h = halma()
    h.input("input_voc4")
    h.playgame()
    print(time.time()- t)