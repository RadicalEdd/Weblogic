from weblogic.management.security.authentication import UserEditorMBean, UserReaderMBean

# Script for user creation on SOA and OSB servers across all environments
# Shitty job needs shitty solution - made by Middleware Shark @IBM
# You are welcome
# PS sorry for passwords in plain text

#
# Declaration of variables for connection to every admin console
#

# string = ['username', 'pass', 't3://port:url']

SOA_SIT = ['username', 'password', 't3://ip:port']


ENV_LIST = [SOA_SIT]

# Groups to be user attached to
group_name1 = "Monitors"
group_name2 = "Operators"

# Raw input of user's data
user_name = raw_input("Enter name of the user: ")
user_password = raw_input("Enter password of the user: ")
user_description = raw_input("Enter user description: ")


for i in ENV_LIST:
    print("Connecting to server: " + i[2])
    try:
        connect(*i)
    except Exception:
        print("I failed to connect to server " + i[2] + ", call Lampros's personal number to investigate further")

    atnr = cmo.getSecurityConfiguration().getDefaultRealm().lookupAuthenticationProvider("DefaultAuthenticator")
    print("Creation of user: " + user_name)
    try:
        atnr.createUser(user_name, user_password, user_description)
        print("User " + user_name + " created successfully!")
    except Exception:
        print("Error: User " + user_name + " already exists!!")

    print("Adding user " + user_name + " to group " + group_name1)
    try:
        atnr.addMemberToGroup(group_name1, user_name)
        print("User " + user_name + " added to " + group_name1 + " successfully!")
    except Exception:
        print("Error: Failed to add user " + user_name + " to group: " + group_name1)

    print("Adding User " + user_name + " to group " + group_name2)
    try:
        atnr.addMemberToGroup(group_name2, user_name)
        print("User added to group " + group_name2 + " successfully!")
    except Exception:
        print("Error: Failed to add user " + user_name + " to group: " + group_name2)
