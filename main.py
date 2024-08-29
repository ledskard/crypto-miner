import sys
import os
import json

try:
    from utils import Start
    from utils import Balance
except ModuleNotFoundError:
    pass


def setup():
    sys.stdout.write("\x1b]2;Salad CLI+ SETUP\x07")
    salad_key = input("Insert your salad Authentication token: ")
    wallet = input("Insert your salad wallet address: ")
    refresh_token = input("Insert your salad refresh token: ")
    data = {
        "salad_key": salad_key,
        "wallet": wallet,
        "salad_refresh_token": refresh_token
    }
    with open("config.json", "w+") as file:
        json.dump(data, file)
    python_var = input("\nEnter the name of your python prefix (for example \"python3\"): ")
    print("installing required libraries")
    os.system(f"{python_var} -m pip install --upgrade pip")
    os.system(f"{python_var} -m pip install pyperclip")
    os.system(f"{python_var} -m pip install python-dateutil")
    os.system(f"{python_var} -m pip install argparse")
    os.system(f"{python_var} -m pip install requests")
    os.system("chmod +x miners/ethminer/ethminer")
    os.system("chmod +x miners/PhoenixMiner/PhoenixMiner")
    os.system("chmod +x miners/t-rex/t-rex")
    os.system("chmod +x miners/XMRig/xmrig")


switch = {
    1: "Balance.Salad_Balance()",
    2: "Lifetime.Salad_Lifetime()",
    3: "XP.Salad_XP()",
    4: "salad_earnings_update.Salad_Earnings()",
    6: "Mining.Salad_Mining()"
}

try:
    with open("config.json") as file:
        pass
except FileNotFoundError:
    setup()

from utils import Start
from utils import Balance
from utils import Mining
from utils import XP
from utils import Lifetime
from utils import salad_earnings_update
import pyperclip

while True:
    info = Start.get_info()
    dun = False
    while not dun:
        # os.system('clear')
        action = Start.starting(info)
        try:
            int(action)
            dun = True
        except TypeError or KeyError:
            pass
        if dun:
            exec(switch[int(action)])
            dun = True
