README
After executing the topology and open the s1 xterm and whichever clients you want to use (c1, c2, c3)

On the server side, execute first the server.py file to setup the server. From this point forward, you can use ‘messagecount’ , ‘usercount’, ‘newuser’ and ‘storedcount’ commands. This means that functionalities 1 to 8 are implemented on the server.

On the client side, after successfully setting up the server, run the client.py python script. Once started, you will have to input a username and a password (functionality 1). The program has 3 usernames and passwords pair already hardcoded: [ivan, ivan], [david,david] and [jacobo, jacobo]. Once logged in, the client will show the number of offline messages (functionality 2) and display a menu with options 1 to 3. (4 is also available but it is not shown on the menu) (functionality 3). 
Option 1: The client logs out (functionality 7)
Option 2: The client is able to post a new message (functionality 6) for all its followers to see. If any follower is only, their client will display the message (functionality 9). 
Option 3: The client can edit its subscriptions (functionality 5).
Option 4 (not shown on the menu but executable) : The client can see the offline messages (functionality 4). 
