# Simula-o-E-Metodos-Analiticos-Filas-Tandem

Este projeto contém um simulador de redes de filas baseado em **Eventos Discretos (Discrete Event Simulation - DES)** desenvolvido em Python. Ele é capaz de modelar e simular redes genéricas de filas (G/G/c/K) com roteamento probabilístico.

O script foi projetado para parar a simulação exatamente após o consumo de um número predefinido de números pseudoaleatórios (ex: 100.000) e gerar um relatório estatístico detalhado de cada fila do sistema.

## 📋 Pré-requisitos

Para executar o simulador, você precisa apenas do **Python 3.x** instalado na sua máquina.
Nenhuma biblioteca externa (como `numpy` ou `pandas`) é necessária, pois o simulador utiliza apenas as bibliotecas padrão do Python (`random` e `heapq`).

## 🚀 Como executar

1. Faça o download ou clone o arquivo `fila_tandem.py` para o seu computador.
2. Abra o terminal (ou prompt de comando) e navegue até a pasta onde o arquivo foi salvo.
3. Execute o seguinte comando:

```bash
python fila_tandem.py
