# kubernetes - setup

The python script `setup.py` spins up a kubernetes cluster at digitalocean
and downloads a kubeconfig file with a token validy of around 30 days.

You need to specify the digitalocean access token to execute the script.

## Preparation

To execute the scripts you need to setup a local virtualenv

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Spin up cluster

```bash
DIGITALOCEAN_ACCESS_TOKEN=mycoolaccesstoken CLUSTER_NAME=homework1 ./setup.py
```

Encrypt the kubeconfig filw with the candidates public gpg key and send it to her.
```bash
# load public key to gpg keychain
# https://www.gnupg.org/gph/en/manual/x56.html
# https://www.gnupg.org/gph/en/manual/x110.html
gpg --import key.asc
gpg --output kubeconfig.gpg --encrypt --recipient <candidatesgpgkeyid> kubeconfig
```

## Cleanup

After the assingment is complete remove the loadbalancer and the kubernetes cluster.

To remove the loadbalancer remove the corresponding service from the kubernetes cluster
```bash
# list all services and check for "loadbalancer" services
KUBECONFIG=./kubeconfig kubectl get services
NAME                   TYPE           CLUSTER-IP      EXTERNAL-IP     PORT(S)        AGE
demoapp-loadbalancer   LoadBalancer   10.245.248.14   46.101.68.163   80:31782/TCP   6m37s
kubernetes             ClusterIP      10.245.0.1      <none>          443/TCP        16m

# delete the service
KUBECONFIG=./kubeconfig kubectl delete service demoapp-loadbalancer
service "demoapp-loadbalancer" deleted
```

Next, delete the whole cluster from the digitalocean account
```bash
DIGITALOCEAN_ACCESS_TOKEN=mycoolaccesstoken CLUSTER_NAME=homework1 ./destroy.py
```