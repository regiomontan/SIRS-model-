######################################################################
# Анимированная модель SIRS 
# S - восприимчивая к заболеванию особь, I - инфицированная,
# R - имеющая иммунитет, V - вакантное место в популяции
######################################################################

import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

delay = 500     # задержка времени выполнения анимации  

# Параметры модели: 
L   = 10        # сторона решётки (при изменении значения L, изменить 
N   = L*L       # матрицу M). N - размер популяции + вакантные клетки V 
p1  = 0.20      # вероятность заболевания, перехода S -> I
p2  = 0.10      # вероятность излечения, перехода I -> R
p3  = 0.05      # вероятность заболевания иммунной особи, перехода R->S
pb  = 0.40      # вероятность рождения, перехода V -> S
pd  = 0.01      # вероятность гибели, перехода R -> V
pdi = 0.05      # pdi - вероятность летального исхода при заболевании, 
                # pd + pdi - вероятность перехода I -> V  
gamma = 0.2     # коэфф. диффузии, средняя скорость перемещения особей

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
#---------------------------------------------------------------------
# Распечатка состояния популяции на итерации iteration
#---------------------------------------------------------------------    
def print_M( iteration ):
    print( "Step: ", iteration )
    for i in range( L ):
        for j in range( L ):
            print( M[i][j], end = '' )
        print()
    print()     
#---------------------------------------------------------------------
# Движок модели. 
# возвращает изменённый список M.
#--------------------------------------------------------------------- 
def modeling( M ):
    for it in range( 1 ):
            
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
            if status == 'V':                                               # (г)
                # соседи текущей особи
                neighbors = [ M[(i - 1) % L][j], M[(i + 1) % L][j],    
                              M[i][(j - 1) % L], M[i][(j + 1) % L]  ]
                # случайный выбор среди соседей
                neighbor = random.choice( neighbors ) 
                if (neighbor == 'S') and (pb > random.random()):
                    M[i][j] = 'S'
            if (status == 'S' or status == 'R') and (pd > random.random()): # (д)
                M[i][j] = 'V'
            if status == 'I' and pd + pdi > random.random():                # (е)
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
            
    return M 
#---------------------------------------------------------------------
# Конвертация особей в цветные клетки решётки:
# I - красный; S - зелёный; R - синий; V - серый
#---------------------------------------------------------------------
def convert_2_img( M ):
    im = [ [0] * L for i in range(L) ]
    for i in range( L ):
        for j in range( L ):
            status = M[i][j]
            if status == 'I':  im[i][j] = 0    # красный
            if status == 'S':  im[i][j] = 22   # зелёный    
            if status == 'R':  im[i][j] = 15   # синий
            if status == 'V':  im[i][j] = 100  # серый 
    return im  
#----------------------------------------------------------------------
def generate_data():
    return convert_2_img( modeling( M ) ) 
#----------------------------------------------------------------------
def update( data ):
    mat.set_data( data )
    return mat 
#----------------------------------------------------------------------
def data_gen():
    while True:
        yield generate_data()
        
#######################################################################        

fig, ax = plt.subplots()
fig.canvas.set_window_title('SIRS-model')
mat = ax.matshow( generate_data(), cmap = 'Set1' )
#fig.colorbar( mat )
# настройка сетки
major_ticks = [0.5 + i for i in range( L ) ] 
minor_ticks = major_ticks
ax.set_xticks( major_ticks )
ax.set_xticks( minor_ticks, minor=True )
ax.set_yticks( major_ticks )
ax.set_yticks( minor_ticks, minor=True )
ax.set_xticklabels( [] )
ax.set_yticklabels( [] )
ax.grid( color = 'black', linewidth = 1, linestyle = '-' )
ax.set_title( "Infectious (red), Susceptible (green), Recovered (blue), Vacant (grey)" )
        
ani = animation.FuncAnimation( fig, update, data_gen, interval = delay, save_count = 50 )

plt.show()


