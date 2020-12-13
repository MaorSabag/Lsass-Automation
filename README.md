# lsass_automation
> Original Author: Maor Sabag


A python script to automate the NTLM hash dumping from the Lsass process


# Dependencies

```
pip3 install -r requirements.txt
```

# Usage

1. Start a Powershell/Cmd as an administrator
2. python3 lsass_dump.py
3. Choose whether you already have the lsass.dmp file or you want to do it locally.
4. Paste the mimikatz directory (make sure there is a 'mimikatz.exe' file in the folder!)
5. let the script do it's magic.

```
python3 lsass_dump.py
```


