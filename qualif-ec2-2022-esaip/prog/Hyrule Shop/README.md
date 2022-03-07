# Hyrule Shop

```
A new shop has opened in the Hyrule fields!

Talking with the vendor, He asks you to help him handle 100 
of his clients for an incredible gift!
```

Level : Easy
Author : Mizu

## Write up
Programming language : Python 🐍

For this challenge, we need to send the bill of a client who tell us what he buys and sells. 

The problem is there a timeout in the anwser so we need to be quick, one solution two solution possible, be superman and calculate and send faster or be normal and write a script.

```
,--.   ,--.              ,---.,--.               ,--.             ,--.                    
|   `.'   |,--. ,--.    /  .-'`--',--.--. ,---.,-'  '-.     ,---. |  ,---.  ,---.  ,---.  
|  |'.'|  | \  '  /     |  `-,,--.|  .--'(  .-''-.  .-'    (  .-' |  .-.  || .-. || .-. | 
|  |   |  |  \   '      |  .-'|  ||  |   .-'  `) |  |      .-'  `)|  | |  |' '-' '| '-' ' 
`--'   `--'.-'  /       `--'  `--'`--'   `----'  `--'      `----' `--' `--' `---' |  |-'  
           `---'                                                                  `--'    
           
           
Welcome adventurer, I heard that you're looking for precious treasures.
I can offer you one of thoses, but first need to handle 100 of my clients in a row.
I will come back when you are finished.
Good luck!

--------------------
Client n°1:
Link enters the shop...
He want to buy a hammer (202521 rupees) and a hammer (401595 rupees). How much will He paid for it?
```

Several problems we got :
* Connection between your script and the server
* Get the client's informations

To create a connection we need to use the module `socket` of python. I found a script to make this connection on github: https://gist.github.com/leonjza/f35a7252babdf77c8421.

Now, we have to manage the bill, by looking at the terminal output I decided to use regular expression with the module `re` of python.

```
(buy|sell) (a|[0-9]+) [a-z]+ (\([0-9]* rupees\))( and (((a|[0-9]+) [a-z]+ (\([0-9]* rupees\)))|(sell|buy) (a|[0-9]+) [a-z]+ (\([0-9]* rupees\))))?
```

This regex get if the first choice of the client is a buy or a sell and how many, we get after the number of rupees that will be add or remove to the final bill, we repeat the this action if we got a second choice.

#### Schema of the information collect by the regular expression
```
He want to buy a hammer (202521 rupees) and sell 97815 hammer (401595 rupees). How much will He paid for it?
           --- -        ---------------     ---- -----        ---------------
          type count         price          type count             price
```

After collecting all the informations, we need a second regex to transform the price into a number, `(202521 rupees)` into `202521`.

There is it : 
```
^\(([0-9]+) rupees\)$
```

To finish, we need to implement those regex into our code, and manage by a set of conditions the informations collected.

Final Code : 
```python
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
```
It is not the best way, one reason because I am using a while loop, also regex could not be fastest method.

There is the flag :
![flag.png]{/images/flag.png}
```
R2Lille{Th3_Gr34t3ST_Sh0P}
```