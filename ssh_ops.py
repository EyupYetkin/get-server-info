import configparser
from paramiko import SSHClient, AutoAddPolicy

config = configparser.ConfigParser()
config.read('config.ini')

known_hosts_path = config.get('ssh', 'known_hosts_path')

def connect_via_ssh(ip, username):
    
    try:
        client = SSHClient()
        
        client.load_host_keys(known_hosts_path)
        
        client.load_system_host_keys()
        client.set_missing_host_key_policy(AutoAddPolicy())
        
        client.connect(ip, username=username)
        
        return client
    except Exception as e:
        print(f"{ip} adresine bağlanti kurulamadi: {str(e)}")
        return None

def get_hostname(client):
    try:
        _, stdout, _ = client.exec_command('hostname')
        hostname=stdout.read().decode("utf8").strip()
        return hostname
    except Exception as e:
        print(f"Hostname alinamadi: {str(e)}")      
    