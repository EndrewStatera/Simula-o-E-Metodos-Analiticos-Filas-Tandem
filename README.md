# Simulador de Redes de Filas (Tandem)

Simulador de redes de filas baseado em **Eventos Discretos (Discrete Event Simulation — DES)** desenvolvido em Python.

Permite modelar redes **G/G/c/K** com **roteamento probabilístico**, utilizando configuração externa via arquivos **YAML**.

---

## Pré-requisitos e Instalação

Antes de executar, garanta que você possui:

* **Python 3.x**
* Biblioteca **PyYAML**

### Instalação

```bash
pip install pyyaml
```

### Nota de Ambiente

> Em alguns sistemas (Linux/macOS), o `pip` pode apontar para Python 2.x.

Se houver erro, utilize:

```bash
pip3 install pyyaml
```

---

## Configuração da Rede (Arquivo YAML)

O simulador utiliza um arquivo YAML (por padrão: `entradas.yaml`) para definir toda a lógica da simulação.

### Estrutura do Arquivo

O arquivo deve conter:

* Parâmetros globais
* Definição das filas
* Regras de roteamento

### Exemplo básico

```yaml
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
```

---

## Execução da Simulação

Navegue até o diretório do projeto e escolha uma das opções:

### Execução Padrão

```bash
python fila_tandem.py
```

ou

```bash
python3 fila_tandem.py
```

---

### Execução com Arquivo Específico

```bash
python fila_tandem.py testes.yaml
```

ou

```bash
python3 fila_tandem.py testes.yaml
```

---

### Nota Importante

> Se o comando `python` não funcionar, utilize `python3` ou a versão específica instalada (ex: `python3.10`).

> Caso o arquivo YAML esteja mal formatado ou ausente, o simulador exibirá uma mensagem de erro sem interromper abruptamente a execução.

---

## Relatório de Saída

Ao final da simulação, será exibido um relatório contendo:

### Informações Globais

* Tempo total da simulação
* Quantidade de números aleatórios utilizados

---

### Estatísticas por Fila

Para cada fila, são apresentados:

* Número de clientes perdidos (overflow)
* Tempo acumulado em cada estado (0 até capacidade máxima)
* Probabilidade percentual de permanência em cada estado

---
