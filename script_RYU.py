#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import time

taskset = 'taskset -c '
threads = '0'
cbench = ' cbench -c'
ip = '172.16.0.53'
#ip = 'localhost'
porta = '6633'
time_exec = 10000
loop = 13
hosts = 100000

comand_file = '>>'

n_switches = [1, 2, 3,4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 20, 22, 24, 26, 28, 30, 32, 36, 40, 44, 48, 52, 56, 60, 64]

#Funcao que monta o comando de Vazao
def throughput_comand(time, loop, switches, hosts):
    return taskset + threads + cbench + ip + ' -p ' + porta + ' -m ' + str(time) + ' -l ' + str(loop) + ' -w 3 -M ' + str(hosts) + ' -t -i 50 -I 5 -s ' + str(switches) + ' '
 
#Funcao que monta o comando de Latencia
def latency_comand(time, loop, switches, hosts):
    return taskset + threads + cbench + ip + ' -p ' + porta + ' -m ' + str(time) + ' -l ' + str(loop) + ' -s ' + str(switches) + ' -M ' + str(hosts) + ' '

#Funcao que pausa a execucao do programa em t segundos
def pausa(t):
    print '\n Pausa de ' + str(t) + ' segundos para preparar o controlador para o próximo teste \n '
    time.sleep(t)
    print '\n Fim da Pausa \n'

#Funcao responsavel por executar o comando de vazao no shecomand_filell
def throughput(controller_name, time, loop, hosts, count):
    comand = throughput_comand(time, loop, count, hosts) + comand_file + controller_name + '_vazao' +'.txt'
    return_code = subprocess.call(comand, shell=True)
    if return_code == 0:
        pausa(60) # Pausa de n segundos para reconfiguracao do controlador
    mensage(return_code)
    return return_code
 
#Funcao responsavel por executar o comando de latencia no shell
def latency(controller_name, time, loop, hosts, count):
    comand = latency_comand(time, loop, count, hosts) + comand_file + controller_name + '_latencia' +'.txt'
    return_code = subprocess.call(comand, shell=True)
    if return_code == 0:
        pausa(60) # Pausa de n segundos para reconfiguracao do controlador
    mensage(return_code)
    return return_code

#Funcao que deixa mais claro o sucesso ou falha do comando no shell
def mensage(mensage_shell):
    if mensage_shell == 0:
        print '\n *************** Executado com sucesso! ***************\n'
    else:
        print 'ERRO, verifique os requisitos para a execução ou se o controlador está sendo executado!'
 
def calc_etapas(intervalo):
    count = 1
    etapa = 0
    while(count <= len(n_switches)):
        etapa = etapa + 1
        count = count + 1 #mudei a disciplina
    return n_switches[etapa - 1]
 
def calc_porcent(atual, total):
    return (atual - 1) * 100 / total
 
#Funcao responsavel pela execucao da avaliacao do controlador
def run(controller_name, intervalo, time, loop):
    flag = -1
    count = intervalo[0]
    count_etapa = 1 #Conta o número de testes realizados
    while(count <= len(n_switches)):
        print '\n********** ETAPA nº ' + str(count_etapa) + ' de ' + str(len(n_switches)) + '**********'
        print str(calc_porcent(count_etapa, calc_etapas(intervalo))) + '% Concluido... \n'
        flag = throughput(controller_name, time, loop, hosts, n_switches[count-1])
        if flag != 0:
            break # Interronper execução, ERRO
        flag = latency(controller_name, time, loop, hosts,  n_switches[count-1])
        if flag != 0:
            break # Interronper execução, ERRO
        count = count + 1 #alterei a disciplina
        count_etapa = count_etapa + 1
    print 'AVALIAÇÃO CONCLUÍDA'
 
run('RYU', [1,64], time_exec, loop)