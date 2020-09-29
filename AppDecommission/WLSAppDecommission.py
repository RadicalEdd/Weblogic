# Script for app decommission through WLST
# For more info contact @Martin Pazourek
import sys

############
# 1. stop JVMs based on argument provided
# 2. Undeploy application on JVM
# 3. Remove virtual host
# 4. Remove manage node
# 5. Datasource
# 6. Remove clusters
############

# Set up secure files for user authentication
MyUserKeyFile = '/usr/local/bin/UserKeyFile'
MyUserConfigFile = '/usr/local/bin/UserConfigFile'

# Set Application variables from arguments provided
argument = sys.argv[1]
domain_name = sys.argv[2] + ':$port'


# Connect to a domain
def server_connect(domain_name):
    print("Connecting to server: ")
    try:
        connect(userConfigFile=MyUserConfigFile, userKeyFile=MyUserKeyFile, url="%s" % domain_name)
        print
        print("Connected to server %s" % domain_name)
        print
    except Exception:
        print
        print("I failed to connect to server %s" % domain_name)
        print


# Stop managed nodes
def stop_server(server_name):
    try:
        shutdown(server_name, 'Server')
        print
    except Exception:
        print
        print('Failed to shutdown server %s' % server_name)


# Get server name
def get_server_name(argument):
    cd('/')
    servers = cmo.getServers()
    for s in servers:
        name = s.getName()
        if name in argument:
            print(s)


# Get cluster name
def get_cluster_name(argument):
    cd('/')
    clusters = cmo.getClusters()
    for c in clusters:
        name = c.getName()
        if name in argument:
            print(c)


# Get all servers running on the cluster
def get_servers_running_on_cluster(argument):
    cd('/')
    clusters = cmo.getClusters()

    for c in clusters:
        c_name = c.getName()
        if c_name in argument:
            cd('/Clusters/%s' % argument)
            servers = cmo.getServers()
            for s in servers:
                s_name = s.getName()
                print(s_name)


# Get servers running on the cluster and shutdown them
def shutdown_running_servers_on_cluster(argument):
    cd('/')
    clusters = cmo.getClusters()

    for c in clusters:
        c_name = c.getName()
        if c_name in argument:
            cd('/Clusters/%s' % argument)
            servers = cmo.getServers()
            for s in servers:
                s_name = s.getName()
                try:
                    shutdown(s_name, 'Server')
                    print
                except Exception:
                    print
                    print('Failed to shutdown server %s' % s_name)


# Undeploy application running on cluster specified in argument
def undeploy_application_running_on_server(argument):
    cd('/')
    edit()
    startEdit()
    domainConfig()
    listAppDeployments = cmo.getAppDeployments()
    listVirtualHosts = cmo.getVirtualHosts()
    # Find virtualhost tageted on the cluster
    for virtual in listVirtualHosts:
        virtual_name = virtual.getName()
        cd('/VirtualHosts/%s' % virtual_name)
        virtual_target = cmo.getTargets()
        for target in virtual_target:
            if target.getName() == argument:
                virtual_host = cmo.getName()
                for appDeployed in listAppDeployments:
                    cd('/AppDeployments/%s' % appDeployed.getName())
                    listAppTargets = cmo.getTargets()
                    for target in listAppTargets:
                        v = target.getName()
                        if v == virtual_host:
                            storeAppName = cmo.getName()
                            try:
                                print
                                cd('/')
                                edit()
                                startEdit()
                                undeploy("%s" % storeAppName)
                                print
                                print("Application %s was undeployed" % storeAppName)
                                print
                            except Exception:
                                print("I failed to undeploy application %s" % storeAppName)
                            activate()


# Undeploy Jolokia application running on the cluster
def undeploy_jolokia(argument):
    cd('/')
    edit()
    startEdit()
    try:
        print
        undeploy("jolokia-hci", "%s" % argument)
        print
        print("Application jolokia-hci was undeployed from %s" % argument)
        print
    except Exception:
        print("I failed to undeploy application jolokia-hci from %s" % argument)
    activate()


