# MQTT Lab – Docker + Mosquitto + Python + Grafana

## Descrição

Uma arquitetura básica utilizando o protocolo MQTT para envio, assinatura e visualização de dados em tempo real utilizando Docker.

A aplicação simula métricas de monitoramento de infraestrutura, gerando dados periodicamente e enviando-os para um broker MQTT. O broker distribui as mensagens para clientes inscritos, enquanto o Grafana atua como assinante e exibe os dados em dashboards em tempo real.

Arquitetura utilizada:

## Tecnologias utilizadas

- **Docker / Docker Compose**
  - Orquestração e gerenciamento dos containers

- **Python**
  - Aplicação responsável pela geração e envio das mensagens

- **Eclipse Paho MQTT**
  - Biblioteca cliente MQTT utilizada pelo Publisher

- **Eclipse Mosquitto**
  - Broker MQTT responsável pelo gerenciamento das mensagens

- **Grafana**
  - Plataforma de visualização e monitoramento

---

## Funcionamento

A aplicação Publisher gera métricas simuladas relacionadas ao monitoramento de um servidor:

Exemplo de payload enviado:

```json
{
   "host":"servidor01",
   "latencia_ms":15,
   "throughput_mbps":180,
   "uso_cpu":43,
   "timestamp":"2026-07-06T01:20:00+00:00"
}
```

Esses dados são enviados para o tópico MQTT:

```text
lab/monitoramento/servidor01
```

O Mosquitto recebe as mensagens e distribui para todos os clientes inscritos.

O Grafana realiza a assinatura do tópico e exibe os dados em dashboards atualizados em tempo real.


## Executando o projeto

Construir e iniciar os containers:

```bash
docker compose up -d --build
```

Verificar containers ativos:

```bash
docker compose ps
```

Resultado esperado:

```text
NAME              STATUS

mqtt-broker       Up
mqtt-publisher    Up
grafana           Up
```


## Como testar no Grafana

Acessar:

```text
http://localhost:3000
```

Credenciais padrão:

```text
Usuário: admin
Senha: admin
```

### Criando dashboard

No menu lateral:

```text
Dashboards
     New Dashboard
     Add Visualization
```

Selecionar o datasource:

```text
MQTT
```

No campo Topic informar:

```text
lab/monitoramento/servidor01
```

## Resultado esperado

Após alguns segundos, o dashboard deverá exibir atualização contínua.

As informações serão atualizadas automaticamente conforme novas mensagens forem publicadas.


A interface do sistema está disponível apenas no Grafana:

```text
http://localhost:3000
```
