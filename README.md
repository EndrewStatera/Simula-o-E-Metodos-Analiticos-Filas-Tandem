# Simulador de Redes de Filas (Tandem)

Este projeto contém um simulador de redes de filas baseado em **Eventos Discretos (Discrete Event Simulation - DES)** desenvolvido em Python. Ele é capaz de modelar e simular redes genéricas de filas (G/G/c/K) com roteamento probabilístico.

A configuração da topologia da rede, tempos de chegada, tempos de atendimento e regras de roteamento é feita externamente através de arquivos de configuração em formato **YAML**.

## 📋 Pré-requisitos e Instalação

Para executar este simulador, você precisará do **Python 3.x** instalado na sua máquina e da biblioteca `PyYAML` para que o script consiga ler os arquivos de configuração.

Abra o seu terminal (ou prompt de comando) e instale a dependência executando:

```bash
pip install pyyaml
Nota de Ambiente: Dependendo do seu sistema operacional (especialmente em distribuições Linux ou no macOS), o comando pip pode estar associado à versão antiga do Python (2.x). Se o comando acima falhar ou disser que o pacote já está instalado mas o script não rodar, utilize explicitamente o instalador do Python 3:

pip3 install pyyaml
Como configurar a rede (Arquivo YAML)
O simulador lê os parâmetros da simulação através de um arquivo YAML. O arquivo padrão procurado pelo sistema é o entradas.yaml.

O arquivo deve conter:

Parâmetros globais (limite de aleatórios e tempo de início).

A lista de filas e suas capacidades/servidores.

A lista de roteamento (probabilidades de transição entre filas).

Exemplo de estrutura (veja o arquivo entradas.yaml para o formato completo):

YAML
limite_aleatorios: 100000
tempo_primeira_chegada: 1.5
fila_primeira_chegada: "Fila 1"

filas:
  - nome: "Fila 1"
    servidores: 2
    capacidade: 3
    chegada_min: 1.0
    chegada_max: 4.0
    atendimento_min: 3.0
    atendimento_max: 4.0
# ...
Como executar a Simulação
Navegue pelo terminal até a pasta onde os arquivos estão localizados e escolha uma das opções abaixo:

Aviso Importante sobre o Comando Python: > Assim como no comando pip, alguns sistemas exigem que você digite python3 em vez de apenas python. Se ao rodar os comandos abaixo você receber um erro de sintaxe ou a mensagem "comando não encontrado", substitua python por python3 (ou a versão específica instalada, como python3.10).

Opção 1: Execução Padrão

Se você quiser rodar o teste principal, basta executar o script sem nenhum argumento. Ele lerá automaticamente o arquivo entradas.yaml presente na mesma pasta.

Bash
python fila_tandem.py
# ou
python3 fila_tandem.py
Opção 2: Execução com Testes Específicos (Professor)

Bash
python fila_tandem.py testes.yaml
# ou
python3 fila_tandem.py testes.yaml
Nota: Se o arquivo estiver mal formatado ou não for encontrado, o simulador informará o erro sem quebrar a execução de forma abrupta.

📊 Relatório de Saída
Ao final da execução, o terminal exibirá um relatório contendo:

O tempo global total da simulação.

O número exato de números aleatórios consumidos.

Estatísticas por Fila:

Número de clientes perdidos (quando a capacidade estoura).

O tempo acumulado que a fila permaneceu em cada estado (de 0 até a capacidade máxima).

A probabilidade percentual (tempo de permanência) de cada estado.