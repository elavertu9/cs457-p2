P2: Anonymous web get
Evan Lavertu
Cody Coleman

About:
  This python program is used to retrieve files on the web anonymously.
  If request is successful, the file will be written in your local directory
  If request fails, an error message will be returned and no file will be written


Usage:
  In order to use this python program, you must start ss.py on each chainlist computer

  ss.py: python3 ss.py -p <PORT>
    * Can be -p or -P
    * Port argument is optional.
    * No argument will use default port 8099
  awget.py: python3 awget.py <URL> -c <CHAINLIST>
    * Can be -c or -C
    * Chainlist argument is optional.
    * No argument will use default chainfile chaingang.txt

URL's:
  This program is capable of handling a list of common top level domains.
  com, org, net, us, co, int, mil, edu, gov, ca, cn, fr, ch, au, in, de, jp, nl, uk, mx, no, ru, br, se, es

Example:
  denver.cs.colostate.edu, boise.cs.colostate.edu, phoenix.cs.colostate.edu, dover.cs.colostate.edu

  * Copy ss.py to the CS lab computers above and enter "python3 ss.py" in the terminal
    * This will use the default port 8099
  * On another CS lab computer of your choice (I prefer Augusta) enter "python3 awget.py google.com" in the terminal
    * This will use the default chainlist containing an entry for every computer you started ss.py on with port 8099. Using URL google.com will return the index.html of google's home page.
