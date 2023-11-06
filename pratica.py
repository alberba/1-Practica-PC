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
semp_fitxa = threading.Semaphore(1)

sospechosos_sala = 0
sospechosos_fichados = 0
sospechosos_declarados = 0
total_sospechosos = 20
porta_tancada = False

def juez():
    global sospechosos_sala, veredicto_done, sospechosos_fichados, sospechosos_declarados, porta_tancada
    time.sleep(0.1)
    print ("----> Jutge Dredd: Jo som la llei!")
    

    time.sleep(1)
    porta_tancada = True
    print("----> Jutge Dredd: Som a la sala, tanqueu porta!")
    
    if sospechosos_sala > 0:
        print("----> Jutge Dredd: Fitxeu als sospitosos presents")
        semp_judge.acquire()
        print("----> Jutge Dredd: Preniu declaració als presents")
        semp_declaracion.release()
        
        # Esperara a que todos los sospechosos de la sala hayan declarado
        print(semp_judge._value)
        semp_judge.acquire()
        print(semp_judge._value)

        print("----> Judge Dredd: Podeu abandonar la sala tots a l'asil!")
        time.sleep(0.1)
        semp_asil.release()
        veredicto_done = True
        
        print("----> Jutge Dredd: La justícia descansa, prendré declaració als sospitosos que queden")
        time.sleep(0.1)
        semp_fora.release()

    else:
        print("----> Jutge Dredd: Si no hi ha ningú me'n vaig!")
        semp_sala.release()

            

def sospechoso(nombre):
    print(f"{nombre}: Som innocent!")
    global sospechosos_sala, sospechosos_fichados, sospechosos_declarados, veredicto_done, porta_tancada
    fichados = False

    semp_sala.acquire()
    if not porta_tancada:
        
        sospechosos_sala += 1
        print(f"{nombre}: Entra al jutjat. Sospitosos: {sospechosos_sala}")
        time.sleep(0.1)

        semp_sala.release()

        semp_fitxa.acquire()
        sospechosos_fichados += 1
        time.sleep(0.1)
        print(f"{nombre} fitxa. Fitxats: {sospechosos_fichados}")
        if sospechosos_fichados == sospechosos_sala and porta_tancada and semp_judge._value == 0:
            fichados = True
            semp_judge.release()
        semp_fitxa.release()

        semp_declaracion.acquire()
        sospechosos_declarados += 1
        print(f"{nombre} declara. Declaracions: {sospechosos_declarados}")
        time.sleep(0.1)
        if sospechosos_declarados == sospechosos_sala:
            semp_judge.release()
        semp_declaracion.release()

        semp_asil.acquire()
        print(f"{nombre} entra a l'Asil d'Arkham")
        time.sleep(0.1)
        semp_asil.release()

    
    else:
        semp_sala.release()
        semp_fora.acquire()
        print(f'{nombre}: No és just vull declarar! Som innocent!')
        time.sleep(0.1)
        semp_fora.release()

juez_thread = threading.Thread(target=juez)
nombre_sospechosos = ["Deadshot", "Harley Quinn", "Penguin", "Riddler", "Bane", "Talia al Ghul",
                       "Ra's al Ghul", "Hugo Strange", "Killer Croc", "Catwoman", "Poison Ivy",
                         "Mr. Freeze", "Jason Todd", "Hush", "Joker", "Clayface", "Deathstroke",
                           "Mad Hatter", "Two-Face", "Scarecrow"]
        
random.shuffle(nombre_sospechosos)

sospechosos_threads = []


for villano in nombre_sospechosos:
    sospechoso_thread = threading.Thread(target=sospechoso, args=(villano,))
    sospechoso_thread.start()
    sospechosos_threads.append(sospechoso_thread)

juez_thread.start()

for sospechoso_thread in sospechosos_threads:
    sospechoso_thread.join()

juez_thread.join()

print("La simulacion ha terminado")


