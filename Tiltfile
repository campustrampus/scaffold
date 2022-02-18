config.define_bool('use_optimized_dockerfile')
cfg = config.parse()

# true does mean ui_target == optimized
if cfg.get("use_optimized_dockerfile",False): # <-- If unset, default to False
	ui_target="optimized"
else:
	ui_target="local"

docker_build(
    'scaffold/backend', 
    './', 
    dockerfile='Dockerfile', 
    target='app',
    ignore=['./web'],
    live_update=[
        sync('./', '/usr/src'),
        run('cd /usr/src && poetry export > requirements.txt && pip install -r requirements.txt',
        trigger='./pyproject.toml'),
    ]
)

docker_build(
    'scaffold/ui', 
    './web',
    dockerfile='./web/Dockerfile',
    target=ui_target,
    live_update=[
        sync('./web', '/app'),
        run('cd /app && yarn install',
        trigger='./web/package.json'),
    ]
)

k8s_yaml(local("helm secrets template scaffold deploy/helm/scaffold -f deploy/helm/local.values.yaml | sed '$d'"))

watch_file('deploy/helm/scaffold-data')
watch_settings(ignore=['scripts','README.md', 'Makefile', 'migrations'])

local_resource(
    name='Port 8000',
    serve_cmd='kubectl port-forward $(kubectl get pods --selector "app.kubernetes.io/name=traefik" --output=name) 8000:8000',
    resource_deps=['scaffold-traefik'],
)

local_resource(
    name='Port 8443',
    serve_cmd='kubectl port-forward $(kubectl get pods --selector "app.kubernetes.io/name=traefik" --output=name) 8443:8443',
    resource_deps=['scaffold-traefik'],
)

k8s_resource(
    'scaffold-postgresql',  
    trigger_mode=TRIGGER_MODE_MANUAL, 
    objects=['scaffold-postgresql:secret'],
    port_forwards=5432
)

k8s_resource(
    'scaffold-rabbitmq',
    objects=[
        'scaffold-rabbitmq:serviceaccount',
        'scaffold-rabbitmq-endpoint-reader:role',
        'scaffold-rabbitmq-endpoint-reader:rolebinding',
        'scaffold-rabbitmq-config:configmap',
        'scaffold-rabbitmq:secret'
    ],
    port_forwards=5672
)

k8s_resource(
    'scaffold-backend',
    objects=[
        'scaffold-backend:serviceaccount',
        'scaffold-backend-secret:Secret',
        'scaffold-backend-config:configmap'
    ],
    resource_deps=[
        'scaffold-postgresql', 
        'scaffold-rabbitmq'
    ],
    port_forwards=8081
)

k8s_resource(
    'scaffold-ui', 
    objects=[
        'scaffold-ui:serviceaccount',
    ],
)

k8s_resource(
    'scaffold-flower', 
    objects=[
        'scaffold-flower:serviceaccount',
        'scaffold-flower-secret:Secret',
        'scaffold-flower-config:configmap'
    ],
    resource_deps=[
        'scaffold-rabbitmq'
    ],
    port_forwards=8888
)

k8s_resource(
    'scaffold-traefik', 
    objects=[
        'scaffold-traefik:ServiceAccount:default',
        'scaffold-traefik:ClusterRole:default',
        'scaffold-traefik:ClusterRoleBinding:default',
        'scaffold-ingress-backend:ingress:default',
        'scaffold-cors-header:middleware:default'
    ]
)
