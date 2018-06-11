# Connecting to Oracle Express 11g R2 using an ORM in Python3

## Summary

This is a "tutorial" of how to connect to Oracle Express using Python
through an ORM Tool. Due to also wanting the ability to monitor database changes there seemed to be two popular choices that would achive this goal, **SQLALchemy** and **PonyORM**.

____________

## Terms

* **ORM**: An Object Relational Mapping (ORM) is a programming techinque for converting between incompatible type systems using OOP languageway. In Python, its the ability to translate python classes to tables on relational databases and automatically converts function calls to SQL statments.

## Enviorment

* Oracle VM VirtualBox
  * Ubuntu
  * Python 3
  * Oracle Express 11R 2G

____________

Set Up
======
## Python

Install [Python](https://www.python.org/)

Since this is one concept but using two different tools, SQLAlchemy and PonyORM, we will be running two independent virtual enviorment to keep our libraries seperated when installing avoiding possible conflicts. Below are the steps to create your enviorments.

1) Create a PonyORM_Example directory and SQLAlchemy_Example

    `mkdir PonyORM_Example  SQLAlchemy_Example`

2) cd into either projects. You'll run the below command in both directories.

    `python -m venv venv`

3) Once you have this set up you should see another directory named venv in the project. To activate the enviorment by running the below command. Ensure you remember which venv you activate.

    `source vemv/bin/activate`

4) Once in this "mode" you can runn all your installs and run the project without worring about a lib conflict issue.

    `pip install -r requirements.txt`  
    or  
    `pip install Flask`

5) To get out of this venv or you are done you will run the below command.

    `decativate`

## Orcle Express 11G 2R

### It is okay if you want to cry when dealing with Oracle. It is not an easy installation and requires constant adjustment when working with it

Overall, Oracle is a **HUGE** powerful tool that can do a lot in regards to data. Regardless, It was a constant battle with Oracle in my enviorment. Below is a link to install Oracle Express in a Ubuntu env. Followed by notes and comments of things that need to be done that I forgot or the link did not mentioned. ENJOY!

https://mikesmithers.wordpress.com/2011/11/26/installing-oracle-11gxe-on-mint-and-ubuntu/

#### Oracle Scructure(?)

Oracle Serivces contains **>** Databases (ONLY XE for Express) which contains **>** table spaces which contains **>** schemas (users which can share object) which contains **>** objects (tables, triggers, and ect.)

#### Permissions Notes

Ensure a user(schema) has all the needed permissions to run queries. Below are the ones I used to achive the bare minimum

    grant CREATE SESSION, ALTER SESSION, CREATE DATABASE LINK, CREATE MATERIALIZED VIEW, CREATE PROCEDURE, CREATE PUBLIC SYNONYM, CREATE ROLE, CREATE SEQUENCE, CREATE SYNONYM, CREATE TABLE, CREATE TRIGGER, CREATE TYPE,CREATE VIEW, UNLIMITED TABLESPACE, DROP ANY SEQUENCE, CREATE SEQUENCE, CREATE ANY SEQUENCE, ALTER ANY SEQUENCE to eddy;

#### Starting Oracle Notes

If the application is not connecting to Oracle make sure the listener is running. For Ubunutu below is how I ran it.

    sudo su oracle-xe start

If this des not work try running

    lsnrctl start

If that doesn't work try running.

    sudo rm -rf /var/temp/.oracle/

For some reason you need to remove socket files...not sure why but when starting listener you will not be able to do so.


##### Source

[Markup Help](https://confluence.atlassian.com/bitbucketserver/markdown-syntax-guide-776639995.html)

[Oracle Installation](https://mikesmithers.wordpress.com/2011/11/26/installing-oracle-11gxe-on-mint-and-ubuntu/)

[lsnrcrl Issue](https://knowledge.exlibrisgroup.com/Primo/Knowledge_Articles/Oracle_Listener_fails_to_start%2C_error_messages_TNS-12555%2C_TNS-12560%2C_TNS-00525)

