from random import random
from math import sqrt

#Матрица игры
matrix = [[2, -3], [-1, 2]]

#Генератор случайных чисел
def rand(p):
    r = random()
    if r <= p:
        d = 0
    else:
        d = 1
    return d

#подсчёт данных
def maths(res, pA, pB, dev,games):
    print('Вероятность выбора первой строки А:', pA)
    print('Вероятность выбора первого столбца B:', pB)
    print('Выиграш А:', res[0], 'Выигрыш В:', res[1])
    aver = res[0]/games
    print('Средний выиграш А за одну игру:', aver)
    expected = 8*pA*pB - 5*pA - 3*pB + 2
    print('Математическое ожидание:', expected)
    print('Среднеквадратичное отклоение:', dev)
    disper = (-2*pA*pB - 3*pB + 5*pA + 4) - expected**2
    print('Дисперсия:', disper)
    print('Теоретическое СКО:', sqrt(disper))



#симуляция игры
def game(pA, pB):
    #количество игр в симуляции
    games = 100
    #для первых двух симуляций
    if (type(pA) == float or type(pA) == int) and (type(pB) == int or type(pB) == float):
        res = [0, 0]
        res_mat = []
        for i in range(games):
            n = matrix[rand(pA)][rand(pB)]
            res_mat.append(n)
            res = [res[0]+n, res[1]-n]
        aver = res[0]/games
        dev = 0
        for i in res_mat:
            dev += ((i - aver))**2
        dev = sqrt(dev/(games-1))
        maths(res, pA, pB, dev, games)
    #для симуляции игрока А с подкреплением
    elif pA == 'reinforcement' and (type(pB) == int or type(pB) == float):
        res = [0, 0]
        res_mat = []
        box = [10, 10]
        pA = box[0]/(box[0]+box[1])
        for i in range(games):
            randomise = rand(pA)
            n = matrix[randomise][rand(pB)]
            if n > 0:
                box[randomise] += 2
            pA = box[0]/(box[0]+box[1])
            res_mat.append(n)
            res = [res[0]+n, res[1]-n]
        aver = res[0]/games
        dev = 0
        for i in res_mat:
            dev += ((i - aver))**2
        dev = sqrt(dev/(games-1))
        maths(res, pA, pB, dev, games)
    # для симуляции игрока А с наказанием
    elif pA == 'punishment' and (type(pB) == int or type(pB) == float):
        res = [0, 0]
        res_mat = []
        box = [100, 100]
        pA = box[0] / (box[0] + box[1])
        for i in range(games):
            randomise = rand(pA)
            n = matrix[randomise][rand(pB)]
            if n < 0:
                box[randomise] += n
            pA = box[0] / (box[0] + box[1])
            res_mat.append(n)
            res = [res[0] + n, res[1] - n]
        aver = res[0] / games
        dev = 0
        for i in res_mat:
            dev += ((i - aver)) ** 2
        dev = sqrt(dev / (games-1))
        maths(res, pA, pB, dev,  games)
    # для симуляции  обучения обоих игроков с подкреплением
    elif pA == 'reinforcement' and pB == 'reinforcement':
        res = [0, 0]
        res_mat = []
        boxA = [10, 10]
        boxB = [10, 10]
        pA = boxA[0] / (boxA[0] + boxA[1])
        pB = boxB[0] / (boxB[0] + boxB[1])
        for i in range(games):
            randomiseA = rand(pA)
            randomiseB = rand(pB)
            n = matrix[randomiseA][randomiseB]
            if n < 0:
                boxB[randomiseB] -= n
            else:
                boxA[randomiseA] += n
            pA = boxA[0] / (boxA[0] + boxA[1])
            pB = boxB[0] / (boxB[0] + boxB[1])
            res_mat.append(n)
            res = [res[0] + n, res[1] - n]
        aver = res[0] / games
        dev = 0
        for i in res_mat:
            dev += ((i - aver)) ** 2
        dev = sqrt(dev / (games-1))
        maths(res, pA, pB, dev, games)






print('Оба игрока равновероятно (с вероятностью ½) выбирают одну или другую строку/столбец')
game(0.5, 0.5)
print('Игрок A равновероятно выбирает строку, а игрок B (случайно) выбирает красный столбец втрое реже, чем синий.')
game(0.5, 0.25)
print('Обучение с подкреплением игрока A')
game('reinforcement', 0.25)
print('Обучение с наказанием игрока A')
game('punishment', 0.25)
print('Оба игрока обучаются с подкреплением')
game('reinforcement', 'reinforcement')