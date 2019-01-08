from __future__ import print_function
from chalice import Chalice, Rate
import requests
import time


app = Chalice(app_name="lambda-AMP4E-ServiceNOW")

# Automatically runs every 2 minutes
@app.schedule(Rate(2, unit=Rate.MINUTES))
def periodic_task(event):
    # !/usr/local/bin/python3

    """
    Copyright (c) 2018 Cisco and/or its affiliates.
    This software is licensed to you under the terms of the Cisco Sample
    Code License, Version 1.0 (the "License"). You may obtain a copy of the
    License at
                   https://developer.cisco.com/docs/licenses
    All use of the material herein must be in accordance with the terms of
    the License. All rights not expressly granted by the License are
    reserved. Unless required by applicable law or agreed to separately in
    writing, software distributed under the License is distributed on an "AS
    IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
    or implied.
    """

    #import requests
    #import json
    #import time

    # User defined values AMP4E
    client_id = ''
    api_key = ''

    # User defined values ServiceNOW
    user = ''
    pwd = ''

    # Define Variables and Constants
    connector_guid = {}
    session = requests.session()
    url = 'https://api.amp.cisco.com/v1/computers'

    # Define Variables and constants for ServiceNOW
    ServiceNOW_url = 'https://<Your Tenant Account>.service-now.com/api/now/table/incident'
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    """
    Function gets the list of Connector_GUIDs from your AMP account and returns the result as a dictionary
    """

    def get_connector_guid():
        # Setting up the request
        temp_guid = {}
        session = requests.session()
        session.auth = (client_id, api_key)
        response = session.get(url)
        response_json = response.json()

        # Get a list of connector guids and put it in a dictionary
        for computer in response_json['data']:
            temp_guid.update({computer['connector_guid']: computer['hostname']})
        # In the event there is pagination in the results
        while 'next' in response_json['metadata']['links']:
            next_url = response_json['metadata']['links']['next']
            response = session.get(next_url)
            response_json = response.json()
            for computer in response_json['data']:
                temp_guid.update({computer['connector_guid']: computer['hostname']})
        return temp_guid, session

    """
    Using the dictionary of GUIDS as input, check events where Malicious entries occurred and then post into ServiceNOW
    """

    def post_ServiceNOW_Incident(connector_guid):
        # So for each guid check disposition and create an incident into ServiceNOW.
        for guid in connector_guid:
            resp_json = session.get(url + '/' + guid + '/' + 'trajectory').json()
            try:
                for disposition in resp_json['data']['events']:
                    # Condition to check if the file is deemed 'Malicious' and that this event occurred in the last 120 seconds
                    if (disposition['file']['disposition'] == 'Malicious' and (int(time.time()) - int(disposition['timestamp'])) <= 120):
                    #if disposition['file']['disposition'] == 'Malicious':
                        # You can remove this print statement - Used it for testing.
                        print(connector_guid.get(guid) + " " + disposition['file']['file_name'] + " " +
                              disposition['file'][
                                  'disposition'])
                        ## Really messy push to ServiceNOW. Made it more readable.
                        sn_response = requests.post(ServiceNOW_url, auth=(user, pwd), headers=headers, \
                                                    data="{\"caller_id\":\"Admin\",\"category\":\"Network\" \
                                                    ,\"subcategory\":\"internal application\",\"business_service\":\"Desktop\" \
                                                    ,\"cmdb_ci\":\"" + connector_guid.get(guid) + "\",\"contact_type\":\"Automation\" \
                                                    ,\"impact\":\"2\",\"urgency\":\"2\",\"short_description\":\"" \
                                                         + connector_guid.get(guid) + " is infected with Malware\" \
                                                         ,\"description\":\"" + disposition['file'][
                                                             'file_name'] + " is on connector " + guid + "\" \
                                                         ,\"assignment_group\":\"NONE\"}")
                        # You can remove this print statement - Used it for testing.
                        print('Status:', sn_response.status_code, 'Headers:', sn_response.headers, 'Error Response:',
                              sn_response.json())
            except:
                continue

    #if __name__ == '__main__':
    connector_guid, session = get_connector_guid()
    none = post_ServiceNOW_Incident(connector_guid)


