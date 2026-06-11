# BRUTE FORCE LAB

This project is a local educational cybersecurity lab demonstrating
how weak authentication systems can be abused through repeated
credential guessing attempts.

The application is intentionally vulnerable in Phase 1 for learning
purposes. The future phase which is Phase 2 introduces defensive mechanisms such as
rate limiting, attack detection, CAPTCHA, IP blocking, and monitoring.

## INTRODUCTION

In this we are going to see how an attacker can conduct a simple brute force attack on an admin website page to gain the credentials that will allow him later to be able to login as a normal user  without anyone to notice that someone who is not allowed to be connected is in the system.
First let define our keywords: 
- LAB: is a special environment where where we are going to be conducting our project, a safe place that will allow us to perform the different commands safely without arming our machine. And to get a LAB we are going to set it up on our machine.
- Brute force: it is a cyberattack method that uses a trial-and-error approach to systematically guess login credentials, passwords, or encryption keys by submitting vast combinations of characters until the correct one is found.
Now that we understand the important terms of our project and how it's all about let now get into it.

# PHASE 1:  BRUTE FORCE ATTACK DEMO LAB

Current phase: In this phase the vulnerabilities are completely intentional for educational purpose only.  

- simple Flask login system
- weak/default credentials
- local-only testing
- demonstration of how repeated credential guessing works
- intentionally minimal protections
## SETTING OUR ENVIRONMENT
So for our project we are going to be working locally on our laptop and we are going to set a `python` environment for our project.

The first thing was to make sure that we have all the requirement necessary for our project.
Here we are going to use for our python environment we will use:
- `python3`
- `python3-pip `
- `python3-venv`
So to be able to get them while we are using KALI LINUX as our Operating System we are going to check if we already have them in our OS because KALI LINUX normally comes with `python3` already installed, for this we are going to open our terminal and type `python3` and that should give us an output.

![[pic1.png]]


In case where it's not pre-installed you can always download them with the command 
`pip install flask flask-login flask-limiter bcrypt`

We are also going to need to installed the tool called `HYDRA` which is will allows us to conduct the Brute force attack, again some versions of KALI LINUX come with it pre-installed and for the others not.

Here is how to check it in the terminal:
`hydra` 

Here is how to install it from your terminal:
`sudo apt install hydra`

![[pic2.png]]

## CREATION OF THE WEBSITE
Now that we have installed everything we are going to be using let now start creating our victim website that will run locally.
For this task we are going to use an IDE called `VSCODIUM` which is the optimized version of `VSCODE` for Linux.

Here is how to install it from the terminal:
`sudo apt install VSCodium`

After its installation now we can launch it and start writing our website's code

![[pic3.png]]


## INITIALIZING THE DATABASE
Now after creating our small victim website, we now need to initialize our database to run locally. Using the terminal we first need to be in the folder where our website is located, for that we are going to be using the `cd` command to move between the different directories that we have in our laptop.
When we are sure that we are in the right directory now we can initialize our database with the command `python3 + (database-name)`

In our case here is how the command looks like: `python3 init_db.py`
And here is how the output should look like:

![[pic4.png]]



As we can see on our picture, we were moving throughout the different directories using the `cd` command till we were in the directory that contains our project then using the `python3 init_db.py` command we were able to initialize our database. The output `database initialized`  just comes to confirm to us that the database for our website has been initialized. 



## RUNNING THE WEBSITE LOCALLY
Now it time to run our website locally so that we can start our attack simulation.
For this step we are going to use the same command which is `python3` as we did for the initialization of the database but here instead of the database name we are going to put `app.py`
Here is how our full command looks like : `python3 app.py`

![[pic5.png]]

As we can see on our screenshot after running the command we can see that the servers is now locally running on `http://127.0.0.1:5000`

And when we go to `http://127.0.0.1:5000` in our browser we can now see our admin login page running as shown on the picture bellow.

![[pic6.png]]

## LOGGING TO THE ADMIN PAGE 
For the admin to be able to login to the admin panel we set the admin user name to be `admin` and his password to be `Admin123!` directly in the website code as we can see on the screenshot bellow:

![[pic7.png]]


