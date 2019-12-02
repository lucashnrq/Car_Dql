# -*- coding:UTF-8 -*-
# Importação das bibliotecas
import gpio as g
import numpy as np
from random import random, randint
import matplotlib.pyplot as plt
import time
import schedule

# Importação do modelo de Deep Q-Learning
from redeneural import Dql

# Está sendo criado um objeto chamado de brain (cérebro), que contém a rede neural que retorna o valor de Q
brain = Dql(3, 6, 0.9)  # 3 entradas (sensores + direção), 6 saídas e valor de gamma
last_reward = 0  # inicialização da última recompensa
g.RGB_init()
g.motor_init()
print('Configurações iniciadas!')
print('Ações gravadas!')
scores = []  # inicialização do valor médio das recompensas (sliding window) com relação ao tempo


def actions(x):
    if x == 0:
        return g.run(0.5)
    if x == 1:
        return g.brake(0.5)
    if x == 2:
        return g.right(0.5)
    if x == 3:
        return g.left(0.5)
    if x == 4:
        return g.spin_right(0.5)
    if x == 5:
        return g.spin_left(0.5)


# Acessa a pasta e busca pelo arquivo "last_brain.pth"
print("Carregando o último brain salvo...")
brain.load() 


def update():  # função que quando chega em um novo estado (pega novos valores dos sensores)
    # especificações das variáveis globais
    print('Alôooo')
    global brain
    global last_reward
    global scores

    ultra_c = g.ultra_c()
    ultra_r = g.ultra_r()
    ultra_l = g.ultra_l()
    print('Leitura dos sensores')

    last_signal = [ultra_c, ultra_r, ultra_l]  # Entrada dos sensores
    action = brain.update(last_reward, last_signal)  # a rede neural vai indicar a próxima ação
    scores.append(brain.score())  # adiciona os valores das recompensas (média das 1000 últimas recompensas)
    actions(action)  # converte a ação atual (0, 1 or 2) nos ângulos de rotação (0°, 20° ou -20°)
    move()  # move o carro baseado na ação gerada pela rede neural
    print('Atualização das entradas da rede neural')

    if ultra_c <= 20 and ultra_r <= 20 and ultra_l <= 20:
        last_reward = -1
    if ultra_c <= 20 and ultra_r > 20 and ultra_l <= 20:
        last_reward = -1
    if ultra_c <= 20 and ultra_r <= 20 and ultra_l > 20:
        last_reward = -1
    if ultra_c > 20 and ultra_r <= 20 and ultra_l <= 20:
        last_reward = -1
    if ultra_c > 20 and ultra_r > 20 and ultra_l <= 20:
        last_reward = -1
    if ultra_c > 20 and ultra_r <= 20 and ultra_l > 20:
        last_reward = -1
    if action == 0:
        last_reward = 0.5


# Execução de todo o código
if __name__ == '__main__':
    try:
        while True:
            update()
    except KeyboardInterrupt:
        print("Salvando brain...")
        brain.save()
        plt.plot(scores)
        plt.show()
        g.stop()
        g.clean()
        pass
