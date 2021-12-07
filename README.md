# beancount-sjtu

Beancount Importer of jAccount API for E-card Transaction.

## Usage

### Get Data from jAccount API

```shell
# generate millisecond timestamp
$ export TIMESTAMP=$(date -d "2021-05-01" "+%s000")

# Generate URL
$ export URL="https://api.sjtu.edu.cn/v1/me/card/transactions?beginDate=${TIMESTAMP}"

# Get token after authenticated
$ export TOKEN=<TOKEN>

# Fetch data
$ curl -H "Authorization: Bearer $TOKEN" $URL > sample.json
```

### Generate Beancount File

```shell
$ bean-extract samples/config.py sample.json
```
