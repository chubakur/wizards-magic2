# To change this template, choose Tools | Templates
# and open the template in the editor.
import socket
import globals
try:
    import json
    print 'JSON'
except ImportError:
    import simplejson as json
    print 'SIMPLEJSON'
#host = "drakmail.ru"
#port = 7712
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def connect():
    global sock
    host = globals.server
    port = globals.port
    print host,port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, int(port)))
    except:
        return 0
    return 1
def get_package():
    #print "SERVICE:"
    #print service_package
    try: 
        MSGLEN, answ = int( sock.recv(8) ), ''
    except ValueError: #empty string (socked closed?)
        return dict(action='value_error')
    except socket.error:
        return dict(action='socket_error')

    while len(answ)<MSGLEN: answ += sock.recv(MSGLEN - len(answ))
        #return answ
    print "GET_PACKAGE RETURN"
    print answ
    return json.loads(answ)

def query_(query):
    query = json.dumps(query)
    service = '%08i'%len(query)
    sock.send(service)
    sock.send(query)
query = lambda x: x
    #print sock.recv(1)
    #return
    #return get_package()62.176.21.105

