# Ron Johnson
# 10/23/2016
import dataprint
from JIRAframework import *

return_json = []
jql = 'project = PRODUTIL AND issuetype in (Story, Bug) AND status not in (Closed, Complete, Resolved)'
flds = 'id,key,summary,status,issuetype,customfield_16738,customfield_10002,description,' \
       'customfield_12402,customfield_25677,customfield_16738'

if not getURL() or not getsessionURL() or not getUsername() or not getPassword():
    print('use JIRAconfig to configure your JIRA instance.')
    exit(0)

current_session = jirasession(getsessionURL(), getUsername(), getPassword())
response_json = current_session.query(getURL(), jql, flds, 9999)
# print('total:{0}'.format(response_json['total']))
# print('expand:{0}'.format(response_json['expand']))
issues_json = response_json['issues']

for issue in issues_json:
    field_json = {}
    field_json['key'] = issue['key']
    field_json['summary'] = issue['fields']['summary']
    field_json['issuetype'] = issue['fields']['issuetype']['name']
    field_json['status'] = issue['fields']['status']['name']
    field_json['points'] = issue['fields']['customfield_10002']
    field_json['description'] = issue['fields']['description']
    field_json['acceptance'] = issue['fields']['customfield_12402']
    field_json['reproduce'] = issue['fields']['customfield_25677']
    try:
        field_json['flagged'] = issue['fields']['customfield_16738'][0]['value']
    except:
        field_json['flagged'] = ''

    return_json.append(field_json)

stats = {'Story': {'Total': 0, 'WellFormed': 0, 'Sized': 0, 'Flagged': 0, 'InProgress': 0, 'Pct': 0},
            'Bug': {'Total': 0, 'WellFormed': 0, 'Sized': 0, 'Flagged': 0, 'InProgress': 0, 'Pct': 0},
            'Total': {'Total': 0, 'WellFormed': 0, 'Sized': 0, 'Flagged': 0, 'InProgress': 0, 'Pct': 0}}

for issue in return_json:
    stats[issue['issuetype']]['Total'] += 1
    if issue['status'] in ['In Progress', 'In QA', 'In Review', 'Product Acceptance']:
        stats[issue['issuetype']]['InProgress'] += 1
    if issue['points'] or issue['points'] == 0:
        stats[issue['issuetype']]['Sized'] += 1
    if issue['description'] and ((issue['issuetype'] == 'Bug' and issue['reproduce']) or
        (issue['issuetype'] == 'Story' and issue['acceptance'])):
        stats[issue['issuetype']]['WellFormed'] += 1
    if issue['flagged'] and issue['flagged'] == 'Impediment':
        stats[issue['issuetype']]['Flagged'] += 1

    stats['Total']['Total'] = stats['Story']['Total'] + stats['Bug']['Total']
    stats['Total']['WellFormed'] = stats['Story']['WellFormed'] + stats['Bug']['WellFormed']
    stats['Total']['Sized'] = stats['Story']['Sized'] + stats['Bug']['Sized']
    stats['Total']['InProgress'] = stats['Story']['InProgress'] + stats['Bug']['InProgress']
    stats['Total']['Flagged'] = stats['Story']['Flagged'] + stats['Bug']['Flagged']

    try:
        stats['Bug']['Pct'] = stats['Bug']['InProgress'] / stats['Total']['InProgress']
    except:
        pass
    try:
        stats['Story']['Pct'] = stats['Story']['InProgress'] / stats['Total']['InProgress']
    except:
        pass

display_list = [['', 'Backlog', 'Well Formed', 'Sized', 'Flagged', 'In-Progress', '%'],
    ['Story', stats['Story']['Total'], stats['Story']['WellFormed'], stats['Story']['Sized'],
     stats['Story']['Flagged'], stats['Story']['InProgress'], '{0:.2%}'.format(stats['Story']['Pct'])],
    ['Bug', stats['Bug']['Total'], stats['Bug']['WellFormed'], stats['Bug']['Sized'],
     stats['Bug']['Flagged'], stats['Bug']['InProgress'], '{0:.2%}'.format(stats['Bug']['Pct'])],
    ['Total', stats['Total']['Total'], stats['Total']['WellFormed'], stats['Total']['Sized'],
     stats['Total']['Flagged'], stats['Total']['InProgress'], '']
]

print(dataprint.to_string(display_list, comments=None, comment_lead=''))
