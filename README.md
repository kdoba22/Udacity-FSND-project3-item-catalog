# **Udacity-FSND-project3-item-catalog**

This project is a simple web application that provides a list of items within several categories. It uses third party authentication, and logged in users can add, edit, and delete their own items.
Its was created using [python](https://www.python.org/), [flask](http://flask.pocoo.org/) and [sqlalchemy](http://sqlalchemy.org)

## **Requirements **
This project requires a vagrant environment setup including [vagrant](https://www.vagrantup.com/), [Oracle Virtualbox](https://www.virtualbox.org/wiki/VirtualBox), [python](https://www.python.org/), [flask](http://flask.pocoo.org/) and [sqlalchemy](http://sqlalchemy.org)

## **Setup**
After installing Vagrant and Oracle's VirtualBox perform the following

1.  Clone the project from github:    
	  git clone https://github.com/kdoba22/Udacity-FSND-project3-item-catalog.git

2.  After project clones, navigate to the Udacity-FSND-project3-item-catalog folder

3.  Bring up the vagrant vm by running 'vagrant up'  (This takes a while)

4.  After this completes connect to the vM by running 'vagrant ssh'  
    **note:**  run 'vagrant halt to shut down vm or cntr-D to disconnect'

5.  Once this command is complete change directories into the vagrant directory, 'cd /vagrant'

6.  Now you need to change directories one last time into the catalog folder, 'cd catalog'

7.  Now the database will need to be populated, so run 'python lotsofitems.py'
	  This job will load the DB with a set of categories and items.

7.  Now your ready to run the project, run 'python views.py'
