import threading
import requests
import random
import ctypes
from colorama import Fore

promos = open("promos.txt", "r").read().splitlines()


class data:
    redeemed = 0
    invalid = 0
    checked = 0
    errors = 0
    valid = 0


lock = threading.Lock()


def info(msg, code, color):
    lock.acquire()
    print(f"{color} [!] {code} - {msg}{Fore.RESET}")
    lock.release()


def getDict():
    proxy = random.choice(open("proxies.txt", "r").read().splitlines())
    return {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
    # get proxy


def update_console():
    while True:
        ctypes.windll.kernel32.SetConsoleTitleW(f"Checked: {data.checked} | Valid: {data.valid} | Invalid: {data.invalid} | Redeemed: {data.redeemed} | Errors: {data.errors}")
        # idk looks cooler for people to keep track on and makes value +10000$???


def check_promo(promo, proxy):
    if data.checked == len(promos):
        print("Checked all codes")
    url = f"https://discord.com/api/v9/entitlements/gift-codes/{promo.replace('https://discord.com/billing/promotions/', '').replace('https://promos.discord.gg/', '').replace('/', '')}"
    # looks so shit had to because people didnt know ctrl h existed
    
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
    }
    # you can just keep user agent or add something idfk
    try:
        req = requests.get(url, headers=headers, proxies=proxy)
        if req.status_code == 404:
            data.invalid += 1
            data.checked += 1
            info("Invalid", promo, Fore.RED)

        elif req.status_code == 200 and req.json()["uses"] == 1:
            data.redeemed += 1
            data.checked += 1
            info("Redeemed", promo, Fore.RED)

        elif req.status_code == 200 and req.json()["uses"] == 0:
            data.valid += 1
            data.checked += 1
            info("Valid", promo, Fore.GREEN)
            open("valid.txt", 'a').write(promo + '\n')
        else:
            data.errors += 1
            data.checked += 1
            print(req.json())
    except Exception:
        check_promo(promo, proxy)
        pass


for promo in promos:
    proxy = getDict()
    t = threading.Thread(target=check_promo, args=[promo, proxy])
    t.start()
    w = threading.Thread(target=update_console)
    w.start()
