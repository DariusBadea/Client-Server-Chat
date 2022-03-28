import socket
import sys
import time
import argparse
import threading

utilizator=sys.argv[1].encode('utf-8')
server=sys.argv[2]
port=int(sys.argv[3])

client = socket.socket( socket.AF_INET, socket.SOCK_STREAM )



print('- Ma conectez la {}:{}'.format(server, port))
client.connect((server, port))
print('- CONECTAT!')
conectat = True

def inregistrare():
    print(f"- Ma inregistrez cu {str(utilizator.decode())}")
    mesaj='register:' + utilizator.decode()
    client.send( mesaj.encode( 'utf-8' ) )

    mesaj_primit = (client.recv(1024)).decode()
    if (mesaj_primit == "Esti deja inregistrat!"):
        print( "SERVER!!: Esti deja inregistrat")
        client.close()
        return False
    else:
        print( mesaj_primit )
    # mesaj_primit = client.recv( 1024 )
    # print( "SERVER: " + mesaj_primit.decode() )

def trimite_mesaj():
        mesaj = input()
        client.send(mesaj.encode('utf-8'))

    # >George: salutare!

def primeste_mesaj():
        mesaj = (client.recv(1024)).decode()
        if len( mesaj ) > 2:
            print(mesaj)

def incheiere_conexiune(client):
    client.close()
    conectat = False
    client.send("Deconectat".encode('utf-8'))
    sys.exit()

threads = []
ret = inregistrare()
if ret != False:
    while True:
        t1 = threading.Thread( target=trimite_mesaj())
        threads.append( t1 )

        t2 = threading.Thread( target=primeste_mesaj() )
        threads.append( t2 )

        t1.start()
        t2.start()

#python client.py Mihai 127.0.0.1 5003