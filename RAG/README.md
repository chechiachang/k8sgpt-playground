### Use custom backend to implement RAG

https://k8sgpt.ai/docs/tutorials/custom-rest-backend

Delete existing azureopenai config before using custom backend

```
kubectl get k8sgpt
kubectl delete k8sgpt azureopenai
```

### Install Qdrant

```
helm repo add qdrant https://qdrant.github.io/qdrant-helm
helm repo update
helm install qdrant qdrant/qdrant --namespace qdrant --create-namespace

kubectl get pos -n qdrant
```

### Azure OpenAI

.env

```
AZURE_OPENAI_API_KEY=""
AZURE_OPENAI_ENDPOINT=""
OPENAI_API_VERSION="2024-12-01-preview"
OPENAI_MODEL="gpt-4o-mini"
```

### Embedding

```
```

### Custom Backend

https://docs.k8sgpt.ai/tutorials/custom-rest-backend/

Run server

```
uv run fastapi dev rag-custom-backend.py
```

Curl quick test

```
curl -XPOST -H "Content-Type: application/json" \
    -d '{"model":"xyz","prompt":"xyz","options":{}}' \
    http://127.0.0.1:8000/completions
```

test with k8sgpt cli
```
k8sgpt auth add --backend customrest \
    --baseurl http://localhost:8000/completions \
    --model gpt-4o-mini

k8sgpt analyze --backend customrest --explain --no-cache --max-concurrency=1 \
    --filter Pod,Service,Ingress,ConfigMap
```

### dockerize and deploy to k8s

```
docker build -t chechiachang/k8sgpt-rag:latest .
docker push chechiachang/k8sgpt-rag:latest

# create secret
kubectl create secret generic rag \
    --from-literal=AZURE_OPENAI_API_KEY="" \
    --from-literal=AZURE_OPENAI_ENDPOINT="" \
    --from-literal=OPENAI_API_VERSION="2024-12-01-preview" \
    --from-literal=OPENAI_MODEL="gpt-4o-mini"

kubectl apply -f deploy/
kubectl get pods svc -n rag
```

test

```
kubectl port-forward svc/rag 8000:8000

curl -XPOST -H "Content-Type: application/json" -d '{"model":"xyz","prompt":"xyz","options":{}}' http://127.0.0.1:8000/completions
```

### Integration

https://docs.k8sgpt.ai/reference/cli/filters/