After login in here is how our admin panel looks like:

**ATTENTION: REMEMBER THIS WEBSITE IS JUST FOR THE PROJECT, JUST FOR PRACTICE THAT'S WHY I DIDN'T PUT MUCH ATTENTION ON THE STYLING AND DETAILS.** 

![[pic8.png]]


And also i implemented a basic functionality like the ability to logout and some some security functionalities like in case a password or username is incorrect to give a maximum number of attempts that is 5 and a timeout to wait until you can try again to login which is 30 seconds as you can see in the picture bellow:

![[pic9.png]]


![[pic10.png]]

## LET'S ATTACK
So now here comes the moment we are going to conduct our attack on the website and see if we can gain access to the admin page.
For this step we are going to use a tool called `hydra` which will allows us to conduct a brute force attack to get the credentials that will allow us to connect to the admin panel.

**Hydra** is an open-source, parallelized network login cracker designed to perform rapid **brute-force** and **dictionary attacks** against various online network protocols and services.

When using hydra we are also going to need to have two word lists, one for the usernames and the other one for the password. For this project i created two small word lists, one that contains each 10 usernames including our username `admin` and the other one 10 passwords including our password `Admin123!` because for hydra to be able to guess the write username or password they must be included in the word lists you provided otherwise it won't give you an output containing the credentials.

It's going to use the contain of those word lists and test each password and username one by one until it get the right password and username. 

**ATTENTION: Performing a brute force attack can be time consuming when your are working with a huge word list that can contain billions of passwords or usernames, so since we are doing it for a simple project that's why i decided to create small and simple word lists to be able to save time.** 

So here as we already know our login credentials are `admin` for the username and `Admin123!` for the password so we are going to use `hydra` and test to see if we will be able to get those credentials that will allow us to log in into the admin panel.
Here I used the command 

- `hydra -L usernames.txt -P passwords.txt 127.0.0.1 -s 5000 http-post-form "/login:username=^USER^&password=^PASS^:F=Invalid" -vV   ` 

a command that I'm going to explain.
Here is the explanation of that command what it does, how it works and the meanings of its components: 

- `hydra`: is a tool that automates repeated authentication attempts against supported protocols and login forms. In our case we are testing our own Flask login lab locally on our machine.
- `-L`:  Load a list of usernames from a file here which is `usernames.txt` which contains multiple usernames inside it.
- `-P`: Load a list of passwords from a file here which is `passwords.txt`  which contains multiple passwords inside it.
**NB: Here hydra is going to combine every username to every password to be able to get the right combination.** 
- `127.0.0.1`: is our target that's running locally.
- `-s`: specifies the port we are conducting the attack on which in our case it's `5000`
**NB: It's because our flask app is running on `http://127.0.0.1:5000`**
- `http-post-form`: This tells hydra that the login uses an HTTP POST web form.
- `"/login:username=^USER^&password=^PASS^:F=Invalid"`: This is the login specification. It has three parts:
	- `/login`: The URL endpoint receiving login requests
	- `username=^USER^&password=^PASS^`: This describes the POST request body. Hydra replaces:
		- `^USER^`: with usernames
		- `^PASS^`: with passwords
	- `F=Invalid`: The `F` means detect failed logins if response contains this text.
- `-vV`: Verbose mode. 

So basically this command read usernames from `usernames.txt`, read passwords from `passwords.txt`, send POST requests to `/login`, replace placeholders with credential combinations, detect failures using `invalid`, and the report attempts that appear successful.

![[pic11.png]]

![[pic12.png]]

![[pic13.png]]

And now as we can see we were able to get the correct combination of username and password that allow us to connect to the admin panel.





# PHASE 2: FLASK AUTHENTICATION SECURITY LAB WITH ATTACK DETECTION.

What i'll add:

- rate limiting
- CAPTCHA
- IP lockouts
- detection dashboards
- SIEM-style monitoring
- live alerts
- logging analytics.

## INTRODUCTION

In this Phase of our project we are now going to protect our website by adding functionalities that we didn't have before. We are also going to be more focused on our website's code because that's where most of our modifications are going to be done.

