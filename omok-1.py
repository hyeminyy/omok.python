# -*- coding: utf-8 -*-
"""
Maker : bychoi@deu.ac.kr 

@author: Com
"""

# sample player file which must be made by student 

from player import *
from stone import *
from random import *

class iot12345_student(player):
     def __init__(self, clr):
          super().__init__( clr)  # call constructor of super class, self 제거
          self.__ai = gomoku_ai(clr)
     
        
     def __del__(self):  # destructor
         pass 
     def __init__(self, clr):
        self._color = clr 
        self._t_cnt = 0
        self.__data_set = [[0 for i in range(19)] for j in range(19)]
        if clr == -1: 
            self.__attack = 1
        else:
            self.__attack = 0
 
        self.__data_set1 = [[0 for i in range(19)] for j in range(19)] #날일진 저장 보드
        self.__data_set2 = [[0 for i in range(19)] for j in range(19)] #날일진 저장 보드 2
 
        self.__dx = [0,1,1,1,0,-1,-1,-1] #한칸 기준 8방향의 x값
        self.__dy = [-1,-1,0,1,1,1,0,-1] #한칸 기준 8방향의 y값
        self.__dx1 = [0,1,2,2,2,2,2,1,0,-1,-2,-2,-2,-2,-2,-1] #두 칸 기준의 x값
        self.__dy1 = [-2,-2,-2,-1,0,1,2,2,2,2,2,-1,0,-1,-2,-2]#두 칸 기준의 y값
        self.__b_len = 19 #보드 크기
        self.__score_four = 450 #사목이 만들어지는 가중치
        self.__score_four_2 = 450#사목이 만들어지는 가중치
       # self.__score_three= 400 #삼목이 만들어지는 가중치
        self.__score_three_2= 370#띈 삼목이 만들어지는 가중치
        self.__f_d = 150 #방어시 위의 가중치에서 빼짐
        self.__t_d =150 #방어시 위의 가중치에서 빼짐
        self.__two_d = 5 #방어시 열린 2목의 경우 20에서 5를 뺌
    
     def Calc_Position(self, board):
        stn = set()
        self.__b_len = len(board)
        for i in range(self.__b_len-1,-1,-1): #상하좌우대각선으로 한 칸 범위에서 놓을 수 있는 좌표를 저장
            for j in range(self.__b_len):
                if board[i][j] == 0:
                    continue
            
                for k in range(8):
                    if (i+self.__dx[k] >= 0 and i+self.__dx[k] < self.__b_len) and (j+self.__dy[k] >= 0 and j+self.__dy[k] < self.__b_len):
                        if board[i+self.__dx[k]][j+self.__dy[k]] == 0:
                            temp= (i+self.__dx[k], j+self.__dy[k])
                            stn.add(temp) 
                        
                    for i in range(self.__b_len-1,-1,-1): #상하좌우대각선으로 두 칸 범위에서 놓을 수 있는 좌표를 저장
                        for j in range(self.__b_len):
                            if board[i][j] == 0:
                                continue

                    for k in range(16):
                        if (i+self.__dx1[k] >= 0 and i+self.__dx1[k] < self.__b_len) and (j+self.__dy1[k] >= 0 and j+self.__dy1[k] < self.__b_len):
                            if board[i+self.__dx1[k]][j+self.__dy1[k]] == 0:
                                temp= (i+self.__dx1[k], j+self.__dy1[k])
                                stn.add(temp)
                                stn = list(stn)
                                
                return stn

     def next_stone(self, board, length):
        if self._t_cnt == 0 and self._color == -1: #검은돌이 처음일 때 오목판의 중앙에 돌을 놓고 날일진 좌표 계산
            stn = stone(self._color, length)
            stn.setX(9)
            stn.setY(9)
            self.create_data_Set1(9, 9, self.__data_set1, self._color)
            self.create_data_Set2(9, 9, self.__data_set2, self._color)
            self._t_cnt = 1
            return stn
        able_stn = self.Calc_Position(board) #움직일 수 있는 돌의 좌표를 구함
        board_weight1 = [[0 for i in range(length)] for j in range(length)] #자신의 돌의 가중치 보드
        board_weight2 = [[0 for i in range(length)] for j in range(length)] #상대돌의 가중치 보드
 
        if self._t_cnt == 1: #두 번 째 차례일 때 계산한 두개의 날일진 좌표에 가중치를 더해줌
    
            self._t_cnt = 2
            for i in able_stn:
                board_weight1[i[0]][i[1]] += abs(self.__data_set1[i[0]][i[1]]* 50)
                board_weight1[i[0]][i[1]] += abs(self.__data_set2[i[0]][i[1]]* 50)
        elif self._t_cnt == 2: #3번째 좌표일 때 어느 날일진에 해당하는지 계산함
            self._t_cnt += 1 #만약 날일진에 해당하지 않는다면 날일진을 사용하지 않음
 
        if self.match_dataset(board, self.__data_set1, 2):
            self.__data_set = self.__data_set1
        elif self.match_dataset(board, self.__data_set2, 2):
                self.__data_set = self.__data_set2
 
        self.Calc_val(board, board_weight1, able_stn, self._color) #현재 놓여진 돌을 기반으로 랜덤성을 부여하기 위해 계산
        self.Calc_val(board, board_weight2, able_stn, self._color*-1)#현재 놓여진 돌을 기반으로 랜덤성을 부여하기 위해 계산
 
        for i in able_stn: #공격에 해당되는 가중치를 구함 자신이 공격 중 일 경우 자신의 공격의 가중치가 더 높고
            if self.__attack == 1: #방어 중 일 경우 상대의 공격 가중치가 더 높아짐
                self.Calc_Attack(board, board_weight2, self._color*-1, i, 1)
                self.Calc_Attack(board, board_weight1, self._color, i, 0)
            else:
                self.Calc_Attack(board, board_weight2, self._color*-1, i, 0)
                self.Calc_Attack(board, board_weight1, self._color*-1, i, 1)
 
        temp3 = copy.deepcopy(board_weight1) 
        for i in able_stn: #더 유리한 수를 찾기 위해 각각의 가중치를 1/2씩 더함
            board_weight1[i[0]][i[1]] += (board_weight2[i[0]][i[1]]//2) # + 
            (self.__data_set[able_stn[i][0]][able_stn[i][1]] * 50)  
            board_weight2[i[0]][i[1]] += ((temp3[i[0]][i[1]]//2) + abs(self.__data_set[i[0]][i[1]] * 70))
        del temp3
 
        temp = self.calc_Max(board_weight1, able_stn) #자신의 가중치중 가장 높은 두개를 구함
        temp2 = self.calc_Max(board_weight2, able_stn)#상대의 가중치중 가장 높은 두개를 구함
 
        self.print_b(board_weight1, board_weight2)
        if temp[0][2] < temp2[0][2]: #자신의 가중치가 높을 경우 공격하고 있는 상태로 바뀜
 
            temp = temp2
            self.__attack = 0 #상대의 가중치가 높을 경우 방어로 바뀜
        else:
            self.__attack = 1

        if self.__attack == 0 and temp2[0][2] < 300: #자신과 상대의 공격수가 없을 경우 자신을 공격으로 바꿈
            self.__attack = 1
        
        if temp[0][2] < temp[1][2] + 130: #자신 또는 상대가 공격중일 경우 더욱 유리한 곳으로 공격 또는 방어를 진행
            board[temp[0][0]][temp[0][1]] = self._color
            board_weight = [[0 for i in range(19)] for j in range(19)]
            able_stn = self.Calc_Position(board)
 
        for i in able_stn:
            if self.__attack == 1:
                self.Calc_Attack(board, board_weight, self._color, i, 0)
            else:
                self.Calc_Attack(board, board_weight, self._color*-1, i, 0)
        max_weight1 = self.calc_Max(board_weight, able_stn)
 
        board[temp[1][0]][temp[1][1]] = self._color 
        board[temp[0][0]][temp[0][1]] = 0
 
        board_weight = [[0 for i in range(19)] for j in range(19)]
        able_stn = self.Calc_Position(board)
 
        for i in able_stn:
            if self.__attack == 1:
                self.Calc_Attack(board, board_weight, self._color, i, 0)
            else:
                self.Calc_Attack(board, board_weight, self._color*-1, i, 0)
            max_weight2 = self.calc_Max(board_weight, able_stn)
        if max_weight2 > max_weight2:
            temp[0] = temp[1]
 
 
 
        stn = stone(self._color, length)
        stn.setX(temp[0][0])
        stn.setY(temp[0][1])
 
        if self._t_cnt == 0 and self._color == 1: #흰돌이 첫 수 일 때 놓여진 좌표로 날일진 좌표를 구함
            self._t_cnt = 1
            self.create_data_Set1(temp[0][0], temp[0][1], self.__data_set1, self._color)
            self.create_data_Set2(temp[0][0], temp[0][1], self.__data_set2, self._color)


        return stn 

     def Calc_val(self, board, board_weight, able_ctn ,clr): #랜덤성을 구하기 위한 함수
        for p in able_ctn:
            for k in range(8):
                cx = p[0]+self.__dx[k]
                cy = p[1]+self.__dy[k]
                if (cx >= 0 and cx < self.__b_len) and (cy >= 0 and cy < self.__b_len):
                    if board[cx][cy] == clr:
                        board_weight[p[0]][p[1]] += 2
                        board_weight[p[0]][p[1]] += random.randint(-3,3)
                    

     def Calc_Attack(self, board, board_weight, clr, p, t):
        x = p[0] #계산할 좌표 x
        y = p[1] #계산할 좌표 y
        # 주석의 1 x 1 1 1 들의 의미
        # x : 놓여지는 좌표
        # 1 : 자신이 놓은 돌
        # -1: 상대가 놓은돌
        # 0 : 아무도 놓지 않은 경우
        #반복문을 통해 4방향 혹은 8방향에 대해서 가중치 검사를 진
        for i in range(4): #4방향 공격검사
            cx1 = x+self.__dx[i]*2
            cy1 = y+self.__dy[i]*2
            cx2 = x+self.__dx[i]
            cy2 = y+self.__dy[i]
            cx3 = x-self.__dx[i]
            cy3 = y-self.__dy[i]
            cx4 = x-self.__dx[i]*2
            cy4 = y-self.__dy[i]*2
            
            if cx1 < 0 or cx1 >= self.__b_len or cy1 < 0 or cy1 >= self.__b_len or\
                cx2 < 0 or cx2 >= self.__b_len or cy2 < 0 or cy2 >= self.__b_len or\
                    cx3 < 0 or cx3 >= self.__b_len or cy3 < 0 or cy3 >= self.__b_len or\
                        cx4 < 0 or cx4 >= self.__b_len or cy4 < 0 or cy4 >= self.__b_len:
                continue

        stn_count = board[cx2][cy2] + board[cx3][cy3] +\
            board[cx1][cy1] + board[cx4][cy4]
        if stn_count == 4*clr:# 1 1 x 1 1
            board_weight[x][y] += 10000 #오목 완성
 
        for i in range(8): #1*4 공격검사
            cx1 = x+self.__dx[i]*4
            cy1 = y+self.__dy[i]*4
            cx2 = x+self.__dx[i]*3
            cy2 = y+self.__dy[i]*3
            cx3 = x+self.__dx[i]*2
            cy3 = y+self.__dy[i]*2
            cx4 = x+self.__dx[i]
            cy4 = y+self.__dy[i]
            cx5 = x-self.__dx[i]
            cy5 = y-self.__dy[i]
            if cx1 >= 0 and cx1 < self.__b_len and cy1 >= 0 and cy1 < self.__b_len and\
                cx2 >= 0 and cx2 < self.__b_len and cy2 >= 0 and cy2 < self.__b_len and\
                    cx3 >= 0 and cx3 < self.__b_len and cy3 >= 0 and cy3 < self.__b_len and\
                        cx4 >= 0 and cx4 < self.__b_len and cy4 >= 0 and cy4 < self.__b_len and\
                            cx5 >= 0 and cx5 < self.__b_len and cy5 >= 0 and cy5 < self.__b_len :
 
                            if board[cx4][cy4] ==clr and board[cx3][cy3] ==clr and  board[cx2][cy2] == clr:
                                if board[cx5][cy5] == 0 and board[cx1][cy1] == 0:#0 x 1 1 1 0
                                    board_weight[x][y] += 5000 #승리조건
                                    board_weight[x][y] -= (t*1000)
                            elif board[cx5][cy5] == 0 and board[cx1][cy1] == clr*-1:#0 x 1 1 1 -1
                                board_weight[x][y] += self.__score_four #4목 공격
                                board_weight[x][y] -= (t*self.__f_d)
       #print("0 x 1 1 1 -1 : (",x,",",y,")")
 
                            elif board[cx5][cy5] == 0 and board[cx1][cy1] == 0 and board[cx2][cy2] == clr:
                                if board[cx4][cy4] == clr and board[cx3][cy3] == 0: #0 x 1 0 1 0
                                    board_weight[x][y] += self.__score_three_2 #3공격일때 가중치
                                    board_weight[x][y] -= (t*self.__t_d)
            #print("0 x 1 0 1 0 : (",x,",",y,")")
                                elif board[cx3][cy3] == clr and board[cx4][cy4] == 0: #0 x 0 1 1 0
                                    board_weight[x][y] += self.__score_three_2 #3공격일때 가중치
                                    board_weight[x][y] -= (t*self.__t_d)
        #print("0 x 0 1 1 0 : (",x,",",y,")")
 
    ### 방어가 되어있고 3이 만들어지는 수
                                elif board[cx5][cy5] == 0 and board[cx1][cy1] == -1 * clr and board[cx2][cy2] == clr:
                                    if board[cx4][cy4] == clr and board[cx3][cy3] == 0: #0 x 1 0 1 -1
                                        board_weight[x][y] += 50
                                        board_weight[x][y] -= (t*self.__two_d)
 
                                elif board[cx4][cy4] == 0 and board[cx3][cy3] == clr: #0 x 0 1 1 -1
                                    board_weight[x][y] += 50
                                    board_weight[x][y] -= (t*self.__two_d)

                                elif board[cx5][cy5] == -1*clr and board[cx1][cy1] == 0 and board[cx2][cy2] == clr:
                                        if board[cx4][cy4] == clr and board[cx3][cy3] == 0: #-1 x 1 0 1 0
                                            board_weight[x][y] += 50
                                            board_weight[x][y] -= (t*self.__two_d)
 
                                elif board[cx4][cy4] == 0 and board[cx3][cy3] == clr: #-1 x 0 1 1 0
                                        board_weight[x][y] += 50
                                        board_weight[x][y] -= (t*self.__two_d)
 
                ##뚫린 2가 만들어지는 경우
                                elif board[cx5][cy5] == 0 and board[cx1][cy1] == 0 and board[cx2][cy2] == clr\
                                    and board[cx3][cy3] == 0 and board[cx4][cy4] == 0: # 0 x 0 0 1 0
                                    board_weight[x][y] += 20
                                    board_weight[x][y] -= (t*self.__two_d)
 
    #1*3 공격검사
        cx1 = x+self.__dx[i]*3
        cy1 = y+self.__dy[i]*3
        cx2 = x+self.__dx[i]*2
        cy2 = y+self.__dy[i]*2
        cx3 = x+self.__dx[i]
        cy3 = y+self.__dy[i]
        cx4 = x-self.__dx[i]
        cy4 = y-self.__dy[i]
        if cx1 >= 0 and cx1 < self.__b_len and cy1 >= 0 and cy1 < self.__b_len and\
            cx2 >= 0 and cx2 < self.__b_len and cy2 >= 0 and cy2 < self.__b_len and\
                cx3 >= 0 and cx3 < self.__b_len and cy3 >= 0 and cy3 < self.__b_len and\
                    cx4 >= 0 and cx4 < self.__b_len and cy4 >= 0 and cy4 < self.__b_len :
                        
                        stn_count = board[cx3][cy3] + board[cx2][cy2]
        if stn_count == clr*2:
            if board[cx1][cy1] == clr and board[cx4][cy4] == clr:#1 x 1 1 1
                board_weight[x][y] += 10000 #오목 완성
                board_weight[x][y] -= (t*2000)
            elif board[cx1][cy1] == 0 and board[cx4][cy4] == 0: # 0 x 1 1 0
                board_weight[x][y] += self.__score_three #3공격일때 가중치
                board_weight[x][y] -= (t*self.__t_d)
 
            elif board[cx1][cy1] + board[cx4][cy4] == clr * 2:

                
                if board[cx2][cy2] == 0 and board[cx3][cy3] == clr: # 1 x 0 1 1
                    board_weight[x][y] += (self.__score_four_2-30) #4목 공격
                    board_weight[x][y] -= (t*self.__f_d)
            #print("-1 1 x 1 1 0 : (",x,",",y,")")
            #뚫린 2가 만들어지는 경우
        elif board[cx1][cy1] == 0 and board[cx4][cy4] == 0:
            if board[cx2][cy2] == clr and board[cx3][cy3] == 0:
                board_weight[x][y] += 20 # 0 x 1 0 0
                board_weight[x][y] -= (t*self.__two_d)
            elif board[cx2][cy2] == 0 and board[cx3][cy3] == clr:
                board_weight[x][y] += 20 # 0 x 0 1 0
                board_weight[x][y] -= (t*self.__two_d)
 
    #2*3 공격검사
        cx1 = x+self.__dx[i]*3
        cy1 = y+self.__dy[i]*3
        cx2 = x+self.__dx[i]*2
        cy2 = y+self.__dy[i]*2
        cx3 = x+self.__dx[i]
        cy3 = y+self.__dy[i]
        cx4 = x-self.__dx[i]
        cy4 = y-self.__dy[i]
        cx5 = x-self.__dx[i]*2
        cy5 = y-self.__dy[i]*2
        if cx1 >= 0 and cx1 < self.__b_len and cy1 >= 0 and cy1 < self.__b_len and\
            cx2 >= 0 and cx2 < self.__b_len and cy2 >= 0 and cy2 < self.__b_len and\
                cx3 >= 0 and cx3 < self.__b_len and cy3 >= 0 and cy3 < self.__b_len and\
                    cx4 >= 0 and cx4 < self.__b_len and cy4 >= 0 and cy4 < self.__b_len and\
                        cx5 >= 0 and cx5 < self.__b_len and cy5 >= 0 and cy5 < self.__b_len :
 
                            stn_count = board[cx4][cy4] + board[cx2][cy2]
        if stn_count == 2*clr:
            if board[cx3][cy3] == clr:
                if board[cx1][cy1] == 0 and board[cx5][cy5] == 0: #0 1 x 1 1 0
                    board_weight[x][y] += 5000 #승리조건
                    board_weight[x][y] -= (t*1000)
                elif board[cx5][cy5] == clr*-1 and board[cx1][cy1] == 0:#-1 1 x 1 1 0
                    board_weight[x][y] += self.__score_four #4목 공격
                    board_weight[x][y] -= (t*self.__f_d)
                    #print("-1 1 x 1 1 0 : (",x,",",y,")")
                elif board[cx5][cy5] == 0 and board[cx1][cy1] == clr*-1:#0 1 x 1 1 -1
                    board_weight[x][y] += (self.__score_four) #4목 공격
                    board_weight[x][y] -= (t*self.__f_d)
                    #print("0 1 x 1 1 -1 : (",x,",",y,")")
                elif board[cx3][cy3] == 0 and board[cx5][cy5] == 0\
                    and board[cx1][cy1] == 0: #0 1 x 0 1 0
                    board_weight[x][y] += self.__score_three_2 #3공격일때 가중치
                    board_weight[x][y] -= (t*self.__t_d)
                    #print("0 1 x 0 1 0 : (",x,",",y,")")
 
                elif board[cx4][cy4] == clr and board[cx3][cy3] == clr \
                    and board[cx2][cy2] == 0:
                        if board[cx5][cy5] == 0 and board[cx1][cy1] == 0: # 0 1 x 1 0 0
                            board_weight[x][y] += (self.__score_three/2) #3공격일때 가중치
                            board_weight[x][y] -= (t*self.__t_d/2)
     #print("0 1 x 1 0 0 : (",x,",",y,")")
                elif board[cx5][cy5] == 0 and board[cx1][cy1] == clr * -1: # 0 1 x 1 0 -1
                    board_weight[x][y] += self.__score_three #3공격일때 가중치
                    board_weight[x][y] -= (t*self.__t_d-10)
                    #print(" 0 1 x 1 0 -1 : (",x,",",y,")")
 
    #방어가 있고 3을 만드는 경우
                elif board[cx4][cy4] == clr and board[cx3][cy3] == 0 and board[cx2][cy2] == clr:
                    if board[cx5][cy5] == clr * -1 and board[cx1][cy1] == 0: #-1 1 x 0 1 0
                        board_weight[x][y] += 50
                        board_weight[x][y] -= (t*self.__two_d)
                elif board[cx1][cy1] == clr * -1 and board[cx5][cy5] == 0: #0 1 x 0 1 -1
                    board_weight[x][y] += 50
                    board_weight[x][y] -= (t*self.__two_d)
 
    #0*4 공격검사
            cx1 = x+self.__dx[i]*4
            cy1 = y+self.__dy[i]*4
            cx2 = x+self.__dx[i]*3
            cy2 = y+self.__dy[i]*3
            cx3 = x+self.__dx[i]*2
            cy3 = y+self.__dy[i]*2
            cx4 = x+self.__dx[i]
            cy4 = y+self.__dy[i]
            if cx1 >= 0 and cx1 < self.__b_len and cy1 >= 0 and cy1 < self.__b_len and\
                cx2 >= 0 and cx2 < self.__b_len and cy2 >= 0 and cy2 < self.__b_len and\
                 cx3 >= 0 and cx3 < self.__b_len and cy3 >= 0 and cy3 < self.__b_len and\
                  cx4 >= 0 and cx4 < self.__b_len and cy4 >= 0 and cy4 < self.__b_len: 
                     
                stn_count = board[cx2][cy2] + board[cx3][cy3] + board[cx1][cy1]
                if stn_count == 3*clr:
                    if board[cx4][cy4] == clr: #x 1 1 1 1
                        board_weight[x][y] += 10000 #오목 완성
                        board_weight[x][y] -= (t*2000)
                    elif board[cx4][cy4] == 0: #x 0 1 1 1
                        board_weight[x][y] += self.__score_four_2 #띈 4 공격
                        board_weight[x][y] -= (t*self.__f_d)
                    #print(" x 0 1 1 1 : (",x,",",y,")")
 
                    elif board[cx2][cy2] + board[cx1][cy1] + board[cx4][cy4] == 3* clr and \
                        board[cx3][cy3] == 0 : # 1 0 1 1 
                        board_weight[x][y] += self.__score_four_2 #띈 4 공격
                        board_weight[x][y] -= (t*self.__f_d)
                    elif board[cx3][cy3] + board[cx1][cy1] + board[cx4][cy4] == 3* clr and \
                        board[cx2][cy2] == 0 : # x 1 1 0 1
                        board_weight[x][y] += self.__score_four_2 #띈 4 공격
                        board_weight[x][y] -= (t*self.__f_d)
 
    #0*5 공격검사
        cx1 = x+self.__dx[i]*5
        cy1 = y+self.__dy[i]*5
        cx2 = x+self.__dx[i]*5
        cy2 = y+self.__dy[i]*4
        cx3 = x+self.__dx[i]*3
        cy3 = y+self.__dy[i]*3
        cx4 = x+self.__dx[i]*2
        cy4 = y+self.__dy[i]*2
        cx5 = x+self.__dx[i]
        cy5 = y+self.__dy[i]
        if cx1 >= 0 and cx1 < self.__b_len and cy1 >= 0 and cy1 < self.__b_len and\
            cx2 >= 0 and cx2 < self.__b_len and cy2 >= 0 and cy2 < self.__b_len and\
                cx3 >= 0 and cx3 < self.__b_len and cy3 >= 0 and cy3 < self.__b_len and\
                    cx4 >= 0 and cx4 < self.__b_len and cy4 >= 0 and cy4 < self.__b_len and\
                        cx5 >= 0 and cx5 < self.__b_len and cy5 >= 0 and cy5 < self.__b_len :
 
            #방어가 있고 3을 만드는 경우
            if board[cx2][cy2] == clr and board[cx3][cy3] == 0:
                if board[cx1][cy1] == -1*clr and board[cx4][cy4] == clr and board[cx5][cy5] == 0:
                    board_weight[x][y] += 50 # x 1 0 0 1 0
                    board_weight[x][y] -= (t*self.__two_d)
            elif board[cx1][cy1] == -1*clr and board[cx4][cy4] == 0 and board[cx5][cy5] == clr:
                board_weight[x][y] += 50 # x 1 0 0 1 -1
                board_weight[x][y] -= (t*self.__two_d)
            elif board[cx1][cy1] == 0 and board[cx4][cy4] == 0 and board[cx5][cy5] == clr:
                board_weight[x][y] += 50 # x 0 1 0 1 -1
                board_weight[x][y] -= (t*self.__two_d)
 
    #2*2 공격검사
        cx1 = x+self.__dx[i]*2
        cy1 = y+self.__dy[i]*2
        cx2 = x+self.__dx[i]
        cy2 = y+self.__dy[i]
        cx3 = x-self.__dx[i]
        cy3 = y-self.__dy[i]
        cx4 = x-self.__dx[i]*2
        cy4 = y-self.__dy[i]*2
        if cx1 >= 0 and cx1 < self.__b_len and cy1 >= 0 and cy1 < self.__b_len and\
            cx2 >= 0 and cx2 < self.__b_len and cy2 >= 0 and cy2 < self.__b_len and\
             cx3 >= 0 and cx3 < self.__b_len and cy3 >= 0 and cy3 < self.__b_len and\
                cx4 >= 0 and cx4 < self.__b_len and cy4 >= 0 and cy4 < self.__b_len:
                    if board[cx1][cy1] == clr and board[cx4][cy4] == clr:
                        if board[cx2][cy2] == clr and board[cx3][cy3] == 0: # 1 0 x 1 1 
                            board_weight[x][y] += self.__score_four_2 #띈 4 공격
                            board_weight[x][y] -= (t*self.__f_d)
 
     def calc_Max(self, board_weight, able_stn):
        score1 = 0 #가중치들 중에서 가중치가 가장 큰 2개를 구함
        x1 = 0
        y1 = 0
        score2 = 0
        x2 = 0
        y2 = 0
        for i in able_stn:
            if board_weight[i[0]][i[1]] > score1:
                score2 = score1
                x2 = x1
                y2 = y1
                score1 = board_weight[i[0]][i[1]]
                x1 = i[0]
                y1 = i[1] 
            return [[x1, y1, score1],[x2,y2,score2]]
            
        def create_data_Set1(self,x,y, board,clr): #날일진을 만드는 메소드 첫 번째 
            if board[x][y] != 0: #재귀함수로 구현함
                return
 
            board[x][y] = clr
 
        if x-2 >= 0 and y-1 >= 0 :
            self.create_data_Set1(x-2, y-1,board,clr)
            if x-1 >= 0 and y+2 < 19 : 
                self.create_data_Set1(x-1, y+2, board,clr)
                if x+2 < 19 and y+1 < 19 :
                    self.create_data_Set1(x+2, y+1, board,clr)
                    if x+1 < 19 and y-2 >= 0 :
                        self.create_data_Set1(x+1, y-2, board,clr)

                        
     def match_dataset(self, board, dataset, cnt):
         flag = 0 #날일진에 해당되는 좌표를 검사하기위한 메소드
         for i in range(len(board)):
             for j in range(len(board)):
                 if board[i][j] == dataset[i][j]:
                     flag += 1
                 
                 if flag == cnt:
                     return True
                 else:
                     return False

     def next(self, board, length):  # override
         print (" **** White player : My Turns **** ")
         stn = stone(self._color)  # protected variable 
         while True:
             x=randint(0,length-1) % length
             y=randint(0,length-1) % length
             if (board[x][y] ==0):
                 break
         stn.setX(x)
         stn.setY(y)
         print (" === White player was completed ==== ")
         return stn
        

    
