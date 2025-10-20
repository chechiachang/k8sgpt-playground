### Use custom backend to implement RAG

https://k8sgpt.ai/docs/tutorials/custom-rest-backend

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
uv run fastapi dev main.py
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

k8sgpt analyze --backend customrest --explain --no-cache --max-concurrency=1
```

### dockerize and deploy to k8s

```
```

### Integration

https://docs.k8sgpt.ai/reference/cli/filters/
