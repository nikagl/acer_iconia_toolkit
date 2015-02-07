#!/bin/python
# coding: utf8
##########################################
# Acer Iconia Toolkit                    #
# version:                0.9.2          #
# date:                   2015-02-07     #
##########################################
version = "v0.9.2"

from struct import calcsize
from time import sleep
import argparse
import os
import re
import subprocess
import sys
import time

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug", help="Print debug messages", action="store_true")
debug = parser.parse_args().debug

python3 = True
if sys.version_info < (3,0):
    python3 = False

arch = calcsize("P") * 8
if arch != 32 and arch != 64:
    print(timestamp() + ": E: Only 64bit and 32bit architecture supported.")
    print("")
    user_input("Press Enter to leave Application...")
    sys.exit(1)

os_name = os.name
bin_folder   = os.path.join("bin", os_name, str(arch)) + os.sep
windows = True
adb = ""
if os_name == "posix":
    windows = False
    adb = "sudo " + bin_folder + "adb "
elif os_name == "nt":
    adb = bin_folder + "adb.exe "
else:
    print(timestamp() + ": Operating System: '" + os_name + "' not supported. Only for Windows and Unix/Linux.")
    print("")
    user_input("Press Enter to leave Application...")
    sys.exit(1)

system_image = os.path.join("system_image", "system.img.gz")
busybox      = os.path.join("bin", "busybox")
baksmali     = os.path.join("bin", "baksmali.jar")
smali        = os.path.join("bin", "smali.jar")
zipalign     = bin_folder + "zipalign "
dev_null     = open(os.devnull, 'w')
su           = ""
dd_count     = ""
dd_seek      = ""
device       = ""
driver_url   = ""
dumchar_line = ""
enableXposed = False
allatonce    = False
a1           = False
a1_811       = False
b1_710       = False
kitkat       = False
system_image_target_dir = "/cache"



def main():
    print("")
    print("======= Acer Iconia Toolkit " + version + " =======")
    print("")
    print("Which device do you have?")
    print("[1] Acer Iconia B1-A71")
    print("[2] Acer Iconia A1-810 / A1-811 / A3-A10 / B1-711 / B1-720")
    print("[3] Acer Iconia B1-710 / B1-A710")
    print("[Q] Quit")
    print("")

    selection = user_input("Enter a selection: ")
    if selection == "q" or selection == "Q":
        sys.exit(0)

    global enableXposed
    global allatonce
    global system_image_target_dir
    global kitkat
    global a1
    global a1_811
    global b1_710
    global device
    global driver_url
    global dd_count
    global dd_seek
    global su

    if selection == "1":
        su = os.path.join("bin", "b1", "su")
        device = "Acer Iconia B1-A71"
        driver_url = "http://goo.gl/doR8L"
        dd_count = "156928"
        dd_seek = "8424"
        dumchar_line = "android 0x0000000026500000 0x00000000020e8000 2 /dev/block/mmcblk0p3"
    elif selection == "2":
        a1 = True
        device = "Acer Iconia A1-810 / A1-811 / A3-A10 / B1-711 / B1-720"
        driver_url = "http://goo.gl/i56Gn"
        dd_count = "262144"
        dd_seek = "17664"
        su = os.path.join("bin", "a1", "su")
        dumchar_line = "android 0x0000000004500000 0x0000000040000000 2 /dev/block/mmcblk0p5"
        # Add-on for A1 KitKat
        print("")
        print("Which device do you have?")
        print("[1] Acer Iconia A1-810 / A1-811 / A3-A10 / B1-711 / B1-720 with Android JellyBean")
        print("[2] Acer Iconia A1-810 / A3-A10 / B1-711 / B1-720 with Android KitKat 4.4.2 or higher")
        print("[3] Acer Iconia A1-811 with Android KitKat 4.4.2 or higher")
        print("[Q]uit")
        selection2 = user_input("Enter a selection: ")
        if selection2 == "q" or selection2 == "Q":
            sys.exit(0)
        if selection2 == "1":
            kitkat = False
        elif selection2 == "2":
            kitkat = True
            device = "Acer Iconia A1-810 / A3-A10 / B1-711 / B1-720 running KitKat"
            system_image_target_dir = "/data/local/tmp"
        elif selection2 == "3":
            kitkat = True
            a1_811 = True
            device = "Acer Iconia A1-811 running KitKat"
            system_image_target_dir = "/data/local/tmp"
        else:
            print("E: Only '1', '2', '3' and 'Q' is allowed!")
            main()
        # End of Add-on for A1 KitKat
    elif selection == "3":
        b1_710 = True
        su = os.path.join("bin", "b1", "su")
        device = "Acer Iconia B1-710 / B1-A710"
        driver_url = "http://goo.gl/Otbkb"
        dd_count = "262144"
        dd_seek = "9448"
    else:
        print("E: Only '1', '2', '3' and 'Q' is allowed!")
        main()
    menu()
    sys.exit(0)

def menu():
    global device

    print("")
    print("======= " + device + " Toolkit " + version + " =======")
    print("")
    print("What do you want to do?")
    print("[1] Root")
    print("[2] Unroot")
    print("[3] Internal 2 External (needs root)")
    print("[4] Odex (needs root)")
    print("[5] Pull system.img.gz from tablet")
    print("[Q] Quit")
    print("")

    selection = user_input("Enter a selection: ")
    if selection == "q" or selection == "Q":
        sys.exit(0)

    if selection == "3":
        swap_menu()

    if selection == "4":
        odex()

    if selection == "5":
        pull_system_image_prepare()
        sys.exit(0)

    if windows:
        if selection == "1":
            root()
        elif selection == "2":
            unroot()
        else:
            print("E: Only '1', '2', '3', '4', '5' and 'Q' is allowed!")
            menu()
    else:
        if selection == "1":
            unix_root_menu()
        elif selection == "2":
            unroot()
        else:
            print("E: Only '1', '2', '3', '4', '5' and 'Q' is allowed!")
            menu()
    sys.exit(0)

