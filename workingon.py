#!/usr/bin/env python
# coding=UTF-8

import argparse
import xmlrpclib
from pprint import pprint
import ConfigParser
import os

###### issue types :::
SERVER   = ""
USERNAME = ""
PASSWORD = ""

ISSUE_TYPES = {
    'epic' : {
        'id': '5',
        'name': 'Epic',
        'subTask': 'false'
        },
    'story' : {
        'id': '6',
        'name': 'Story',
        'subTask': 'false'
        },
    'test_scenario' : {
        'id': '10',
        'name': u'Sc\xe9nario de test',
        'subTask': 'false'
        },
    'feature':{
        'id': '2',
        'name': 'New Feature',
        'subTask': 'false'
        },
    'impediment':{
        'id': '17',
        'name': 'Impediment',
        'subTask': 'false'
        },
    'improvement': { 
        'id': '4',
        'name': 'Improvement',
        'subTask': 'false'
        },
    'innovation' : { 
        'id': '16',
        'name': 'Innovation',
        'subTask': 'false'
        },
    'bug' : { 
        'id': '1',
        'name': 'Bug',
        'subTask': 'false'
        },
    'contenu' : {
        'id': '15',
        'name': 'Contenu',
        'subTask': 'false'
        },
    'language' : { 
        'id': '14',
        'name': 'Langage',
        'subTask': 'false'
        },
    'maintenance' : { 
        'id': '8',
        'name': 'Maintenance',
        'subTask': 'false'
        },
    'task' : { 
        'id': '3',
        'name': 'Task',
        'subTask': 'false'
        },
    'spike' : { 
        'id': '9',
        'name': 'Spike',
        'subTask': 'false'
        }
    }
### END issue types

# parser = argparse.ArgumentParser()
# parser.add_argument("action2", help="which action do you want to do? [ show_issue_types, create, update, view_projects_list ] ")

# parser = argparse.ArgumentParser()
# parser.add_argument('action')
# parser.add_argument('rest', nargs="*")
def connect():
    s = xmlrpclib.ServerProxy( SERVER , allow_none=True)
    auth = s.jira1.login( USERNAME, PASSWORD)
    return s, auth

def find_in_array_of_dict(content, key, elem):
    res =[item for item  in content if item[key] == elem]
    if len(res) == 1 :
        return res.pop()
    return {}

def create_new(args) : # to do 
    #print dir(args), args.fix_version
    s , auth = connect()
    issue_type = ISSUE_TYPES.get( args.opt1, '6')## need a better way
    all_fix_versions = s.jira1.getVersions( auth, args.projectkey )
    fix_version = find_in_array_of_dict(all_fix_versions, "name", args.fix_version ).get("id")
    assignee = USERNAME if args.assign_to_me else args.assignee
    issue = { 
        'project': args.projectkey, 
        'type': issue_type['id'],
        'summary': args.msg, 
        'description': args.description if args.description else args.msg, 
        #"assignee" : assignee, 
        'status' : args.status,
        'fixVersions': [ {'id': fix_version }]}
    if assignee :
        issue['assignee'] = assignee
    #print issue
    newissue = s.jira1.createIssue(auth, issue )
    print "Created issue ::  %(key)s => http://nfbtools.nfb.ca:8080/browse/%(key)s " % newissue, newissue
    #print args

def update_issue(args): # to do
    print "updating"
    print args

def comment_issue(args):
    s , auth = connect()
    s.jira1.addComment(auth, args.opt1, args.msg )
    print "comment added on issue %(issue)s => http://nfbtools.nfb.ca:8080/browse/%(issue)s" % {'issue' : args.opt1}

def show_issue(args):
    s , auth = connect()
    pprint( s.jira1.getIssue(auth, args.opt1) )   

def show_fix_versions(args):
    s , auth = connect()
    res = s.jira1.getVersions( auth, args.projectkey )
    print ":::: fix versions in the system ::::"
    pprint( res )  
    for item in res :
        print "id : %(id)s \t| name : %(name)s \t| \n-------" % item

def show_statuses(args):
    s , auth = connect()
    res = s.jira1.getStatuses( auth )
    print ":::: statuses in the system ::::"
    #pprint( res )  
    for item in res :
        print "id : %(id)s \t| name : %(name)s \t| \n|description : %(description)s\n-------" % item

