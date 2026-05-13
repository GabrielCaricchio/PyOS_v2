# ==========================================
# IMPORTS
# ==========================================

import time
import random
import sys

# ==========================================
# ESTRUTURAS DO KERNEL
# ==========================================

tabela_processos = []
pid_counter = 1000

# IPC (Memória Compartilhada)
ipc_memoria = {}

# Recursos compartilhados
impressora = {
    "livre": True,
    "pid": None
}

scanner = {
    "livre": True,
    "pid": None
}

#===========================================
# LOGO PyOS
#===========================================
def logo_pyos():
    # --- DEFINIÇÃO DE CORES ---
    # Esses códigos estranhos são "Escapes ANSI". O terminal os lê como instruções de cor, 
    # em vez de texto comum. \033[ inicia o comando, o número define a cor.
    VERDE = "\033[1;32m"   # 1 deixa em negrito, 32 é o código para verde
    BRANCO = "\033[1;37m"  # 37 é o código para branco
    RESET = "\033[0m"      # O código 0 diz ao terminal para voltar à cor padrão (branco ou cinza)

    # --- O DESENHO (ASCII ART) ---
    # O 'r' antes das aspas significa 'raw' (cru). Ele impede que o Python tente 
    # interpretar as barras invertidas (\) como comandos, tratando tudo como desenho.
    logo = r"""
     ____         ___   ____ 
    |  _ \ _   _ / _ \ / ___|
    | |_) | | | | | | |\___ \
    |  __/| |_| | |_| | ___) |
    |_|    \__, |\___/ |____/ 
           |___/             
              
               ____          ____
              /    \________/    \
             |  /\    PYOS      /\  |
             | |  |   V2.0     |  | |
             |  \/____    _____\/  /
              \______ \  / _______/
                     \ \/ /
                      \  /
                       \/
    """

    # --- EXIBIÇÃO DO LOGO ---
    print(VERDE) # Aplica a cor verde no terminal para tudo o que vier abaixo
    
    # logo.splitlines() pega o texto gigante e o corta em uma lista de linhas individuais.
    # O laço 'for' pega uma linha por vez dessa lista para processar.
    for linha in logo.splitlines():
        print(linha) # Imprime a linha atual
        # time.sleep(0.1) faz o programa "dormir" por 0.1 segundos antes de ir para a próxima linha.
        # Isso cria a ilusão de que o sistema está carregando a imagem de baixo para cima.
        time.sleep(0.1) 

    # --- EFEITO DE DIGITAÇÃO ---
    mensagem = "\n >> Iniciando Sistema..."
    
    # sys.stdout.write funciona como o print, mas não pula linha automaticamente no final.
    sys.stdout.write(BRANCO) # Muda a cor do pincel para branco
    
    # Aqui, o 'for' percorre cada LETRA da mensagem, uma por uma.
    for letra in mensagem:
        sys.stdout.write(letra) # Escreve a letra atual na tela
        
        # O comando flush() é crucial: por padrão, o computador guarda o texto na memória 
        # e só joga na tela quando enche um "balde". O flush força o balde a esvaziar NA HORA,
        # garantindo que a letra apareça instantaneamente conforme o loop roda.
        sys.stdout.flush() 
        
        time.sleep(0.04) # Pausa curtíssima para simular alguém digitando rápido
    
    # No final, imprimimos o RESET para que o comando seguinte do usuário não saia colorido.
    print(RESET + "\n")

# ==========================================
# PCB
# ==========================================

class PCB:
    """Process Control Block"""

    def __init__(self, nome):

        global pid_counter

        self.pid = pid_counter
        self.nome = nome

        # Estados:
        # PRONTO
        # EXECUTANDO
        # BLOQUEADO
        # ZUMBI
        self.estado = "PRONTO"

        self.ciclos_restantes = random.randint(2, 6)

        # Prioridade:
        # 1 = baixa
        # 2 = média
        # 3 = alta
        self.prioridade = random.randint(1, 3)

        pid_counter += 1

# ==========================================
# BOOT
# ==========================================

def boot():

    print("Iniciando PyOS Kernel v2.0...")
    time.sleep(1)

    print("Carregando módulos de memória [OK]")
    time.sleep(0.5)

    print("Iniciando escalonador [OK]")
    time.sleep(0.5)

    print("Inicializando IPC [OK]")
    time.sleep(0.5)

    print("Montando sistema de arquivos [OK]")
    time.sleep(0.5)

    print("\nBem-vindo ao PyOS.")
    print("Digite 'help' para ver os comandos.\n")

# ==========================================
# PROCESSOS
# ==========================================

def spawn_process(nome):

    # Nível 1 — Limite de memória
    ativos = [
        p for p in tabela_processos
        if p.estado != "ZUMBI"
    ]

    if len(ativos) >= 5:
        print("[Kernel Panic] ERRO: Out of Memory (OOM)")
        return

    novo = PCB(nome)

    tabela_processos.append(novo)

    print(
        f"[Kernel] Processo '{nome}' criado "
        f"com PID {novo.pid} "
        f"(Prioridade {novo.prioridade})"
    )