def swap_menu():
    print("")
    print("===== Internal 2 External ======")
    print("Make sure an external micro sd card is plugged in.")

    if not windows:
        subprocess_call("sudo chmod +x " + bin_folder + "adb")

    check_adb()

    # Check which configuration is present
    print("")
    print("Checking current partition settings...")
    subprocess_call(adb + "pull /etc/vold.fstab")

    vold_fstab_str = "vold.fstab"
    try:
        with open(vold_fstab_str):
            print_debug(timestamp() + ": Successfully pulled vold.fstab.")
    except IOError:
        print("E: Failed to check partition settings. Couldn't pull /etc/vold.fstab.")
        wait_for_enter_exit_error()

    config_internal = ""
    config_external = ""
    vold_fstab = open(vold_fstab_str, "r")
    lines = vold_fstab.readlines()
    print("")
    print("Current SD partition configuration: ")

    sd_name = "mtk-sd"
    if a1:
        sd_name = "mtk-msdc"

    for l in lines:
        if l.startswith("#"):
            continue
        if "dev_mount sdcard /storage/sdcard0 emmc@fat /devices/platform/goldfish_mmc.0 /devices/platform/" + sd_name + ".0/mmc_host" in l:
            print("Internal SD -> Internal (Default).")
            config_internal = "default"
        elif "dev_mount sdcard2 /storage/sdcard1 auto /devices/platform/goldfish_mmc.1 /devices/platform/" + sd_name + ".1/mmc_host" in l:
            print("External SD -> External (Default).")
            config_external = "default"
        elif "dev_mount sdcard /storage/sdcard1 emmc@fat /devices/platform/goldfish_mmc.1 /devices/platform/" + sd_name + ".0/mmc_host" in l:
            print("Internal SD -> External (Swapped).")
            config_internal = "swapped"
        elif "dev_mount sdcard2 /storage/sdcard0 auto /devices/platform/goldfish_mmc.0 /devices/platform/" + sd_name + ".1/mmc_host" in l:
            print("External SD -> External (Swapped).")
            config_external = "swapped"
    vold_fstab.close()
    os.remove(vold_fstab_str)

    if config_internal == "" or \
       config_external == "":
        print("E: Failed to determine sd partition configuration.")
        wait_for_enter_exit_error()

    if config_internal != config_external:
        print("E: Mixed up SD partition configuration.")
        wait_for_enter_exit_error()

    print("")
    print("Would you like to backup data from your partition, mapped as External SD, before swapping partitions?")
    print("[1] Yes")
    print("[2] I need more Internal space! Now!")
    print("[Q] Quit")
    print("")

    selection = user_input("Enter a selection: ")
    if selection == "q" or selection == "Q":
        sys.exit(0)

    # swap partitions with or w/o backup
    backup = True
    if selection == "2" or \
       selection.lower() == "no":
        backup = False
    else:
        backup_ext_sd(config_internal)

    swap_ext_to_int_sd(config_internal)

    if backup:
        restore_ext_sd(config_internal)

#    print(timestamp() + ": Trying to reboot your device...")
#    subprocess_call(adb + "shell reboot")
    print("")
    print(timestamp() + ": SUCCESS!")
    print("The SD partitions of your " + device + " are now successfully swapped.")
    print("Do a reboot and enjoy.")
    print_thanks()
    wait_for_enter_exit_success()


def odex():
    print("")
    print("========== Odexing " + device + " ==========")

    if not windows:
        subprocess_call("sudo chmod +x " + bin_folder + "adb")

    check_adb()

    print("")
    print( "Hit Enter to start Odexing. This can take a while. If your " + device + " does a reboot, you succeeded." )
    wait_for_enter_start()

    # remount /system with RW permissions
    if debug:
        p = subprocess.Popen(adb + "shell", stdin=subprocess.PIPE, shell=True)
    else:
        p = subprocess.Popen(adb + "shell", stdin=subprocess.PIPE, stderr=dev_null, stdout=dev_null, shell=True)
    process_input(p,"su")
    process_input(p,"mount -o rw,remount /system")
    process_input(p,"chmod 777 /system/bin/")
    process_input(p,"chmod 777 /system/xbin/")
    process_input(p,"exit")
    process_input(p,"exit")
    p.stdin.flush()

    # copy dexo tool and its files
    subprocess_call(adb + "push bin/odex/dexo /system/bin/")
    subprocess_call(adb + "shell su -c 'chmod 777 /system/bin/dexo'")
    subprocess_call(adb + "push bin/odex/dexopt-wrapper /system/bin/")
    subprocess_call(adb + "shell su -c 'chmod 777 /system/bin/dexopt-wrapper'")
    subprocess_call(adb + "push bin/odex/busyodex /system/xbin/")
    subprocess_call(adb + "shell su -c 'chmod 777 /system/xbin/busyodex'")
    subprocess_call(adb + "push bin/odex/zip /system/xbin/")
    subprocess_call(adb + "shell su -c 'chmod 777 /system/xbin/zip'")
    subprocess_call(adb + "push bin/odex/zipalign /system/xbin/")
    subprocess_call(adb + "shell su -c 'chmod 777 /system/xbin/zipalign'")

    # odex and remount /system as RO
    if debug:
        p = subprocess.Popen(adb + "shell", stdin=subprocess.PIPE, shell=True)
    else:
        p = subprocess.Popen(adb + "shell", stdin=subprocess.PIPE, stderr=dev_null, stdout=dev_null, shell=True)

    process_input(p,"su")
    process_input(p,"chmod 755 /system/bin/")
    process_input(p,"chmod 755 /system/xbin/")
    process_input(p,"cd /system/xbin")
    process_input(p,"/data/local/tmp/busybox cp -r busybox bb1")
    process_input(p,"/data/local/tmp/busybox cp -r busyodex busybox")
    process_input(p,"/data/local/tmp/busybox --help | /data/local/tmp/busybox grep 'Currently defined functions:' -A300 | /data/local/tmp/busybox grep -v 'Currently defined functions:' | /data/local/tmp/busybox tr , '\n' | /data/local/tmp/busybox xargs -n1 /data/local/tmp/busybox ln -s busybox")
    process_input(p,"cp -r bb1 busybox")
    process_input(p,"rm bb1")
    p.stdin.flush()

    subprocess_call(adb + "shell su -c 'dexo -all'")

    # no remount /system RO because dexo -all does a reboot anyway

    print("")
    print(timestamp() + ": If your " + device + " is now rebooting, you're successfully odexed!")
    print_thanks()
    wait_for_enter_exit_success()

def unix_root_menu():
    print("")
    print("What do you want to do?")
    print("[1] Root from scratch (without prerooted system.img.gz).")
    print("[2] Root with prerooted system.img.gz (must be placed in folder 'system_image' on your PC)")
    print("[Q] Quit")

    selection = user_input("Enter a selection: ")
    if selection == "q" or selection == "Q":
        sys.exit(0)

    if selection == "1":
        unix_root_from_scratch()
    elif selection == "2":
        root()
    else:
        print("E: Only '1' or '2' is allowed!")
        unix_root_menu()