def show_issue_types(args):
    head =  "\n:::: Listing of issue type understood by %s ::::"
    if args.opt1 and args.opt1 in ["local"]: # take from the file
        print head % "the local script"
        for key,item in ISSUE_TYPES.items() :
            print "\tissue type : %(key)s \t- %(name)s" % {'key' : key, 'name' : item['name']}
    else :
        print head % "the Jira system"
        s , auth = connect()
        #res = s.jira1.getProjectsNoSchemes(auth)
        res = s.jira1.getIssueTypesForProject(auth , args.projectid)
        #pprint(res)
        for issue_type in res : 
            # pprint(issue_type)
            print "\tissue type : %(key)s \t- %(name)s\n\t-----\n\t%(descr)s\n" % {'key' : issue_type['name'].lower(), 'name' : issue_type['name'], "descr" : issue_type['description']}

    print "---" * 20, "\n",args

def show_projects(args):
    s , auth = connect()
    res = s.jira1.getProjectsNoSchemes(auth)
    for item in res :
        #pprint(item)
        print "id : %(id)s \t| key : %(key)s  \t| \n| description : %(description)s \n" % item

def write_config(username="asd", password="ads", server='http://nfbtools.nfb.ca:8080/rpc/xmlrpc'):
    config = ConfigParser.RawConfigParser()
    config.add_section('settings')
    config.set('settings', 'username', username)
    config.set('settings', 'password', password)
    config.set('settings', 'server', server)
    # Writing our configuration file to 'example.cfg'
    homepath = os.path.expanduser("~")
    filename = str(os.path.join( homepath, ".workingon.cfg" ))
    with open( filename, 'w+b') as configfile:
        config.write(configfile)

def read_config():
    homepath = os.path.expanduser("~")
    filename = str(os.path.join( homepath, ".workingon.cfg" ))
    config = ConfigParser.RawConfigParser()
    config.read( filename )  
    print "setting server info"
    globals()['SERVER']   = config.get('settings', 'server')
    globals()['USERNAME'] = config.get('settings', 'username')
    globals()['PASSWORD'] = config.get('settings', 'password')
    #print SERVER, USERNAME, PASSWORD
    #print globals()

if __name__ == '__main__' :
    try :
        #print ":::: reading config ::::"
        read_config()
        print "--------------"
    except ConfigParser.NoSectionError:
        print "--- error writting config in '~/.workingon.cfg'. Please adjust it!!"
        write_config()

    parser = argparse.ArgumentParser(prog='PROG')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--create', dest='func', action='store_const', const=create_new) #, dest="action")
    group.add_argument('--update', dest='func', action='store_const', const=update_issue)
    group.add_argument('--comment', dest='func', action='store_const', const=comment_issue)
    group.add_argument('--show_issue', dest='func', action='store_const', const=show_issue)
    group.add_argument('--show_issue_types', dest='func', action='store_const', const=show_issue_types)
    group.add_argument('--show_projects', dest='func', action='store_const', const=show_projects)
    group.add_argument('--show_statuses', dest='func', action='store_const', const=show_statuses)

    group.add_argument('--show_fix_versions', dest='func', action='store_const', const=show_fix_versions)
    ##
    group.add_argument('--delete', dest="delete_options", nargs='+') # for show info?
    parser.add_argument('-projectkey', default='NFB')
    parser.add_argument('-projectid', default='10010')
    parser.add_argument('-fix_version')
    parser.add_argument('-description')
    group2 = parser.add_mutually_exclusive_group()
    group2.add_argument('-title')
    group2.add_argument('-msg')
    parser.add_argument('-u', help='username')
    parser.add_argument('-p', help='password')
    parser.add_argument('opt1', nargs="?")
    group3 = parser.add_mutually_exclusive_group()
    group3.add_argument('-assign_to', dest="assignee")
    group3.add_argument('-assign_to_me', action='store_true')
    ###
    group4 = parser.add_mutually_exclusive_group() # should not accept anything
    group4.add_argument('-set_status', dest="status", default="1", action='store_const', const='1')
    group4.add_argument('-start', dest="status", default="3", action='store_const', const='3')
    group4.add_argument('-done', dest="status", default="5", action='store_const', const='5')
    group4.add_argument('-reopen', dest="status", default="4", action='store_const', const='4')

    ### create a ~/.workingon to store username [& password]


    args = parser.parse_args()
    #print args #, args.action
    if args.func :
        #print "executing :: ", args.func, args
        args.func(args)
    else :
        print "\nfound no function to execute"
        #print args




