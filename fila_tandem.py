import random
import heapq

class StopSimulation(Exception):
    """Exceção usada para parar a simulação exatamente quando o limite de aleatórios for atingido."""
    pass

class ControladorRNG:
    """Gerenciador de números aleatórios para garantir o limite exato de consumo."""
    def __init__(self, limite=100000, seed=None):
        if seed is not None:
            random.seed(seed)
        self.limite = limite
        self.contador = 0

    def gerar(self):
        if self.contador >= self.limite:
            raise StopSimulation()
        self.contador += 1
        return random.random()

    def uniforme(self, a, b):
        u = self.gerar()
        return a + (b - a) * u

class Fila:
    """Representa um nó (uma fila) na rede de simulação."""
    def __init__(self, nome, servidores, capacidade, min_chegada=None, max_chegada=None, min_atend=0, max_atend=0):
        self.nome = nome
        self.servidores = servidores
        self.capacidade = capacidade
        
        # Parâmetros de distribuição Uniforme (G/G/...)
        self.min_chegada = min_chegada
        self.max_chegada = max_chegada
        self.min_atend = min_atend
        self.max_atend = max_atend
        
        # Variáveis de Estado
        self.estado = 0 # Número de clientes no sistema (fila + servidores)
        self.perdas = 0
        self.tempos_acumulados = {i: 0.0 for i in range(capacidade + 1)}

    

class SimuladorRede:
    def __init__(self, limite_aleatorios=100000, seed=None):
        self.rng = ControladorRNG(limite_aleatorios, seed)
        self.filas = {}
        self.roteamento = {} # Formato: { 'Origem': [('Destino', probabilidade), ...] }
        self.eventos = []    # Fila de prioridade (Min-Heap) para os eventos
        self.tempo_global = 0.0

    def adicionar_fila(self, fila):
        self.filas[fila.nome] = fila

    def configurar_roteamento(self, origem, destino, probabilidade):
        if origem not in self.roteamento:
            self.roteamento[origem] = []
        self.roteamento[origem].append((destino, probabilidade))

    def agendar_evento(self, tempo, tipo_evento, fila_nome, externa=False):
        # O heap do Python ordena pelo primeiro item da tupla (o tempo)
        heapq.heappush(self.eventos, (tempo, tipo_evento, fila_nome, externa))

    def atualizar_tempos(self, tempo_atual):
        """Atualiza a área sob a curva (tempo) em que cada fila permaneceu em seu estado atual."""
        delta = tempo_atual - self.tempo_global
        for fila in self.filas.values():
            fila.tempos_acumulados[fila.estado] += delta
        self.tempo_global = tempo_atual

    def processar_chegada(self, fila_nome, tempo_atual, externa):
        fila = self.filas[fila_nome]
        
        if fila.estado < fila.capacidade:
            fila.estado += 1
            # Se há servidor disponível, o cliente entra em atendimento e agenda sua saída
            if fila.estado <= fila.servidores:
                tempo_servico = self.rng.uniforme(fila.min_atend, fila.max_atend)
                self.agendar_evento(tempo_atual + tempo_servico, 'SAIDA', fila_nome)
        else:
            fila.perdas += 1

        # Se foi uma chegada externa, agenda a próxima chegada externa para esta fila
        if externa and fila.min_chegada is not None:
            tempo_chegada = self.rng.uniforme(fila.min_chegada, fila.max_chegada)
            self.agendar_evento(tempo_atual + tempo_chegada, 'CHEGADA', fila_nome, True)

    def processar_saida(self, fila_nome, tempo_atual):
        fila = self.filas[fila_nome]
        fila.estado -= 1

        # Se ainda há clientes na fila esperando, o servidor puxa o próximo
        if fila.estado >= fila.servidores:
            tempo_servico = self.rng.uniforme(fila.min_atend, fila.max_atend)
            self.agendar_evento(tempo_atual + tempo_servico, 'SAIDA', fila_nome)

        # Lógica de Roteamento na Rede
        if fila_nome in self.roteamento:
            u = self.rng.gerar()
            prob_acumulada = 0.0
            destino_escolhido = None
            
            for destino, prob in self.roteamento[fila_nome]:
                prob_acumulada += prob
                if u <= prob_acumulada:
                    destino_escolhido = destino
                    break
            
            # Se houver um destino, o cliente chega na próxima fila instantaneamente
            if destino_escolhido:
                self.processar_chegada(destino_escolhido, tempo_atual, externa=False)

    def executar(self, tempo_primeira_chegada, fila_primeira_chegada):
        # Agenda o start da simulação
        self.agendar_evento(tempo_primeira_chegada, 'CHEGADA', fila_primeira_chegada, externa=True)

        try:
            while self.eventos:
                tempo_atual, tipo_evento, fila_nome, externa = heapq.heappop(self.eventos)
                
                # Atualiza os estatísticas antes de mudar o estado
                self.atualizar_tempos(tempo_atual)

                if tipo_evento == 'CHEGADA':
                    self.processar_chegada(fila_nome, tempo_atual, externa)
                elif tipo_evento == 'SAIDA':
                    self.processar_saida(fila_nome, tempo_atual)
                    
        except StopSimulation:
            # A simulação para instantaneamente quando o 100.000º número é gerado
            pass

    def gerar_relatorio(self):
        print("="*50)
        print(" RELATÓRIO DA SIMULAÇÃO (REDE DE FILAS)")
        print("="*50)
        print(f"Tempo Global da Simulação: {self.tempo_global:.4f}")
        print(f"Números Aleatórios Consumidos: {self.rng.contador}\n")

        for nome, fila in self.filas.items():
            print(f"--- {nome} ---")
            print(f"Perdas de Clientes: {fila.perdas}")
            print("Estados | Tempo Acumulado | Probabilidade")
            print("-" * 43)
            
            for estado in range(fila.capacidade + 1):
                tempo_estado = fila.tempos_acumulados[estado]
                probabilidade = (tempo_estado / self.tempo_global) * 100 if self.tempo_global > 0 else 0
                print(f"  {estado:2d}    | {tempo_estado:15.4f} | {probabilidade:10.2f}%")
            print("\n")


