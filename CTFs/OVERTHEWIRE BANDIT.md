**OVERTHEWIRE BANDIT**
First let start wit defining what is "overthewire bandit" and what is its purpose. Overthewire bandit  is a free wargame for designed to teach Linux command line skills and cyber security concepts through interactive challenges. It help beginner to learn and get familiar with Linux command on the CLI or command line terminal. It consist of multiple levels through which the user have to first connect to the overthewire server and then look for specific keys hidden in the server, each of those keys allow him to pass to the next level otherwise he won't be able to go to the next level.

# LEVEL0: 

For this first level the challenge was to just explain to you what is the game all about and how to connect to the overthewire server using `ssh` , the name of the host `bandit.labs.overthewire.org`, the port which is port `2220` , the username `bandit0`, and the password which is `bandit0`.
So after opening your terminal on your computer the command you type is:
```
ssh bandit0@bandit.labs.overthewire.org -p 2220
```
![[swappy-20260422-233855.png]]
and then the password `bandit0`. 
![[swappy-20260422-233932.png]]
After being connected now we search for the key that will allows us to connect to level1. The password was located in a file in the home directory, the file was called 'readme' and to be able to read its content i used the `cat` command and found the password.
![[swappy-20260422-233947.png]]

# LEVEL1
Now for the first level i was asked to find the password stored in a files called " - " located into the home directory.
To be able to get the password for this level i had to find a way to open a file of this (-) type. For this i used the `nano` command and the name of the file `nano ./-`
![[swappy-20260422-234013.png]]
and here was the password inside the file
![[swappy-20260422-234001.png]]

# LEVEL2
On level2 of our wargame the challenge was to find the password stored in a file called "--spaces in this filename--" that was located into the home directory. This challenge was an opportunity for me to learn how to open files with such names names that start with -- and end with -- . To be able to solve this i used the `cat` command and  " " and the name of the file `cat "--spaces in this filename--"` 
![[swappy-20260422-234023.png]]

# LEVEL3
The challenge on this level was to find the password the password hidden in a given directory. 
To be able to solve this challenge the first thing i did was to check my location in the server using the command `pwd` , then from my current directory i needed to know what are the different files or folders  that it contains and to do that i used the `ls` command. After finding the directory the next step was to enter the directory and list all the files inside it , first i used the command `cd` to be able to enter the directory `cd inhere`, to be able to see all the different files inside that directory i used the `ls` command but this command allows you to only view the files that are not hidden, so to be able to see the hidden files i used the `ls` command with the option `la` which gave us `ls -la`  , and the last step after finding our hidden file was to see its contain and the command that is used for that is the `cat` command with the name of the file:
![[swappy-20260422-234032.png]]
and here was was our password.

# LEVEL4
This challenge was one the those that i found hard but i was able to find the solution for the. The challenge was to find a password stored in the only human-readable file inside the inhere directory. 
First i started with the `ls` command to list everything that was stored in my current directory and i found the inhere directory. Then i used the `cd` command to be able to enter that directory and the `ls` command to list everything stored in that directory. Now i had a list of all the files stored in that directory and the solution i had to get the password was to open the files one after another using the `cat` command and the name of the file.
![[swappy-20260422-234044.png]]

# LEVEL5
The password for this challenge was stored in a file among many other but with a specific size which was 1033 bytes and was not executable. To be able to find that file i first started with listing the different files and folders in my current directory using the `ls` command then with the `cd` command to enter that directory that was stored in my current directory, after that while in the new directory which is inhere i used the `ls` command with the option `l` to be able to get their properties `ls -l` and see which is executable and not and i found that all of them were not executable, so i now had to find the one with the size that was specified in the challenge which is 1033 bytes. To do that i used the `find` command and i specified that it was to search from the current directory that why i used `./` and finally i used the option `size` and specified the size which is 1033 bytes.
![[swappy-20260422-234053.png]]

# LEVEL6
For the this level of the wargame the challenge was to find the password stored on the server with specificity like it was owned by a certain user and a certain group at the same time with a given size.
So to be able to solve this i needed to use the command `find` , specify the type of the document, specify the user, specify he group and specify the size of the file. So i started with the `find` command followed by the option that specify the type of the document which is `-type` then we specified the document using `f` saying that it's a file then i used the option `-user` to specify the user owner and his name and i used the option `-group` to specify the group owner and finally i used the option `-size` to specify the size of the document.
so the command was:

`find / -type f -user bandit7 -group bandit6 -size 33c`

![[swappy-20260422-234103.png]]
after running our command this was the output and it was very long and most of them were denying me the permission so i had to manually check in the output one by one to see if i find one file that doesn't require permission and i found it:
![[swappy-20260422-234119.png]]
Now after find the file we were looking for i needed to open it and see its contains by using the `cat` command and the name of the file.
So the command was:

`cat /var/lib/dpkg/info/bandit7.password`

![[swappy-20260422-234130.png]]
and after running our command here was our password for this level.

# LEVEL7
