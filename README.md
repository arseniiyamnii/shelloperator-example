# Shell operator example  
## how to deploy  
```bash
kubectl create configmap testscript --from-file=hooks/shell/ -o yaml --dry-run=client | kubectl apply -f -
```
```bash
kubectl apply -f shell-operator-pod.yaml
```
Create rbac
```bash
kubectl create serviceaccount monitor-pods-acc
kubectl create clusterrole monitor-operator --verb=get,watch,list,patch --resource=deployments,configmaps
kubectl create clusterrolebinding monitor-operator --clusterrole=monitor-operator --serviceaccount=vavada-dev:monitor-pods-acc
```

For using with python change image inside deployment to image builded from Dockerfile, and apply hooks from python dirrectory

## Как это работает 

Сперва оператор вызывает хук, и получает конфигурацию того, когда хук будет срабоатывать. В документации по шел оператору можно найти
варианты этой конфигурации. Там ничего сложного. Вот так вот выглядит конфигурация:
```bash
if [[ $1 == "--config" ]] ; then
  cat <<EOF
configVersion: v1
kubernetes:
- apiVersion: v1
  kind: Configmap
  executeHookOnEvent: ["Added","Modified"]
EOF
```

Далее когда условие из конфигурации срабатывает, создается файл, путь к которому лежит в переемнной окружения
$BINDING_CONTEXT_PATH. В этой переменной окружения находятся путь к состояния объектов, что изменилось и так далее. Парся этот файл мы можем что
либо делать с объектами. Главное rbac правильно выставлять не забывать
В одном поде оператора могут находится сразу несколько хуков
todo: научится запускать хуки в несколько потоков, чтобы повышать устойчивость оператора к переездам. Скорее всего это удобней всего сделать
с помощью каких то временных конфигмапов которыми разные поды будут синхронизировать данные о работе, чтобы не дублировать действия

В отличие от инструкции из документации к оператору, мы используем конфигмапы для доставки хуков в оператор, а не кастомный докерфайл. За
счет этого проще деплоить новые хуки
Использование crd тут довольно таки простое. Просто деплоим crd и cr, и следим за состоянием cr. В зависимости от состояния выполняем
действия. Для удобства можно на разные действия создать разные хуки
Это все легко отрабатывает внутри minikube. Можно прост задеплоить, и посмотреть как работает. Чтобы увидеть что все работает, можно
задеплоить оператор с shell скриптами, и попробовать немного поменять скрипт(добавить комент). Оператор должен запустить reload на самого
себя, чтобы обновить конфигмап в поде
При использовании оператора с python, в нем также будут работать и shell скрипты, так что моджно удобно экспериментировать с оператором
