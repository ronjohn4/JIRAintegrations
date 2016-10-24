import dataprint
import requests
import json
from jira import *

return_json = {}
jql = 'project = PRODUTIL AND issuetype in (Epic) order by Rank'
flds = 'key,summary,status,resolutiondate'

if not getURL() or not getsessionURL() or not getUsername() or not getPassword():
    print('use JIRAconfig to configure your JIRA instance.')
    exit(0)

current_session = jirasession(getsessionURL(), getUsername(), getPassword())
response_json = current_session.query(getURL(), jql, flds, 9999)

# load epic structure in rank order
# print('total:{0}'.format(response_json['total']))
# print('expand:{0}'.format(response_json['expand']))
issues_json = response_json['issues']

for seq, issue in enumerate(issues_json):
    # print(seq, issue['fields']['summary'])
    # return_json[issue['key']] = dict(Name=issue['fields']['summary'], Status=issue['fields']['status']['name'],
    #                        Total=0, Story=0, Bug=0, WellFormed=0, Sized=0, Flagged=0, InProgress=0, Done=0)
    # print('issue:{0}',format(issue))
    if issue['fields']['status']['name'] == 'Closed':
        return_json[issue['key']] = dict(Name=issue['fields']['summary'], Status=issue['fields']['status']['name'],
                                         Total=0, Story=0, Bug=0, WellFormed=0, Sized=0, Flagged=0, InProgress=0,
                                         Done=0, Seq='', CloseDate=issue['fields']['resolutiondate'][:10])
    else:
        return_json[issue['key']] = dict(Name=issue['fields']['summary'], Status=issue['fields']['status']['name'],
                                         Total=0, Story=0, Bug=0, WellFormed=0, Sized=0, Flagged=0, InProgress=0,
                                         Done=0, Seq='{0:0>4}'.format(seq), CloseDate='')

# Stats entry for work that doesn't have an epic
return_json['In Progress'] = dict(Name='No Epic', Status='In_Progress',
                                  Total=0, Story=0, Bug=0, WellFormed=0, Sized=0, Flagged=0, InProgress=0,
                                  Done=0, Seq='0000', CloseDate='')
return_json['Product Acceptance'] = dict(Name='No Epic', Status='Product_Acceptance',
                                         Total=0, Story=0, Bug=0, WellFormed=0, Sized=0, Flagged=0, InProgress=0,
                                         Done=0, Seq='0000', CloseDate='')
return_json['In Review'] = dict(Name='No Epic', Status='In_Review',
                                Total=0, Story=0, Bug=0, WellFormed=0, Sized=0, Flagged=0, InProgress=0,
                                Done=0, Seq='0000', CloseDate='')
return_json['Ready'] = dict(Name='No Epic', Status='Ready',
                            Total=0, Story=0, Bug=0, WellFormed=0, Sized=0, Flagged=0, InProgress=0,
                            Done=0, Seq='0000', CloseDate='')
return_json['Design'] = dict(Name='No Epic', Status='Design',
                             Total=0, Story=0, Bug=0, WellFormed=0, Sized=0, Flagged=0, InProgress=0,
                             Done=0, Seq='0000', CloseDate='')
return_json['Closed'] = dict(Name='No Epic', Status='Closed',
                             Total=0, Story=0, Bug=0, WellFormed=0, Sized=0, Flagged=0, InProgress=0,
                             Done=0, Seq='9999', CloseDate='')
return_json['Resolved'] = dict(Name='No Epic', Status='Resolved',
                               Total=0, Story=0, Bug=0, WellFormed=0, Sized=0, Flagged=0, InProgress=0,
                               Done=0, Seq='9999', CloseDate='')

# Load work item counts into Epic structure created above
jql = 'project = PRODUTIL AND issuetype in (Story, Bug)'
flds = 'id,key,summary,status,issuetype,customfield_16738,customfield_10002,description,customfield_12402,customfield_25677,customfield_16738,customfield_10300'
url = base_url.format(jql, flds, 9999)

# todo-Add paging for big projects
session_response = current_session.get(url)

if session_response.status_code == 200:
    response_json = json.loads(session_response.text)
    # print('total:{0}'.format(response_json['total']))
    # print('expand:{0}'.format(response_json['expand']))
    issues_json = response_json['issues']

    for issue in issues_json:
        if issue['fields']['customfield_10300']:
            key = issue['fields']['customfield_10300']
        else:
            key = issue['fields']['status']['name']

        return_json[key]['Total'] += 1
        if issue['fields']['issuetype']['name'] == 'Story':
            return_json[key]['Story'] += 1
        if issue['fields']['issuetype']['name'] == 'Bug':
            return_json[key]['Bug'] += 1
        if issue['fields']['status']['name'] in ('In Progress', 'Product Acceptance', 'In Review'):
            return_json[key]['InProgress'] += 1
        if issue['fields']['status']['name'] in ('Closed', 'Resolved'):
            return_json[key]['Done'] += 1
        if issue['fields']['customfield_10002']:
            return_json[key]['Sized'] += 1

        try:
            if issue['fields']['customfield_16738'][0]['value'] == 'Impediment':
                return_json[key]['Flagged'] += 1
        except:
            pass

        if (issue['fields']['issuetype']['name'] == 'Story' and issue['fields']['customfield_12402']) or \
                (issue['fields']['issuetype']['name'] == 'Bug' and issue['fields']['customfield_25677']):
            return_json[key]['WellFormed'] += 1
else:
    pass

# print the stats
display_list = []
display_list.append(
    ['Key', 'Epic', 'Status', 'Total', 'Bug', 'Story', 'Sized', 'Flagged', 'Well Formed', 'In Progress', 'Done', ' Seq',
     'Close Date'])

for key, epic in return_json.items():
    display_list.append([
        key,
        epic['Name'],
        epic['Status'],
        epic['Total'],
        epic['Bug'],
        epic['Story'],
        epic['Sized'],
        epic['Flagged'],
        epic['WellFormed'],
        epic['InProgress'],
        epic['Done'],
        epic['Seq'],
        epic['CloseDate']
    ])

# print(dataprint.to_string(display_list, comments=None, comment_lead=''))

def getKey(item):
    return '{0}{1}'.format(item[11], item[12])

sorted_display_list = sorted(display_list, key=getKey)
print(dataprint.to_string(sorted_display_list, comments=None, comment_lead=''))
