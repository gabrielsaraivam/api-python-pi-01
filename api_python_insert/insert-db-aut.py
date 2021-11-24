import psutil
import time
import os
import smtplib
from email.message import EmailMessage
# from functools import reduce
from connectdb import *
from mailer import mailer

count_lista = -1
fk_maq = 1
multiplicador = 1

contador_alerta = 0
tempo_atual = 0
contador_infinito = 1


print('='*10,'INÍCIO DAS MEDIÇÕES','='*10)
print('-'*10,'Ctrl+C para parar','-'*10,'\n')

data = []
cpu = []
memory = []
disk = []
numero_tarefas = []
usuario = []
fk_maquina = []

def flush(cpu, memory, disk, numero_tarefas, usuario, fk_maquina):
    cpu_insert = cpu[count_lista]
    memory_insert = memory[count_lista]
    disk_insert = disk[count_lista]
    tarefas_insert = numero_tarefas[count_lista]
    usuario_insert = usuario[count_lista]
    fk_insert = fk_maquina[count_lista]
    insert_db(cpu_insert, memory_insert, disk_insert, tarefas_insert, usuario_insert, fk_insert)

def captura_dados():

    data_hora = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    cpu_percent = psutil.cpu_percent(interval=1) * multiplicador
    mem_percent = psutil.virtual_memory().percent * multiplicador
    disk_percent = psutil.disk_usage('/').percent * multiplicador
    numero_tarefas_ativas = len(psutil.pids()) * round(multiplicador)
    usuario_logado = psutil.users()[0].name
    fk_maquina_atual = fk_maq
    
    data.append(data_hora)
    cpu.append(float(cpu_percent))
    memory.append(float('{0:.2f}'.format(mem_percent)))
    disk.append(float(disk_percent))
    numero_tarefas.append(numero_tarefas_ativas)
    usuario.append(usuario_logado)
    fk_maquina.append(fk_maquina_atual)
    
    exibir_dados(cpu_percent, mem_percent, disk_percent, numero_tarefas_ativas, usuario_logado, fk_maquina_atual)
    intervalo_captura(cpu_percent, mem_percent, disk_percent)
    

def exibir_dados(cpu_percent, mem_percent, disk_percent, numero_tarefas_ativas, usuario_logado, fk_maquina_atual):

    print("-"*50)
    print(f"\nMáquina {fk_maq}")
    print(f"\nData e hora: {data[i]}")
    print(f"\nCPU - Percentual de uso: {cpu_percent:.2f}%")
    print(f"Memória - Percentual de uso: {mem_percent:.2f}%")
    print(f"Disco - Percentual de uso: {disk_percent:.2f}%")
    print(f"Número de tarefas: {numero_tarefas_ativas}")
    print(f"Usuário: {usuario[i]}\n")
    print("-"*50)

def intervalo_captura(cpu_percent, mem_percent, disk_percent):

    global contador_alerta
    global tempo_atual
    global contador_infinito


    if ((cpu_percent >= 80 or mem_percent >= 50 or disk_percent >= 70) and contador_alerta < 3):
        contador_alerta += 1
        tempo_atual = 15
        time.sleep(14)
        print("-"*50, "\n")
        print(f"\n\nAlerta Nível 1, máquina {fk_maq} enviado\n\n")
        print("-"*50, "\n")

        assunto = f"Alerta nivel 1 - leitura: {contador_infinito}" 
        texto = f"Melhor dar uma olhada. - leitura: {contador_infinito}"
        try: 
            mailer(assunto, texto)
        except:
            print('Deu erro')


    elif ((cpu_percent >= 80 or mem_percent >= 50 or disk_percent >= 70) and contador_alerta >= 3):
        tempo_atual = 5
        time.sleep(4)
        print("-"*50, "\n")
        print(f"\n\nAlerta CRÍTICO, máquina {fk_maq} enviado\n\n")
        print("-"*50, "\n")

        assunto = f"Alerta crítico - leitura: {contador_infinito}"
        texto = f"Deu ruim!!!!!!!! - leitura: {contador_infinito}"
        try: 
            mailer(assunto, texto)
        except:
            print('Deu erro')

    else:
        tempo_atual = 30
        contador_alerta = 0
        time.sleep(29)

    print(f"Intervalo atual de captura: {tempo_atual}s")
    # print(f"Contador alerta: {contador_alerta}")
    contador_infinito += 1

try:

    while True:
        
        for i in range(0,3):
            
            # Máquina 1 (dados reais)
            if fk_maq == 1:
                multiplicador = 1

            # Máquinas 2 e 3 (dados simulados)
            elif fk_maq == 2:
                multiplicador = 1.2
            else:
                multiplicador = 0.9

            captura_dados()
            count_lista = count_lista + 1
            flush(cpu, memory, disk, numero_tarefas, usuario, fk_maquina)

            fk_maq = fk_maq + 1

        fk_maq = 1

except KeyboardInterrupt:
    pass

flush(cpu, memory, disk, numero_tarefas, usuario, fk_maquina)
