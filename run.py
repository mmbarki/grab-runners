import os
import glob
import subprocess
import datetime

# now = datetime.datetime.now()
# now_str = now.strftime("%d%m%Y_%H:%M")
# print(now)
# print(now_str)

webgrabplus_exe = r'C:\Program Files (x86)\WebGrab+Plus\bin\WebGrab+Plus.exe'
webgrabplus_dir = r'C:\Users\Mbarki\AppData\Local\WebGrab+Plus'
out_dir = webgrabplus_dir + r'\out'
archives_dir = out_dir + r'\archives'
xmltv_files_dir = r'F:\Developpement\SOURCES\xmltv\xmltv_files'

print("XMLTV   ....................................................................................... Begin")

print(".........................................................................................step 1: init")

exist = glob.glob(out_dir + r'\guide*.xmltv')
if exist:
    print(r'moving last ".xmltv" file  to "out\archives"')
    exist = glob.glob(archives_dir)
    if not exist:
        os.system('mkdir ' + archives_dir)

    os.chdir(out_dir)
    os.system('mv guide*.xmltv ' + archives_dir)
else:
    print('everything is alright, nothing to do')


# call webgrab++:
print("........................................................................................ step 2: Grabing")
sortie = subprocess.call(webgrabplus_exe + ' "' + webgrabplus_dir + '"')
exist = glob.glob(out_dir + r'\guide*.xmltv')

#exit()
# test grabing result:
if sortie == 0 and exist:
    print(
        "Grabing done ................................................................................... [OK]")

    # rename file:
    now = datetime.datetime.now()
    now_str = now.strftime("%d%m%Y_%H_%M")
    file_name = 'guide_' + now_str + '.xmltv'

    os.chdir(out_dir)
    os.system('mv  guide.xmltv ' + file_name)

    print('guide.xmltv renamed to "' + file_name)

    # copy file to xmltv_files
    os.system('cp ' + file_name + ' ' + xmltv_files_dir + '\\files')
    os.system('cp ' + file_name + ' ' + xmltv_files_dir + '\\guide.xmltv')

    #exit()
    # commit file to git
    print("................................................................................. step 3: Push to github")
    os.chdir(xmltv_files_dir)
    os.system('git add .')
    os.system('git commit -m "build file: ' + file_name + '"')
    os.system('git push origin master')

    print('file "' + file_name + '" pushed to Git repository')

else:
    print("Grabing error ....................................... [KO]")
    # exit()

#  end
print("XMLTV   ....................................................................................... end")
