from database_ops import perform_database_operation


def users_ops(conn, client, ip, hostname):
    
    commandPasswd = "cat /etc/passwd"
    _, stdout, _ = client.exec_command(commandPasswd)
    
    cursor = conn.cursor()
    commandFetchDb = '''
    SELECT ip, hostname, username, uid 
    FROM users 
    WHERE ip=%s::inet
    '''
    data = (ip,)
    cursor.execute(commandFetchDb, data)
    db_users = cursor.fetchall()  
    cursor.close()

    passwd_users = []
   
    for line in stdout:
        fields = line.strip().split(':')

        username = fields[0]
        uid = fields[2]
        passwd_users.append((ip, hostname, username, int(uid)))
        
        
        query = """INSERT INTO users (ip, hostname, username, uid) 
        VALUES (%s, %s, %s, %s) ON CONFLICT (ip, uid) DO UPDATE 
        SET hostname=EXCLUDED.hostname, 
        username = EXCLUDED.username, 
        uid = EXCLUDED.uid;
        """
        
        data = (ip, hostname, username, uid)
        perform_database_operation(conn, query, data)
       
    for db_user in db_users:
        if db_user not in passwd_users:
            query ='DELETE FROM users WHERE ip= %s AND uid= %s'
            data = (db_user[0], db_user[3])
            perform_database_operation(conn, query, data)











"""
query = 'INSERT INTO users (hostname, username, uid) VALUES (%s, %s, %s) ON CONFLICT (uid) DO UPDATE SET username = EXCLUDED.username, uid = EXCLUDED.uid;'
data = (ip, hostname, username, int(uid))
perform_database_operation(conn,query,data)

"""
 
#tabloyu çek
#/etc/passwd deki username ve uidleri çek
#tablodaki passwd var mı yoksa sil
##tabloyu çekecen satır satır gezecen 
##her satırda passwd de var mı kontrol etcen yoksa o satırı silecen        
"""    

passwd_users.append((ip, hostname, username, int(uid)))
    
for db_user in db_users:
    if db_user not in passwd_users:
        query = 'DELETE FROM users WHERE ip = %s AND hostname = %s AND username = %s AND uid = %s;'
        data = (db_user[0], db_user[1], db_user[2], db_user[3])
        perform_database_operation(conn, query, data)
"""