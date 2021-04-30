#####################################################################
# Модель SIRS 
# S - восприимчивая к заболеванию особь, I - инфицированная,
# R - имеющая иммунитет, V - вакантное место в популяции
#####################################################################

import random
import matplotlib.pyplot as plt


# Параметры модели: 
L   = 10        # сторона решётки (при изменении значения L, изменить 
N   = L*L       # матрицу M). N - размер популяции 
p1  = 0.20      # вероятность заболевания, перехода S -> I
p2  = 0.10      # вероятность излечения, перехода I -> R
p3  = 0.05      # вероятность заболевания иммунной особи, перехода R -> S
pb  = 0.70      # вероятность рождения, перехода V -> S
pd  = 0.01      # вероятность гибели, перехода R -> V
pdi = 0.05      # pdi - вероятность летального исхода при заболевании, 
                # pd + pdi - вероятность перехода I -> V  
gamma = 0.2     # коэфф. диффузии, средняя скорость перемещения особей

iterations = 40 # число итераций модели  

# Начальное состояние популяции (должно быть L строк и столбцов):
M = [  ['V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V' ],
       ['V', 'S', 'I', 'I', 'I', 'I', 'V', 'V', 'S', 'V' ],
       ['V', 'S', 'S', 'S', 'S', 'S', 'S', 'I', 'S', 'V' ],
       ['V', 'R', 'V', 'S', 'I', 'S', 'S', 'S', 'V', 'V' ],
       ['V', 'S', 'V', 'S', 'R', 'R', 'I', 'S', 'V', 'V' ],
       ['V', 'R', 'V', 'S', 'I', 'S', 'S', 'S', 'V', 'V' ],
       ['V', 'R', 'I', 'R', 'R', 'R', 'R', 'I', 'V', 'V' ],
       ['V', 'V', 'V', 'I', 'V', 'V', 'I', 'V', 'V', 'V' ],
       ['V', 'V', 'V', 'V', 'V', 'V', 'V', 'I', 'V', 'V' ], 
       ['V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V' ]
    ]
    
def print_M( iteration ):
    print( "Step: ", iteration )
    for i in range( L ):
        for j in range( L ):
            print( M[i][j], end = '' )
        print()
    print()     

def modeling( number_of_iterations ):
    S, I, R, V = [], [], [], []
    for it in range( number_of_iterations + 1 ):
        print_M( it )
        S_counter, I_counter, R_counter, V_counter = 0, 0, 0, 0
        for i in range( L ):
            for j in range( L ):
                curr = M[i][j]
                if curr == 'S':
                    S_counter += 1; 
                if curr == 'I':
                    I_counter += 1; 
                if curr == 'R':
                    R_counter += 1; 
                if curr == 'V':
                    V_counter += 1;
        S.append( S_counter )
        I.append( I_counter )
        R.append( R_counter )
        V.append( V_counter ) 
                
        # (1) этап заболевания
        for n in range( N ): 
            i, j = random.randrange( 0, L ), random.randrange( 0, L )
            status = M[i][j]
            if status == 'S':                          # (а)
                # соседи текущей особи
                neighbors = [ M[(i - 1) % L][j], M[(i + 1) % L][j],    
                              M[i][(j - 1) % L], M[i][(j + 1) % L]  ]
                # случайный выбор среди соседей
                neighbor = random.choice( neighbors ) 
                if neighbor == 'I' and p1 > random.random():
                    M[i][j] = 'I'
            if status == 'I' and p2 > random.random(): # (б)
                M[i][j] = 'R'
            if status == 'R' and p3 > random.random(): # (в)
                M[i][j] = 'S'  
                
        # (2) этап воспроизводства          
        for n in range( N ):
            i, j = random.randrange(0, L), random.randrange(0, L)
            status = M[i][j]
            if status == 'V':                                          # (г)
                # соседи текущей особи
                neighbors = [ M[(i - 1) % L][j], M[(i + 1) % L][j],    
                              M[i][(j - 1) % L], M[i][(j + 1) % L]  ]
                # случайный выбор среди соседей
                neighbor = random.choice( neighbors ) 
                if (neighbor == 'S') and (pb > random.random()):
                    M[i][j] = 'S'
            if (status == 'S' or status == 'R') and (pd > random.random()): # (д)
                M[i][j] = 'V'
            if status == 'I' and pd + pdi > random.random():            # (е)
                M[i][j] = 'V'
        
        # (3) этап миграции          
        for n in range( int(gamma*N) ):
            i, j = random.randrange(0, L), random.randrange(0, L)
            status = M[i][j]
            # соседи текущей особи
            neighbors = [ M[(i - 1) % L][j], M[(i + 1) % L][j],    
                          M[i][(j - 1) % L], M[i][(j + 1) % L] ]
            # случайный выбор среди соседей
            neighbor = random.choice( neighbors )
            M[i][j]  = neighbor
            neighbor = status
            
    return S, R, I, V            
####################################################
   
S, R, I, V  = modeling( iterations ) 

X  = [ k for k in range( iterations + 1 ) ]

plt.figure( "SIRS" )
plt.xlabel( "iteration" )         
plt.ylabel("S, I, R, V")    
plt.grid()             
plt.plot( X, S, color = "green", label = 'S' )
plt.plot( X, I, color = "red",   label = 'I' )
plt.plot( X, R, color = "blue",  label = 'R' )
plt.plot( X, V, color = "grey", label = 'V' )
plt.legend( loc = "upper left")
plt.show()











    





