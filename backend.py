from unittest import result
import websockets
import asyncio
from subprocess import call
import os, sys, sqlite3




async def socket_server(websocket,port):
    global ip_address_pruef

    # Existenz feststellen
    if os.path.exists("snmpdaten.db"):
        print("Datei bereits vorhanden")
        #os.remove("snmpdaten.db")
        #sys.exit(0)


    if not os.path.exists("/etc/telegraf/telegraf.conf"):
        rc1 = call("./telegraf_conf1.sh", shell=True)

    # Verbindung zur Datenbank erzeugen
    connection = sqlite3.connect("snmpdaten.db")

    # Datensatz-Cursor erzeugen
    cursor = connection.cursor()

    listoftable = cursor.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='SNMPINFO';""").fetchall()

    if listoftable == []:
        print('Table not found!')
         # Datenbanktabelle erzeugen
        sql = """CREATE TABLE SNMPINFO(ipaddress TEXT PRIMARY KEY, username TEXT, securitylevel TEXT, authenticationprotocol TEXT, passphrase TEXT, privacyprotocol TEXT,  privacykeys TEXT)"""
        cursor.execute(sql)

    else:
        print('Table found!')
    
    a = await websocket.recv()
    a = a.split(",")

    if (a[0]=="add"):
        print("----------------------------------------------------ADD--Device----------------------------------------------------")
        # Datensatz erzeugen
        sql = """INSERT INTO SNMPINFO(ipaddress, username, securitylevel, authenticationprotocol, passphrase, privacyprotocol,  privacykeys) VALUES( "{}", "{}", "{}", "{}", "{}", "{}", "{}")""".format( a[1], a[2], a[3], a[4], a[5], a[6], a[7])
        cursor.execute(sql)
        connection.commit()
        # Verbindung beenden
        connection.close()

        connection = sqlite3.connect("snmpdaten.db")
        cursor = connection.cursor()

        # SQL-Abfrage
        sql = "SELECT * FROM SNMPINFO"
        cursor.execute(sql)

        #   all rows
        for f in cursor:
            print(f[0], f[1], f[2], f[3], f[4], f[5], f[6])

        # Last Row
        result = cursor.execute("SELECT * FROM SNMPINFO").fetchall()[-1]
        
        rc2 = call("./telegraf_conf2 {} {} {} {} {} {} {}".format(result[0], result[1], result[2], result[3], result[4], result[5], result[6]), shell=True)
        
        

        # Verbindung beenden
        connection.close()
        

    elif(a[0]=="delete"):
        print("----------------------------------------------------Delete--Device----------------------------------------------------")
        connection = sqlite3.connect("snmpdaten.db")
        cursor = connection.cursor()
        sql = """DELETE FROM SNMPINFO WHERE ipaddress="{}";""".format(a[1])
        cursor.execute(sql)
        connection.commit()
        # Verbindung beenden
        connection.close()

        connection = sqlite3.connect("snmpdaten.db")
        cursor = connection.cursor()

        # SQL-Abfrage
        sql = "SELECT * FROM SNMPINFO"
        cursor.execute(sql)
        os.remove("/etc/telegraf/telegraf.conf") 
        rc_drop_telegraf_influx = call("./influx-drop-telegraf.sh", shell=True)
        rc3 = call("./telegraf_conf1.sh", shell=True)
        for f in cursor:
            print(f[0], f[1], f[2], f[3], f[4], f[5], f[6])
            rc4 = call("./telegraf_conf2 {} {} {} {} {} {} {}".format(f[0], f[1], f[2], f[3], f[4], f[5], f[6]), shell=True)
        connection.close()



start_server = websockets.serve(socket_server,'localhost',8765)

asyncio.get_event_loop().run_until_complete(start_server)

asyncio.get_event_loop().run_forever()
