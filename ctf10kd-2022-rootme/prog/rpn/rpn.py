import socket, re

class Netcat:
    def __init__(self, ip, port):
        self.buff = ""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip, port))
    def read(self, length=1024):
        return self.socket.recv(length)
    def read_until(self, data):
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

nc = Netcat('ctf10k.root-me.org', 8002)

def evaluate(expression):
  expression = expression.split()
  stack = []
  for ele in expression:
    if ele not in '/x+-': stack.append(int(ele))
    else:
      right = stack.pop()
      left = stack.pop()
      if ele == '+': stack.append(left + right)
      elif ele == '-': stack.append(left - right)
      elif ele == 'x': stack.append(left * right)
      elif ele == '/': stack.append(int(left / right))
   
  return stack.pop()

for i in range(100):
    inpt = nc.read_until('>')
    print(inpt)
    rpn = re.findall(r'(.*)\n>', inpt)[0]

    print(rpn)
    solve = str(evaluate(rpn))
    print('>>',solve)
    nc.write(solve+'\n')
    print(nc.read_until('\n'))

print(nc.read_until('\n'))
nc.close()