from os import listdir, system
from os.path import isfile, join
import time

######################
# RASPBERRY PI
######################
rpi_ssh = "pi@192.168.1.3"
rpi_dir = "/home/pi/photobooth/export"

######################
# PATHS
######################
root_path = "./"

jpg_dir = root_path + "img/rpi"
jpg_path = jpg_dir + "/"
gif_dir = root_path + "img/photobooth"
gif_path =  gif_dir + "/"

jpg_archive_path = root_path + "img/archive"

data_file_path = root_path + "data.js"

######################
# CONFIG
######################
fetch_interval = 5
gif_delay = 50

######################
# FUNCTIONS
######################
def fetch_jpg_from_rpi():
    system("scp %s:%s/* %s" % (rpi_ssh, rpi_dir, jpg_dir))

def remove_jpg_from_rpi(keys):
    for key in keys:
        system("ssh %s 'rm %s/%s*'" % (rpi_ssh, rpi_dir, key))

def create_gifs():

    gifs = dict()

    for f in listdir(jpg_dir):
        if(f[-3:] == "jpg"):
            key = f[:-7]
            if(not gifs.has_key(key)):
                gifs[key] = []

            gifs[key].append(f)

    keys = []
    for key in gifs:
        print "Creating gif: " + gif_path + key + ".gif"
        graphicsmagick = "gm convert -delay " + str(gif_delay) + " " + jpg_path + key + "*.jpg " + gif_path + key + ".gif"
        system(graphicsmagick) #make the .gif
        keys.append(key)

    return keys

def archive_jpgs():
    system("mv " + jpg_path + "* " + jpg_archive_path)


def update_slideshow_data_file():

    gifs = list()
    for g in listdir(gif_dir):
        if(g[-3:] == "gif"):
            gifs.append(g)

    # Print the latest one first
    gifs.reverse()

    # JSON data with all files
    js = "data = [\"" + "\", \"".join(gifs) + "\"];"

    # Write to file
    f = open(data_file_path, 'w')
    f.write(js)
    f.close()

######################
# MAIN PROGRAM
######################

while(True):
    print "Fetch jpgs from rpi.."
    fetch_jpg_from_rpi()
    print "Create gifs from fetched jpgs.."
    keys = create_gifs()
    print "Remove jpgs from rpi..."
    remove_jpg_from_rpi(keys)
    print "Move already processed jpgs to archive.."
    archive_jpgs()
    print "Update data.js.."
    update_slideshow_data_file()
    print "Done!"
    time.sleep(fetch_interval)
