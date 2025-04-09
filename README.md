# python-patreon-list
**python-patreon-list** is a Python project that simplify access to patrons list and other informations from Patreon *(cause their API / python library is quite a mess)*.

The project is based on the patreon-python project from Patreon ([GitHub repository](https://github.com/Patreon/patreon-python)) and simplify its use.
If you need more informations on it, you can check the [official documentation](https://docs.patreon.com/?python#introduction).

> [!IMPORTANT]
> To use all items from this project you will need a `Creator access token` (called here `creator_id`).
> 
> To get it, see the [app registration page](https://www.patreon.com/portal/registration/register-clients) from Patreon.

## Python Script
The Python Script is just a script that you can use to inspire yourself and use part in your own code. 
It is functionnal though. It print the list of every patrons and the number of patrons for every membership.
Think to complete with your own `creator_id` before use.
If you want a even simplier way to take advantage of this beautiful code, consider using the library. 

## Python Library
The Python Library is a .py file you can import in your project to get Patreon informations the simplier way possible.
If you want an example of how to use it, check the example file in the same folder.

## OBS Script
The OBS Script has been created to be used for live streaming purposes. It get the list of every patrons and put it in a txt file that you can display on one of your OBS scene.
The script is based on the obspython library. It can be imported in the script tool of OBS Studio.

To use it, just import it and complete the following parameters :

- `Creator ID` : paste your `Creator access token` (see [Patreon app registration page](https://www.patreon.com/portal/registration/register-clients))
- `File Path` : choose the file that will be filled with the list of patrons
- `Check delay (ms)` : write down the time between two update of the list (the api request for patron list is quite heavy and take some time so for it is recommended to not set a check delay to low for OBS performance purposes. A good number is *3600000* (= 1 hour))
