import paramiko, time
 
## List of IP addresses to add to blacklist in the Mikrotik routers.
ip_list = ['8.8.8.8', '8.8.8.4']

## List of Router Devices to connect and run the commands
router_list = ['172.16.1.1', '172.16.1.2']

## Function to Initialize the client Object from Paramiko lybrary, stablish the connection with the credentials provided below and run the commands.
def exec(router):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print('parametros de conexion')
    ## Credentials and IP address for the device to connect
    client.connect(router, username='user', password='pass')  
    print('conection attempt - ' + str(router))
    for x in ip_list:
        ## Command to add the IP address to the BlakcList
        stdin, stdout, stderr = client.exec_command(str('/ip firewall address-list add list="BlackList" address=' + x))
        time.sleep(3)
        print('run - add list="BlackList" address=' + str(x))
        for line in stdout:
            print(line.strip('\n'))
    ## Command to agregate the DROP action to the objects created previously in the router.
    stdin, stdout, stderr = client.exec_command('/ip firewall filter add chain=forward in-interface=ether1-WAN src-address-lis=BLOQUEOS action=drop')
    client.close()
    print('Connection closed')

def run():
    for x in range(len(router_list)):
        router = router_list[x]
        exec(router)
        print(str(x) + ' - ' + str(router_list[x]))


if __name__ == '__main__':
    run()