Here we are going to:
- add better logging
- build a log viewer
- add rate limiting time 
- add IP based lockout 
- Detect automated tools 
- add statistics
- make the UI more cybersecurity themed
Now let get into it.

## ADDING BETTER LOGGING

Here the first thing we are going to do is to look for the function that deals with the logging in our website and that function can be found in the `app.py` file of the website. 

![[pic14.png]]

After we found our function the next step will be to replace it with a better and more secure one. In our case here is the function that I used to replace our previous function. 

![[pic15.png]]


Here with the new function we can see that our new logging can now request for the IP of the device that tries to connect, a timestamp showing when the login happens in real time, the status of the login if it succeed or failed, the user agent either a browser or an automated tool, and an attempt counter which allows to track how many time a device attempted to log in.

Now let launch an attack again and see if it will work. We should be able to see in the `attempts.log` file of our website the different log in attempts with the time, username, status, IP, and the use-agent(either browser or automation tool in our case `hydra`).

![[pic16.png]]

![[pic17.png]]

After launching the attack we can see that the we were still able to get the login credentials for the admin page, the purpose of the changes we have made is not yet to stop an attack but to be able to recognize one once we check the login attempts.
Here is now the output in our `attempts.log` file.

![[pic18.png]]

As we can see in our file the login attempts that occurs and their statuses and only one of them has as status `SUCCESS` meaning the we were able to get the credentials wanted. We can also see that we were able to detect that the logins were attempted by an automated tool called `hydra`. 



## BUILD A REAL LOG VIEWER

Now here we don't want to have to go to the `attempts.log` file to be able to see the log attempts, we want to add a log viewer at the admin panel so that he will be able to see them directly when he logs in and make quick decisions.

Here we need to look for the function that deals with the admin panel and in our case that function is `admin()` that's located in the `aap.py` file and modify it so that it can allow us to see the different logins once the admin in logged in.

![[pic19.png]]

Here is our new function that will deal with the admin panel.

![[pic20.png]]


Now after adding it we also need to modify our website's style so that it can be able to properly show the dashboard.

Here is how our admin panel used to be

![[pic21.png]]

And here is how it looks now 

![[pic22.png]]

And as we can see on this second picture all the logs are appearing at the admin panel once he is logged in.
AS we said this will allow the admin to be able to see in real time the different login attempts and make suitable and fast decisions.

## RATE LIMITING

This is now where we now start actively blocking attacks coming from `hydra` . Here we will use `Flask-limiter`. 
First we need to download it using: `pip install flask-limiter`

After modifying multiple parts of our website code it should no be able to detect a brute force attack, record the attack, flag the suspicious IP, and temporary lock the account. 

To test that we are going to our login page and input multiple fake passwords and usernames. 

As we can see on the bellow pictures after too many attempts to log in the IP of our device was flagged and the account was temporary locked:

As we can see in our logs the attacker tried to log in multiple times with the wrong username or password:

![[pic24.png]]

As we can see on this screenshot the account was locked due to multiple failed attempts to log in:

![[pic23.png]]



## IP BASED LOGOUT

Our current system can only and simply block a username after multiple log in attempts failures but remember an attack can try multiple usernames when trying to guess the correct one. 

In our code again we are going to add or replace part of it to make it more secure an allow it to log out suspicious IPs. 

The above part added to our code gives a limit attempts and temporary block the IP of a device after trying to log in multiple times.

![[pic25.png]]

The above piece of code added verifies if an IP has been locked:

![[pic26.png]]

The above piece of code added count the number of log in attempts from a specific IP:

![[pic27.png]]

The above piece of code handle when a user successfully log in:

![[pic28.png]]

And finally here after testing we can see that the user has been blocked due to multiple log in attempts:

![[pic29.png]]




## CONCLUSION

This project demonstrates a simple but realistic cybersecurity lab focused on authentication security and attack detection. It shows how a basic login system can be progressively hardened by adding logging, rate limiting, IP-based lockouts, and detection of automated attack tools.

Beyond functionality, the project highlights how real-world systems monitor and respond to brute-force attempts in real time, transforming raw login data into actionable security insights. Overall, it serves as a foundational SOC-style simulation, bridging the gap between web development and practical cybersecurity defense techniques.