def pull_system_image_prepare():
    print("")
    print("=========== Pull System Image ===========")

    print("Before we can start, please do following:")
    if windows:
        print("1. Make sure drivers for your " + device + " are installed, you can find them here: " + driver_url)
        print("2. Plug-In your " + device + " into this PC.")
        print("3. Enable USB Debugging Mode by going into Settings -> Developer Tools.")
    else:
        print("1. Plug-In your " + device + " into this PC.")
        print("2. Enable USB Debugging Mode by going into Settings -> Developer Tools.")
    wait_for_enter_start()

    if not windows:
        subprocess_call("sudo chmod +x " + bin_folder + "adb")

    check_adb()
    push_busybox()
    start_telnet_server()
    check_dumchar_info()
    pull_system_image()

def pull_system_image():
    # pull system.img.gz
    print(timestamp() + ": Creating system.img.gz (this will take about 7 minutes) ...")

    if debug:
        p = subprocess.Popen(adb + "shell", stdin=subprocess.PIPE, shell=True)
    else:
        p = subprocess.Popen(adb + "shell", stdin=subprocess.PIPE, stdout=dev_null, shell=True)
    process_input(p,"/data/local/tmp/busybox telnet 127.0.0.1 1234")
    process_input(p,"dd if=/dev/block/mmcblk0 bs=4096 skip=" + dd_seek + " count=" + dd_count + " | gzip > " + system_image_target_dir + "/system.img.gz")
    p.stdin.flush()
    sleep(300)
    process_input(p,"exit")
    process_input(p,"exit")
    p.stdin.flush()

    # chmod system_image_target_dir
    if debug:
        p = subprocess.Popen(adb + "shell", stdin=subprocess.PIPE, shell=True)
    else:
        p = subprocess.Popen(adb + "shell", stdin=subprocess.PIPE, stdout=dev_null, shell=True)

    process_input(p,"/data/local/tmp/busybox telnet 127.0.0.1 1234")
    process_input(p,"chmod 777 " + system_image_target_dir)
    process_input(p,"chmod 777 " + system_image_target_dir + "/system.img.gz")
    p.stdin.flush()
    sleep(2)
    process_input(p,"exit")
    process_input(p,"exit")
    p.stdin.flush()
    sleep(0.5)

    if debug:
        out = subprocess.check_output(adb + "shell ls -l " + system_image_target_dir, shell=True)
    else:
        out = subprocess.check_output(adb + "shell ls " + system_image_target_dir, shell=True)
    if python3:
        out = out.decode("utf-8")
    print_debug(out)

    if "opendir failed, Permission denied" in out:
        print(timestamp() + ": fail")
        wait_for_enter_exit_error()
    if "system.img.gz" not in out:
        print(timestamp() + ": Failed to create a system.img.gz. Missing telnet connection could be the problem. Try again.")
        wait_for_enter_exit_error()

    print(timestamp() + ": Successfully created a system.img.gz under " + system_image_target_dir + ".")

    print(timestamp() + ": Pulling system.img.gz from " + device + " (This can take upto 15 minutes)...")
    subprocess_call(adb + "pull " + system_image_target_dir + "/system.img.gz")
    try:
        with open("system.img.gz"):
            print(timestamp() + ": Successfully pulled system image to: '" + os.path.abspath("system.img.gz") + "'.")
    except IOError:
        print(timestamp() + ": E: system.img.gz couldn't be pulled from tablet.")
        wait_for_enter_exit_error()

def unix_root_from_scratch():
    # Add-on for SuperSU Root
    print("")
    print("Do you want to use the originally included superuser or SuperSU-v2.40?")
    print("[1]superuser")
    print("[2]SuperSU")
    print("[Q]uit")
    
    selection = user_input("Enter a selection: ")
    if selection == "q" or selection == "Q":
        sys.exit(0)
    if selection == "1":
        SuperSU = False
    elif selection == "2":
        SuperSU = True
    else:
        print("E: Only '1', '2' or 'Q' are allowed!")
        main()
    # End of Add-on for SuperSU Root

    # Add-on for Xposed Framework
    if EnableXposed:
        print("")
        print("Do you want to use Xposed Framework (2.7 experimental1) -- DOES NOT WORK AT THE MOMENT?")
        print("[Y]es")
        print("[N]o")
        print("[Q]uit")
        selection = user_input("Enter a selection: ")
        if selection == "q" or selection == "Q":
            sys.exit(0)
        if selection == "y" or selection == "Y":
            Xposed = True
        elif selection == "n" or selection == "N":
            Xposed = False
        else:
            print("E: Only 'Y', 'N' or 'Q' are allowed!")
            main()
    # End of Add-on for Xposed Framework

    # Add-on for writeable external sdcard
    print("")
    print("Do you want to make your external SDCard writeable?")
    print("[Y]es")
    print("[N]o")
    print("[Q]uit")
    selection = user_input("Enter a selection: ")
    if selection == "q" or selection == "Q":
        sys.exit(0)
    if selection == "y" or selection == "Y":
        extsdwrite = True
    elif selection == "n" or selection == "N":
        extsdwrite = False
    else:
        print("E: Only 'Y', 'N' or 'Q' are allowed!")
        main()
    # End of Add-on for writeable external sdcard

    # Add-on for doing it all at once
    print("")
    print("Do you want to do everything all at once (= do not wait for input before restoring system.img?")
    print("")
    print("Make sure to:")
    print("1. Plugin both computer and device into power")
    print("2. Do not touch the device")
    print("3. Do not EVER disconnect the USB of the device")
    print("4. Make sure to wait till everything succeeds!")
    print("")
    print("Failure to do so may cause disconnect in the restore procedure which can brick the device!")
    print("")
    print("[Y]es")
    print("[N]o")
    print("[Q]uit")
    print("")
    selection = user_input("Enter a selection: ")
    if selection == "q" or selection == "Q":
        sys.exit(0)
    if selection == "y" or selection == "Y":
        allatonce = True
    elif selection == "n" or selection == "N":
        allatonce = False
    else:
        print("E: Only 'Y', 'N' or 'Q' are allowed!")
        main()
    # End of Add-on for doing it all at once

    print("")
    print("================== Root =================")
    start_info()
    print("The following procedures can take up to 30 minutes!")
    if allatonce:
		print("To finally play back the rooted system.img.gz a confirmation will be needed then.")
    else:
		print("To finally play back the rooted system.img.gz NO confirmation will be needed (all at once).")
    wait_for_enter_start()

    subprocess_call("sudo chmod +x " + bin_folder + "adb")

    check_adb()
    push_busybox()
    start_telnet_server()
    check_dumchar_info()
    pull_system_image()

    print(timestamp() + ": Adding stuff to system.img ...")
    print(timestamp() + ": Unzipping system.img ...")
    
    subprocess_call("sudo chmod 777 system.img.gz")
    subprocess_call("gunzip system.img.gz")
    
    try:
        with open("system.img"):
            print_debug(timestamp() + ": Successfully unzipped pulled system.img.gz")
    except IOError:
        print(timestamp() + ": E: Couldn't unzip system.img.")
        wait_for_enter_exit_error()

    # mount system.img.gz
    print(timestamp() + ": Mounting system.img ...")
    subprocess_call("sudo mkdir /media/iconia")
    if not os.path.exists("/media/iconia"):
        print(timestamp() + ": E: Couldn't create Directory '/media/iconia'")
        print(timestamp() + ": Cleaning up...")
        subprocess_call("rm system.img*")
        wait_for_enter_exit_error()

    subprocess_call("sudo mount -o loop system.img /media/iconia")
    if not os.path.exists("/media/iconia/bin"):
        print(timestamp() + ": E: Failed to mount system.img.")
        print(timestamp() + ": Cleaning up...")
        subprocess_call("sudo rm -rf /media/iconia")
        subprocess_call("rm system.img*")
        wait_for_enter_exit_error()

    # Add-on for SuperSU Root
    if SuperSU:
        print(timestamp() + ": Adding SuperSU...")
        add_SuperSU()
    else:
        print(timestamp() + ": Adding superuser...")
        add_superuser()
    # End of Add-on for SuperSU Root

    # Add-on for Xposed Framework
    if Xposed:
        print(timestamp() + ": Adding Xposed...")
        add_Xposed()
    # End of Add-on for Xposed Framework

    # Add-on for writeable external sdcard
    if extsdwrite:
        print(timestamp() + ": Adding new platform.xml for writeable external sdcard...")
        change_extsdwrite()
    # End of Add-on for writeable external sdcard

    # unmount system.img.gz
    print(timestamp() + ": Unmounting system.img...")
    subprocess_call("sudo umount /media/iconia")
    subprocess_call("sudo rm -rf /media/iconia")
    subprocess_call("gzip system.img")
    try:
        with open("system.img.gz"):
            print(timestamp() + ": Successfully gzipped system.img again.")
    except IOError:
        print(timestamp() + ": E: Couldn't gzip system.img containing the su binary.")
        subprocess_call("rm system.img*")
        wait_for_enter_exit_error()

    # remove old system.img.gz
    print(timestamp() + ": Removing old system.img.gz from your " + device + "...")
    if debug:
        p = subprocess.Popen(adb + "shell", stdin=subprocess.PIPE, shell=True)
    else:
        p = subprocess.Popen(adb + "shell", stdin=subprocess.PIPE, stdout=dev_null, shell=True)
    process_input(p,"rm " + system_image_target_dir + "/system.img.gz")
    process_input(p,"exit")
    p.stdin.flush()

    # push rooted system.img.gz
    print(timestamp() + ": Copying rooted system.img.gz to your " + device + " (This can take upto 15 minutes)...")
    subprocess_call(adb + "push system.img.gz " + system_image_target_dir)
    p = subprocess.Popen(adb + "shell ls " + system_image_target_dir, stdout=subprocess.PIPE, shell=True)
    p.wait()

    found = False
    out = p.stdout.readlines()
    for o in out:
        if python3:
            o = o.decode("utf-8")
        print_debug(o)
        if "system.img.gz" in o:
            found = True
            break
    if found:
        print(timestamp() + ": Successfully copied system.img.gz to " + system_image_target_dir)
    else:
        print(timestamp() + ": Failed to copy system.img.gz. Make sure the folder 'system_image' contains a system.img.gz suiting to your installed firmware.")
        subprocess_call("rm system.img*")
        wait_for_enter_exit_error()

    write_system_image()


