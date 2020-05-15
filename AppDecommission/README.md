# WLS App decommission
Decommission application from single environment via WLST scripting tool.


Script is running based on two arguments: Cluster name & console where application is running. 
For time being script is placed on $host - Script can be executed from this server to any target.

Script path: 
/usr/local/bin/WLSAppDecommission.py

```
> /opt/fmw/oracle_common/common/bin/wlst.sh /usr/local/bin/WLSAppDecommission.py ClusterName Domain
```


Script takes a cluster name to find all related managed servers, virtualhosts, data sources, clusters and deployed applications.
Script stops  managed nodes. Undeploy application. Remove related virtual server. Removes related servers, data source and relation to cluster. Removes cluster itself.
