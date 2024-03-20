import os
import glob
import subprocess
import datetime
import platform

# from os.path import expanduser home = expanduser("~")


# ---------------------------------------------------------------------------------------------------------------------------------------
# os.chdir('/home/jeedom/webGrab/.wg++')

# subprocess.call(['./run.sh'])
# subprocess.call('php /develops/grabbers/racacax/XML-TV-Fr/script_all.php', shell=True)

# subprocess.call('ls -l', shell=True)
# exit()

# os.chdir('/home/jeedom/webGrab/.wg++')

# exist = glob.glob('/home/jeedom/webGrab/.wg++/guide.xmltv')

# print 'file guide.xmltv exist ? : ', exist
# os.uname()
# print platform.system()
# platform.uname()
# print sys.platform

# exit()
# --------------------------------------------------------------------------------------------------------------------------------------


os_ = platform.system()
git_racacax_revision = 'v3.2.1'

print(r'Os: "' + os_ + '"')
print(r'git_racacax_revision: "' + git_racacax_revision + '"')

# ~/dev/epg/grab-runners
if os_ == 'Windows':
    grabber_dir = r'F:/Developpement/SOURCES/racacax_fork/XML-TV-Fr'
    grabber_run_cmd = r'php ' + grabber_dir + r'/manager.php export'

    xmltv_files_dir = r'F:/Developpement/SOURCES/xmltv/xmltv_files'
    runner_dir = r'F:/Developpement/SOURCES/xmltv/grab-runners'

elif os_ == 'Linux':
    home = os.getenv("HOME")
    grabber_dir = home + r'/dev/epg/grabbers/XML-TV-Fr'
    grabber_conf_dir = grabber_dir + r'/config'
    grabber_run_cmd = r'php ' + grabber_dir + r'/manager.php export'

    xmltv_files_dir = home + r'/dev/epg/xmltv_files'
    runner_dir = home + r'/dev/epg/grab-runners'

else:
    print('unknown Os. "' + os_ + '", program is stopped')
    exit()

out_dir = grabber_dir + r'/var/export'
archives_dir = out_dir + r'/archives'
xmltv_files_logs_dir = xmltv_files_dir + r'/logs'

print('git_branch : ' + git_racacax_revision)
print('grabber_dir : ' + grabber_dir)
print('grabber_run_cmd : ' + grabber_run_cmd)
print('xmltv_files_dir : ' + xmltv_files_dir)
print('runner_dir : ' + runner_dir)
print('out_dir : ' + out_dir)
print('archives_dir : ' + archives_dir)

# exit()

print("XMLTV  (Racacax) .............................................................................. Begin")

print('')
print('')
print(".......................................................................... step 1: Resync with github")

os.chdir(xmltv_files_dir)

# if credentials management is not already done, enable this line for 1st run only:
# os.system('git config credential.helper store')

print(r'Xmltv files: (force) update from Git repository ...')
os.system('git fetch')
os.system('git checkout master')
os.system('git reset --hard origin/master')
print('done.')
print('')

print('')
print(".........................................................................................step 2: init")

print(r'saving "channels.json" as "channels.old.json" on Grabber config directory ...')
os.chdir(grabber_conf_dir)
os.system('mv channels.json channels.old.json')
print('done.')
print('')

os.chdir(runner_dir)

print(r'Runners: (force) update scripts and configs from Git repository ...')
os.system('git fetch')
os.system('git checkout master')
os.system('git reset --hard origin/master')
print('done.')
print('')

print(r'copying "channels.json" file to Grabber config directory ...')
os.system(r'cp config_racacax_files/channels.json ' + grabber_conf_dir)
print('done.')
print('')

print(r'copying "config.json" file to Grabber config directory ...')
os.system(r'cp config_racacax_files/config.json ' + grabber_conf_dir)
print('done.')
print('')

exist = glob.glob(out_dir + r'/guide*.xmltv')
if exist:
    print(r'moving last ".xmltv" file to "out/archives" (except guide.xmltv) on Grabber directory ...')
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

# exit()

# call Grabber:
print('')
print("........................................................................................ step 3: Grabing")

os.chdir(grabber_dir)

print(r'Grabbers: update grabber from racacax Git repository ...')

if git_racacax_revision != '':
    print('resync with Git repository done, revision : ' + git_racacax_revision)
    os.system(r'git checkout origin/' + git_racacax_revision)
else:
    print('resync with Git repository done, branch : master')
    os.system('git checkout master')
    os.system('git reset --hard origin/master')

print('')
print('done.')

if os_ == 'Windows':
    sortie = subprocess.call(grabber_run_cmd)
if os_ == 'Linux':
    # sortie = subprocess.call(['.' + webgrabplus_runner, webgrabplus_dir])
    sortie = subprocess.call(grabber_run_cmd, shell=True)

exist = glob.glob(out_dir + r'/xmltv.xml')

# exit()

# test grabing result:
if sortie == 0 and exist:
    print('')
    print("Grabing done ................................................................................... [OK]")

    # copy xmltv.xml file:
    now = datetime.datetime.now()
    now_str = now.strftime("%d%m%Y_%H_%M")
    file_name = 'guide_FR_' + now_str + '.xmltv'

    os.chdir(out_dir)
    os.system('cp xmltv.xml ' + file_name)

    print('xmltv.xml copied to "' + file_name)
    print('')

    # copy file to xmltv_files
    os.system('cp ' + file_name + ' ' + xmltv_files_dir + '/files')
    os.system('cp ' + file_name + ' ' + xmltv_files_dir + '/guide_FR.xmltv')

    os.system('cp ' + runner_dir + r'/cron_racacax.log ' + xmltv_files_logs_dir)
    print('copying log files done.')
    print('')

    # exit()

    # commit file to git
    print('')
    print("................................................................................. step 4: Push to github")

    os.chdir(xmltv_files_dir)

    os.system('git add .')
    os.system('git commit -m "build file: ' + file_name + '"')
    # os.system('git fetch origin')
    # os.system('git rebase origin/master')
    os.system('git push origin master')

    print('file "' + file_name + '" pushed to Git repository')
    print('')

else:
    print("Grabing error ....................................... [KO]")
    print('')
    # exit()

#  end
print('')
print('')
print("XMLTV   ....................................................................................... end")
