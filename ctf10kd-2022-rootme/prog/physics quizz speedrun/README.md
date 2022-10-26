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

The output is a binary encoded message, that means `Yo, please tell me what is the value of the atomic weight for the Chlorine`.

Thus our goal is to get the atomic informations and send the answer of this question.

Lets programming it!

> Note: In this write up, all message send and receive will be automaticly decoded/encoded to binary.

### Programmation

Programming language : Python 🐍

#### 1. Connection

First of all, we need to etablish a connection between our script and the server, for that I will use the function `create_connection` from the module `websocket` in python.

#### 2. Get the datas

I use a regex to get the subject and the atomic element of the question.

```re
'(cas|electrons|weight)[a-z ]+([A-Za-z]+)'
```

Schema:

```
Yo, please tell me what is the value of the atomic weight for the Chlorine
                                                   ------         --------
                                                   Subject        Atomic element
```

#### 3. Searching the element's informations

After a few research on internet, I discover a github where there is a .json file with a database of all elements with their informations (number of atoms, atomic mass, author, ...) Which in our case is helpful. However, there is no information about the [CAS number](https://en.wikipedia.org/wiki/CAS_Registry_Number) of the elements.

Thus, I choose to scrap the site `https://commonchemistry.cas.org/results?q=`, the CAS number store here `<div class="result-content" aria-label="{CAS-NUMBER}">`.

```python
page = requests.get(f"https://commonchemistry.cas.org/results?q={groups[1]}").content
soup = BeautifulSoup(page, "html.parser")
result = re.findall(r'[0-9-]+', soup.find('div', attrs={'class':'result-content'})['aria-label'])[0]')
```

> The regex I use just recover the CAS `XXX-XX-X`

#### 3. Answer the question

Thus, after getting all the informations we need, we access to the elements informations with the JSON file, CAS website, send the anwser then loop it.

## Final code

```python
from websocket import create_connection
import re, requests, os
from bs4 import BeautifulSoup
import json

def toBinary(a):
  l,m=[],[]
  for i in a:
    l.append(ord(i))
  for i in l:
    m.append(int(bin(i)[2:]))
  return m

elements = []
with open(os.path.dirname(os.path.abspath(__file__)) + '/periodic.json', 'r') as f:
        JSON = json.loads(f.read())

        for i in range(len(JSON['elements'])):
            elements.append(JSON['elements'][i].get('name'))

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def bin2str(bin_data):
    str_data = ''
    for i in range(0, len(bin_data), 8):
            binary = bin_data[i:i + 8]
            decimal_data = int(binary, 2)
            str_data += chr(decimal_data)
    return str_data




while True:
    ws = create_connection("ws://ctf10k.root-me.org:8000")

    while True:
        str_data = bin2str(ws.recv())

        regex = re.search(r"(cas|electrons|weight)[a-z ]+([A-Za-z]+)", str_data)
        try:
            groups = regex.groups()
        except AttributeError:
            print(str_data)

        if groups[0] == 'cas' :
            page = requests.get(f"https://commonchemistry.cas.org/results?q={groups[1]}").content
            soup = BeautifulSoup(page, "html.parser")

            result = re.findall(r'[0-9-]+', soup.find('div', attrs={'class':'result-content'})['aria-label'])[0]
        elif groups[0] == 'weight':
            result = round(JSON['elements'][elements.index(groups[1])].get('atomic_mass'), 3)
            # Patched
            # if isinstance(result, int): result = "%.1f" % result
        elif groups[0] == 'electrons':
            result = sum(JSON['elements'][elements.index(groups[1])].get('shells'))


        print(str_data, '\n>>', result)
        result = str(result)
        ws.send(''.join(f"{ord(i):08b}" for i in result))
        res = bin2str(ws.recv())
        if res.find('WRONG')!=-1 or res.find('Congratz, ')!=-1: break

    if res.find('Congratz, ')!=-1: print(f"{bcolors.OKGREEN}{bcolors.BOLD}Success{bcolors.ENDC}")
    else: print(f"{bcolors.FAIL}Error while processing, restarting script...{bcolors.ENDC}")
    ws.close()
```

_Note: Because for this challenge I don't use the same database from the source code. My script is not 100% accurante, that is why the script is in a second while loop._

There is the flag 😄🚩

```
Well done! Your flag is RM{34sy_d3pth_f1rst_s3arch}
```
