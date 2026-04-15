import random
import heapq
import sys
import yaml

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
            if fila.estado <= fila.servidores:
                tempo_servico = self.rng.uniforme(fila.min_atend, fila.max_atend)
                self.agendar_evento(tempo_atual + tempo_servico, 'SAIDA', fila_nome)
        else:
            fila.perdas += 1

        if externa and fila.min_chegada is not None:
            tempo_chegada = self.rng.uniforme(fila.min_chegada, fila.max_chegada)
            self.agendar_evento(tempo_atual + tempo_chegada, 'CHEGADA', fila_nome, True)

    def processar_saida(self, fila_nome, tempo_atual):
        fila = self.filas[fila_nome]
        fila.estado -= 1

        if fila.estado >= fila.servidores:
            tempo_servico = self.rng.uniforme(fila.min_atend, fila.max_atend)
            self.agendar_evento(tempo_atual + tempo_servico, 'SAIDA', fila_nome)

        if fila_nome in self.roteamento:
            u = self.rng.gerar()
            prob_acumulada = 0.0
            destino_escolhido = None
            
            for destino, prob in self.roteamento[fila_nome]:
                prob_acumulada += prob
                if u <= prob_acumulada:
                    destino_escolhido = destino
                    break
            
            if destino_escolhido:
                self.processar_chegada(destino_escolhido, tempo_atual, externa=False)

    def executar(self, tempo_primeira_chegada, fila_primeira_chegada):
        self.agendar_evento(tempo_primeira_chegada, 'CHEGADA', fila_primeira_chegada, externa=True)

        try:
            while self.eventos:
                tempo_atual, tipo_evento, fila_nome, externa = heapq.heappop(self.eventos)
                self.atualizar_tempos(tempo_atual)

                if tipo_evento == 'CHEGADA':
                    self.processar_chegada(fila_nome, tempo_atual, externa)
                elif tipo_evento == 'SAIDA':
                    self.processar_saida(fila_nome, tempo_atual)
                    
        except StopSimulation:
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
# CÓDIGO DE EXECUÇÃO VIA YAML
# ==========================================
def executar_de_yaml(caminho_arquivo):
    try:
        # Tenta abrir e ler o arquivo yaml
        with open(caminho_arquivo, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        
        # Verifica se as configurações básicas existem
        if not config or 'filas' not in config:
            raise ValueError("Parâmetros insuficientes")

        limite = config.get('limite_aleatorios', 100000)
        simulador = SimuladorRede(limite_aleatorios=limite)

        for f in config.get('filas', []):
            capacidade = float('inf') if str(f.get('capacidade')).lower() == 'inf' else f.get('capacidade')
            
            fila = Fila(
                nome=f['nome'],
                servidores=f['servidores'],
                capacidade=capacidade,
                min_chegada=f.get('chegada_min'),
                max_chegada=f.get('chegada_max'),
                min_atend=f.get('atendimento_min'),
                max_atend=f.get('atendimento_max')
            )
            simulador.adicionar_fila(fila)

        for r in config.get('roteamento', []):
            simulador.configurar_roteamento(r['origem'], r['destino'], r['probabilidade'])

        tempo_inicio = config.get('tempo_primeira_chegada', 1.5)
        fila_inicio = config.get('fila_primeira_chegada')

        print(f"🚀 Executando simulação a partir do arquivo: {caminho_arquivo}...\n")
        simulador.executar(tempo_primeira_chegada=tempo_inicio, fila_primeira_chegada=fila_inicio)
        simulador.gerar_relatorio()

    except (FileNotFoundError, yaml.YAMLError, ValueError, KeyError, TypeError):
        # Captura qualquer erro de arquivo não encontrado, YAML malformado ou campos faltando
        print(f"arquivo {caminho_arquivo} corrompido ou sem parâmetros para teste.")


if __name__ == "__main__":
    # Pega o arquivo passado por linha de comando ou assume 'entradas.yaml' como padrão
    arquivo_yaml = sys.argv[1] if len(sys.argv) > 1 else 'entradas.yaml'
    executar_de_yaml(arquivo_yaml)