# ==========================================
# ESCALONADOR
# ==========================================

def escalonador_tick():

    # Apenas processos PRONTOS
    prontos = [
        p for p in tabela_processos
        if p.estado == "PRONTO"
    ]

    if not prontos:
        print("[CPU] Ociosa. Nenhum processo pronto.")
        return

    # Nível 4 — Prioridades
    prontos.sort(
        key=lambda p: p.prioridade,
        reverse=True
    )

    processo_atual = prontos[0]

    # EXECUTANDO
    processo_atual.estado = "EXECUTANDO"

    print(
        f"\n[CPU] Executando "
        f"PID {processo_atual.pid} "
        f"({processo_atual.nome}) "
        f"[PRIO {processo_atual.prioridade}]"
    )

    time.sleep(1)

    processo_atual.ciclos_restantes -= 1

    # Processo terminou
    if processo_atual.ciclos_restantes <= 0:

        # Nível 7 — Processo zumbi
        processo_atual.estado = "ZUMBI"

        print(
            f"[Kernel] PID {processo_atual.pid} terminou "
            f"e virou ZUMBI."
        )

    else:

        # Volta para fila
        processo_atual.estado = "PRONTO"

        tabela_processos.remove(processo_atual)
        tabela_processos.append(processo_atual)

        print(
            f"[Kernel] Chaveamento de contexto. "
            f"PID {processo_atual.pid} voltou para fila."
        )

# ==========================================
# DEADLOCK
# ==========================================

def verificar_deadlock():

    if (
        not impressora["livre"]
        and
        not scanner["livre"]
    ):

        print("\n[Kernel Panic] DEADLOCK DETECTADO")
        print(
            f"Impressora -> PID {impressora['pid']}"
        )
        print(
            f"Scanner -> PID {scanner['pid']}"
        )

# ==========================================
# SHELL
# ==========================================

