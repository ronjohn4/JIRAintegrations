# JIRA Integrations Scripts

`JIRAWeb.py` - simply unformatted list of active epics and associated stats.  There is also a completed epic list.

`JIRAbacklogstats.py` - command to display statistics on a backlog.

`JIRAbacklogsummary.py` - command to display epic level statistics for a backlog.

`JIRAconfig.py` - command to display and set the JIRA itegration configuration (username, password, url, etc).  Creates a pickle file with config data used by all other programs.

`JIRAdataacive.py` - data access layer returning only active epics.

`JIRAdatacomplete.py` - data access layer returning only complete epics.

`JIRAframework.py` - framework giving base level data access and config access

`JIRAissuedump.py` - dump the full list of fields for a given JIRA key.  Work in progress.

`JIRAissuelist.py` - dump statistics for given list of JIRA keys.

`JIRApulse.py` - displays status related information about the list of JIRA keys.  Gives an idea of JIRA progress being made.
