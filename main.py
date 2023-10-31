
"""
from database_ops import connect_to_database, clean_db,close_database_connection
from ssh_ops import connect_via_ssh, get_hostname
from memory import memory_ops
from cpu import cpu_ops
from users import users_ops
import configparser, threading

threads = []
hosts =[] 

conn = connect_to_database()

config = configparser.ConfigParser()
config.read('config.ini')

    
for section in config.sections():
    if section.startswith("server"):
        ip = config[section]['ip']
        hosts.append(ip)

print(hosts)
clean_db(conn, hosts)

def server_ops(conn, client, ip, hostname):
    memory_ops(conn, client, ip, hostname)
    cpu_ops(conn, client, ip, hostname)
    users_ops(conn, client, ip, hostname)
    print(ip,username)

for section in config.sections():
    if section.startswith("server"):
        ip = config[section]['ip']
        username = config[section]['username']
        client = connect_via_ssh(ip, username)
        hostname = get_hostname(client)
        thread = threading.Thread(target=server_ops, args=(conn, client, ip, hostname))
        threads.append(thread)
        thread.start()
        

for thread in threads:
    thread.join()

close_database_connection(conn)
"""

from database_ops import connect_to_database, clean_db, close_database_connection
from ssh_ops import connect_via_ssh, get_hostname
from memory import memory_ops
from cpu import cpu_ops
from users import users_ops
import configparser
import threading

def thread_memory_ops(conn, client, ip, hostname):
    memory_ops(conn, client, ip, hostname)

def thread_cpu_ops(conn, client, ip, hostname):
    cpu_ops(conn, client, ip, hostname)

def thread_users_ops(conn, client, ip, hostname):
    users_ops(conn, client, ip, hostname)

threads = []
hosts = []

conn = connect_to_database()

config = configparser.ConfigParser()
config.read('config.ini')

for section in config.sections():
    if section.startswith("server"):
        ip = config[section]['ip']
        hosts.append(ip)

print(hosts)
clean_db(conn, hosts)

for section in config.sections():
    if section.startswith("server"):
        ip = config[section]['ip']
        username = config[section]['username']
        client = connect_via_ssh(ip, username)
        hostname = get_hostname(client)

        memory_thread = threading.Thread(target=thread_memory_ops, args=(conn, client, ip, hostname))
        cpu_thread = threading.Thread(target=thread_cpu_ops, args=(conn, client, ip, hostname))
        users_thread = threading.Thread(target=thread_users_ops, args=(conn, client, ip, hostname))

        memory_thread.start()
        cpu_thread.start()
        users_thread.start()

        threads.extend([memory_thread, cpu_thread, users_thread])

for thread in threads:
    thread.join()

close_database_connection(conn)


"""
while True:
    for section in config.sections():
        
        ip = config[section]['ip']
        username = config[section]['username']
        print(ip,username)
        client = connect_via_ssh(ip,username)
        hostname = get_hostname(client)
        memory_ops(conn, client, ip, hostname)
        cpu_ops(conn, client, ip, hostname)
        users_ops(conn, client, ip, hostname)
"""

