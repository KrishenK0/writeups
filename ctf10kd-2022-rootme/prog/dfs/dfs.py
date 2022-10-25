import socket, re

def dfs(visited, graph, node):
    if node not in visited:
        visited.add(node)
        for neighbour in graph[node]:
            dfs(visited, graph, int(neighbour))

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

nc = Netcat('ctf10k.root-me.org', 8001)
for i in range(60):
    visited = set()  # Set to keep track of visited nodes.
    res = nc.read_until('>')
    graph = {}
    print(res)

    target = list(re.search(r'node ([0-9]+) from (([0-9]+))', res).groups())

    n = 0
    for groups in re.findall(r'Node ([0-9]+)(.*:([0-9, ]+))?', res):
        graph[n] = []
        for i in groups[-1].split(','):
            if i.strip() != '': graph[n].append(i.strip())
 
        n+=1

    print(target[1],'--reach-->',target[0])

    dfs(visited, graph, int(target[1]))
    print(visited)

    output = 'yes' if int(target[0]) in visited else 'no'
    print('>>', output)
    nc.write(output+'\n')
    print(nc.read_until('\n'))

print(nc.read_until('\n'))
nc.close()
