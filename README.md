# Kubernetes for Finance Data Platform

## 1. About platform

- Finance Data Platform is build by Kubernetes with many opensource framework as Kafka, Druid, Airflow and MySQL.

## 2. Usage

- Firstly, install kubectl and helm

- Extract folder code and _cd_ to this folder

- Install Web-Administrator components:

```
# create namespace for Web-Administrator components
kubectl create namespace ns-webadmin

# install
helm install web-finance ./web-administrator/helm -n ns-webadmin
```

- Install Airflow components:

```
# create namespace for Airflow components
kubectl create namespace ns-airflow

# install
helm install airflow apache-airflow/airflow --values=./airflow/airflow-values.yaml -n ns airflow
```

- Install Druid components:

```
# create namespace for Druid components
kubectl create namespace ns-druid

# install
helm install druid ./druid -n ns-druid
```

- Install Kafka components:

```
# create namespace for Kafka components
kubectl create namespace ns-kafka

# install
helm install kafka bitnami/kafka --values=./kafka/kafka-values.yaml -n ns-kafka
```

- Install MySQL components:

```
# create namespace for MySQL components
kubectl create namespace ns-mysql

# install
helm install mysql bitnami/mysql --values=./mysql/values.yaml -n ns-mysql
```

## 3. Git resource

**https://github.com/tuantoquq/k8s-practice**
