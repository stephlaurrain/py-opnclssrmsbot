import os
import sys
import gc
from opnclssrm import Bot
from datetime import datetime


class Menuitem:
    def __init__(self, command, label, nbparams, jsonfile, ret):
        self.command = command
        self.label = label
        self.nbparams = nbparams
        self.jsonfile = jsonfile
        self.ret = ret

rootApp = os.getcwd()


def dotail(profil):

    logFilename = "{0}{1}log{1}{3}{2}.log".format(rootApp, os.path.sep, profil, dnow)
    os.system("tail -f {0}".format(logFilename))



hardgreen = "\033[32m\033[1m"
normalgreen = "\033[32m\033[2m"
normalcolor = "\033[0m"


def mencol(nb, fonc, comment):
    return "{0}{3} - {4} {1} - {5}{2}".format(hardgreen, normalgreen, normalcolor, nb, fonc, comment)


def drkcol(str):
    return "{0}{2}{1}".format(hardgreen, normalcolor, str)


def clear():
    return os.system('clear')
# \033[40m

# os.system('setterm -background black -foreground green')

nbargs = len(sys.argv)

jsonfilefromarg = "default" if (nbargs == 1) else sys.argv[1]
#modemenu = "default" if (nbargs < 3) else sys.argv[2]

clear()


while True:
    print(drkcol("\nHi Neo, I'm the OpenClassrooms bot"))
    print(drkcol("Your wish is my order\n"))
    print(drkcol("What I can do for you :\n"))

    menulist = []
    menulist.append(Menuitem("simplyconnect", "simply connect", 0, jsonfilefromarg, False))
    menulist.append(Menuitem("getsessions", "get sessions elements", 0, jsonfilefromarg, False))
    menulist.append(Menuitem("login", "login to OpnClssrms", 0, jsonfilefromarg, False))
    menulist.append(Menuitem("dash", "dashboard", 0, jsonfilefromarg, False))
    menulist.append(Menuitem("booked", "planifiees", 0, jsonfilefromarg, False))


    menulist.append(Menuitem("test", "test", 0, jsonfilefromarg, False))

    for idx, menuitem in enumerate(menulist):
        print (mencol(idx, menuitem.command, menuitem.label))
        if menuitem.ret:
            print(drkcol("#####"))

    print(drkcol("#####"))
    print(mencol("55", "tail", "actual default log"))

    print(drkcol("#####"))
    print(mencol("66", "advanced", "advanced menu"))
    print(mencol("77", "desktop", "desktop menu"))
    print(mencol("88", "default", "default menu"))
    print(drkcol("#####"))
    print(mencol("93", "editparams", "edit default.json"))
    # print (mencol("94","editparams","edit checkvisited.json"))    
    print(mencol("98", "stop", "stop current process"))
    print(mencol("99", "exit", "exit this menu"))
    dothat = input(drkcol("\n\nReady to rock : "))

    today = datetime.now()
    dnow = today.strftime(r"%y%m%d")

    if dothat == "55":
        print(drkcol("\ntail -f default\n"))
        dotail("default")
    if dothat == "93":
        print(drkcol("\edit params -r\n"))
        os.system("nano data/default.json")    
    if dothat == "99":
        print(drkcol("\nsee you soon, Neo\n"))
        # del bot
        gc.collect
        quit()
    try:
        if int(dothat) < 50:
            cmdstr = "nop"

            item = menulist[int(dothat)]
            cmd = item.command
            print (cmd)
            prms = int(item.nbparams)
            prmcmdlist = []
            for i in range(prms):
                prmcmdlist.append(input(drkcol(f"enter param {i} :")))
            prm2 = "" if (len(prmcmdlist) < 1) else prmcmdlist[0]
            prm3 = "" if (len(prmcmdlist) < 2) else prmcmdlist[1]
            bot = Bot()
            bot.main(cmd, item.jsonfile, prm2, prm3)
            del bot
    except Exception as e:
        print (e)
        print(f"\n{hardgreen}bad command (something went wrong){normalcolor}\n")
