# Connecting to Oracle Express 11g R2 using an ORM in Python3

## Summary

This is a "tutorial" of how to connect to Oracle Express using Python through an ORM Tool. Due to also wanting the ability to monitor database changes there seemed to be two popular choices that would achive this goal, **SQLALchemy** and **PonyORM**.

____________

## Terms

* **ORM**: An Object Relational Mapping (ORM) is a programming techinque for converting between incompatible type systems using OOP languageway. In Python, its the ability to translate python classes to tables on relational databases and automatically converts function calls to SQL statments.

## Enviorment

* Oracle VM VirtualBox
  * Ubuntu
  * Python 3
  * Oracle Express 11R 2G

____________

## Pros/Cons

ORM  | Pros  | Cons
---|---|---
SQLAlechmy | Inheritance is easily applied and manipulated. More Libraries are able to work with SQLAlchemy | Does Not Create Sequences automatically and Ensure tablespace is not in set to SYS for users the migration won't work.
PonyORM    | Creates Sequences automatically, Creates ER Diagram when using online tool. Migration set up is in different file. More Tools available | Inheritance are difficult to use especially with migration changes. Not a huge community base, and library can be buggy.

You can still use normal SQL Statements with both ORMs which is a great backup.

Set Up
======
## Python

Install [Python](https://www.python.org/)

Since this is one concept but using two different tools, SQLAlchemy and PonyORM, we will be running two independent virtual environment to keep our libraries separated when installing. THis is to avoiding possible conflicts with libraries. Below are the steps to create your environments.

1) Create a PonyORM_Example directory and SQLAlchemy_Example

    ```sh
    mkdir PonyORM_Example  SQLAlchemy_Example
    ```

2) cd into either projects. You'll run the below command in both directories.

    ```sh
    python3 -m venv venv
    ```

3) Once you have this set up you should see another directory named venv in the project. To activate the environment you'll run the below command. Ensure you remember which venv you have activated.

    ```bash
    source vemv/bin/activate
    ```

4) Once in this "mode" you can run all your installs and run the project without worrying about a lib conflict issue.

    ```bash
    pip install -r requirements.txt
    ```
    or  
    ```bash
    pip install Flask
    ```

5) To get out of this venv or you are done you will run the below command.

    ```bash
    decativate
    ```

## Oracle Express 11G 2R

### It is okay if you want to cry when dealing with Oracle. It is not an easy installation and requires constant adjustment when working with it

Overall, Oracle is a **HUGE** powerful tool that can do a lot in regards to data. Regardless, It was a constant battle with Oracle in my environment. Below is a link to install Oracle Express in a Ubuntu env. Followed by notes and comments of things that need to be done that I forgot or the link did not mentioned. ENJOY!

https://mikesmithers.wordpress.com/2011/11/26/installing-oracle-11gxe-on-mint-and-ubuntu/

#### Oracle Structure(?)

Oracle Services contains **>** Databases (ONLY XE for Express) which contains **>** table spaces which contains **>** schemas (users which can share object) which contains **>** objects (tables, triggers, and ect.)

#### Permissions Notes

Ensure a user(schema) has all the needed permissions to run queries. Below are the ones I used to achieve the bare minimum

```bash
grant CREATE SESSION, ALTER SESSION, CREATE DATABASE LINK, CREATE MATERIALIZED VIEW, CREATE PROCEDURE, CREATE PUBLIC SYNONYM, CREATE ROLE, CREATE SEQUENCE, CREATE SYNONYM, CREATE TABLE, CREATE TRIGGER,CREATE TYPE, CREATE VIEW, UNLIMITED TABLESPACE, DROP ANY SEQUENCE, CREATE SEQUENCE, CREATE ANY SEQUENCE, ALTER ANY SEQUENCE to eddy;
```

#### Oracle Tablespace Issue

SQLAlchemy Does work!!! It needed to have a proper tablesapce. One of the issues SQLAlchemy has and you can read in the sources at the bottom is that when creating a user the default tablespace will be in SYSTEM. Well SQLAlchemy avoids the SYSTEM tablespace when making modifications because the proper way to create schemas in Oracle is to create a new tablespace and then enter users there or enter them in the USERS tablespace. Regardless, you can change the users table space by running the below command. USERS can be the new default or you can create a new tablespace.

```sh
ALTER USER eddy DEFAULT TABLESPACE users;
```

NOTE! Ensure the tablespace is PERMANENT. You can Check that by running the below command.

```sh
SELECT tablespace_name, contents FROM dba_Tablespaces;
```

#### Starting Oracle Notes

If the application is not connecting to Oracle make sure the listener is running. For Ubuntu below is how I ran it.

```sh
sudo su oracle-xe start
```

If this does not work try running

```sh
lsnrctl start
```

If that doesn't work try running.

```sh
sudo rm -rf /var/temp/.oracle/
```

For some reason you need to remove socket files...not sure why but when starting listener you will not be able to do so.

##### Source

[Markup Help](https://confluence.atlassian.com/bitbucketserver/markdown-syntax-guide-776639995.html)
[Oracle Installation](https://mikesmithers.wordpress.com/2011/11/26/installing-oracle-11gxe-on-mint-and-ubuntu/)
[lsnrcrl Issue](https://knowledge.exlibrisgroup.com/Primo/Knowledge_Articles/Oracle_Listener_fails_to_start%2C_error_messages_TNS-12555%2C_TNS-12560%2C_TNS-00525)
[SQLAlechemy Oracle Not Seeing Changes](https://groups.google.com/forum/#!msg/sqlalchemy-alembic/Q32ErOhqyiM/OA6blzebDQAJ)
[Checking Tablespace](http://dbaclass.com/article/ora-30033-undo-tablespace-cannot-be-specified-as-default-user-tablespace/)
[Other Oracle User Fun](www.siue.edu/~dbock/cmis565/module14-1-users.htm)
