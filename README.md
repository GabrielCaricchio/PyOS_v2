<div align="center">
  <h1>Trabalho de Sistemas Operacionais (SO)</h1>
  <h4>Professor: Filipe Araujo</h4>

  <table>
    <tr>
      <td align="center">
        <a href="https://github.com/FilipeHSAraujo">
          <img src="https://avatars.githubusercontent.com/u/84210747?v=4" width="100px;" alt="Filipe Araujo"/><br />
          <sub><b>Filipe Araujo</b></sub>
        </a>
      </td>
    </tr>
  </table>

  <h4>Turma: SI 3°P manhã</h4>
  <h4>Sistema: PyOS v2 (Simulador de SO feito com Python)</h4>
  <h4>Equipe:</h4>

  <table style="white-space: nowrap; display: inline-block; max-width: 100%; overflow-x: auto;">
    <tr>
      <td align="center" valign="top" style="min-width: 140px; max-width: 140px; padding: 10px;">
        <a href="https://github.com/Daniel-Willian-Silva">
          <img src="https://avatars.githubusercontent.com/u/229531037?v=4" width="100px;" alt="Daniel Willian da Silva"/><br />
          <sub><b>Daniel Willian da Silva</b></sub><br />
          <sub>Matrícula: 01831927</sub>
        </a>
      </td>
      <td align="center" valign="top" style="min-width: 140px; max-width: 140px; padding: 10px;">
        <a href="https://github.com/GabrielCaricchio">
          <img src="https://avatars.githubusercontent.com/u/235008081?v=4" width="100px;" alt="Gabriel Arruda Caricchio"/><br />
          <sub><b>Gabriel Arruda Caricchio</b></sub><br />
          <sub>Matrícula: 01824947</sub>
        </a>
      </td>
      <td align="center" valign="top" style="min-width: 140px; max-width: 140px; padding: 10px;">
        <a href="https://github.com/Ingrid-Motta06">
          <img src="https://avatars.githubusercontent.com/u/229673223?v=4" width="100px;" alt="Ingrid Motta Santos"/><br />
          <sub><b>Ingrid Motta Santos</b></sub><br />
          <sub>Matrícula: 01834701</sub>
        </a>
      </td>
      <td align="center" valign="top" style="min-width: 140px; max-width: 140px; padding: 10px;">
        <a href="https://github.com/marcosmatheus1828-dotcom">
          <img src="https://avatars.githubusercontent.com/u/228708069?v=4" width="100px;" alt="Marcos Matheus gomes Nerys"/><br />
          <sub><b>Marcos Matheus gomes Nerys</b></sub><br />
          <sub>Matrícula: 01779978</sub>
        </a>
      </td>
      <td align="center" valign="top" style="min-width: 140px; max-width: 140px; padding: 10px;">
        <a href="https://github.com/Subaru21-bot">
          <img src="https://avatars.githubusercontent.com/u/239859485?v=4" width="100px;" alt="Pedro Henrique Rodrigues da Silva"/><br />
          <sub><b>Pedro Henrique Rodrigues da Silva</b></sub><br />
          <sub>Matrícula: 01794091</sub>
        </a>
      </td>
    </tr>
  </table>
</div>

---

## 🚀 Como Executar

Certifique-se de ter o Python 3 instalado em sua máquina.

1.  Clone este repositório:
    ```bash
    git clone https://github.com/GabrielCaricchio/PyOS_v2.git
    ```
2.  Navegue até a pasta do projeto:
    ```bash
    cd PyOS_v2
    ```
3.  Execute o Kernel:
    ```bash
    python init.py
    ```
---

## 🛠️ Comandos do Shell (User Space)

Ao iniciar o PyOS v2, você terá acesso a um terminal interativo (`root@pyos:~#`):

| Comando | Descrição |
| :--- | :--- |
| `help` | Exibe a lista com todos os comandos disponíveis no simulador. |
| `spawn [nome]` | Cria um novo processo na RAM (gera um PID único). |
| `ps` | Lista todos os processos ativos e seus respectivos estados. |
| `cpu` | Executa 1 ciclo (tick) de clock no processador (Escalonador). |
| `run` | Executa continuamente os ciclos de clock até finalizar os processos. |
| `kill [PID]` | Encerra e remove o processo especificado da memória. |
| `block [PID]` | Bloqueia o processo (ex: simulando espera por uma operação de E/S). |
| `unblock [PID]` | Desbloqueia o processo, retornando-o para o estado de pronto. |
| `lock [recurso] [PID]` | Solicita ao Semáforo o acesso exclusivo do processo a um recurso. |
| `unlock [recurso] [PID]` | Libera o recurso bloqueado pelo processo para o uso de outros. |
| `fork [PID]` | Cria uma cópia exata (processo filho) a partir do PID informado. |
| `wait` | Faz o processo pai esperar até que o processo filho termine. |
| `send [PID] [mensagem]` | Envia uma mensagem via IPC (Comunicação Interprocessos) para o PID alvo. |
| `read [PID]` | Lê as mensagens recebidas na fila de IPC do processo especificado. |
| `clear` | Limpa a tela do terminal do simulador. |
| `exit` | Desliga e encerra a execução do simulador. |


---
<div>

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

---

</div>
