import random
import threading
import time

SOSPITOS = 20
JUDGE = 1

semp_judge = threading.Semaphore(0)
semp_fora = threading.Semaphore(0)
semp_sala = threading.Semaphore(1)
semp_declaracion = threading.Semaphore(0)
semp_asil = threading.Semaphore(0)

sospechosos_sala = 0
sospechosos_fichados = 0
sospechosos_declarados = 0
total_sospechosos = 20
porta_tancada = False

def juez():
    global sospechosos_sala, veredicto_done, sospechosos_fichados, sospechosos_declarados, porta_tancada
    time.sleep(random.randint(100, 3000)/1000)
    print ("----> Jutge Dredd: Jo som la llei!")
    

    time.sleep(random.randint(100, 3000)/1000)
    porta_tancada = True
    print("----> Jutge Dredd: Som a la sala, tanqueu porta!")
    
    if sospechosos_sala > 0:
        print("----> Jutge Dredd: Fitxeu als sospitosos presents")
        semp_judge.acquire()
        print("----> Jutge Dredd: Preniu declaració als presents")
        semp_declaracion.release()
        
        # Esperara a que todos los sospechosos de la sala hayan declarado
        semp_judge.acquire()

        print("----> Judge Dredd: Podeu abandonar la sala tots a l'asil!")
        time.sleep(0.2)
        semp_asil.release()
        veredicto_done = True
        
        print("----> Jutge Dredd: La justícia descansa, prendré declaració als sospitosos que queden")
        time.sleep(random.randint(100, 3000)/1000)
        semp_fora.release()

    else:
        print("----> Jutge Dredd: Si no hi ha ningú me'n vaig!")

            

def sospechoso(nombre):
    time.sleep(random.randint(100, 3000)/1000)
    print(f"{nombre}: Som innocent!")
    global sospechosos_sala, sospechosos_fichados, sospechosos_declarados, veredicto_done, porta_tancada

    semp_sala.acquire()
    if not porta_tancada:
        
        sospechosos_sala += 1
        print(f"{nombre}: Entra al jutjat. Sospitosos: {sospechosos_sala}")
        time.sleep(random.randint(100, 3000)/1000)

        semp_sala.release()

        time.sleep(random.randint(100, 3000)/1000)

        sospechosos_fichados += 1
        print(f"{nombre} fitxa. Fitxats: {sospechosos_fichados}")
        if sospechosos_fichados == sospechosos_sala:
            semp_judge.release()

        semp_declaracion.acquire()
        time.sleep(random.randint(100, 3000)/1000)
        sospechosos_declarados += 1
        print(f"{nombre} declara. Declaracions: {sospechosos_declarados}")
        if sospechosos_declarados == sospechosos_sala:
            semp_judge.release()
        semp_declaracion.release()

        semp_asil.acquire()
        print(f"{nombre} entra a l'Asil d'Arkham")
        semp_asil.release()

    
    else:
        semp_sala.release()
        semp_fora.acquire()
        print(f'{nombre}: No és just vull declarar! Som innocent!')
        semp_fora.release()

juez_thread = threading.Thread(target=juez)
nombre_sospechosos = ["Deadshot", "Harley Quinn", "Penguin", "Riddler", "Bane", "Talia al Ghul",
                       "Ra's al Ghul", "Hugo Strange", "Killer Croc", "Catwoman", "Poison Ivy",
                         "Mr. Freeze", "Jason Todd", "Hush", "Joker", "Clayface", "Deathstroke",
                           "Mad Hatter", "Two-Face", "Scarecrow"]
        
random.shuffle(nombre_sospechosos)

sospechosos_threads = []


for villano in nombre_sospechosos:
    sospechosos_threads.append(threading.Thread(target=sospechoso, args=(villano,)))

juez_thread.start()

for sospechoso_thread in sospechosos_threads:
    sospechoso_thread.start()

juez_thread.join()

for sospechoso_thread in sospechosos_threads:
    sospechoso_thread.join()

print("La simulacion ha terminado")


