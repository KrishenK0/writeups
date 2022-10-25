# Physics quizz speedrun

```
You found a super cool ranked quizz online about physics. It rewards anybody that can complete it faster than all of the predecessors.

Note : the atomic weight must be rounded to one decimal number.
```
Difficulty: medium\
Point : 374\
Author : Elf#4541

## Write up

### Overview
```
0101100101101111001011000010000001110000011011000110010101100001011100110110010100100000011101000110010101101100011011000010000001101101011001010010000001110111011010000110000101110100001000000110100101110011001000000111010001101000011001010010000001110110011000010110110001110101011001010010000001101111011001100010000001110100011010000110010100100000011000010111010001101111011011010110100101100011001000000111011101100101011010010110011101101000011101000010000001100110011011110111001000100000011101000110100001100101001000000100001101101000011011000110111101110010011010010110111001100101
```
The output shows us a list of nodes, where some nodes have edges pointing to others (pointing to other nodes) and some do not.
The challenge is to create a DFS algorithm, for searching a node from another one in a tree.

The goal is to send if we can get to the target node from the beginning one.

Lets programming it!

### Programmation
Programming language : Python 🐍

#### 1. Connection
First of all, we need to etablish a connection between our script and the server, for that I will use `socket` module from python. But the best method is to use `pwn`, because it offers a faster way for connecting.

#### 2. Get the datas
We need to get the list of all nodes' children from the output. For performing that, I used powerful regexes (although).

First regex, it store the target node number and what number we start when searching.
```re
'node ([0-9]+) from (([0-9]+))'
```
Schema :
```
Here's my graph's adjacency list, can you tell me if I can reach node 6 from 0 please? (yes / no)
                                                                      -      -
                                                                    Target  Start
...
```
Second regex, it get the node number and his childrens.
```re
'Node ([0-9]+)(.*:([0-9, ]+))?'
```
Schema :
```
...
Node 0 has a directed edge to : 7, 15
     -                          -----
   Number                     Childrens
...
```

#### 2. Iterate the childrens

We need to iterate all children node, that means each child we met, we are restarting the iteration. To performs that, we need to define a recursive function. We stop the current iteration if we already met the nodes.

Our recursive function is:
```python
def dfs(visited, graph, node):
    if node not in visited:
        visited.add(node)
        for neighbour in graph[node]:
            dfs(visited, graph, int(neighbour))
```
Source : https://www.educative.io/answers/how-to-implement-depth-first-search-in-python


#### 3. Answer the question

After iterate the nodes, we need to see if we encounter the target then send the answer.
```python
output = 'yes' if int(target[0]) in visited else 'no'
```

Thus, we put the function and the data in the for loop, and after iteration we will get the flag.

>Because we know the number of question, no need to do a while loop this time. 😛

## Final code

```python
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
```

*Note: The connection method can be optimize by using the `pwn` module.*

There is the flag 😄🚩
```
Well done! Your flag is RM{34sy_d3pth_f1rst_s3arch}
```