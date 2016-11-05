# Ron Johnson
# 10/23/2016

"""
JIRA Config.

Usage:
  jiraconfig.py  <issue>
  jiraconfig.py  (-h | --help | -v | --version)

Options:
  -h --help        Show this screen.
  -v --version     Show version.
"""

from docopt import docopt
from JIRAframework import *

if __name__ == '__main__':
    arguments = docopt(__doc__, version='JIRA Config 1.0')

# print(arguments)

if not getURL() or not getsessionURL() or not getUsername() or not getPassword():
    print('use JIRAconfig to configure your JIRA instance.')
    exit(0)

current_session = jirasession(getsessionURL(), getUsername(), getPassword())

# Pull the data for the list of Jira IDs
try:
    response_json = current_session.issue(getURL(), arguments['<issue>'])
    # print(response_json)
except Exception as e:
    print('{0}'.format(e))

flds = response_json['fields']

# for key, value in response_json.items():
#     print('----------------------')
#     print('{0}:{1}'.format(key, value))
#     # print('{0}'.format(key))

for key, value in flds.items():
    if value:
        print('{0}'.format(value))
        print('{0}'.format(current_session.fieldname(key)))
        print()
        # print('{0}:{1}'.format(current_session.fieldname(key)), value)







# print(current_session.fieldname('customfield_11900'))
# print(current_session.fieldname('summary'))
# exit(0)

