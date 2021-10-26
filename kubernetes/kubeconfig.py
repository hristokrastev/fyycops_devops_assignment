#!/usr/bin/env python

"""
    download the kubeconfig file for the specified cluster
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
            returns the id if it exists
            returns none if it doesnt
        """

        r = requests.get('{}/kubernetes/clusters'.format(self.base_url), headers=self.request_headers)
        r.raise_for_status()
        response_body = r.json()

        for c in response_body['kubernetes_clusters']:
            if c['name'] == name:
                self.k8s_cluster_id = c['id']
                continue

        return self.k8s_cluster_id


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
        CLUSTER_KUBECONFIG_VALIDITY = os.getenv("CLUSTER_KUBECONFIG_VALIDITY", 2592000) # valid for 30 days in seconds

        if not DO_TOKEN:
            raise ValueError("Digitalocean Access token not specified.")

        # initialize digitalocean client
        print("Initialize client")
        do = DigitalOceanClient(DO_TOKEN)

        # check if cluster already exists
        if not do.check_for_cluster(CLUSTER_NAME):
            raise BaseException("Kubernetes cluster '{}' not found.".format(CLUSTER_NAME))

        # get kubeconfig file valid for N seconds
        # (set to 30days)
        print("Download kubeconfig file")
        with open('kubeconfig-{}'.format(CLUSTER_NAME), 'w') as file:
            file.write(do.retrieve_kubeconfig(CLUSTER_KUBECONFIG_VALIDITY))

    except:
        e = sys.exc_info()
        print(e)
        sys.exit(1)

    
