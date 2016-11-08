from JIRAframework import *


def epics_complete():
    # sorted_display_list2 = [{'Key': 'test1','f2': 'test2'},{'Key': 'testa','f2': 'testb'}]
    # return render_template('epicsactive.html', entries=sorted_display_list2)

    return_json = {}
    jql = 'project = PRODUTIL AND issuetype in (Epic) order by Rank'
    flds = 'key,summary,status,resolutiondate'

    if not getURL() or not getsessionURL() or not getUsername() or not getPassword():
        print('use JIRAconfig to configure your JIRA instance.')
        exit(0)

    current_session = jirasession(getsessionURL(), getUsername(), getPassword())

    # load epic structure in rank order
    response_json = current_session.query(getURL(), jql, flds, 9999)
    issues_json = response_json['issues']

    for seq, issue in enumerate(issues_json):
        if issue['fields']['status']['statusCategory']['name'] == 'Done':
            return_json[issue['key']] = dict(Name=issue['fields']['summary'], Status=issue['fields']['status']['name'],
                                             Total=0, Story=0, Bug=0, WellFormed=0, Sized=0, Flagged=0, InProgress=0,
                                             Done=0, Seq='', CloseDate=issue['fields']['resolutiondate'][:10])
        else:
            return_json[issue['key']] = dict(Name=issue['fields']['summary'], Status=issue['fields']['status']['name'],
                                             Total=0, Story=0, Bug=0, WellFormed=0, Sized=0, Flagged=0, InProgress=0,
                                             Done=0, Seq='{0:0>4}'.format(seq), CloseDate='')

    # Load work item counts into Epic structure created above
    jql = 'project = PRODUTIL AND issuetype in (Story, Bug)'
    # jql = 'project = PRODUTIL AND issuetype in (Story, Bug) ' \
    #       'and resolution not in ("Cannot Reproduce", Duplicate, Rejected, "Won\'t Do", "Won\'t Fix/Complete")'
    flds = 'id,key,summary,status,issuetype,customfield_16738,customfield_10002,description,customfield_12402,' \
           'customfield_25677,customfield_16738,customfield_10300'
    response_json = current_session.query(getURL(), jql, flds, 9999)
    issues_json = response_json['issues']

    for issue in issues_json:
        if issue['fields']['customfield_10300']:
            key = issue['fields']['customfield_10300']
        else:
            key = issue['fields']['status']['name']

        # Stats entry for work that doesn't have an epic
        if key not in return_json:
            if issue['fields']['status']['statusCategory']['name'] == 'Done':
                return_json[key] = dict(Name='No Epic', Status=key,
                                        Total=0, Story=0, Bug=0, WellFormed=0, Sized=0, Flagged=0, InProgress=0,
                                        Done=0, Seq='9999', CloseDate='')
            else:
                return_json[key] = dict(Name='No Epic', Status=key,
                                        Total=0, Story=0, Bug=0, WellFormed=0, Sized=0, Flagged=0, InProgress=0,
                                        Done=0, Seq='0000', CloseDate='')

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

    # print the stats
    display_list = []
    # display_list.append(
    #     ['Key', 'Epic', 'Status', 'Total', 'Bug', 'Story', 'Sized', 'Flagged', 'Well Formed', 'In Progress', 'Done', ' Seq',
    #      'Close Date'])

    for key, epic in return_json.items():
        if epic['CloseDate'] or epic['Seq'] == '9999':
            display_list.append({
                'key': key,
                'name': epic['Name'],
                'status': epic['Status'],
                'total': epic['Total'],
                'bug': epic['Bug'],
                'story': epic['Story'],
                'sized': epic['Sized'],
                'flagged': epic['Flagged'],
                'wellformed': epic['WellFormed'],
                'inprogress': epic['InProgress'],
                'done': epic['Done'],
                'seq': epic['Seq'],
                'closedate': epic['CloseDate']
            })


    def getKey(item):
        return '{0}{1}'.format(item['seq'], item['closedate'])

    sorted_display_list = sorted(display_list, key=getKey)
    return sorted_display_list
