# RPN

```
Who needs parentheses when you can use Jan's RPN to get an unambiguous formula?
```
Difficulty: easy\
Point : 144\
Author : Elf#4541

## Write up

### Overview
```
647 383 22 869 + - +
>
```
Like the title of the challenge tell us, this is RPN (Reverse Polish Notation) calcul. It is a mathematical notatation in which operators follow theirs operands.

There is an example with the calcul above:
```
647 383 22 869 + - +
647 383 891 - +
647 -508 +
139
```
So the operation `647 383 22 869 + - +` equals to `139`.

Lets programming it!

### Programmation
Programming language : Python 🐍

#### 1. Connection
First of all, we need to etablish a connection between our script and the server, for that I will use `socket` module from python. But the best method is to use `pwn`, because it offers a faster way for connecting.

#### 2. Get the datas
As you can see, we need to get the calcul from the output. For that I used a powerful method, the regex.

```re
'(.*)\n>'
```
>Explenation : I take everything between the **>**
```
Can you solve this for me?
858 802 727 815 17 x 779 - + + +
---------------------------------
>
```
#### 2. Calcul the RPN

For the calcul part, we need to split each operators and operands, then list them and if it is an operand, do the operation with two previous number

The translation in python give us this function.
```python
def evaluate(expression):
  # splitting expression at whitespaces
  expression = expression.split()
   
  # stack
  stack = []
   
  # iterating expression
  for ele in expression:
     
    # ele is a number
    if ele not in '/x+-':
      stack.append(int(ele))
     
    # ele is an operator
    else:
      # getting operands
      right = stack.pop()
      left = stack.pop()
       
      # performing operation according to operator
      if ele == '+':
        stack.append(left + right)
         
      elif ele == '-':
        stack.append(left - right)
         
      elif ele == '*':
        stack.append(left * right)
         
      elif ele == '/':
        stack.append(int(left / right))
   
  # return final answer.
  return stack.pop()
```
Source : https://www.geeksforgeeks.org/evaluate-the-value-of-an-arithmetic-expression-in-reverse-polish-notation-in-java/


Thus, put the function and the data in the for loop, and after iteration we will get the flag.


>First we need to put this to a while loop, iterate the numbers of questions, else we cannot show the flag with my script

## Final code

```python
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
```

*Note: The script is not the most optimal, because it use a forloop, so you need to know how many question there are. And the connection method can be optimize with the `pwn` module as I said before*

There is the flag 😄
```
Congratz! Your flag is RM{Luk4s13w1cz_w0uld_b3_pr0ud}
```