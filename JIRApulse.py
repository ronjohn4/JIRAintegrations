# Ron Johnson
# 11/4/2016

"""
JIRA Pulse

Usage:
  jirapulse.py  <JIRAkey> ...
  jirapulse.py  (-h | --help | -v | --version)

Options:
  -h --help        Show this screen.
  -v --version     Show version.
"""

import dataprint
from docopt import docopt
from JIRAframework import *

if __name__ == '__main__':
    arguments = docopt(__doc__, version='JIRA Pulse 1.0')

return_json = []
return_json.append(['Key', 'Status', 'Updated'])

if not getURL() or not getsessionURL() or not getUsername() or not getPassword():
    print('use JIRAconfig to configure your JIRA instance.')
    exit(0)

current_session = jirasession(getsessionURL(), getUsername(), getPassword())

# Pull the data for the list of Jira IDs
for key in arguments['<JIRAkey>']:
    try:
        response_json = current_session.issue(getURL(), key)
        return_row = [key,
                      response_json['fields']['status']['statusCategory']['name'],
                      response_json['fields']['updated'][:19]
                      ]
    except Exception as e:
        return_row = [key,
                      'server response {0}'.format(str(e)),
                      'None']

    return_json.append(return_row)

print(dataprint.to_string(return_json, comments=None, comment_lead=''))
