import os
import time
import requests
import sys
import json


def get_info():
    with open('config.json') as f:
        js = json.load(f)
    salad_auth = js['salad_key']
    salad_refresh_token = '1'
    cookie = {
        "auth": 'CfDJ8Md7UgHDpVlPsHha1CoqW3V6DQAKQe77wMyHmjHo-TmiRdp2GJiXE6VUl2ziMEem00opSjwo2gHx24xruJxNyoctvDDoIB95GW7HrzYluK6IlAWJBnDdpoy92gnP4ncUYOu5xKqMehu_nGFSHg5aYVp8iSIl2EpzWfys73Yvf6HIGm5r1_FBzGQo_hyMxHdX4lkuR0EXU-r1W0fo359JwelBxED50u9nhE-GNGhmdsR1hWjhXW-EJWBsXPPo9lqcUGUztY5R0YtDcs0yz6W9R14AiI-gGsBZSsisKdaHCvmTnN9fWwO3hYONBcKGWYQB_zhm8E1YXho42pbxzLkFL_DGjcoH4YuJdzcBKWhodZ1DKqTua4i3Gcmb6_rxZqe1PRzzroLeHC23o70AsIsNZgo7ieLPljAusFnk37rzDDjD1tqHtCBjXL1n0dnHm3cem2Lq9NVNxBqono37rImsZF3bWawG9gZr75SYYSiLzAF69SFRhegb-Q6mGIhoo4sVQwKYLCB2w06f7OoU0dR5lx9U5fxrFmNNX-lfAC96PBBdwrdTkWBURQbAaUDW2YazwU9gbteXRnO5HeL7fo2cAJs; _gcl_au=1.1.1959961582.1724937767; _ga=GA1.1.914834142.1724937767; mp_19d3c46327408e71cc887b121a537328_mixpanel=%7B%22distinct_id%22%3A%20%22%24device%3A1919e4d884e790-000ae7693ef36-4c657b58-1fa400-1919e4d884e790%22%2C%22%24device_id%22%3A%20%221919e4d884e790-000ae7693ef36-4c657b58-1fa400-1919e4d884e790%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpr%22%3A%20%5B%5D%2C%22__mpap%22%3A%20%5B%5D%7D; mp_e1b0f0af3b3c1db43cfcd002ebee4a0d_mixpanel=%7B%22distinct_id%22%3A%20%22%24device%3A1919e4d8850791-0543704f240596-4c657b58-1fa400-1919e4d8850791%22%2C%22%24device_id%22%3A%20%221919e4d8850791-0543704f240596-4c657b58-1fa400-1919e4d8850791%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpr%22%3A%20%5B%5D%2C%22__mpap%22%3A%20%5B%5D%7D; __hstc=131114960.aeae3b633bedc1084bf9ed3699cb2b5e.1724937767473.1724937767473.1724937767473.1; hubspotutk=aeae3b633bedc1084bf9ed3699cb2b5e; __hssrc=1; _lfa=LF1.1.400386d077f9bbb4.1724937767530; _fuid=OTE2OWIwYjQtOWJkOC00NTU4LWE1NTEtZGNlZTNjYzE0MWQ5; _rdt_uuid=1724937766614.f1968528-7776-4daf-a35d-8f021ed2d2da; flaretrk=%2eyJmaXJzdFZpc2l0RGF0ZSI6IlRodSwgMjkgQXVnIDIwMjQgMTM6MjI6NDYgR01UIiwic3VibWl0UGFnZSI6Imh0dHBzOi8vc2FsYWQuY29tL2Rvd25sb2FkIiwicmVmZXJyZXJVUkwiOiIiLCJsYW5kaW5nVVJMIjoiaHR0cHM6Ly9zYWxhZC5jb20vIiwibGFzdFJlZmVycmVyVVJMIjoiIiwibGFzdExhbmRpbmdVUkwiOiJodHRwczovL3NhbGFkLmNvbS8iLCJsYXN0Vmlld2VkVVJMIjoiaHR0cHM6Ly9zYWxhZC5jb20vIiwiZHJpbGxEYXRhIjp7ImNoYW5uZWwiOiJEaXJlY3QgdHJhZmZpYyIsImRyaWxsRG93bjEiOiJOb25lIiwiZHJpbGxEb3duMiI6Ik5vbmUiLCJkcmlsbERvd24zIjoiTm9uZSIsImRyaWxsRG93bjQiOiJOb25lIn0sImxhc3REcmlsbERhdGEiOnsiY2hhbm5lbCI6IkRpcmVjdCB0cmFmZmljIiwiZHJpbGxEb3duMSI6Ik5vbmUiLCJkcmlsbERvd24yIjoiTm9uZSIsImRyaWxsRG93bjMiOiJOb25lIiwiZHJpbGxEb3duNCI6Ik5vbmUifSwiZ2NsaWQiOiIiLCJtc2Nsa2lkIjoiIiwiZmJjbGlkIjoiIiwiaWQiOiIiLCJjdXN0b21GaWVsZHMiOnt9LCJsYW5kaW5nX3VybCI6Imh0dHBzOi8vc2FsYWQuY29tLyIsInRlc3RfZGF0YSI6IkZyb20gcmVmZXJyZXIsIG9yaWdpbmFsIFVSTDogaHR0cHM6Ly9zYWxhZC5jb20vIiwibGFuZGluZ19wYWdlX2dyb3VwIjoiLyJ9; _hjSessionUser_3718964=eyJpZCI6IjkwZjIxZWM2LTJlNGMtNTExYi04ZTA5LWYyMTI1ZDY5MTZmYyIsImNyZWF0ZWQiOjE3MjQ5Mzc3Njc0MjIsImV4aXN0aW5nIjp0cnVlfQ==; _ga_EBPSP9ECNX=GS1.1.1724937766.1.1.1724937770.56.0.0; _hjSessionUser_2225817=eyJpZCI6ImIwMmU4YzdjLThiYzYtNWExMy05NDU2LWZjODliZDM0Y2FlOSIsImNyZWF0ZWQiOjE3MjQ5Mzc4MDQ1OTgsImV4aXN0aW5nIjpmYWxzZX0=; _hjSession_2225817=eyJpZCI6IjI0NDk1NWVlLWRjOTMtNDZiOS05ODE5LTE3ZDNkNDNlNTIyZiIsImMiOjE3MjQ5Mzc4MDQ1OTgsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=; cf_clearance=niMyxCTvgQvEv_fHnTf.5A4.I6Ox.pnLaZTUv8gLex4-1724939820-1.2.1.1-U_jpWykgbTY2hgcbxIJ6Pyes0QQONbFiHMhBkLL6Wd9IRkyV58JsdXVlITfTzqFjcpTDfRyC5.tLjtNL1Kpz_YcN4k6pAuNcHtbM.pLHKVuaVNttAEgp2XwxSjDqoCQtp7Gdg0NIf5cLpJ97oEYC8gIFixvtskNGOvPP9X.VO5zoCvyP5wKUDzaqLJDnLUVlQfwXwPGl40aMUufeDW3HYmL2MBHhvA07LMnDSWZBv57zPWffcr_mxitW5dQBeYOzxIMvWzTAzxZmvozszx6ZdU8F8ZJ5wvxYJ1zO10gyRSSUsyUZOCbbbAmxiaeCCs49oTOFXIGwKvb091TktAQwjgQBndNFUydnRppwlBhCKUUuoT5nLOYXl3QUX6t_IWQ3aPpX40qc5HlLvMyBOiAlAQ; mp_68db9194f229525012624f3cf368921f_mixpanel=%7B%22distinct_id%22%3A%20%22f9235d65-1d07-40a0-b047-8d43236ab5e1%22%2C%22%24device_id%22%3A%20%221919e6cc5f61eacfd-09ff2968475546-4c657b58-1fa400-1919e6cc5f61eacfd%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fsalad.com%2Faccount%2Fsummary%22%2C%22%24initial_referring_domain%22%3A%20%22salad.com%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fsalad.com%2Faccount%2Fsummary%22%2C%22%24initial_referring_domain%22%3A%20%22salad.com%22%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpr%22%3A%20%5B%5D%2C%22__mpap%22%3A%20%5B%5D%2C%22%24user_id%22%3A%20%22f9235d65-1d07-40a0-b047-8d43236ab5e1%22%7D',
        "X-XSRF-TOKEN": '1'
    }
    headers = {       
        "Host": "salad.com",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/78.0.3904.130 Safari/537.36",
        "Content-Type": "application/json; charset=UTF-8",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://salad.com",
        "Referer": "https://salad.com",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
        "X-XSRF-TOKEN": salad_refresh_token,
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "origin": "https://salad.com",
        "priority": "u=1, i",
        "sec-ch-ua": "Chromium;v=128, Not;A=Brand;v=24, Microsoft Edge;v=128",
        "sec-ch-ua-mobile":"?0",
        "sec-ch-ua-platform":"Windows",
        "sec-fetch-site":"same-site",
    }
    with open('utils/Login screen.txt', encoding='utf-8') as f:
        login_screen = f.read()

    salad_user = requests.get(url='https://app-api.salad.com/api/v1/profile', headers=headers, cookies=cookie)
    if salad_user.status_code != 200:
        print('REPLACE YOUR SALAD AUTH CODE!')
        input()
        exit()
    salad_user = salad_user.json()

    referral = requests.get(url='https://app-api.salad.com/api/v1/profile/referral-code', headers=headers,
                            cookies=cookie)
    if referral.status_code != 200:
        print('REPLACE YOUR SALAD AUTH CODE!')
        input()
        exit()
    referral = referral.json()
    return [salad_user, referral, login_screen]


def print_info(salad_user, login_screen):
    print(login_screen)
    print('Username: ' + str(salad_user['username']))
    print('Email: ' + str(salad_user['email']))
    print('User id: ' + str(salad_user['id']))
    # print('Username: HIDDEN IN TEST MODE!')
    # print('Email: HIDDEN IN TEST MODE!')
    # print('User id: HIDDEN IN TEST MODE!')
    print("\n\n")




def starting(info):
    os.system('clear')
    sys.stdout.write("\x1b]2;Salad CLI+\x07")
    color = "\033[32m"  # this color is green
    os.system(f"echo {color}")
    print(info[2])
    # input selection
    select = input(
        "Select option! \n1. Balance \n2. Lifetime \n3. XP \n4. Earning History \n5. Copy Referral Code \n"
        "6. Start mining!"
        " \nSelect: ")
    if select == "1" or select.lower() == "balance":
        return 1

    if select == "2" or select.lower() == "lifetime":
        return 2

    if select == "3" or select.lower() == "xp":
        return 3

    if select == "4" or select.lower() == "earning history":
        return 4

    if select == "5" or select.lower() == "copy referral code":
        return 5

    if select == "6" or select.lower() == "start mining":
        return 6
    print_info(info[0], info[2])
