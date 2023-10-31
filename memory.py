from database_ops import perform_database_operation


def memory_ops(conn, client, ip, hostname):
    
    commandMemTotal="grep 'MemTotal' /proc/meminfo | awk '{print $2}'"
    commandMemFree = "grep 'MemFree' /proc/meminfo | awk '{print $2}'"
    
    _, stdout, _ = client.exec_command(commandMemTotal)
    resultMemTotal = int(stdout.read().decode("utf8").strip())
    
    _, stdout, _ = client.exec_command(commandMemFree)
    resultMemFree =  int(stdout.read().decode("utf8").strip())
        
        
    query = '''
    INSERT INTO memory (ip, hostname, memtotal, memfree) 
    VALUES (%s, %s, %s, %s) 
    ON CONFLICT (ip) DO UPDATE 
    SET hostname=EXCLUDED.hostname, 
        memtotal = EXCLUDED.memtotal, 
        memfree = EXCLUDED.memfree;
    '''
    data = (ip, hostname, int(resultMemTotal), int(resultMemFree))
    
    perform_database_operation(conn,query,data)