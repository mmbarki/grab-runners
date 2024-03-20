import os
import glob
import subprocess
import datetime
import platform
import ConfigParser  # Utilise ConfigParser au lieu de configparser dans Python 3

# directories
wg_dir          = ''
wg_run_file     = ''
xmltv_files_dir = ''
runner_dir      = ''
out_dir         = ''
archives_dir    = ''

# credentials
wg_username     = ''
wg_email        = ''
wg_password     = ''
grab_result     = 0

print(".............................................................................. step 1: 'config.ini'")

os_ = platform.system().lower()
print 'Os: "' + os_ + '"'

config_dir = 'config_wgPlus_files'
config_file = '{}/config.conf'.format(config_dir)

# check if 'config.ini' exists
if not os.path.isfile(config_file):
    print("Erreur : configuration file  '{}' not found.".format(config_file))
    exit()

# open 'config.ini' file
config = ConfigParser.ConfigParser()
config.read(config_file)

# check if all sections exist
if not config.has_section("credentials") or not config.has_section(os_) :
    print("error: file '{}' content is not valid, some sections are empty.".format(config_file))
    exit()

# read credentials
wg_username = config.get("credentials", "wg_username")
wg_email = config.get("credentials", "wg_email")
wg_password = config.get("credentials", "wg_password")

# check credentials
if wg_username == '' or wg_email == '' or wg_password == '':
    print('error: some config elements are empty')
    exit()

# read os directories config
wg_dir = config.get(os_, "wg_dir")
wg_run_file = config.get(os_, "wg_run_file")
xmltv_files_dir = config.get(os_, "xmltv_files_dir")
runner_dir = config.get(os_, "runner_dir")

# check os directories config
if wg_dir == '' or wg_run_file == '' or xmltv_files_dir == '' or runner_dir == '':
    print('error: some config({}) elements are empty'.format(os_))
    exit()

out_dir = '{}/out'.format(wg_dir)
archives_dir = '{}/archives'.format(out_dir)

print('Os                  : {}'.format(os_))
print('wg_run_file         : {}'.format(wg_run_file))
print('wg_dir              : {}'.format(wg_dir))
print('xmltv_files_dir     : {}'.format(xmltv_files_dir))
print('runner_dir          : {}'.format(runner_dir))
print('out_dir             : {}'.format(out_dir))
print('archives_dir        : {}'.format(archives_dir))

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
os.chdir(wg_dir)
os.system('mv WebGrab++.config.xml WebGrab++.config_old.xml')
print('done.')
print('')

os.chdir(runner_dir)

if 1!=1:
    print(r'(force) update runners and configs from Git repository ...')
    os.system('git fetch')
    os.system('git checkout master')
    os.system('git reset --hard origin/master')
    print('done.')
    print('')

print(r'copying "WebGrab++.config.xml" file to WebGrab++ directory ...')
os.system(r'cp config_wgPlus_files/WebGrab++.config.xml ' + wg_dir)
print('done.')
print('')

print(r'copying sites.ini files to WebGrab++ directory ...')
os.system(r'cp config_wgPlus_files/*.ini ' + wg_dir)
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

os.chdir(wg_dir)

sortie = -1
if os_ == 'windows':
    sortie = subprocess.call(wg_run_file + ' "' + wg_dir + '"')
elif os_ == 'linux':
    # sortie = subprocess.call(['.' + wg_run_file, wg_dir])
    # sortie = subprocess.call(['. run.net.sh'])
      sortie = subprocess.call(['./run.net.sh'])
else:
    print("Unknown os '{}'".format(os_))
    sortie = -1

#exit()

# test grabbing result:
if sortie == 0 and os.path.isfile(out_dir + r'/guide.xmltv'):
    print('')
    print('')
    print("Grabbing  ..................................................................................... [OK]")
    print('')

   # copy guide.xmltv file:
    now_str = datetime.datetime.now().strftime("%d%m%Y_%H_%M")
    file_name = 'guide_AR_' + now_str + '.xmltv'

    # copy 'guide.xmltv' into files directory:
    os.chdir(out_dir)
    os.system('cp guide.xmltv {}/files/{}'.format(xmltv_files_dir, file_name))
    os.system('cp guide.xmltv {}/guide_AR.xmltv'.format(xmltv_files_dir))
    print('guide.xmltv copied to files directory')
    print('')

    print('')
    print('step 4: done.')
    print('')

    #exit()

    # commit file to git
    print("................................................................................. step 4: Push to github")

    os.chdir(xmltv_files_dir)

    os.system('git add .')
    os.system('git commit -m "build file: {}"'.format(file_name))
    #os.system('git fetch origin')
    #os.system('git rebase origin/master')
    os.system('git push origin master')

    print('file "{}" pushed to Git repository'.format(file_name))
    print('')

else:
    print("Grabbing error ............................................................................... [KO]")
    # exit()

#  end
print("XMLTV   ....................................................................................... end")
