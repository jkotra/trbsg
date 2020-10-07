import argparse
import zipfile
import os
import time
import datetime
import shutil

parser = argparse.ArgumentParser()

parser.add_argument('-r',action='store_true',dest="r", default=False)
parser.add_argument('-c',action='store_true',dest="c", default=False)
parser.add_argument('-i',action='store', type=int, dest="i", default=None)
parser.add_argument('--path',action='store',dest="path", default= "C:\\Users\\{user}\\Documents\\My Games\\They Are Billions\\".format(user=os.getlogin()))

args = parser.parse_args()


def getTime():
    return "{}".format(datetime.datetime.fromtimestamp(time.time()))

def restoreSave(file, path):
    print(file)
    zf = zipfile.ZipFile(file, 'r')
    zf.extractall(path)
    zf.close()
    print("backup [{}] restored to [{rp}]".format(file, rp=path))

def showMenu():
    for file in os.listdir("saves"):
        print("Backup", file, "at", datetime.datetime.fromtimestamp(os.path.getmtime("saves\\"+file)))
    
    backup_restore = input("Backup to restore > ")
    restoreSave(os.path.join("saves", backup_restore) , args.path)

def zipSave(path):
    zipfname = "saves\\{n}".format(n=len(os.listdir("saves"))+1)
    shutil.make_archive(zipfname, 'zip', path)
    print("Backup completed ", zipfname)


def watch(path):
    print("Watching: ", path)

    modified_times = []
    for root, _, files in os.walk(path):
        for file in files:
            if ".zx" in file:
                modified_times.append(os.path.getmtime(os.path.join(root, file)))


    
    while True:
        current_modified_times = []

        for root, _, files in os.walk(path):
            for file in files:
                if ".zx" in file:
                    try:
                        current_modified_times.append(os.path.getmtime(os.path.join(root, file)))
                    except FileNotFoundError:
                        continue    
  

        if current_modified_times != modified_times:
            print(modified_times, current_modified_times)
            modified_times = current_modified_times

            zipSave(path)
        else:
            if args.i is not None:
                time.sleep(args.i)
            continue


def main():
    if args.r:
        showMenu()
    elif args.c:
        shutil.rmtree("saves")
    else:
        if not os.path.exists("saves"):
            os.mkdir("saves")
        watch(args.path)     

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Bye!")    