#!/usr/bin/env python
# coding=UTF-8

import argparse
import xmlrpclib
from pprint import pprint


###### issue types :::


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
    s = xmlrpclib.ServerProxy('http://nfbtools.nfb.ca:8080/rpc/xmlrpc')
    auth = s.jira1.login('username', 'password')
    return s, auth

def create_new(args) : # to do 
    print "creating"
    print args

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
    #pprint( res )  
    for item in res :
        print "id : %(id)s \t| name : %(name)s \t| \n|description : %(description)s\n-------" % item

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

if __name__ == '__main__' :

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
    group3.add_argument('-assign_to')
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
        print "executing :: ", args.func, args
        args.func(args)
    else :
        print "found no function to execute"
        print args




