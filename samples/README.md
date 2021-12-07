# Samples

```json
{
    "dateTime": 1623835790000,
    "system": "闵二外档",
    "merchant": "新疆餐厅",
    "description": "持卡人消费",
    "amount": -18,
    "cardBalance": 1.68
}
```

```shell
$ bean-extract samples/config.py samples/sample.json
```

```beancount
2021-06-16 * "上海交通大学" "持卡人消费"
  merchant: "新疆餐厅"
  system: "闵二外档"
  time: "17:29:50"
  Assets:CN:SVC:SJTU       -18.00 CNY
  Expenses:SJTU:Cafeteria   18.00 CNY
```
