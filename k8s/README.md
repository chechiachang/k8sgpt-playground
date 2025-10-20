### docker

```
docker run --rm ghcr.io/k8sgpt-ai/k8sgpt:v0.4.26 --help
```

### k8s 

[minukube](https://minikube.sigs.k8s.io/docs/start/)

```
minikube config set driver docker
minikube config view
minikube start --kubernetes-version=v1.34.0

kubectx minikube
kubectl get nodes
```

### Prepare k8sgpt Operator

https://docs.k8sgpt.ai/getting-started/in-cluster-operator/

### Install k8sgpt Operator

```
helm repo add k8sgpt https://charts.k8sgpt.ai
helm repo update

helm install k8sgpt k8sgpt/k8sgpt-operator --values install/values.yaml
```

uninstall

```
helm uninstall k8sgpt
```

### Apply K8sGpt Resources: AzureOpenAI

Create k8sgpt secret for [AI backends](https://github.com/k8sgpt-ai/k8sgpt-operator?tab=readme-ov-file#other-ai-backend-examples)

```
kubectl create secret generic azureopenai \
    --from-literal=azure-api-key=your-api-key

kubectl create -f config/azureopenai.yaml

kubectl get pods
kubectl logs azureopenai

kubectl get k8sgpt
```

- Install
- Adopter
- Guardrails


