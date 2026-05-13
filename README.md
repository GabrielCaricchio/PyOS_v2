# 🟢 Nível 1 — Limite de Memória (OOM)
Objetivo

Impedir que o sistema aceite mais de 5 processos simultaneamente.

Lógica da solução

A tabela tabela_processos representa a RAM do sistema.
Basta verificar o tamanho dela antes de criar um novo processo.

Se já existirem 5 processos:

o kernel bloqueia a criação
exibe erro de memória
não instancia o PCB
Alteração principal

Na função spawn_process():

def spawn_process(nome):

    # Simulação de limite de RAM
    if len(tabela_processos) >= 5:
        print("[Kernel Panic] ERRO: Out of Memory (OOM)")
        return

    novo_processo = PCB(nome)
    tabela_processos.append(novo_processo)

    print(f"[Kernel] Processo '{nome}' criado com PID {novo_processo.pid}")

# 🟡 Nível 2 — Automador de Clock (run)
Objetivo

Criar um comando que execute automaticamente a CPU até todos os processos terminarem.

Lógica da solução

Hoje:

cada comando cpu executa apenas 1 tick

O run:

executa escalonador_tick() continuamente
para apenas quando não houver processos ativos

Isso simula:

clock do processador
timer interrupt automático
SO executando continuamente
Alteração principal

Adicionar no shell():

elif acao == "run":

    print("[Kernel] Iniciando execução automática...\n")

    while tabela_processos:
        escalonador_tick()
        time.sleep(0.5)

    print("\n[Kernel] Todos os processos finalizaram.")

Adicionar no help:

print("  run          - Executa a CPU continuamente")

# 🟡 Nível 3 — Gargalo de E/S (BLOQUEADO)
Objetivo

Adicionar estado BLOQUEADO.

Lógica da solução

Processos podem:

executar
esperar E/S (disco, teclado, impressora)
voltar para prontos

O escalonador NÃO deve executar processos bloqueados.

Alterações principais
Novos estados

No PCB:

self.estado = "PRONTO"

Estados possíveis:

PRONTO
EXECUTANDO
BLOQUEADO
TERMINADO
Escalonador ignora bloqueados

Alterar:

prontos = [p for p in tabela_processos if p.estado != "TERMINADO"]

Para:

prontos = [
    p for p in tabela_processos
    if p.estado == "PRONTO"
]
Comando block
elif acao == "block":

    if len(comando) > 1:

        alvo = int(comando[1])

        for p in tabela_processos:
            if p.pid == alvo:
                p.estado = "BLOQUEADO"
                print(f"[Kernel] PID {alvo} bloqueado aguardando E/S.")
Comando unblock
elif acao == "unblock":

    if len(comando) > 1:

        alvo = int(comando[1])

        for p in tabela_processos:
            if p.pid == alvo:
                p.estado = "PRONTO"
                print(f"[Kernel] PID {alvo} voltou para fila de prontos.")

# 🟠 Nível 4 — Prioridades
Objetivo

Executar primeiro processos mais importantes.

Lógica da solução

Cada processo recebe:

prioridade alta
média
baixa

O escalonador escolhe:

maior prioridade
depois Round Robin dentro da prioridade
Alteração no PCB
self.prioridade = random.randint(1, 3)

Exemplo:

1 = baixa
2 = média
3 = alta
Escalonador com prioridade

Antes:

processo_atual = prontos[0]

Depois:

prontos.sort(key=lambda p: p.prioridade, reverse=True)

processo_atual = prontos[0]
Mostrar prioridade no ps
print(f"{'PID':<6} | {'PRIO':<5} | {'NOME':<12}")

# 🔴 Nível 5 — Semáforos
Objetivo

Controlar acesso exclusivo a recurso compartilhado.

Lógica da solução

Somente:

1 processo por vez
pode usar a impressora

Semáforo:

1 → livre
0 → ocupado

Se ocupado:

processo entra em BLOQUEADO
Estrutura do recurso
impressora = {
    "livre": True,
    "pid": None
}
Comando lock
elif acao == "lock":

    alvo = int(comando[1])

    if impressora["livre"]:

        impressora["livre"] = False
        impressora["pid"] = alvo

        print(f"[Kernel] PID {alvo} adquiriu a impressora.")

    else:
        print("[Kernel] Impressora ocupada.")
Comando unlock
elif acao == "unlock":

    alvo = int(comando[1])

    if impressora["pid"] == alvo:

        impressora["livre"] = True
        impressora["pid"] = None

        print(f"[Kernel] PID {alvo} liberou a impressora.")

# 🔴 Nível 6 — Deadlock
Objetivo

Simular impasse entre processos.

Lógica da solução

Cenário clássico:

Processo A segura Impressora
Processo B segura Scanner
A quer Scanner
B quer Impressora

Nenhum avança.

Estrutura
scanner = {
    "livre": True,
    "pid": None
}
Simulação

PID 1000:

lock impressora

PID 1001:

lock scanner

Depois:

PID 1000 tenta scanner
PID 1001 tenta impressora

Ambos ficam BLOQUEADOS.

Detecção simples
if not impressora["livre"] and not scanner["livre"]:
    print("[Kernel Panic] DEADLOCK DETECTADO")

# 🟣 Nível 7 — Processos Zumbis
Objetivo

Processos terminados continuam na RAM.

Lógica da solução

Na vida real:

processo termina
mas PCB continua
aguardando processo pai chamar wait()

Isso gera:

ZUMBI
Alteração no término

Antes:

tabela_processos.remove(processo_atual)

Depois:

processo_atual.estado = "ZUMBI"
Comando wait
elif acao == "wait":

    tabela_processos = [
        p for p in tabela_processos
        if p.estado != "ZUMBI"
    ]

    print("[Kernel] Coleta de processos zumbis concluída.")

# 💀 Nível 8 — fork()
Objetivo

Clonar processos.

Lógica da solução

fork():

cria cópia do processo pai
mesmo contexto
novo PID
Comando fork
elif acao == "fork":

    alvo = int(comando[1])

    for p in tabela_processos:

        if p.pid == alvo:

            clone = PCB(p.nome + "_child")

            clone.ciclos_restantes = p.ciclos_restantes
            clone.estado = "PRONTO"

            tabela_processos.append(clone)

            print(f"[Kernel] Processo clonado.")

# 🔥 Nível Supremo — IPC (Comunicação entre Processos)
Objetivo

Permitir troca de mensagens entre processos.

Lógica da solução

Criar memória compartilhada:

um dicionário global
processos escrevem e leem mensagens
Estrutura IPC
ipc_memoria = {}
Comando send
elif acao == "send":

    pid = comando[1]
    mensagem = " ".join(comando[2:])

    ipc_memoria[pid] = mensagem

    print("[IPC] Mensagem enviada.")
Comando read
elif acao == "read":

    pid = comando[1]

    msg = ipc_memoria.get(pid)

    if msg:
        print(f"[IPC] Mensagem: {msg}")
    else:
        print("[IPC] Nenhuma mensagem.")