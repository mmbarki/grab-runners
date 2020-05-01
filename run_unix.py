import os
import glob
import subprocess
import datetime



# ---------------------------------------------------------------------------------------------------------------------------------------
#os.chdir('/home/jeedom/webGrab/.wg++')

#subprocess.call(['./run.sh'])

#exit()

os.chdir('/home/jeedom/webGrab/.wg++')

exist = glob.glob('guide.xmltv')

print 'file guide.xmltv exist ? : ', exist

exit()
# --------------------------------------------------------------------------------------------------------------------------------------


# Windows ------------------------------------------------------------------
#webgrabplus_exe = r'C:\Program Files (x86)\WebGrab+Plus\bin\WebGrab+Plus.exe'
#webgrabplus_dir = r'C:\Users\Mbarki\AppData\Local\WebGrab+Plus'
#xmltv_files_dir = r'F:\Developpement\SOURCES\xmltv\xmltv_files'
#---------------------------------------------------------------------------

# Unix ------------------------------------------------------------------
unix = True
webgrabplus_sh = r'/run.sh'
webgrabplus_dir = r'/home/jeedom/webGrab/.wg++'
xmltv_files_dir = r'/home/jeedom/webGrab/xmltv_files'
#---------------------------------------------------------------------------

out_dir = webgrabplus_dir + r'/out'
archives_dir = out_dir + r'/archives'

print('webgrabplus_sh : ' + webgrabplus_sh)
print('webgrabplus_dir : ' + webgrabplus_dir)
print('xmltv_files_dir : ' + xmltv_files_dir)
print('out_dir : ' + out_dir)
print('archives_dir : ' + archives_dir)

#exit()

print("XMLTV   ....................................................................................... Begin")

print(".........................................................................................step 1: init")

exist = glob.glob(out_dir + r'/guide*.xmltv')
if exist:
    print(r'moving last ".xmltv" file  to "out/archives"')
    exist = glob.glob(archives_dir)
    if not exist:
        os.system('mkdir ' + archives_dir)

    os.chdir(out_dir)
    os.system('mv guide*.xmltv ' + archives_dir)
else:
    print('everything is alright, nothing to do')


# call webgrab++:
print("........................................................................................ step 2: Grabing")

os.chdir(webgrabplus_dir)


#os.chdir('/home/jeedom/webGrab/.wg++')
#subprocess.call(['./run.sh'])


if unix == True:
	sortie = subprocess.call(['.' + webgrabplus_sh])
else:
	sortie = subprocess.call(webgrabplus_exe + ' "' + webgrabplus_dir + '"')

exist = glob.glob('guide.xmltv')

print 'sortie: ', sortie
print 'file guide.xmltv exist ? : ', exist

exit()
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
    os.system('cp ' + file_name + ' ' + xmltv_files_dir + '/files')
    os.system('cp ' + file_name + ' ' + xmltv_files_dir + '/guide.xmltv')

    exit()
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
