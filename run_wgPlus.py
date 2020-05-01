import os
import glob
import subprocess
import datetime
import platform



# ---------------------------------------------------------------------------------------------------------------------------------------
#os.chdir('/home/jeedom/webGrab/.wg++')

#subprocess.call(['./run.sh'])

#exit()

# os.chdir('/home/jeedom/webGrab/.wg++')

# exist = glob.glob('/home/jeedom/webGrab/.wg++/guide.xmltv')

# print 'file guide.xmltv exist ? : ', exist
#os.uname()
#print platform.system()
#platform.uname()
#print sys.platform

#exit()
# --------------------------------------------------------------------------------------------------------------------------------------


os_ = platform.system()

print 'Os: "' + os_ + '"'


if os_ == 'Windows':
	webgrabplus_runner = r'C:/Program Files (x86)/WebGrab+Plus/bin/WebGrab+Plus.exe'
	webgrabplus_dir = r'C:/Users/Mbarki/AppData/Local/WebGrab+Plus'

	xmltv_files_dir = r'F:/Developpement/SOURCES/xmltv/xmltv_files'
	python_runner_dir = r'F:/Developpement/SOURCES/xmltv/xmltv_python'

elif os_ == 'Linux':
	webgrabplus_runner = r'/run.sh'
	webgrabplus_dir = r'/develops/grabbers/wgPlus/.wg++'

	xmltv_files_dir = r'/develops/grabbers/xmltv_files'
	python_runner_dir = r'/develops/grabbers/xmltv_python'

else:
	print 'unknown Os. "' + os_ + '", program is stopped'
	exit()


out_dir = webgrabplus_dir + r'/out'
archives_dir = out_dir + r'/archives'

print('webgrabplus_runner : ' + webgrabplus_runner)
print('webgrabplus_dir : ' + webgrabplus_dir)
print('xmltv_files_dir : ' + xmltv_files_dir)
print('python_runner_dir : ' + python_runner_dir)
print('out_dir : ' + out_dir)
print('archives_dir : ' + archives_dir)

#exit()

print("XMLTV   ....................................................................................... Begin")

print(".......................................................................... step 1: Resync with github")

os.chdir(xmltv_files_dir)

# if credentials management is not already done, enable this line for 1st run only:
#os.system('git config credential.helper store')

os.system('git fetch origin')
os.system('git checkout master')
os.system('git reset --hard origin/master')

print('resync with Git repository done')

print(".........................................................................................step 2: init")

print(r'saving "WebGrab++.config.xml" as "WebGrab++_old.config.xml" on WebGrab++ directory ...')
os.chdir(webgrabplus_dir)
os.system('mv WebGrab++.config.xml WebGrab++.config_old.xml')
print('done.')

os.chdir(python_runner_dir)

print(r'copying "WebGrab++.config.xml" file to WebGrab++ directory ...')
os.system(r'cp config_wgPlus_files/WebGrab++.config.xml ' + webgrabplus_dir)
print('done.')

print(r'copying sites.ini files to WebGrab++ directory ...')
os.system(r'cp config_wgPlus_files/*.ini ' + webgrabplus_dir)
print('done.')

exist = glob.glob(out_dir + r'/guide*.xmltv')
if exist:
    print(r'moving last ".xmltv" file to "out/archives" (except guide.xmltv) on WebGrab++ directory ...')
    exist = glob.glob(archives_dir)
    if not exist:
        os.system('mkdir ' + archives_dir)

    os.chdir(out_dir)
    os.system('mv guide_*.xmltv ' + archives_dir)
    print('done.')
else:
    print('everything is alright, nothing to do')

#exit()

# call webgrab++:
print("........................................................................................ step 3: Grabing")

os.chdir(webgrabplus_dir)

if os_ == 'Windows':
	sortie = subprocess.call(webgrabplus_runner + ' "' + webgrabplus_dir + '"')
if os_ == 'Linux':
	sortie = subprocess.call(['.' + webgrabplus_runner, webgrabplus_dir])


exist = glob.glob(out_dir + r'/guide.xmltv')

#exit()

# test grabing result:
if sortie == 0 and exist:
    print(
        "Grabing done ................................................................................... [OK]")

    # copy guide.xmltv file:
    now = datetime.datetime.now()
    now_str = now.strftime("%d%m%Y_%H_%M")
    file_name = 'guide_' + now_str + '.xmltv'

    os.chdir(out_dir)
    os.system('cp guide.xmltv ' + file_name)

    print('guide.xmltv copied to "' + file_name)

    # copy file to xmltv_files
    os.system('cp ' + file_name + ' ' + xmltv_files_dir + '/files')
    os.system('cp ' + file_name + ' ' + xmltv_files_dir + '/guide_AR.xmltv')

    #exit()

    # commit file to git
    print("................................................................................. step 4: Push to github")

    os.chdir(xmltv_files_dir)

    os.system('git add .')
    os.system('git commit -m "build file: ' + file_name + '"')
    #os.system('git fetch origin')
    #os.system('git rebase origin/master')
    os.system('git push origin master')

    print('file "' + file_name + '" pushed to Git repository')

else:
    print("Grabing error ....................................... [KO]")
    # exit()

#  end
print("XMLTV   ....................................................................................... end")
