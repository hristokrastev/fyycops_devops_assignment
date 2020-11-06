#!/usr/bin/env python

"""
    spin up a digitalocean kubernetes cluster 
    with an additional admin user and an installed
    kubernetes dashboard
"""

from dotenv import load_dotenv, find_dotenv
import os
import sys
import requests
import time
import json

class DigitalOceanClient(object):
    def __init__(self, token):
        super().__init__()

        self.token = token
        self.request_headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token)
        }
        self.base_url = 'https://api.digitalocean.com/v2'

        # cluster id of freshly deployed cluster
        self.k8s_cluster_id = None

        # test authentication by getting account info
        r = requests.get('{}/account'.format(self.base_url), headers=self.request_headers)
        r.raise_for_status()

    def check_for_cluster(self, name):
        """
            check if the given cluster already exists
            returns false if it does, returns true if it doesnt
        """

        r = requests.get('{}/kubernetes/clusters'.format(self.base_url), headers=self.request_headers)
        r.raise_for_status()
        response_body = r.json()

        for c in response_body['kubernetes_clusters']:
            if c['name'] == name:
                return False

        return True

    def deploy_cluster(self, name, size, nodes, version, region):
        payload = {
            'name': name,
            'region': region, 
            'version': version,
            'tags': ['homework'],
            'node_pools': [
                {
                    'size': size,
                    'name': '{}pool1'.format(name),
                    'count': int(nodes)
                }
            ]
        }
        r = requests.post('{}/kubernetes/clusters'.format(self.base_url), 
            headers=self.request_headers, 
            data=json.dumps(payload)
        )
        r.raise_for_status()
        response_body = r.json()

        self.k8s_cluster_id = response_body['kubernetes_cluster']['id']

    def wait_for_cluster(self):
        while True:
            r = requests.get(
                '{}/kubernetes/clusters/{}'.format(self.base_url, self.k8s_cluster_id), 
                headers=self.request_headers
            )
            r.raise_for_status()
            response_body = r.json()
            status = response_body['kubernetes_cluster']['status']['state']

            if status == 'running':
                break
            else:
                print("... wait for cluster deployment to finish (current state: {})".format(status))
                time.sleep(60)

    def retrieve_kubeconfig(self, validity):
        payload = { 'expiry_seconds': int(validity) }
        r = requests.get(
            '{}/kubernetes/clusters/{}/kubeconfig'.format(self.base_url, self.k8s_cluster_id), 
            headers=self.request_headers,
            params=payload
        )
        r.raise_for_status()
        return r.text


if __name__ == "__main__":
    try:
        print("Load application config")
        # load configuration values from .env
        load_dotenv(find_dotenv())

        # configure application
        DO_TOKEN = os.getenv("DIGITALOCEAN_ACCESS_TOKEN")
        CLUSTER_NAME = os.getenv("CLUSTER_NAME", 'homework1')
        CLUSTER_SIZE = os.getenv("CLUSTER_SIZE", 's-2vcpu-4gb')
        CLUSTER_NODES = os.getenv("CLUSTER_NODES", '2')
        CLUSTER_VERSION = os.getenv("CLUSTER_VERSION", '1.18.10-do.2')
        CLUSTER_REGION = os.getenv("CLUSTER_REGION", 'fra1')
        CLUSTER_KUBECONFIG_VALIDITY = os.getenv("CLUSTER_KUBECONFIG_VALIDITY", 2592000)

        if not DO_TOKEN:
            raise ValueError("Digitalocean Access token not specified.")

        # initialize digitalocean client
        print("Initialize client")
        do = DigitalOceanClient(DO_TOKEN)

        # check if cluster already exists
        if not do.check_for_cluster(CLUSTER_NAME):
            raise BaseException("Kubernetes cluster '{}' already exists.".format(CLUSTER_NAME))
    
        # deploy cluster
        print ("Deploy kubernetes cluster")
        do.deploy_cluster(
            name=CLUSTER_NAME, 
            size=CLUSTER_SIZE, 
            nodes=CLUSTER_NODES,
            version=CLUSTER_VERSION,
            region=CLUSTER_REGION
        )
        # wait for cluster deployment to finish
        do.wait_for_cluster()

        # get kubeconfig file valid for N seconds
        # (set to 30days)
        print("Download kubeconfig file")
        with open('kubeconfig', 'w') as file:
            file.write(do.retrieve_kubeconfig(CLUSTER_KUBECONFIG_VALIDITY))

    except:
        e = sys.exc_info()
        print(e)
        sys.exit(1)

    
