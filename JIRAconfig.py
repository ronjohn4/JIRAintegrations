# Ron Johnson
# 10/23/2016

"""
JIRA Config.

Usage:
  jiraconfig.py  --url <newURL>
  jiraconfig.py  --sessionurl <newsessionURL>
  jiraconfig.py  --username <newusername>
  jiraconfig.py  --password <newpassword>
  jiraconfig.py  --list
  jiraconfig.py  (-h | --help | -v | --version)

Options:
  -l --list        List current configuration.
  -u --url         Set JIRA base url.
  -s --sessionurl  Set JIRA sessionurl.
  -u --username    Set username for JIRA.
  -p --password    Set password for JIRA.
  -h --help        Show this screen.
  -v --version     Show version.
"""

from docopt import docopt
import pickle

if __name__ == '__main__':
    arguments = docopt(__doc__, version='JIRA Config 1.0')

c = {}
file_Name = "config"

try:
    fileObject = open(file_Name, 'rb')
    c = pickle.load(fileObject)
except:  #no config file found, will be created below
    pass

if arguments['--list']:
    for key, value in c.items():
        print('{0}: {1}'.format(key, value))
if arguments['--username']:
    c['username'] = arguments['<newusername>']
if arguments['--password']:
    c['password'] = arguments['<newpassword>']
if arguments['--url']:
    c['URL'] = arguments['<newURL>']
if arguments['--sessionurl']:
    c['sessionURL'] = arguments['<newsessionURL>']

fileObject = open(file_Name, 'wb')
pickle.dump(c, fileObject)
fileObject.close()