# ==========================================
# CÓDIGO DE TESTE DO TRABALHO (VALIDAÇÃO)
# ==========================================
if __name__ == "__main__":
    # 1. Instancia o simulador informando a condição de parada (100.000 aleatórios)
    # A seed é opcional, mas deixamos sem para que seja aleatório a cada execução.
    simulador = SimuladorRede(limite_aleatorios=100000)

    # 2. Configura as filas (Nome, Servidores, Capacidade, MinChegada, MaxChegada, MinAtend, MaxAtend)
    # Fila 1 - G/G/2/3, chegadas entre 1..4, atendimento entre 3..4
    fila1 = Fila("Fila 1 (G/G/2/3)", servidores=2, capacidade=3, min_chegada=1, max_chegada=4, min_atend=3, max_atend=4)
    
    # Fila 2 - G/G/1/5, atendimento entre 2..3 (Sem chegadas externas, logo, Min/Max chegada são None)
    fila2 = Fila("Fila 2 (G/G/1/5)", servidores=1, capacidade=5, min_chegada=None, max_chegada=None, min_atend=2, max_atend=3)

    simulador.adicionar_fila(fila1)
    simulador.adicionar_fila(fila2)

    # 3. Configura o Roteamento (Tandem)
    # 100% (1.0) dos clientes que saem da Fila 1 vão para a Fila 2
    simulador.configurar_roteamento("Fila 1 (G/G/2/3)", "Fila 2 (G/G/1/5)", 1.0)

    # 4. Executa a simulação
    # O primeiro cliente chega no tempo 1.5 na Fila 1
    simulador.executar(tempo_primeira_chegada=1.5, fila_primeira_chegada="Fila 1 (G/G/2/3)")

    # 5. Imprime o Relatório Final
    simulador.gerar_relatorio()