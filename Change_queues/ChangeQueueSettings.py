# Example of queue path
# '/JMSSystemResources/$app/JMSResource/$app/UniformDistributedQueues/$appqueue/DeliveryParamsOverrides/$appsStatusQueue'
delivery_param_queues = [
'/path/to/jms/queue',
'/path/to/jms/queue',
]


delivery_failure_queues = [
'/path/to/jms/queue',
'/path/to/jms/queue',
]

# Secure files with credentials
WUserKeyFile = '/opt/oracle/fmw_12.2.1.3.0/oracle_common/common/bin/WUuserKeyFile.secure'
WUserConfFile = '/opt/oracle/fmw_12.2.1.3.0/oracle_common/common/bin/WUserConfFile.secure'

# Connect to a server
print("Connecting to server: ")
try:
    connect(userConfigFile=WUserConfFile, userKeyFile=WUserKeyFile, url='t3://host:port')
except Exception:
    print("I failed to connect to the server")

# Unlock domain for editing
edit()
startEdit()

# Changing time to live parameter
for queue in delivery_param_queues:
    print("Changing time to live for: %s" % (queue))
    cd(queue)
    cmo.setTimeToLive(1000)

# Changing expiration policy to discard and redelivery limit to 1
for queue in delivery_failure_queues:
    print("Changing expiration policy for: %s" % (queue))
    cd(queue)
    cmo.setExpirationPolicy('Discard')
    cmo.setRedeliveryLimit(1)

# Activate changes and disconnect from domain
print("Activating changes ...")
activate()
print("Disconnecting ...")
disconnect()