def add_superuser():
    if a1 and not kitkat:
        subprocess_call("sudo tar -C /media/iconia -xzvf bin/a1/a1su.tgz")
    else:
        subprocess_call("sudo cp " + su + " /media/iconia/bin")
    
    subprocess_call("sudo chmod 06755 /media/iconia/bin/su")

    try:
        with open("/media/iconia/bin/su"):
            print(timestamp() + ": Successfully mounted pulled system image and added su.")
    except IOError:
        print(timestamp() + ": E: Couldn't add su to system.img.")
        print(timestamp() + ": Cleaning up...")
        subprocess_call("sudo umount /media/iconia")
        subprocess_call("sudo rm -rf /media/iconia")
        subprocess_call("rm system.img*")
        wait_for_enter_exit_error()


def add_SuperSU():
    subprocess_call("sudo rm /media/iconia/bin/su")
    subprocess_call("sudo mv /media/iconia/etc/install-recovery.sh /media/iconia/etc/install-recovery_original.sh")
    subprocess_call("sudo mkdir /media/iconia/bin/.ext")
    subprocess_call("sudo chmod 0777 /media/iconia/bin/.ext")
    subprocess_call("sudo cp bin/UPDATE-SuperSU-v2.40/common/Superuser.apk /media/iconia/app/Superuser.apk")
    subprocess_call("sudo cp bin/UPDATE-SuperSU-v2.40/common/install-recovery.sh /media/iconia/etc/install-recovery.sh")
    subprocess_call("sudo cp bin/UPDATE-SuperSU-v2.40/armv7/su /media/iconia/xbin/daemonsu")
    subprocess_call("sudo cp bin/UPDATE-SuperSU-v2.40/armv7/su /media/iconia/xbin/sugote")
    subprocess_call("sudo cp bin/UPDATE-SuperSU-v2.40/armv7/su /media/iconia/xbin/su")
    subprocess_call("sudo cp bin/UPDATE-SuperSU-v2.40/armv7/su /media/iconia/bin/.ext/.su")
    subprocess_call("sudo cp /media/iconia/bin/mksh /media/iconia/xbin/sugote-mksh")
    subprocess_call("sudo cp bin/UPDATE-SuperSU-v2.40/armv7/supolicy /media/iconia/xbin/supolicy")
    subprocess_call("sudo cp bin/UPDATE-SuperSU-v2.40/armv7/libsupol.so /media/iconia/lib/libsupol.so")
    subprocess_call("sudo chmod 0644 /media/iconia/app/Superuser.apk")
    subprocess_call("sudo chmod 0755 /media/iconia/etc/install-recovery.sh")
    subprocess_call("sudo chmod 0755 /media/iconia/xbin/daemonsu")
    subprocess_call("sudo chmod 0755 /media/iconia/xbin/su")
    subprocess_call("sudo chmod 0755 /media/iconia/bin/.ext/.su")
    subprocess_call("sudo chmod 0755 /media/iconia/xbin/sugote")
    subprocess_call("sudo chmod 0755 /media/iconia/xbin/sugote-mksh")
    subprocess_call("sudo chmod 0755 /media/iconia/xbin/supolicy")
    subprocess_call("sudo chmod 0644 /media/iconia/lib/libsupol.so")
    subprocess_call("sudo ln -s /media/iconia/etc/install-recovery.sh /media/iconia/bin/install-recovery.sh")

    try:
        with open("/media/iconia/xbin/su"):
            print(timestamp() + ": Successfully mounted pulled system image and added SuperSU.")
    except IOError:
        print(timestamp() + ": E: Couldn't add SuperSU to system.img.")
        print(timestamp() + ": Cleaning up...")
        subprocess_call("sudo umount /media/iconia")
        subprocess_call("sudo rm -rf /media/iconia")
        subprocess_call("rm system.img*")
        wait_for_enter_exit_error()


