Shiny
=====
Description
-----------
This will get up and running a local Shiny Server to enable viewing of 
the sample Shiny application and the creation your own Shiny app. This is 
suitable for both local development and for future deployment of a Shiny 
Server with your app.

The files and commands described below will create a virtual machine (VM) 
running Ubuntu Server 14.04 and install all the necessary R and Shiny 
packages into the VM. Shiny app files will be editable using your host 
machine. The Shiny server will be accessed in your browser at *localhost:7070*.
Requirements
------------
You will need to use Mac OSX or Linux and install the following:

+ **VirtualBox:** https://www.virtualbox.org/wiki/Downloads
+ **Vagrant:** https://www.vagrantup.com/downloads
+ **Fabric:** http://www.fabfile.org/installing.html

It is likely that you already have Python, which Fabric requires. If you are 
unsure, open Terminal and execute `python`.
Installation
------------

