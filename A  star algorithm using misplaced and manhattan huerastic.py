## ## implementation of A* algorithm using misplaced and manhattan heuristic
import numpy as np
class Node:
    def __init__(self, d, level, fv):

        self.d = d
        self.level = level
        self.fv = fv

    def g_child(self):

        x, y = self.finding_blank_row_column(self.d, '_')
        childs = []
        val = [[x, y - 1], [x, y + 1], [x - 1, y], [x + 1, y]]
        for i in val:
            c = self.moving_blank(self.d, x, y, i[0], i[1])
            if c is not None:
                c_node = Node(c, self.level + 1, 0)
                childs.append(c_node)
        return childs

    def moving_blank(self, mt, x1, y1, x2, y2):

        if x2 >= 0 and x2 < len(self.d) and y2 >= 0 and y2 < len(self.d):
            temp_mt = []
            temp_mt = self.make_copy(mt)
            t = temp_mt[x2][y2]
            temp_mt[x2][y2] = temp_mt[x1][y1]
            temp_mt[x1][y1] = t
            return temp_mt
        else:
            return None

    def make_copy(self, nd):

        temp = []
        for i in nd:
            t = []
            for j in i:
                t.append(j)
            temp.append(t)
        return temp

    def finding_blank_row_column(self, puz, x):

        for i in range(0, len(self.d)):
            for j in range(0, len(self.d)):
                if puz[i][j] == x:
                    return i, j
import time


class Puz_8:
    def __init__(self, size):

        self.no = size
        self.open = []
        self.close = []

    def take_input(self):

        p = []
        for i in range(0, self.no):
            t = input().split(" ")
            p.append(t)
        return p

    def choose_heuristic(self):
        n = int(input())
        return n

    def index_2d(self,data,element):
        for i in range(len(data)):
            if element in data[i]:
                return  i,data[i].index(element)

    def fx(self, start, goal,n):
        if(n==1):
            return self.hx_misplaced(start.d, goal) + start.level
        elif(n==2):
            return self.hx_manhattan(start.d, goal) + start.level

    def hx_misplaced(self, start, goal):

        t = 0
        for i in range(0, self.no):
            for j in range(0, self.no):
                if start[i][j] != goal[i][j] and start[i][j] != '_':
                    t = t + 1
        return t
    def hx_manhattan(self,state,goal):
        dist=0
        for i in range(len(state)):
            for j in range(len(state[i])):
                goal_i,goal_j=self.index_2d(goal,state[i][j])
                dist+=abs(i-goal_i)+abs(j-goal_j)
        return dist

    def cal(self):

        print("Enter the start matrix:")
        start = self.take_input()
        print("Enter the goal matrix:")
        goal = self.take_input()

        print("Choose Heuristic Function:\n1.No. of Misplaced Tiles\n2. Manhattan Distance")
        n = self.choose_heuristic()

        ## initializing starting time for execution
        start_time = time.time()
        print("\nexecution start time:{}\n".format(start_time), end=" ")
        start = Node(start, 0, 0)
        start.fv = self.fx(start, goal,n)
        optimal_path_cost = 0
        self.open.append(start)
        visited=[]
        optimal_state_expl = 1
        print("\noptimal path is follows:\n")
        while True:
            i=0
            while i < len(self.open):
                current = self.open[i]
                if current.d not in visited:
                    break
                i=i+1
            optimal_path_cost = optimal_path_cost + current.fv
            print("\nstate: {}\n".format(optimal_state_expl))
            for i in current.d:
                for j in i:
                    print(j, end=" ")
                print("")
            if(n==1):
                hurastic = self.hx_misplaced(current.d, goal)
            else:
                hurastic = self.hx_manhattan(current.d, goal)

            ## checking if state is matching to goal state or not
            if (hurastic == 0):

                print("\nstate has been matched to goal state successfully.\n")

                ## printing last state which is goal state
                print("\nGoal state is :\n")
                for i in current.d:
                    for j in i:
                        print(j, end=" ")
                    print("")
                ## optimal number of state 
                print("\nNumber of optimal state are {}\n".format(optimal_state_expl))

                ##printing number of state which has been explored
                total_count = len(self.close) + len(self.open)
                print("\nNumber of state which has been explored are {}\n".format(total_count))

                print("\nOptimal path cost is:{}\n".format(optimal_path_cost))

                end_time = time.time()
                print("\nend time:{}\n".format(end_time), end=" ")
                exec_time = end_time - start_time
                print("\ntime taken for program execution :{}".format(exec_time))
                break
            for i in current.g_child():
                i.fv = self.fx(i, goal,n)
                self.open.append(i)
            self.close.append(current)
            visited.append(current.d)
            del self.open[0]
            ##sorting list according to fx value
            self.open.sort(key=lambda x: x.fv, reverse=False)
            optimal_state_expl = optimal_state_expl + 1


p = Puz_8(3)
p.cal()
