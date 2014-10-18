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
*localhost:7070*. This should greatly simplify the process of creating a 
Shiny Server.
Requirements
------------
If you are using Windows the requirements and process should be similar, 
if not exactly the same. The installation of Python/Fabric is likely the 
only challenge, but both work on Windows if installed correctly.

System Requirements: 2GB RAM Min. and 3GB Free HD Space

For ease, use Mac OSX or Linux and install the following:

+ **VirtualBox:** https://www.virtualbox.org/wiki/Downloads
+ **Vagrant:** https://www.vagrantup.com/downloads
+ **Fabric:** http://www.fabfile.org/installing.html

It is likely that you already have Python, which Fabric requires. If you are 
unsure, open Terminal and execute `python`. The requirements above occupy 
~200 megabytes of space (largely from VirtualBox and Vagrant). They can be 
removed once you are done with Shiny Server, but it is suggested that you do 
not uninstall them since they are common development tools that you might use
in the future.

Installation
------------
Clone or download this repository onto your computer. Then open your Terminal
and `cd` into the repository on your computer. Run `vagrant up` to create 
the virtual machine. Finally, run `fab vagrant setup_vagrant` to install and
set up the Shiny Server and its dependencies. That's it! The last line in 
your terminal should give you the status of your Shiny Server. Open your browser
and visit *localhost:7070* to view the sample app.

To shutdown the server execute `vagrant halt`. This will stop the VM. To boot 
the server again execute `vagrant up`. You do not need to execute `fab 
vagrant setup_vagrant` if the process completed successfully earlier.
Creating Apps
-------------
During the setup process, the Shiny Server on your VM was directed to look in a 
new shared folder called **project** that was created in your repository. When 
you view the sample Shiny app in your browser, the Shiny Server reads the 
files in this folder. Any modifications to files in this folder will be 
visible to the VM, so you can simply delete the sample app and develop your app
in **project/** on your host machine.
Uninstallation
--------------
Since everything is installed into a VM, you can easily remove the VM to 
uninstall the server and reclaim disk space. In your **shiny** folder, 
execute `vagrant destroy` and then `vagrant box remove 'ubuntu/trusty64'`.
