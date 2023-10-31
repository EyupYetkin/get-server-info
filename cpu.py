from database_ops import perform_database_operation


def cpu_ops(conn, client, ip, hostname):

    commandModelName = "lscpu | grep -m 1 'Model name' | cut -f 2 -d ':' | awk '{$1=$1}1'"
    commandCpuType = "uname -p"
    commandCpuNumberOfCore = "nproc"
    
    _, stdout, _ = client.exec_command(commandModelName)
    resultCpuName = stdout.read().decode("utf8").strip()

    _, stdout, _ = client.exec_command(commandCpuType)
    resultCpuType = stdout.read().decode("utf8").strip()
    
    _, stdout, _ = client.exec_command(commandCpuNumberOfCore)
    resultCpuNumberOfCore = int(stdout.read().decode("utf8").strip())
    
    query = '''
    INSERT INTO cpu (ip, hostname, cpuname, cputype, cpunumberofcore) 
    VALUES (%s, %s, %s, %s, %s) ON CONFLICT (ip) DO UPDATE 
    SET hostname = EXCLUDED.hostname, 
        cpuname = EXCLUDED.cpuname, 
        cputype = EXCLUDED.cputype, 
        cpunumberofcore = EXCLUDED.cpunumberofcore;
    '''
    data = (ip, hostname, resultCpuName, resultCpuType, int(resultCpuNumberOfCore))
    
    perform_database_operation(conn,query,data)