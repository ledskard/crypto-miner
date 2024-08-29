import os
import time
import sys
import json


def Salad_Mining():
    print('entrou')
    norm = True
    wallet = "3LHpkPBNRwXhJ7ttGYD5ToWmGgQ1PE7zGe.z8nwbcswzb19xkb"
    sys.stdout.write("\x1b]2;Choose miner...\x07")
    color = "\033[32m"  # this is green
    os.system('echo ' + color)
    select = input("Select miner! \n"
                   "1. Phoenixminer (Nvidia-GPU) \n"
                   "2. T-rex (Nvidia-GPU) \n"
                   "3. Return \nSelect: ")
    if select == "1" or select.lower() == "phoenixminer":
        os.system('clear')
        sys.stdout.write("\x1b]2;Mining ethash with PhoenixMiner\x07")
        if norm:
            os.system(
                r" sudo ../miners/PhoenixMiner/PhoenixMiner -logfile phoenixlog.txt -rmode 0 -rvram 1 -pool"
                print('connected to phoenix')
                r" stratum+tcp://daggerhashimoto.usa.nicehash.com:3353 -pool2"
                print('starting pool')
                r" stratum+tcp://daggerhashimoto.eu.nicehash.com:3353 -ewal " + (
                    wallet) + " -esm 3 -allpools 1 -allcoins 0")
        else:
            os.system(
                r"../miners/PhoenixMiner/PhoenixMiner -logfile phoenixlog.txt -rmode 0 -rvram 1 -pool"
                r" stratum+tcp://daggerhashimoto.usa.nicehash.com:3353 -pool2"
                r" stratum+tcp://daggerhashimoto.eu.nicehash.com:3353 -ewal " + (
                    wallet) + " -esm 3 -allpools 1 -allcoins 0")

    elif select == "2" or select.lower() == "t-rex" or select.lower() == "trex":
        os.system("clear")
        sys.stdout.write("\x1b]2;Mining ethash with T-Rex miner\x07")
        if norm:
            os.system(
                r"../miners/t-rex/t-rex -a ethash -o"
                r" stratum+tcp://daggerhashimoto.usa.nicehash.com:3353"
                rf" -u {wallet}")
        else:
            os.system(
                r"../miners/t-rex/t-rex -a ethash -o"
                r" stratum+tcp://daggerhashimoto.usa.nicehash.com:3353"
                rf" -u {wallet}")
    else:
        print("Quitting...")
        time.sleep(1)

if __name__ == "__main__":
    Salad_Mining()
