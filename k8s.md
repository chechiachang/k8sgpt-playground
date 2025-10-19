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

Create k8sgpt secret for [AI backends](https://github.com/k8sgpt-ai/k8sgpt-operator?tab=readme-ov-file#other-ai-backend-examples)

```
# AZURE OPENAI
kubectl create secret generic k8sgpt-secret \
    --from-literal=azure-api-key=your-api-key
```

k8sgpt helm install


```
helm repo add k8sgpt https://charts.k8sgpt.ai
helm repo update

cd install
helm install k8sgpt k8sgpt/k8sgpt-operator --values dev/values.yaml
```

helm uninstall

```
helm uninstall k8sgpt
```

### K8sGpt Resource

```
kubectl create -f deploy/dev/values.yaml

kubectl get pods
```

- Install
- Adopter
- Guardrails


