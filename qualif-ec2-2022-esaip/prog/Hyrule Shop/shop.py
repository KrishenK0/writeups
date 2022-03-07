import socket, re, time
 
class Netcat:

    """ Python 'netcat like' module """

    def __init__(self, ip, port):

        self.buff = ""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip, port))

    def read(self, length = 1024):

        """ Read 1024 bytes off the socket """

        return self.socket.recv(length)
 
    def read_until(self, data):

        """ Read data into the buffer until we have data """

        while not data in self.buff:
            self.buff += self.socket.recv(1024).decode()
 
        pos = self.buff.find(data)
        rval = self.buff[:pos + len(data)]
        self.buff = self.buff[pos + len(data):]
 
        return rval
 
    def write(self, data):

        self.socket.send(data.encode())
    
    def close(self):

        self.socket.close()


# start a new Netcat() instance
nc = Netcat('hyruleshop.ec2qualifications.esaip-cyber.com', 55555)
regex = r"(buy|sell) (a|[0-9]+) [a-z]+ (\([0-9]* rupees\))( and (((a|[0-9]+) [a-z]+ (\([0-9]* rupees\)))|(sell|buy) (a|[0-9]+) [a-z]+ (\([0-9]* rupees\))))?"
dregex = r"^\(([0-9]+) rupees\)$"

while True:
    line = nc.read_until('?')

    bill = 0

    # Collect the informations (type, count, price)
    res = re.findall(regex, line)

    # Show the datas received
    print(line)

    if len(res) > 0:
        dv = 1
        value = 0

        for i in range(len(res[0])):
            number = 0

            # Check if the client want to buy or sell the product
            if res[0][i] == 'sell' : dv = -1
            elif res[0][i] == 'buy': dv = 1

            # Check if the count is equal to 1 or more
            if res[0][i] == 'a': value = 1
            elif res[0][i].isdigit() : value = int(res[0][i])

            # Get the price
            nb = re.findall(dregex, res[0][i])
            if nb: number = int(nb[0])

            # Add/Remove the number of product buy/sell with his price
            if value > 0 and number > 0: bill += dv*value*number


        # Send the bill to the server
        nc.write(str(bill) + '\n')

        # Show what we send (better for check if there is any issues)
        print(f'>> {bill}')

    # idk why I use a while whereas I know the number of clients
    if(line.find('n°100') != -1): break

# Show the flag
while True:
    flag = nc.read().decode()
    if(flag.find('R2Lille') != -1): 
        print(flag[flag.find('R2Lille'):])
        break