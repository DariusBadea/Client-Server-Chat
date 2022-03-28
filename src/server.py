import socket
import sys
import argparse
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ip= sys.argv[1]
port=int(sys.argv[2])
print('- Ascult pe portul {} si adresa {}'.format(port, ip))

server.bind((ip, port))
server.listen(10)
threads =[]
global useri, conexiuni
useri=[]
conexiuni=[]
lock = threading.Lock()

def inregistrare(user, conn):
    if (useri.__contains__(user) == 0):

        lock.acquire()
        useri.append(user)
        conexiuni.append( conn )
        lock.release()

        conn.send( f"{user}, te-ai conectat".encode( 'utf-8' ) )
        print(f"{user} s-a inregistrat!")
        print("Utilizatori online: ")
        for i in useri:
            print(i)

    elif (useri.__contains__(user) == 1):
        print(f"Utilizatorul {user} deja inregistrat!!!")
        conn.send("Esti deja inregistrat!".encode('utf-8'))
        conn.close()


def trimite_mesaj(mesaj, conn):

    destinatar = mesaj[0][1:len(mesaj[0])]
    expeditor = str(useri[conexiuni.index(conn)])
    send_to = conexiuni[useri.index(destinatar)]

    print( expeditor + " catre " + destinatar )

    mesaj[0] = "<-"+expeditor+ ":"
    res = "".join(mesaj)
    send_to.send(res.encode('utf-8'))


def interpretare_mesaj(conn, addr):
    while True:
        try:
            data = (conn.recv( 1024 )).decode()
            mesaj = data.split(":")
                        # register:Mihai
                        # >George: salut!
            if (mesaj[0] == "register"):
                inregistrare(mesaj[1], conn)
            elif(mesaj[0][0] == ">" ):
                trimite_mesaj(mesaj, conn)

        except:
            conn.close()



while True:
    print("- Astept conexiuni ...")
    conn, addr = server.accept()
    t = threading.Thread(target=interpretare_mesaj, args=(conn, addr))
    threads.append( t )
    t.start()



#C:\Users\Darius\PycharmProjects\retele\venv
#python server.py 0.0.0.0 5003
