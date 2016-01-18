Shiny
=====

Description
-----------

This will create and run a local Shiny Server for R to enable viewing of the 
sample Shiny application and the creation your own Shiny app. This is 
suitable for both local development and future deployment of a Shiny Server 
with your app.

Creating the server requires very few commands since the process is 
almost entirely automated by Fabric. The commands described below will create
a virtual machine (VM) running Ubuntu Server 14.04 and install the necessary 
R and Shiny packages onto the VM, with R Markdown enabled (allowing the 
server to serve Markdown docs). Shiny app files will be editable using your 
host machine. The Shiny server will be accessed in your browser at 
[localhost:7070](http://localhost:7070). This should greatly simplify the
process of creating a Shiny Server.

Requirements
------------

If you are using Windows the requirements and process should be similar, 
if not exactly the same. The installation of Python/Fabric is likely the 
only challenge, but both work on Windows if installed correctly. For ease, 
use Mac OS X or Linux.

System Requirements: 2GB RAM Min. and 3GB Free HD Space

Install the following:

+ **VirtualBox:** https://www.virtualbox.org/wiki/Downloads
+ **Vagrant:** https://www.vagrantup.com/downloads
+ **Fabric:** http://www.fabfile.org/installing.html

It is likely that you already have Python, which Fabric requires. If you are 
unsure, open Terminal and execute `python`.

The requirements above occupy ~200 megabytes of space (largely from 
VirtualBox and Vagrant). They can be removed once you are done with Shiny 
Server, but it is suggested that you do not uninstall them since they are 
common development tools that you might use in the future.

You also need to have an SSH key, since it will be used when setting up your 
VM with Vagrant. See the GitHub instructions for [checking for and creating 
an SSH key][1]. You do not need to go through Step 3 and 4 in their 
instructions, and if you find a key named `id_rsa` in Step 1 then you can 
also skip Step 2.

Installation
------------

Clone or download this repository onto your computer. Then open your Terminal
and `cd` into the repository on your computer. Run `vagrant up` to create 
the virtual machine. Finally, run `fab vagrant setup_vagrant` to install and
set up the Shiny Server and its dependencies. That's it! The last line in 
your terminal should give you the status of your Shiny Server. Open your 
web browser and using the address bar visit
[localhost:7070](http://localhost:7070) to view the sample app.

To shutdown the server execute `vagrant halt`. This will stop the VM. To boot 
the server again execute `vagrant up`. You do not need to execute `fab 
vagrant setup_vagrant` if the process completed successfully earlier.

If things do not run as expected see the Troubleshooting section below. 

Creating Apps
-------------

During the setup process, the Shiny Server on your VM was directed to look in a 
new shared folder called **project** that was created in your repository. When 
you view the sample Shiny app in your browser, the Shiny Server reads the 
files in this folder. Any modifications to files in this folder will be 
visible to the VM, so you can simply delete the sample app and develop your app
in **shiny/project/** on your host machine. (See the bottom of this Readme for
a visual of the directory structure).

The setup sequence also created a folder called **writeable-project** in the 
same location as **project**. In order to support certain apps' underlying R 
functions, Shiny server sometimes requires write access to an app folder. Such 
apps should be placed into (and developed in) **shiny/writeable-project**. In
**project** you will find a symlink named *proj* that points to the
app-writeable folder in order to give the Shiny server and your browser access
to apps in there. Try copying the **sample-apps** folder in **project** to the 
**writeable-project** folder, then use your browser to visit
*localhost:7070/proj/sample-apps*. Notice that the name of the symlink is used
in the URL for apps in the **writeable-project** folder. You can rename the
symlink to adjust that portion of the URL. If you are developing an app in
**project** and you see `ERROR: Cannot open the connection` in your 
browser when trying to access the app, it probably needs write access.

If your app requires any additional R packages, SSH into the VM with `vagrant
ssh` (make sure you are in the **shiny** folder first) and install them. For 
example, you can install the deSolve package with `vagrant ssh` and then 
`sudo R -e "install.packages('deSolve', repos='http://cran.rstudio.com/')"`.
Note that some packages might have dependencies outside of R. For example, in
order to install the R package RCurl, you will first have to install
libcurl4-gnutls-dev on Ubuntu via `sudo apt-get install libcurl4-gnutls-dev`.
Alternatively, if you're looking for something reproducible and you're familiar
with Python, you can add the installation of an R package to the `fab vagrant
setup_vagrant` sequence; check out the function
`sub_install_additional_packages()` in **fabfile.py** for instructions.

Uninstallation
--------------

Since everything is installed into a VM, you can easily remove the VM to 
uninstall the server and reclaim disk space. In your **shiny** folder, 
execute `vagrant destroy` and then `vagrant box remove 'ubuntu/trusty64'`.

Troubleshooting
---------------

For starters, know that you can destroy and reinitiate your VM and run 
`fab vagrant setup_vagrant` as many times as you want. This is especially 
useful if the setup process is interrupted. Some more specific problems and 
solutions are below.

+ If you see multiple `Connection timeout: Retrying....` warnings after running 
`vagrant up` and the process seems frozen, it is likely that you do not have an 
SSH key. See the link in the Requirements section for instructions on how to
create one.
+ If you had to install any of the requirements (VirtualBox, Vagrant, 
Fabric), try restarting your computer and beginning again. Make sure to 
destroy your VM before starting over.
+ If you see an error regarding an installation of Paramiko when executing 
`fab vagrant setup_vagrant`, remove Fabric and reinstall Paramiko: open 
Terminal and execute `sudo pip uninstall fabric`, then `sudo pip install 
paramiko==1.10`, then `sudo pip install fabric`.
+ If you do not see the **project** folder in your **shiny** folder (or 
**shiny-master** if you downloaded a .zip of the repo) after you run `vagrant
up`, then Vagrant might be facing permissions issues when trying to 
create the folder. Delete your VM, create a blank folder called **project** 
in your repo, and start over. See below for the expected folder structure.
+ If you see `ERROR: Cannot open the connection` in your browser when trying 
to access an app you are developing, the app probably needs write access. Try
moving the app into the **writeable-project** folder.
+ If you are running out of memory while trying to install a package you 
can increase the amount of RAM available to the VM. Open up *Vagrantfile*, 
which controls the settings for the VM, and edit the line that looks similar 
to `["modifyvm", :id, "--memory", "1792"]`. Change `1792` MB (1.8GB), save 
the file, then execute `vagrant reload` to restart the VM with the new
settings.

### Directory Structure

After `vagrant up` completes, your directory structure should look like this:  
*/shiny/*  
|-- fabfile.py  
|-- .gitignore  
|-- *project/*  
|-- README.md  
|-- Vagrantfile  
|-- *writeable-project/*

When `fab vagrant setup_vagrant` is done, you should have this:  
*/shiny/*  
|-- fabfile.py  
|-- .gitignore  
|-- *project/*  
|&nbsp;&nbsp;&nbsp; |-- index.html  
|&nbsp;&nbsp;&nbsp; |-- proj  
|&nbsp;&nbsp;&nbsp; |-- *sample-apps/*  
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |-- *hello/*  
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;
&nbsp; |-- server.R  
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;
&nbsp; |-- ui.R  
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |-- *rmd/*  
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp; |-- index.Rmd  
|-- README.md  
|-- Vagrantfile  
|-- *writeable-project/*

Any discrepancies in the above should give you some indication of where 
things went wrong.

[1]: https://help.github.com/articles/generating-ssh-keys/

TODO
----

1. Grab the current stable version of Shiny from the site for always up-to-date
   installation
2. Add a .Rproj so people can checkout from the repo directly in RStudio
3. Add Fabric function to push to a production server on AWS
