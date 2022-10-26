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