# Get and remove related virtual host and remove it
# find a way of adding cn00a1.cz.infra to the name
def remove_related_virtualhost(argument):
    cd('/')
    edit()
    startEdit()
    domainConfig()
    listVirtualHosts = cmo.getVirtualHosts()
    # Find virtualhost tageted on the cluster

    for virtual in listVirtualHosts:
        virtual_name = virtual.getName()
        cd('/VirtualHosts/%s' % virtual_name)
        virtual_target = cmo.getTargets()
        for target in virtual_target:
            if target.getName() == argument:
                virtual_host = cmo.getName()
                edit()
                startEdit()
                try:
                    # cluster name + server name to create whole name of virtualhost
                    delete("%s" % virtual_host, "VirtualHosts")
                    print
                except Exception:
                    print
                    print("I failed to remove virtual host %s" % virtual_host)
                    print
                activate()


# Undeploy application
def undeploy_application(application_name):
    edit()
    startEdit()
    try:
        print
        undeploy("%s" % application_name)
        print
        print("Application %s was undeployed" % application_name)
        print
    except Exception:
        print("I failed to undeploy application %s" % application_name)
    activate()


# Remove related data sources
def remove_related_data_source(argument):
    edit()
    startEdit()
    domainConfig()
    cd('/')
    cd('SystemResources')

    listDataSource = cmo.getSystemResources()
    # Find virtualhost tageted on the cluster

    for ds in listDataSource:
        ds_name = ds.getName()
        cd('/SystemResources/%s' % ds_name)
        ds_target = cmo.getTargets()
        for target in ds_target:
            if target.getName() == argument:
                ds_name = cmo.getName()
                edit()
                startEdit()
                try:
                    # cluster name + server name to create whole name of virtualhost
                    delete("%s" % ds_name, "JDBCSystemResource")
                    print
                except Exception:
                    print
                    print("I failed to remove data source %s" % ds_name)
                    print
                activate()


# Remove virtual host
def remove_virtual_host(virtual_host_name):
    edit()
    startEdit()
    try:
        # cluster name + server name to create whole name of virtualhost
        delete("%s" % virtual_host_name, "VirtualHosts")
        print
    except Exception:
        print
        print("I failed to remove virtual host %s" % virtual_host_name)
        print
    activate()


# Before removing managed nodes we must remove all managed nodes from the cluster
# Remove managed nodes
def remove_server(server_name):
    try:
        edit()
        startEdit()
        cmo.destroyMigratableTarget(getMBean('/MigratableTargets/%s (migratable)' % server_name))
        editService.getConfigurationManager().removeReferencesToBean(
            getMBean('/MigratableTargets/%s (migratable)' % server_name))
        cd('/')
        cd('/Servers/%s' % server_name)
        cmo.setCluster(None)
        activate()
        cd('/')
        startEdit()
        delete('%s' % server_name, 'Servers')
        activate()
        print
    except Exception:
        print
        print("I failed to remove servers %s" % server_name)
        print


# Remove cluster
def remove_cluster(cluster_name):
    edit()
    startEdit()
    try:
        delete("%s" % cluster_name, "Clusters")
        print
    except Exception:
        print
        print("I failed to remove cluster %s" % cluster_name)
        print
    activate()


# Remove servers running on a cluster
def remove_related_servers(argument):
    cd('/')
    domainConfig()
    cd('/Clusters/%s' % argument)
    server_in_cluster = cmo.getServers()
    for server in server_in_cluster:
        server_name = server.getName()
        edit()
        startEdit()
        try:
            cmo.destroyMigratableTarget(getMBean('/MigratableTargets/%s (migratable)' % server_name))
            editService.getConfigurationManager().removeReferencesToBean(
                getMBean('/MigratableTargets/%s (migratable)' % server_name))
            cd('/')
            cd('/Servers/%s' % server_name)
            cmo.setCluster(None)
            activate()
            cd('/')
            startEdit()
            delete('%s' % server_name, 'Servers')
            print
        except Exception:
            print
            print("I failed to remove servers %s" % server_name)
            print
        activate()


# Remove a cluster
def remove_related_cluster(argument):
    domainConfig()
    cd('/')
    edit()
    startEdit()
    try:
        delete("%s" % argument, "Clusters")
        print
    except Exception:
        print
        print("I failed to remove cluster %s" % argument)
        print
    activate()


server_connect(domain_name)
shutdown_running_servers_on_cluster(argument)
undeploy_jolokia(argument)
undeploy_application_running_on_server(argument)
remove_related_virtualhost(argument)
remove_related_servers(argument)
remove_related_data_source(argument)
remove_related_cluster(argument)

