# Ron Johnson
# 10/23/2016
from jira import *

parms = ['PRODUTIL-768', 'PRODUTIL-721', 'ERROR-xxx']
return_json = []

if not getURL() or not getsessionURL() or not getUsername() or not getPassword():
    print('use JIRAconfig to configure your JIRA instance.')
    exit(0)

current_session = jirasession(getsessionURL(), getUsername(), getPassword())

# Pull the data for the list of Jira IDs
for key in parms:
    try:
        response_json = current_session.issue(getURL(), key)
        return_row = {'key': key,
                      'status': response_json['fields']['status']['statusCategory']['name'],
                      'updated': response_json['fields']['updated']
                      }
    except Exception as e:
        return_row = {'key': key,
                      'status': 'server response {0}'.format(str(e)),
                      'updated': 'None'
                      }
    return_json.append(return_row)

print(return_json)
