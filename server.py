import socket
import random
import time
import protocol
import threading
from _thread import *

L = []

czyzgadl = 0
free_id = [1, 2, 3, 4, 5, 6, 7]

tajna_liczba = random.randint(1, 25)  # losowanie tajnej liczby z przedzialu 1-9
czy_ktos_odgadl = False


# losowanie id
def random_id():
    global free_id
    while True:
        id = random.randint(1, 7)
        for i in free_id:
            if id == i:  # == kurwa
                free_id.remove(id)
                return int(id)
            else:
                continue

# metoda do wymiany informacji z klientami
def new_client(sock, addr, id):
    try:
        global free_id
        global czy_ktos_odgadl
        czy_odgadles = False
        messagerecived = sock.recv(1024)
        messagerecived = protocol.datadecode(messagerecived)
        messagesend = protocol.dataencode(0, 0, id, 0, 0)
        sock.send(messagesend)  # wyslanie id dla klienta
        received = conn.recv(1024)  # odebranie wiadomosci z liczba nieparzysta L
        received = protocol.datadecode(received)
        L.append(received['number'])

        while True:
            if czy_ktos_odgadl == True:
                break
            if czy_odgadles == True:
                break
            if len(L) == 2:
                liczba_prob = int(((L[0]) + L[1]) / 2)  # obliczenie liczby prob
                messagesend = protocol.dataencode(1, 1, id, liczba_prob, 0) #zakodowanie wiadomosci z liczba prob
                sock.send(messagesend)  # przelsanie wiadomosci z liczba prob
                print("Tajna liczba do odgadniecia " + str(tajna_liczba))
                print("Liczba prob wynosi " + str(liczba_prob))
                while True:
                    if liczba_prob > 0:
                        received = sock.recv(1024)  # odebranie wiadomosci ze zgadywana liczba
                        received = protocol.datadecode(received)
                        if received['operation'] == 2:
                            if received['answer'] == 0:
                                liczba = received['number']
                                if czy_ktos_odgadl == False:
                                    if liczba == tajna_liczba:
                                        liczba_prob -= 1
                                        print("Client {}:{} odgadl liczbe!".format(addr[0], str(addr[1])))
                                        messagesend = protocol.dataencode(2, 2, id, 0, 0)
                                        sock.send(
                                        messagesend)  # jesli klient odgadl liczbe wysylana jest mu odpowiednia wiadomosc
                                        czy_odgadles = True
                                        czy_ktos_odgadl = True
                                        break
                                    elif liczba != tajna_liczba:
                                        liczba_prob -= 1
                                        print("Client {}:{}:proboj dalej!".format(addr[0], str(addr[1])))
                                        messagesend = protocol.dataencode(2, 1, id, 0, 0)
                                        sock.send(
                                            messagesend)  # jesli klient nie odgadl liczby wysylana jest mu odpoweidnia wiadomosc
                                elif czy_ktos_odgadl == True:
                                    messagesend = protocol.dataencode(2, 3, id, 0, 0)
                                    sock.send(messagesend)
                                    break
                    elif liczba_prob == 0:  # dodatkowy warunek
                        if czy_ktos_odgadl == True:
                            messagesend = protocol.dataencode(2, 3, id, 0, 0)
                            sock.send(messagesend)
                            break

            elif len(L) != 2:
                while True:  # oczekiwanie az obaj uzytkownicy podadza liczbe do obliczenia liczby prob
                    time.sleep(1)
                    if len(L) == 2:
                        break

        free_id.append(int(id))  # dodanie id do tablicy wolnych id po rozlaczniu z klientem
        sock.close()
    except ConnectionResetError:
        free_id.append(int(id))  # dodanie id do tablicy wolnych id po rozlaczniu z klientem
        sock.close()


HOST = '127.0.0.1'  # Adres IP serwera
PORT = 65432  # Port uzywany przez serwer

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("socket created")
s.bind((HOST, PORT))
print("sock has been bounded")
s.listen(2)

while True:
    conn, addr = s.accept()
    print("connected with " + addr[0] + ":" + str(addr[1]))
    start_new_thread(new_client, (conn, addr, random_id()))