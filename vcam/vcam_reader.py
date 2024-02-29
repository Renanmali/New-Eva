import os
import subprocess
from time import sleep
import SharedArray as sa

LOCK_FOLDER = ".lock"

ctrl = dict()

def init(parent_module):

    create = not os.path.isdir(LOCK_FOLDER)

    ctrl["create"] = create

    if create:
        print("Attempting to create virtual camera...")
        dir_path = os.path.dirname(os.path.realpath(__file__))
        vcam_process = subprocess.Popen(["python3", dir_path+"/vcam.py"], stdout=subprocess.PIPE)
        ctrl["vcam_pid"] = vcam_process.pid
        # print(vcam_process, vcam_process.pid, vcam_pid)
        # print("-------------")

    while not os.path.isdir(LOCK_FOLDER):
        sleep(0.3)

    if create:
        print("Created virtual camera (feeding shm://vcam)")

    if os.path.exists(LOCK_FOLDER+"/"+parent_module):
        print(f"ERROR: Reader name '{parent_module}' is not available.")
        exit(1)

    with open(LOCK_FOLDER+"/"+parent_module, "x") as _:
        pass

    ctrl["parent_module"] = parent_module
    
    shm = sa.attach("shm://vcam")
    print("Connected to virtual camera")

    return shm


def close():

    os.remove(LOCK_FOLDER+"/"+ctrl["parent_module"])
    if ctrl["create"]:
        lockfiles = os.listdir(LOCK_FOLDER)
        if lockfiles: # check if is not an empty list
            print("\nWARNING: virtual camera is still feeding other instances.\nIf you want to close the virtual camera, please close the following instances first:")
            for filename in os.listdir(LOCK_FOLDER):
                print(filename)
            print()
        while len(os.listdir(LOCK_FOLDER)) > 0:
            # print("-> Attempeted closing. Waiting for another 0.5s")
            sleep(0.5)
        os.rmdir(LOCK_FOLDER)
        from signal import SIGTERM
        os.kill(ctrl["vcam_pid"], SIGTERM)

        sa.delete("shm://vcam")
        print("Deleted virtual camera (at shm://vcam)")
    else:
        print("Disconnected from virtual camera")

    return True