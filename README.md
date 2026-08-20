SCRIPT PYTHON 

1. Script em Python para escalar (subir/descer) pods no OpenShift 3, rodando via CLI (`oc`) a partir de um bastion host.
2. Escala todos de uma vez para `0` (down) ou `1` (up) 


# Scale Pods — OpenShift 3.11

Script em Python para escalonar (subir/descer) DeploymentConfigs no OpenShift 3.11,
executado via CLI (`oc`) a partir de um bastion host com acesso administrativo ao cluster.

## O que faz

- Escala todos os DeploymentConfigs de um ambiente de uma vez, para `0` (down) ou `1` (up)
- Confirma automaticamente se o rollout foi concluído com sucesso

## Como usar

```bash
python3 scale_pods.py down          # desce todos os pods
python3 scale_pods.py up            # sobe todos os pods
```

### Opções

```bash
python3 scale_pods.py up --timeout 180              # aumenta o tempo de espera do rollout para 180s
python3 scale_pods.py up --sem-verificar-rollout     # sobe sem confirmar se os pods ficaram prontos
```

# Contexto

Desenvolvido para uso em ambiente de produção OpenShift 3.11, como parte de rotinas de
suporte e infraestrutura (nível 1 / DevOps Jr).

## Tecnologias

- Python 3
- OpenShift CLI (`oc`)