def shell():

    global tabela_processos

    while True:

        try:

            comando = input(
                "root@pyos:~# "
            ).strip().split()

            if not comando:
                continue

            acao = comando[0].lower()

            # ==================================
            # EXIT
            # ==================================

            if acao == "exit":

                print("Desligando sistema...")
                break

            # ==================================
            # HELP
            # ==================================

            elif acao == "help":

                print("\nComandos disponíveis:\n")

                print("spawn [nome]")
                print("ps")
                print("cpu")
                print("run")

                print("kill [PID]")

                print("block [PID]")
                print("unblock [PID]")

                print("lock [recurso] [PID]")
                print("unlock [recurso] [PID]")

                print("fork [PID]")

                print("wait")

                print("send [PID] [mensagem]")
                print("read [PID]")

                print("clear")
                print("exit\n")

            # ==================================
            # CLEAR
            # ==================================

            elif acao == "clear":

                print("\033[H\033[J", end="")

            # ==================================
            # SPAWN
            # ==================================

            elif acao == "spawn":

                if len(comando) > 1:

                    spawn_process(comando[1])

                else:
                    print(
                        "Uso correto: spawn [nome]"
                    )

            # ==================================
            # PS
            # ==================================

            elif acao == "ps":

                print(
                    f"\n{'PID':<6} | "
                    f"{'PRIO':<5} | "
                    f"{'NOME':<15} | "
                    f"{'ESTADO':<12} | "
                    f"CICLOS"
                )

                print("-" * 65)

                for p in tabela_processos:

                    print(
                        f"{p.pid:<6} | "
                        f"{p.prioridade:<5} | "
                        f"{p.nome[:15]:<15} | "
                        f"{p.estado:<12} | "
                        f"{p.ciclos_restantes}"
                    )

                if not tabela_processos:
                    print("Nenhum processo.")

            # ==================================
            # CPU
            # ==================================

            elif acao == "cpu":

                escalonador_tick()

            # ==================================
            # RUN
            # ==================================

            elif acao == "run":

                print(
                    "\n[Kernel] Execução automática iniciada.\n"
                )

                while True:

                    ativos = [
                        p for p in tabela_processos
                        if p.estado != "ZUMBI"
                    ]

                    if not ativos:
                        break

                    escalonador_tick()

                    time.sleep(0.5)

                print(
                    "\n[Kernel] Todos os processos terminaram."
                )

            # ==================================
            # KILL
            # ==================================

            elif acao == "kill":

                if len(comando) > 1:

                    try:

                        alvo = int(comando[1])

                        tabela_processos = [
                            p for p in tabela_processos
                            if p.pid != alvo
                        ]

                        print(
                            f"[Kernel] PID {alvo} destruído."
                        )

                    except ValueError:

                        print("PID inválido.")

                else:

                    print(
                        "Uso correto: kill [PID]"
                    )

            # ==================================
            # BLOCK
            # ==================================

            elif acao == "block":

                if len(comando) > 1:

                    alvo = int(comando[1])

                    for p in tabela_processos:

                        if p.pid == alvo:

                            p.estado = "BLOQUEADO"

                            print(
                                f"[Kernel] PID {alvo} "
                                f"bloqueado."
                            )

            # ==================================
            # UNBLOCK
            # ==================================

            elif acao == "unblock":

                if len(comando) > 1:

                    alvo = int(comando[1])

                    for p in tabela_processos:

                        if p.pid == alvo:

                            p.estado = "PRONTO"

                            print(
                                f"[Kernel] PID {alvo} "
                                f"desbloqueado."
                            )

            # ==================================
            # LOCK
            # ==================================

            elif acao == "lock":

                if len(comando) < 3:

                    print(
                        "Uso: lock [recurso] [PID]"
                    )

                    continue

                recurso = comando[1]
                pid = int(comando[2])

                alvo = None

                for p in tabela_processos:

                    if p.pid == pid:
                        alvo = p
                        break

                if not alvo:
                    print("PID não encontrado.")
                    continue

                # IMPRESSORA
                if recurso == "impressora":

                    if impressora["livre"]:

                        impressora["livre"] = False
                        impressora["pid"] = pid

                        print(
                            f"[Kernel] PID {pid} "
                            f"adquiriu IMPRESSORA."
                        )

                    else:

                        alvo.estado = "BLOQUEADO"

                        print(
                            f"[Kernel] Impressora ocupada. "
                            f"PID {pid} bloqueado."
                        )

                # SCANNER
                elif recurso == "scanner":

                    if scanner["livre"]:

                        scanner["livre"] = False
                        scanner["pid"] = pid

                        print(
                            f"[Kernel] PID {pid} "
                            f"adquiriu SCANNER."
                        )

                    else:

                        alvo.estado = "BLOQUEADO"

                        print(
                            f"[Kernel] Scanner ocupado. "
                            f"PID {pid} bloqueado."
                        )

                verificar_deadlock()

            # ==================================
            # UNLOCK
            # ==================================

            elif acao == "unlock":

                if len(comando) < 3:

                    print(
                        "Uso: unlock [recurso] [PID]"
                    )

                    continue

                recurso = comando[1]
                pid = int(comando[2])

                if recurso == "impressora":

                    if impressora["pid"] == pid:

                        impressora["livre"] = True
                        impressora["pid"] = None

                        print(
                            f"[Kernel] Impressora liberada."
                        )

                elif recurso == "scanner":

                    if scanner["pid"] == pid:

                        scanner["livre"] = True
                        scanner["pid"] = None

                        print(
                            f"[Kernel] Scanner liberado."
                        )

            # ==================================
            # WAIT
            # ==================================

            elif acao == "wait":

                tabela_processos = [
                    p for p in tabela_processos
                    if p.estado != "ZUMBI"
                ]

                print(
                    "[Kernel] Processos zumbis removidos."
                )

            # ==================================
            # FORK
            # ==================================

            elif acao == "fork":

                if len(comando) > 1:

                    alvo_pid = int(comando[1])

                    for p in tabela_processos:

                        if p.pid == alvo_pid:

                            clone = PCB(
                                p.nome + "_child"
                            )

                            clone.estado = "PRONTO"

                            clone.ciclos_restantes = (
                                p.ciclos_restantes
                            )

                            clone.prioridade = (
                                p.prioridade
                            )

                            tabela_processos.append(clone)

                            print(
                                f"[Kernel] PID {p.pid} "
                                f"clonado -> "
                                f"novo PID {clone.pid}"
                            )

                            break

            # ==================================
            # SEND
            # ==================================

            elif acao == "send":

                if len(comando) >= 3:

                    pid = comando[1]

                    mensagem = " ".join(
                        comando[2:]
                    )

                    ipc_memoria[pid] = mensagem

                    print(
                        f"[IPC] Mensagem enviada "
                        f"para PID {pid}"
                    )

                else:

                    print(
                        "Uso: send [PID] [mensagem]"
                    )

            # ==================================
            # READ
            # ==================================

            elif acao == "read":

                if len(comando) > 1:

                    pid = comando[1]

                    mensagem = ipc_memoria.get(pid)

                    if mensagem:

                        print(
                            f"[IPC] PID {pid}: "
                            f"{mensagem}"
                        )

                    else:

                        print(
                            "[IPC] Nenhuma mensagem."
                        )

            # ==================================
            # COMANDO INVÁLIDO
            # ==================================

            else:

                print(
                    f"bash: {acao}: "
                    f"comando não encontrado."
                )

        except KeyboardInterrupt:

            print(
                "\nUse 'exit' para desligar."
            )

        except ValueError:

            print(
                "Erro: valor inválido."
            )

# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":
    logo_pyos()
    boot()
    shell()