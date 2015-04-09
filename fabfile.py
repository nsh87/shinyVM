from fabric.api import run, sudo, env, require, settings, local
from fabric.contrib.files import exists
import subprocess

### VARIABLES ###

# Origin of our repository, and the repository
GIT_ORIGIN = 'git@github.com'
GIT_REPO = 'nsh87/shiny'

# Packages to install in Vagrant
INSTALL_PACKAGES = ['r-base',
                    'gdebi-core',
                    'haskell-platform']

### ENVIRONMENTS ###

def vagrant():
    """Defines the Vagrant virtual machine's environment variables.
    Local development and server will us this environment."""

    # Configure SSH things
    raw_ssh_config = subprocess.Popen(['vagrant', 'ssh-config'],
                                      stdout=subprocess.PIPE).communicate()[0]
    ssh_config = dict([l.strip().split() for l in raw_ssh_config.split("\n")
                       if l])
    env.hosts = ['127.0.0.1:%s' % (ssh_config['Port'])]
    env.user = ssh_config['User']
    env.key_filename = ssh_config['IdentityFile']

    # Development will happen on the master branch
    env.repo = ('origin', 'master')

### ROUTINES ###

def setup_vagrant():
    """Sets up the Vagrant environment"""
    require('hosts', provided_by=[vagrant])  # Sets the environment for Fabric
    sub_add_repos()
    sub_install_packages()
    sub_install_shiny()

def reload():
    require('hosts', provided_by=[vagrant])
    sudo('restart shiny-server')

### SUB-ROUTINES ###

def sub_add_repos():
    """Adds any repositories needed to install packages"""
    if not exists('/etc/apt/sources.list.d/cran.list', use_sudo=True):
        # Add the repository for R
        sudo('sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 '
             '--recv-keys E084DAB9')
        run('sudo sh -c "echo \'deb http://cran.rstudio.com/bin/linux/ubuntu '
            'trusty/\' >> /etc/apt/sources.list.d/cran.list"')

def sub_install_packages():
    """Installs the necessary packages to get Shiny running"""
    sudo('apt-get update')
    sudo('apt-get -y upgrade')
    package_str = ' '.join(INSTALL_PACKAGES)
    sudo('apt-get -y install ' + package_str)

def sub_install_shiny():
    """Installs Shiny package and Shiny Server"""
    # Install Shiny package for R
    sudo('R -e "install.packages(\'shiny\', '
         'repos=\'http://cran.rstudio.com/\')"')

    # Install Shiny Server using gdebi. According to documentation, will be
    # installed into /opt/shiny-server/ with main executable in
    # /opt/shiny-server/bin/shiny-server. Also new user 'shiny' will be
    # created.
    sudo('mkdir -p /usr/src/shiny')
    sudo('''cd /usr/src/shiny; if [ ! -e shiny-server-1.3.0.403-amd64.deb ];
    then a='http://download3.rstudio.org/ubuntu-12.04/x86_64/shiny-server-' ; \
    b='1.3.0.403-amd64.deb' ; \
    wget $a$b ; \
    echo y | gdebi shiny-server-1.3.0.403-amd64.deb ; \
    fi''')

    # Move server directory at /srv/shiny-server to shared Vagrant folder if
    # the shared folder is empty. This will copy sample Shiny app in the
    # process.
    sudo('''if [ 'find /www-shiny -maxdepth 0 -empty | read v' ]; then \
    cp -LR /srv/shiny-server/* /www-shiny/ ; \
    rm -rf /srv/shiny-server ; \
    ln -s /www-shiny/ /srv/shiny-server;
    fi''')

    sub_install_rmarkdown()
    sub_make_writeable_project()

    # Restart VM
    local('vagrant reload')
    run('status shiny-server')

def sub_make_writeable_project():
    """Creates a symlink from Shiny's web server folder to a shiny:shiny
    writeable folder for app development.
    
    Shiny server runs in /www-shiny (/project on the host machine), whose
    owner is vagrant:vagrant. Shiny server runs as user shiny:shiny; so if
    you have an app that needs to write anything, you can't do it in
    /www-shiny. You have to do it in another owned by shiny:shiny.
    """
    sudo('''cd /www-shiny; if [ ! -L proj ]; then \
    ln -s /www-shiny-writeable/ proj ;
    fi''')
    

def sub_install_rmarkdown():
    """Installs the packages required for Shiny to serve markdown documents.
    Haskell is a prerequisite that should have been installed earlier. Pandoc is
    also required."""
    run('cabal update')
    run('cabal install pandoc')
    sudo('R -e "install.packages(\'rmarkdown\', '
         'repos=\'http://cran.rstudio.com/\')"')