def add_Xposed():
#    subprocess_call("sudo rm /media/iconia/app/de.robv.android.xposed.installer_v33_36570c.apk")
#    subprocess_call("sudo rm /media/iconia/app/de.robv.android.xposed.installer_v32_de4f0d.apk")
    subprocess_call("sudo cp -a /media/iconia/bin/app_process /media/iconia/bin/app_process.orig")
    subprocess_call("sudo cp bin/de.robv.android.xposed.installer_v33_36570c/assets/arm/app_process_xposed_sdk16 /media/iconia/bin/app_process")
    subprocess_call("sudo chmod 0755 /media/iconia/bin/app_process")
    try:
        with open("/media/iconia/bin/app_process.orig"):
            print(timestamp() + ": Successfully mounted pulled system image and added Xposed.")
    except IOError:
        print(timestamp() + ": E: Couldn't add Xposed to system.img.")
        print(timestamp() + ": Cleaning up...")
        subprocess_call("sudo umount /media/iconia")
        subprocess_call("sudo rm -rf /media/iconia")
        subprocess_call("rm system.img*")
        wait_for_enter_exit_error()


def change_extsdwrite():
    subprocess_call("sudo cp -a /media/iconia/etc/permissions/platform.xml /media/iconia/etc/permissions/platform.xml.orig")
    subprocess_call("sudo cp bin/platform.xml /media/iconia/etc/permissions")
    subprocess_call("sudo chmod 0644 /media/iconia/etc/permissions/platform.xml")
    try:
        with open("/media/iconia/etc/permissions/platform.xml.orig"):
            print(timestamp() + ": Successfully mounted pulled system image and added platform.xml for writeable external sdcard.")
    except IOError:
        print(timestamp() + ": E: Couldn't add platform.xml for writeable external sdcard to system.img.")
        print(timestamp() + ": Cleaning up...")
        subprocess_call("sudo umount /media/iconia")
        subprocess_call("sudo rm -rf /media/iconia")
        subprocess_call("rm system.img*")
        wait_for_enter_exit_error()


def root():
    print("")
    print("================== Root =================")
    start_info()
    wait_for_enter_start()

    if not windows:
        subprocess_call("sudo chmod +x " + bin_folder + "adb")

    if a1 and kitkat:
        su = os.path.join("bin", "a1", "su")

    check_adb()
    push_busybox()
    start_telnet_server()
    check_dumchar_info()
    check_firmware_version()
    push_system_image()
    write_system_image()


def unroot():
    print("")
    print("================= Unroot ================")
    start_info()
    wait_for_enter_start()

    if not windows:
        subprocess_call("sudo chmod +x " + bin_folder + "adb")

    check_adb()
    remove_su_binary()


