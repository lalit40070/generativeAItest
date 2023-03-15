#Introduction

This is the backend API repo for the Imagine Studio App

### Project Structure
```
├── app
│   ├── api ( End points are defined in this)
│   │   ├── dependencies ( dependencies for api endpoints)
        |-- routes ( All routes for the app divided into routes needed for the app)
│   ├── config ( Celery needed implentation here)
│   ├── models (All Schemas needed for APIs are here.)
    |-- settings ( All app deployment config handled here)
       |-- production.py ( production deployment) ( handle environment variables here)
│   ├── db ( All code related to logic for backend is here)
        |-- repositories ( Core logic is here for APIs)
        |-- migrations ( Alembic based migrations for DB is here)
        |-- queries ( All sql queries are part of this)
├── services
│   ├── All essential APIs not related to APIs
├── Dockerfile 
├── Kubernetes ( All deployment related files are here)
├── requirements.txt
└── .gitignore
```

###Deploy for Development
<ol>
<li> Create .env file and add all configurations here. You can also find these on confluence
<li> uncomment the .env_file and comment .env_prefix in production.py in app/settings folder to use configuration from .env file. If you choose to use via environment variables leave it the same.

</ol>

###Deploy on Kubernetes
<ol>
<li> Create namespace backend ( Already available on cluster)
```
kubectl create namespace backend --kubeconfig "path to kubeconfig"
```
<li> Create secrets.yaml file to pass secret information for the deployment like DB url and Credentials for S3
```
kubectl apply -f secrets.yaml 
```
Note: This file is not found on github. It is on confluence
<li> Apply nginx.yaml file to create ingress for the app ( Already applied. Modify it if adding new routes to the app)


```
kubectl apply -f nginx.yaml
```
<li> We use cloud front signer pem file. We upload it into the cluster using below command. This file will also be on confluence

```
kubectl -n <namespace-for-config-map-optional> create configmap cloudfrontsigner —from-file="path to private key"

```
<li> Create deployment for the app

```
kubectl apply -f deployment.yaml
```# generativeAItest
