import os
import glob
import subprocess
import datetime
import platform


webgrabplus_runner = ''
webgrabplus_dir = ''
xmltv_files_dir = ''
runner_dir = ''
os_ = platform.system()
print 'Os: "' + os_ + '"'


# -- CONFIGURATION ---------------------------------------------------------------------------------------------------------------------
# uncomment or copy this bloc and edit it (only lines with *) according to your configuration, you can fill in the confs of both systems 
# (windows/linux) if you want your script to be runnable in both without making any changes each time
# -- -----------------------------------------------------------------------------------------------------------------------------------
#if os_ == 'Windows':
#*	webgrabplus_runner = r'c:/path/to/your/wgPlus/install/directory'
#*	webgrabplus_dir = r'c:/path/to/your/wgPlus/working/directory'

#*	xmltv_files_dir = r'c:/path/to/your/xmltv_files/destination'
#*	runner_dir = r'c:/path/to/this/grab-runner/script'

#elif os_ == 'Linux':
#*	webgrabplus_runner = r'/path/to/your/wgPlus/install/directory'
#*	webgrabplus_dir = r'/path/to/your/wgPlus/working/directory'

#*	xmltv_files_dir = r'/path/to/your/xmltv_files/destination'
#*	runner_dir = r'/path/to/this/grab-runner/script'

#else:
#	print 'unknown Os. "' + os_ + '", program is stopped'
#	exit()

# --------------------------------------------------------------------------------------------------------------------------------------

if os_ == 'Windows':
	webgrabplus_runner = r'C:/Program Files (x86)/WebGrab+Plus/bin/WebGrab+Plus.exe'
	webgrabplus_dir = r'C:/Users/Mbarki/AppData/Local/WebGrab+Plus'

	xmltv_files_dir = r'F:/Developpement/SOURCES/xmltv/xmltv_files'
	runner_dir = r'F:/Developpement/SOURCES/xmltv/grab-runners'

elif os_ == 'Linux':
	webgrabplus_runner = r'/run.net.sh'
	webgrabplus_dir = r'/home/mohammed/dev/epg/grabbers/wgPlus/.wg++'

	xmltv_files_dir = r'/home/mohammed/dev/epg/xmltv_files'
	runner_dir = r'/home/mohammed/dev/epg/grab-runners'
else:
	print 'unknown Os. "' + os_ + '", program is stopped'
	exit()

print(".............................................................................. step 0: checking ...")

if webgrabplus_runner == '' or webgrabplus_dir == '' or xmltv_files_dir == '' or runner_dir == '':
	print 'config not found, please edit this script and update the config block, the program is stopped'
	exit()

out_dir = webgrabplus_dir + r'/out'
archives_dir = out_dir + r'/archives'

print('webgrabplus_runner : ' + webgrabplus_runner)
print('webgrabplus_dir    : ' + webgrabplus_dir)
print('xmltv_files_dir    : ' + xmltv_files_dir)
print('runner_dir         : ' + runner_dir)
print('out_dir            : ' + out_dir)
print('archives_dir       : ' + archives_dir)

#exit()

print("XMLTV   ....................................................................................... Begin")

print(".......................................................................... step 1: Resync with github")

os.chdir(xmltv_files_dir)

os.system('git fetch origin')
os.system('git checkout master')
os.system('git reset --hard origin/master')

print('resync with Git repository done')

print(".........................................................................................step 2: init")

print(r'saving "WebGrab++.config.xml" as "WebGrab++_old.config.xml" on WebGrab++ directory ...')
os.chdir(webgrabplus_dir)
os.system('mv WebGrab++.config.xml WebGrab++.config_old.xml')
print('done.')
print('')

os.chdir(runner_dir)

print(r'(force) update runners and configs from Git repository ...')
os.system('git checkout master')
os.system('git fetch')
os.system('git reset --hard origin/master')
print('done.')
print('')

print(r'copying "WebGrab++.config.xml" file to WebGrab++ directory ...')
os.system(r'cp config_wgPlus_files/WebGrab++.config.xml ' + webgrabplus_dir)
print('done.')
print('')

print(r'copying sites.ini files to WebGrab++ directory ...')
os.system(r'cp config_wgPlus_files/*.ini ' + webgrabplus_dir)
print('done.')
print('')

exist = glob.glob(out_dir + r'/guide*.xmltv')
if exist:
    print(r'moving last ".xmltv" file to "out/archives" (except guide.xmltv) on WebGrab++ directory ...')
    exist = glob.glob(archives_dir)
    if not exist:
        os.system('mkdir ' + archives_dir)

    os.chdir(out_dir)
    os.system('mv guide_*.xmltv ' + archives_dir)
    print('done.')
    print('')
else:
    print('everything is alright, nothing to do')
    print('')

#exit()

# call webgrab++:
print("........................................................................................ step 3: Grabbing")

os.chdir(webgrabplus_dir)

if os_ == 'Windows':
	sortie = subprocess.call(webgrabplus_runner + ' "' + webgrabplus_dir + '"')
if os_ == 'Linux':
	sortie = subprocess.call(['.' + webgrabplus_runner, webgrabplus_dir])


exist = glob.glob(out_dir + r'/guide.xmltv')

#exit()

# test grabbing result:
if sortie == 0 and exist:
    print("Grabbing done ................................................................................... [OK]")
    print('')

    # copy guide.xmltv file:
    now = datetime.datetime.now()
    now_str = now.strftime("%d%m%Y_%H_%M")
    file_name = 'guide_' + now_str + '.xmltv'

    os.chdir(out_dir)
    os.system('cp guide.xmltv ' + file_name)

    print('guide.xmltv copied to "' + file_name)
    print('')

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
    print('')

else:
    print("Grabbing error ....................................... [KO]")
    # exit()

#  end
print("XMLTV   ....................................................................................... end")