def write_system_image():
    print(timestamp() + ": Writing rooted system.img.gz. This is going to take 2 minutes.")
    print(timestamp() + ": IN -ANY- CASE, DON'T INTERRUPT THIS PROCESS, OR YOUR DEVICE COULD BE -BRICKED-")
    # Add-on for doing it all at once
    if allatonce:
        print(timestamp() + ": Doing it all at once...")
    else:
        wait_for_enter_start()
    # End of Add-on for doing it all at once

    if debug:
        p = subprocess.Popen(adb + "shell", stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    else:
        p = subprocess.Popen(adb + "shell", stdin=subprocess.PIPE, stdout=dev_null, shell=True)

    process_input(p,"/data/local/tmp/busybox telnet 127.0.0.1 1234")
    process_input(p,"/data/local/tmp/busybox zcat " + system_image_target_dir + "/system.img.gz | dd of=/dev/block/mmcblk0 bs=4096 seek=" + dd_seek + " count=" + dd_count)
    p.stdin.flush()
    progress_root()
    process_input(p,"exit")
    process_input(p,"exit")
    p.stdin.flush()
    if debug:
        p.stdout.flush()

#    print(timestamp() + ": Trying to reboot your device...")
#    subprocess_call(adb + "shell reboot")
    print("")
    print(timestamp() + ": SUCCESS!")
    print(timestamp() + ": Your " + device + " is now rooted. Unplug your tablet and reboot (if reboot was not successful. Install Superuser from the Google Play Store and have fun ;-)")
    print(timestamp() + ": If your tablet is turned off and doesn't turn on anymore, take a pin and press the reset button on the right side of the Iconia B1, above the power button.")
    print_thanks()
    wait_for_enter_exit_success()


def remove_su_binary():
    wait_for_enter_start()

    p = subprocess.Popen(adb + "shell", stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)

    process_input(p,"su")
    process_input(p,"mount -o rw,remount /system/")
    process_input(p,"rm /system/bin/su")
    process_input(p,"rm /system/xbin/su")
    process_input(p,"rm /system.bin/.ext/.su")
    process_input(p,"mount -o ro,remount /system/")
    process_input(p,"exit")
    process_input(p,"exit")
    p.stdin.flush()
    p.stdout.flush()

    for _ in range(7):
        p.stdout.readline()

    out = p.stdout.readline()
    if python3:
        out = out.decode("utf-8")

    print(out)
    if "not found" in out:
        print("")
        print(timestamp() + ": FAILED!")
        print(timestamp() + ": Your " + device + " is already unrooted.")
        wait_for_enter_exit_error()
    else:
#        print(timestamp() + ": Trying to reboot your device...")
#        subprocess_call(adb + "shell reboot")
        print("")
        print(timestamp() + ": SUCCESS!")
        print(timestamp() + ": Your " + device + " is now unrooted.")
        print(timestamp() + ": Unplug your tablet, do a reboot, install Root Checker on Google Play Store to verify.")
        print_thanks()
        wait_for_enter_exit_success()


def backup_ext_sd(config):
    print("")
    print(timestamp() + ": Backing up External SD...")
    print(timestamp() + ": Dependent of how much data you have stored, this can take pretty a while...")

    # remove old files in backup folder if existing
    backup_folder = os.path.join("external2internal", "external_backup")
    if windows:
        subprocess_call("del /Q " + backup_folder + "\\*")
    else:
        subprocess_call("sudo rm -rf " + backup_folder + "/*")

    # pull all files from external partition
    if config == "default":
        subprocess_call(adb + "pull /mnt/sdcard/ " + backup_folder)
    else:
        subprocess_call(adb + "pull /mnt/sdcard2/ " + backup_folder)


def swap_ext_to_int_sd(config):
    print("")
    if config == "default":
        print(timestamp() + ": Swap Internal SD -> External SD and External SD -> Internal SD...  ")
    else:
        print(timestamp() + ": Swap External SD -> Internal SD and Internal SD -> External SD...  ")
    print("")

    # swapping partitions
    wait_for_enter_start()
    print(timestamp() + ": Swapping Partitions...")

    subfolder = "b1"
    if a1:
        subfolder = "a1"
    elif b1_710:
        subfolder = "b1-710"

    if config == "default":
        subprocess_call(adb + "push " + os.path.join("external2internal", subfolder, "vold.fstab.swapped") + " /data/local/tmp/vold.fstab")
        if a1 or b1_710:
            subprocess_call(adb + "push " + os.path.join("external2internal", subfolder, "vold.fstab.nand.swapped") + " /data/local/tmp/vold.fstab.nand")
    else:
        subprocess_call(adb + "push " + os.path.join("external2internal", subfolder, "vold.fstab.default") + " /data/local/tmp/vold.fstab")
        if a1 or b1_710:
            subprocess_call(adb + "push " + os.path.join("external2internal", subfolder, "vold.fstab.nand.default") + " /data/local/tmp/vold.fstab.nand")

    p = subprocess.Popen(adb + "shell", stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)

    process_input(p,"su")
    process_input(p,"mount -o rw,remount /system/")
    process_input(p,"cat /data/local/tmp/vold.fstab > /etc/vold.fstab")
    if a1 or b1_710:
        process_input(p,"cat /data/local/tmp/vold.fstab.nand > /etc/vold.fstab.nand")
    process_input(p,"mount -o ro,remount /system/")
    process_input(p,"exit")
    process_input(p,"exit")
    p.stdin.flush()
    p.stdout.flush()

    for _ in range(7):
        if debug:
            out = p.stdout.readline()
            if python3:
                out = out.decode("utf-8")
            print(out)

    out = p.stdout.readline()
    if python3:
        out = out.decode("utf-8")
    print_debug(out)

    if "not found" in out:
        print(timestamp() + ": E: Failed to mount /system. Device not rooted!")
        print(timestamp() + ": SD Partitions couldn't be swapped.")
        wait_for_enter_exit_success()

    print(timestamp() + ": Successfully swapped SD Partitions.")


def restore_ext_sd(config):
    print("")
    print(timestamp() + ": Restoring External SD Data...")
    print(timestamp() + ": Dependent of how much data you have stored, this can take pretty a while...")
    wait_for_enter_start()

    dest = ""
    if config == "default":
        dest = " /mnt/sdcard/"
    else:
        dest = " /mnt/sdcard2/"

    # delete old files from destination first
    subprocess_call(adb + "shell rm -r" + dest + "*")
    subprocess_call(adb + "push " + os.path.join("external2internal", "external_backup") + dest)
    print(timestamp() + ": Successfully restored External data.")


def progress_root():
    for i in range(60):
        sleep(2)
        if i == 0:
            sys.stdout.write("R")
        elif i == 20:
            sys.stdout.write("O")
        elif i == 40:
            sys.stdout.write("O")
        elif i == 59:
            sys.stdout.write("T")
        else:
            sys.stdout.write(".")
        sys.stdout.flush()
    print("")


def push_busybox():
    print(timestamp() + ": Copying Busybox to your " + device + ".")
    subprocess_call(adb + "push " + busybox + " /data/local/tmp")
    subprocess_call(adb + "shell chmod 755 /data/local/tmp/busybox")
    print(timestamp() + ": Successfully copied Busybox to your " + device + ".")


def start_telnet_server():
    print(timestamp() + ": Starting Telnet server on your " + device + ".")

    out = subprocess.check_output(adb + "shell dumpsys power", shell=True)
    if python3:
        out = out.decode("utf-8")
    print_debug(out)

    check_device_powered(out)
    print(timestamp() + ": Turn on your " + device + " now and unlock the screen.")
    if kitkat:
        print(timestamp() + ": Make sure your " + device + " is and stays(!) in PORTRAIT mode!")
    print(timestamp() + ": Hit ENTER when you are done.")
    wait_for_enter_start()
    print("")
    print(timestamp() + ": Don't touch the screen! I'm taking it over now ;-)")

    subprocess_call(adb +       'shell input keyevent KEYCODE_HOME')
    sleep(1.5)
    if not kitkat:
        subprocess_call(adb +       'shell am start -n com.mediatek.engineermode/.EngineerMode com.mediatek.connectivity/.CdsInfoActivity\n')
    if kitkat:
        subprocess_call(adb +       'shell am start -n com.mediatek.engineermode/.EngineerMode\n')
    sleep(0.5)
    if not kitkat:
        for _ in range(4):
            subprocess_call(adb +   'shell input keyevent KEYCODE_DPAD_DOWN')
            sleep(0.1)
        subprocess_call(adb +       'shell input keyevent KEYCODE_ENTER')
        sleep(0.1)
        subprocess_call(adb +       'shell input text "/data/local/tmp/busybox"')
        sleep(0.1)
        subprocess_call(adb +       'shell input keyevent KEYCODE_SPACE')
        sleep(0.1)
        subprocess_call(adb +       'shell input text "telnetd"')
        sleep(0.1)
        subprocess_call(adb +       'shell input keyevent KEYCODE_SPACE')
        sleep(0.1)
        subprocess_call(adb +       'shell input text "-l"')
        sleep(0.1)
        subprocess_call(adb +       'shell input keyevent KEYCODE_SPACE')
        sleep(0.1)
        subprocess_call(adb +       'shell input text "/system/bin/sh"')
        sleep(0.1)
        subprocess_call(adb +       'shell input keyevent KEYCODE_SPACE')
        sleep(0.1)
        subprocess_call(adb +       'shell input text "-p"')
        sleep(0.1)
        subprocess_call(adb +       'shell input keyevent KEYCODE_SPACE')
        sleep(0.1)
        subprocess_call(adb +       'shell input text "1234"')
        sleep(0.1)
        subprocess_call(adb +       'shell input tap 50 200')
    else:
        for _ in range(4):
            subprocess_call(adb +   'shell input tap 730 95')
            sleep(0.1)
        if a1_811:
            subprocess_call(adb +       'shell input tap 400 320')
        else:
            subprocess_call(adb +       'shell input tap 400 275')
        sleep(0.1)
        subprocess_call(adb +       'shell input tap 745 55')
        sleep(0.1)
        subprocess_call(adb +       'shell input tap 365 530')
        sleep(0.1)
        print(timestamp() + ": Removing old characters. This may take a minute or two!")
        for _ in range(80):
            subprocess_call(adb +   'shell input keyevent KEYCODE_FORWARD_DEL')
            subprocess_call(adb +   'shell input keyevent KEYCODE_DEL')
        sleep(0.1)
        subprocess_call(adb +       'shell input text "/data/local/tmp/busybox"')
        sleep(0.1)
        subprocess_call(adb +       'shell input keyevent KEYCODE_SPACE')
        sleep(0.1)
        subprocess_call(adb +       'shell input text "telnetd"')
        sleep(0.1)
        subprocess_call(adb +       'shell input keyevent KEYCODE_SPACE')
        sleep(0.1)
        subprocess_call(adb +       'shell input text "-l"')
        sleep(0.1)
        subprocess_call(adb +       'shell input keyevent KEYCODE_SPACE')
        sleep(0.1)
        subprocess_call(adb +       'shell input text "/system/bin/sh"')
        sleep(0.1)
        subprocess_call(adb +       'shell input keyevent KEYCODE_SPACE')
        sleep(0.1)
        subprocess_call(adb +       'shell input text "-p"')
        sleep(0.1)
        subprocess_call(adb +       'shell input keyevent KEYCODE_SPACE')
        sleep(0.1)
        subprocess_call(adb +       'shell input text "1234"')
        sleep(0.1)
        subprocess_call(adb +       'shell input tap 515 390')
    sleep(0.1)

    print(timestamp() + ": Checking, if telnet server is started. If the tool crashes now, try to start telnet server manually by clicking on 'Run'.")
    if windows:
        out = subprocess.check_output(adb + 'shell ps | findstr "\/data/local/tmp/busybox"', shell=True)
    else:
        out = subprocess.check_output(adb + 'shell ps | grep "/data/local/tmp/busybox"', shell=True)
    if python3:
        out = out.decode("utf-8")
    print_debug(out)
    if "/data/local/tmp/busybox" not in out:
        print(timestamp() + ": E: Telnet server was NOT started on the tablet. If you keep on getting this error, busybox was not pushed onto tablet.")
        print(timestamp() + ": Retrying now.")
        start_telnet_server()

    print(timestamp() + ": Successfully started Telnet server on your " + device + ".")


def check_dumchar_info():
    p = subprocess.Popen(adb + "shell", stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    process_input(p,"/data/local/tmp/busybox telnet 127.0.0.1 1234 | cat /proc/dumchar_info")
    process_input(p,"exit")
    process_input(p,"exit")
    p.stdin.flush()

    string_found = False
    for _ in range(25):
        out = p.stdout.readline()
        if python3:
            out = out.decode("utf-8")
        print_debug(out)
        if a1:
            if "android" in out and \
               "0x0000000040000000" in out and \
               "0x0000000004500000" in out and \
               " 2 " in out and \
               "/dev/block/mmcblk0p5" in out:
                string_found = True
                break
        elif b1_710:
            if "android" in out and \
               "0x0000000040000000" in out and \
               "0x00000000024e8000" in out and \
               " 2 " in out and \
               "/dev/block/mmcblk0p3" in out:
                string_found = True
                break
        else:
            if "android" in out and \
               "0x00000000020e8000" in out and \
               " 2 " in out and \
               "/dev/block/mmcblk0p3" in out:
                if "0x0000000015e00000" in out:
                    print(timestamp() + ": !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print(timestamp() + ": Your device has 'android 0x0000000015e00000 0x00000000020e8000 2 /dev/block/mmcblk0p3' in dumchar_info. Continuing could brick your device!")
                    print(timestamp() + ": !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    wait_for_enter_start()
                elif not "0x0000000026500000" in out:
                   continue
                string_found = True
                break

    if not string_found:
        if a1:
            print(timestamp() + ": E: The line 'android 0x0000000004500000 0x0000000040000000 2 /dev/block/mmcblk0p5' wasn't found in /proc/dumchar_info.")
        if b1_710:
            print(timestamp() + ": E: The line 'android 0x0000000040000000 0x00000000024e8000 2 /dev/block/mmcblk0p3' wasn't found in /proc/dumchar_info.")
        else:
            print(timestamp() + ": E: The line 'android 0x0000000026500000 0x00000000020e8000 2 /dev/block/mmcblk0p3' wasn't found in /proc/dumchar_info.")
            print(timestamp() + ": E: The line 'android 0x0000000015e00000 0x00000000020e8000 2 /dev/block/mmcblk0p3' wasn't found in /proc/dumchar_info.")
        print(timestamp() + ": YOUR PARTITION SETTING IS NOT SUPPORTED, YET!")
        wait_for_enter_exit_error()


def check_firmware_version():
    print("")
    print(timestamp() + ": Checking firmware version.")
    build_prop = "build.prop"

    subprocess_call(adb + "pull /system/build.prop")

    try:
        with open("build.prop"):
            print_debug(timestamp() + ": Successfully pulled build.prop.")
    except IOError:
        print(timestamp() + ": E: Failed to check firmware version: 'adb pull /system/build.prop' failed.")
        wait_for_enter_exit_error()

    f = open(build_prop, "r")
    lines = f.readlines()
    for l in lines:
        if l.startswith("ro.build.pandora.id="):
            if a1:
                if "Acer_AV052_A1-810_" in l:
                    fw_version = l.split("Acer_AV052_A1-810_")[1].split("_WW_GEN1")[0]
                elif "Acer_AV052_B1-711_" in l:
                    fw_version = l.split("Acer_AV052_B1-711_")[1].split("_WW_GEN1")[0]
                elif "Acer_AV052_A3-A10_" in l:
                    fw_version = l.split("Acer_AV052_A3-A10_")[1].split("_WW_GEN1")[0]
                elif "Acer_AV052_B1-720_" in l:
                    fw_version = l.split("Acer_AV052_B1-720_")[1].split("_WW_GEN1")[0]
                else:
                    fw_version = l.split("Acer_AV052_A1-811_")[1].split("_TWN_GEN1")[0]
            elif b1_710:
                if "Acer_AV051_B1-710_" in l:
                    fw_version = l.split("Acer_AV051_B1-710_")[1].split("_WW_GEN1")[0]
                else:
                    fw_version = l.split("Acer_AV051_B1-A710_")[1].split("_WW_GEN1")[0]
            else:
                fw_version = l.split("Acer_AV051_B1-A71_")[1].split("_WW_GEN1")[0]
            print(timestamp() + ": Firmware version '" + fw_version + "' installed. MAKE SURE YOUR system.img.gz IN system_image FOLDER IS OF THE SAME VERSION, OTHERWISE YOU GET A BOOTLOOP!")
            break
    f.close()
    os.remove(build_prop)

def check_adb():
    global a1

    p = subprocess.Popen(adb + "devices", stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    print("")
    print(timestamp() + ": Trying to establish ADB Connection...")
    p.wait()

    found = False
    for _ in range(4):
        out = p.stdout.readline()
        if python3:
            out = out.decode("utf-8")
        print_debug(out)
        if "0123456789ABCDEF" in out:
            found = True
            break
        elif a1:
            regexp = re.compile(r'[a-zA-Z0-9]{11,16}\s+device')
            if regexp.search(out) is not None:
                found = True
                print_debug(timestamp() + ": Device ID is: " + out[:16])
                break

    if found:
        print(timestamp() + ": ADB Connection to your " + device + " successful.")
    else:
        print(timestamp() + ": E: Couldn't connect to your " + device + " over adb. Plug-In the device with USB-Debugging Mode turned on.")
        if windows:
            print(timestamp() + ": Check if drivers are properly installed.")
        wait_for_enter_exit_error()

def push_system_image():
    print(timestamp() + ": Copying rooted system.img.gz to your " + device + " (This can take upto 15 minutes)...")
    wait_for_enter_start()

    try:
        with open(os.path.join("system_image", "system.img.gz")):
            print_debug(timestamp() + ": system.img.gz found in folder 'system_image'.")
    except IOError:
        print(timestamp() + ": E: No system.img.gz found in folder 'system_image' in toolkit directory.")
        wait_for_enter_exit_error()

    if debug:
        p = subprocess.Popen(adb + "shell", stdin=subprocess.PIPE, shell=True)
    else:
        p = subprocess.Popen(adb + "shell", stdin=subprocess.PIPE, stdout=dev_null, shell=True)
    process_input(p,"/data/local/tmp/busybox telnet 127.0.0.1 1234")
    process_input(p,"chmod 777 " + system_image_target_dir)
    process_input(p,"chmod 777 " + system_image_target_dir + "/system.img.gz") # in case system.img.gz already exists
    p.stdin.flush()
    sleep(3)
    process_input(p,"exit")
    process_input(p,"exit")
    p.stdin.flush()

    subprocess_call(adb + "push " + system_image + " " + system_image_target_dir)
    p = subprocess.Popen(adb + "shell ls " + system_image_target_dir, stdout=subprocess.PIPE, shell=True)
    p.wait()
    found = False
    out = p.stdout.readlines()
    for o in out:
        if python3:
            o = o.decode("utf-8")
        print_debug(o)
        if "system.img.gz" in o:
            found = True
            if not debug:
                break

    if found:
        print(timestamp() + ": Successfully copied system.img.gz to " + system_image_target_dir)
    else:
        print(timestamp() + ": Failed to copy system.img.gz. Make sure the folder 'system_image' of this toolkit contains a system.img.gz suiting to your installed firmware.")
        wait_for_enter_exit_error()

def start_info():
    if windows:
        print("Before we can start, please do following:")
        print("1. Make sure drivers for your " + device + " are installed, you can find them here: " + driver_url)
        print("2. Plug-In your " + device + " into this PC.")
        print("3. Enable USB Debugging Mode by going into Settings -> Developer Tools.")
        print("4. Put prerooted system.img.gz into folder: system_image of this toolkit.")
        print("5. Keep your device plugged in until it's finally rooted, or this procedure is aborted!")
        if a1:
            print("6. !!! UNPLUG ALL OTHER DEVICES!!!")
        print("")
        print("If you sucessfully applied the steps above, we can now start.")
        print("You can always abort by pressing Ctrl+C")
        print("")
    else:
        print("Before we can start, please do following:")
        print("1. Plug-In your " + device + " into this PC.")
        print("2. Enable USB Debugging Mode by going into Settings -> Developer Tools.")
        print("3. Keep your device plugged in until it's finally unrooted, or this procedure is aborted!")
        if a1:
            print("4. !!! UNPLUG ALL OTHER DEVICES!!!")
        print("")
        print("If you sucessfully applied the steps above, we can now start.")
        print("You can always abort by pressing Ctrl+C.")
        print("")

def wait_for_enter_start():
    print("")
    print("[ENTER] Continue")
    print("[Q]     Quit")
    print("")

    if python3:
        selection = input("Enter a selection: ")
    else:
        selection = raw_input("Enter a selection: ")

    if selection.lower() == "q":
        sys.exit(0)

def wait_for_enter_exit_success():
    print("")
    if python3:
        input("Press Enter to leave Application...")
    else:
        raw_input("Press Enter to leave Application...")
    sys.exit(0)

def wait_for_enter_exit_error():
    if not debug:
        print("")
        print("If you keep getting this error, try to run toolkit with -d or --debug parameter")
    if python3:
        input("Press Enter to leave Application...")
    else:
        raw_input("Press Enter to leave Application...")
    sys.exit(1)

def print_thanks():
    print(timestamp() + ": Thanks to XDA: pawitp, alba81, FireDiamond, Optimissimus99, bullbrand, sodaFR, MatrixDJ96, ak6, min-dfreak, agentdeep, nick_1964, sampod and you ;-)")

def print_debug(string):
    if debug:
        print(string)

def check_device_powered(out):
    if a1:
        return

    # device in standby? -> Wake up
    sleeping = True
    while sleeping:
        # device turned off
        if "mPowerState=0" in out:
            subprocess_call(adb + "shell input keyevent KEYCODE_POWER", True)
        sleep(1)
        # device in lockscreen? -> Request Unlock
        if "mPowerState=3" not in out:
            print(timestamp() + ": PLEASE UNLOCK THE SCREEN OF YOUR TABLET!")
            wait_for_enter_start()
            sleep(0.5)

            out = subprocess.check_output(adb + "shell dumpsys power", shell=True)
            if python3:
                out = out.decode("utf-8")
            print_debug(out)
        else:
            sleeping = False


def timestamp():
	return time.strftime('%Y/%m/%d %H:%M:%S')
    
def user_input(msg):
    if python3:
        return input(msg)
    else:
        return raw_input(msg)
    
def process_input(p,cmd):
    cmd += "\n"
    if python3:
        p.stdin.write(bytes(cmd, "utf-8"))
    else:
        p.stdin.write(cmd)
        
def subprocess_call(cmd,mute_stderr=False):
    if debug:
        subprocess.call(cmd, shell=True)
    else:
        if mute_stderr:
            subprocess.call(cmd, stderr=dev_null, stdout=dev_null, shell=True)
        else:
            subprocess.call(cmd, stdout=dev_null, shell=True)
        


if __name__ == "__main__":
    main()
