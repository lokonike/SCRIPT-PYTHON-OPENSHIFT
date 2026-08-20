import subprocess  # usado pra rodar comandos de terminal
import argparse    # usado pra ler o que foi digitado no terminal

#LISTA DE PODS PARA SEREM ESCALADOS OU REDUZIDOS, PODE SER ADICIONADO MAIS DE UM POD, SEPARADOS POR VIRGULA
pods = [ 
    
]

#funcao procura os namespaces, se achar devolve o nome, se nao achar devolve com "none"
def descobrir_namespace(nome): 
    cmd = ["oc", "get", "dc", "--all-namespaces",
           "-o", "jsonpath={range .items[?(@.metadata.name==\"" + nome + "\")]}{.metadata.namespace}{end}"]
    resultado = subprocess.run(cmd, capture_output=True, text=True)

    if resultado.returncode == 0 and resultado.stdout.strip():
        return resultado.stdout.strip()
    else:
        return None


def escalar(nome, replicas, verificar_rollout, timeout):
    namespace = descobrir_namespace(nome) #descobre o namespace

    if namespace is None: 
        print(f"{nome}: FALHOU -> dc nao encontrado em nenhum namespace")
        return False, "dc nao encontrado em nenhum namespace"

    cmd = ["oc", "scale", f"dc/{nome}", f"--replicas={replicas}", "-n", namespace] #scale ou downscale dos pods
    resultado = subprocess.run(cmd, capture_output=True, text=True)  

    if resultado.returncode != 0: 
        erro = resultado.stderr.strip()
        print(f"{nome} ({namespace}): FALHOU -> {erro}")
        return False, erro

    # faz esperar o pod "ficar pronto" quando estamos subindo (replicas > 0)
    if verificar_rollout and replicas > 0:
        rollout_cmd = ["oc", "rollout", "status", f"dc/{nome}",
                       "-n", namespace, f"--timeout={timeout}s"]
        rollout = subprocess.run(rollout_cmd, capture_output=True, text=True)

        if rollout.returncode != 0:
            erro = rollout.stderr.strip() or rollout.stdout.strip()
            print(f"{nome} ({namespace}): FALHOU -> pod nao ficou pronto -> {erro}")
            return False, f"pod nao ficou pronto -> {erro}"

    print(f"{nome} ({namespace}): OK")
    return True, None


parser = argparse.ArgumentParser()
parser.add_argument("acao", choices=["down", "up"]) #so aceita up ou down
parser.add_argument( 
    "--timeout", type=int, default=90,
    help="Tempo maximo (segundos) esperando o pod ficar pronto no 'up' (default: 90)"
) #quantos segundos esperar por pod (opcional)
parser.add_argument(
    "--sem-verificar-rollout", action="store_true",
    help="Nao espera o pod ficar pronto no 'up', so confirma que o comando de scale foi aceito"
)
args = parser.parse_args()

replicas = 0 if args.acao == "down" else 1
verificar_rollout = not args.sem_verificar_rollout

sucesso = 0
falha = 0
falharam = []  # guarda (nome, motivo) de cada falha
#Vai somando em sucesso falha e guardando (nome, motivo) de cada falha numa lista chamada "falhara"
for nome in pods:
    ok, motivo = escalar(nome, replicas, verificar_rollout, args.timeout)
    if ok:
        sucesso += 1
    else:
        falha += 1
        falharam.append((nome, motivo))

print(f"\nTotal: {sucesso} ok, {falha} falharam")

if falharam:
    print("\nPods que precisam ser verificados/subidos manualmente:")
    for nome, motivo in falharam:
        print(f"  - {nome}: {motivo}")