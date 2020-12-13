# lsass_automation
A python script to automate the NTLM hash dumping form the Lsass process
The Usage is easy, first of all you have to run the script on a windows OS.
Make sure you have the nessecery python module, you can pip3 install -r requirements.txt .

1. Start a Powershell/Cmd as an administrator
2. python3 lsass_dump.py
3. Choose whether you already have the lsass.dmp file or you want to do it locally.
4. Paste the mimikatz directory (make sure there is a 'mimikatz.exe' file in the folder!)
5. let the script do it's magic.
