import socket
import time
import protocol


def wczytaj_liczbe():
    while True:
        num_l = input('Podaj nieparzysta liczbe <= 255: ')
        if num_l.isdigit() == True:
            num_l = int(num_l)
            if num_l % 2 == 1:
                return num_l
            else:
                continue
        else:
            print("Zly format danych!")


HOST = '127.0.0.1'  #Adres IP serwera
PORT = 65432  #Port uzywany przez serwer
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:  # Klient czeka aż serwer będzie dostępny + wyjątki
    try:
        s.connect((HOST, PORT))
        break
    except ConnectionRefusedError:
        print("...")
        time.sleep(5)

try:
    print("Wysylam zadanie wejscia na serwer")
    messagesend = protocol.dataencode(0, 1, 0, 0, 0)
    s.send(messagesend)
    messagereceive = s.recv(1024)
    decodemessagereceive = protocol.datadecode(messagereceive)

    if decodemessagereceive['operation'] == 0 and decodemessagereceive['answer'] == 0:
        id = protocol.d['id']
        print("Otrzymane id: {}".format(id))
        while True:
            num_l = wczytaj_liczbe()  # zastosowanie funkcji wczytaj_liczbe()
            if num_l <= 255:
                break
            else:
                print("Niepoprawna liczba!")
        messagesend = protocol.dataencode(1, 0, id, num_l, 0)
        s.send(messagesend)
        print("Wyslano wiadomosc z liczba prob ")
        messagereceive = s.recv(1024)
        decodemessagereceive = protocol.datadecode(messagereceive)

        if decodemessagereceive['operation'] == 1 and decodemessagereceive['answer'] == 1:
            liczba_prob = protocol.d['number']
            print("Liczba prob: {}".format(liczba_prob))
            print("Zakres tajnej liczby <1,25>")
            while liczba_prob > 0:  # Petla rozgrywki
                try:
                    while True:
                        num_s = int(input('Podaj liczbe <= 255: '))
                        if num_s <=255:
                            break
                        else:
                            print("Niepoprawna liczba!")
                    messagesend = protocol.dataencode(2, 0, id, num_s, 0)
                    s.send(messagesend)
                    messagereceive = s.recv(1024)
                    decodemessagereceive = protocol.datadecode(messagereceive)
                    if decodemessagereceive['operation'] == 2 and decodemessagereceive['answer'] == 1:
                        liczba_prob -= 1
                        print("Nie trafiles, proboj dalej. Pozostalo {} prob!".format(liczba_prob))
                    elif decodemessagereceive['operation'] == 2 and decodemessagereceive['answer'] == 2:
                        print("Trafiles! ")
                        break
                    elif decodemessagereceive['operation'] == 2 and decodemessagereceive['answer'] == 3:
                        print("Przegrales, przeciwnik byl szybszy! ")
                        break
                except ConnectionResetError:
                    print("Nastapilo rozlaczenie! ")
                    break

    else:
        print("Nie mozna uzyskac id")

except ConnectionResetError:
    print("Nastapilo rozlaczenie! ")
print("Koniec Gry! ")