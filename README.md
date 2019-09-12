# Item Catalog Project
Item Catalog project is the fourth project for the [Udacity Full Stack Web Developer Nanodegree Program.](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004)

## About the project: 
In this project, you’ll combine your knowledge of building dynamic websites with persistent data storage to create a web application that provides a compelling service to your users. 
You will learn how to develop a RESTful web application using the Python framework Flask along with implementing third-party OAuth authentication. Then you'll learn when to properly use the various HTTP methods available to you and how these methods relate to CRUD (create, read, update and delete) operations.

To accomplished this you'll develop an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.


# How to Run the Program

## Setting up the project

1.  Install [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) 
	    to install and manage virtual machine to create an enviroment to run the project.   
	
2.  Download the VM configuration zip file by [Udacity](https://d17h27t6h515a5.cloudfront.net/topher/2017/May/59125904_fsnd-virtual-machine/fsnd-virtual-machine.zip)
	    OR Clone the repository from [here](https://github.com/udacity/fullstack-nanodegree-vm)
	
3.  Clone this repo [here]() to the vagrant folder that is inside  
	    the VM configuration file that was downloaded/cloned above.  
	
4.  Once the project has been setup, navigate into the project directory
	    with 'Vagrantfile' and then `cd item-catalog-project`

## Run the Program
	
5.  Start the virtual machine with `vagrant up`
	
6.  Connect to the virtual machine with `vagrant ssh`
	
7.  Go to the folder where the guest/host files are shared `cd /vagrant`
	
8.  Navigate to the project folder inside vagrant enviroment  `cd /catalog`

9.  Initialize the database: `python database_setup.py`

10. Populate the database with data run the command: `python manymenus.py`

11. To launch the application run the command: `python project.py`

12. Open the browser and go to `http://localhost:5000`

# Troubleshooting
If your command prompt does not start with vagrant after typing `vagrant ssh` then please try the `winpty vagrant ssh` on your Windows system.

# Resource Links
[Udacity Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004)

pycodestyle \
https://pycodestyle.readthedocs.io/en/latest/intro.html \
https://www.python.org/dev/peps/pep-0008/

PostgreSQL documentaion \
https://www.postgresql.org/docs/current/index.html

Installing Vagrant on Ubuntu \
https://howtoprogram.xyz/2016/07/23/install-vagrant-ubuntu-16-04/

Google Sign-In for server-side apps \
https://developers.google.com/identity/sign-in/web/server-side-flow
