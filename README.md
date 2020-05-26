# dcMinitel

This script enables you to post to Dotclear from your Minitel. It is currently just a proof of concept with lots of rough edges.

## Dependencies

You need to install the following dependencies:

- https://github.com/Zigazou/PyMinitel
- https://pypi.org/project/Pillow/


## Setup the minitel

This script will automatically setup the connexion to your minitel. If your minitel boots up in a menu, you will need to hit Fnct-Sommaire to leave the menu.

## Launch the script

You need to have xmlrpc activated on your dotclear blog. Once it is done, you can set the SERVER_URL environment variable to your xmlrpc endpoint URL and launch the script.



## License

This code is published under GPL v3. It contains some parts from the examples included in https://github.com/Zigazou/PyMinitel published under the same license. The Dotclear Logo is (c) Dotclear.
