import json
import requests
from collections import defaultdict

# ID of the pdccn2 template
templateID = 10367448

# Certificates for Administ
clientCrt = ".../public.crt"
clientKey = ".../.key"

# Url for api to get template info
url = "https://$url/template/{}".format(templateID)

r = requests.get(url, verify=False, cert=(clientCrt, clientKey))


class ParserModule(object):
    # Gather information and create a dictionary with following information
    # Database, Datasource, Cluster, Max_connection setting
    def create_dict(self, content):
        # Content in api is json string so it must be loaded as json
        content_json = json.loads(content['content'])

        # Creating a dictionary in following form:
        # {database: {ds: {cluster: max_connections}
        db_info = defaultdict(dict)

        for i in (content_json['Weblogic']['Domains'].keys()):
            if len(content_json['Weblogic']['Domains'][i]['JDBC'].keys()) > 1:
                for k, v in content_json['Weblogic']['Domains'][i]['JDBC'].items():
                    if k != 'JDBCDefaults':

                        db_name = v['database']
                        db_source = v['name']
                        target_cluster = v['Targets']['Clusters']
                        capacity = v['customParameters']['max_capacity']

                        # Creating nested dictionary
                        if db_name not in db_info:
                            db_info[db_name] = {}

                        if db_source not in db_info[db_name]:
                            db_info[db_name][db_source] = {}

                            # List of target clusters must be added one by one
                            # Assigning capacity per cluster
                            for c in target_cluster:
                                db_info[db_name][db_source][c] = capacity
                                db_info[db_name][db_source]['MngNodes'] = {}

                                # Assigne machines to the key
                                # While having cluster name accessing servers in template
                                # Getting all assigned machines and creating key:value-list pair

                                for i in (content_json['Weblogic']['Domains'].keys()):
                                    for y in (content_json['Weblogic']['Domains'][i]['Servers'].keys()):
                                        for z, x in (content_json['Weblogic']['Domains'][i]['Servers'][y].items()):
                                            # c = cluster name == y = cluster name
                                            if z == 'Machine' and c == y:
                                                db_info[db_name][db_source]['MngNodes'] = x

        # Returning final dictionary in format:
        # {database: {ds: {cluster: max_connections, MngNodes: [List-of-Machines-assgined]}
        return db_info

    # Get nested dictionary and calculate max connections per database
    # max-connections * mng nodes count
    def calculate_connection(self, content):
        # Calling constructed nested dictionary from previous function
        db_info = self.create_dict(content)
        db_connections = {}

        # Create dictionary with DBs
        for i in db_info.keys():
            db_connections[i] = 0
            for y in db_info[i]:
                # number of mng nodes
                sum_mng_nodes = len(db_info[i][y]['MngNodes'])
                for k, v in db_info[i][y].items():
                    if k != 'MngNodes':
                        calc = int(sum_mng_nodes) * int(v)

                db_connections[i] += calc

        return db_connections


content = r.json()

info = ParserModule()
print(info.calculate_connection(content))
