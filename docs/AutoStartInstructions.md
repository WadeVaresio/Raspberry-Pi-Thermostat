# Creating a Startup Script on a Raspberry Pi

# Steps:
You will need to create a launcher script and configure the Pi to run the script on boot.

## Create the shell script
1. Create a shell script in your project directory. Do this in terminal by running the command `touch launcher.sh`
2. Edit the shell script so it navigates into your directory and runs your main python script, example `cd home/pi/ProjectName`
3. Make the launcher script executable by running `chmod u+x filename` in your projects source code directory ex. `chmod u+x launcher.sh`.

### Example Launcher Script
```bash
#!/usr/bin/env bash

cd /home/pi/Cloned-Location
python3 main.py
```

## Auto run script on boot
1. Go into the terminal and run `crontab -e`
2. Select the editor you want to use in terminal to edit the crontab (nano or vim)
3. Enter the line at the bottom `@reboot sh /path/to/your/launcher/script`
    * Ensure the path to your launcher script is correct, if it is incorrect the auto start will fail
4. Reboot the pi and test if it works.

## Troubleshooting
Ensure that the password on the Raspberry Pi is disabled upon startup, [guide](https://elinux.org/RPi_Debian_Auto_Login).

You may need to add a system path for your imports example:
```python
import sys
sys.path.insert(0, '/usr/local/lib/python3.5/dist-packages')
```
