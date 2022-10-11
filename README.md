# Rasa Bot with neo4j

## Introduction

A simple Chinese weather robot (chatbot) built using Rasa technology stack (Rasa2.0, Rasa X, Slack) 

## Setup


1. clone project and install requirements

```bash
git clone https://github.com/fangjiegao/rasa_neo4j.git
cd rasa_neo4j
pip install -r requirements.txt
```


2. Train model by running:

   If you specify your project name in configure file, this will save your model at /models/your_project_name. 
   Otherwise, your model will be saved at /models/default

```
rasa train --num-threads 4
```
/Users/sherry/PycharmProjects/rasa-neo4j/rasa/__main__.py train --config config.yml --domain domain.yml --data data/
![-w1620](http://roger-markdown.oss-cn-beijing.aliyuncs.com/2020/12/26/16088726901168.jpg)

3. Run the raas action server:

```
rasa run actions
```
/Users/sherry/PycharmProjects/rasa-neo4j/rasa/__main__.py run --port 5005 --endpoints endpoints.yml --credentials credentials.yml --debug
/Users/sherry/PycharmProjects/rasa-neo4j/rasa/__main__.py run actions --port 5055 --actions actions --debug


4. Open a new terminal and now you can curl results from the server, for example:

```
rasa x
```

5. Connecting a bot to Slack

- [doc](https://rasa.com/docs/rasa/connectors/slack )

