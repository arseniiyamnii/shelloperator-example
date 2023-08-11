#!/usr/bin/env bash

# данный хук следит за обновлениями конфигмапов. Когда конфигмап как либо обновляется - оператор находит деплойменты в которых используется
# этот конфигмап, и выполняет на них роллаут, чтобы новый конфигмап применился. Этот скрипт еще можно дополнять, но в целом с задачей
# справляется

if [[ $1 == "--config" ]] ; then
  cat <<EOF
configVersion: v1
kubernetes:
- apiVersion: v1
  kind: Configmap
  executeHookOnEvent: ["Added","Modified"]
EOF
else
  configName=$(jq -r .[0].object.metadata.name $BINDING_CONTEXT_PATH)
        echo $configName
	if [[ "${configName}" != "null" ]]; then
	deployment=$(kubectl get deployments.apps -o json | jq -r '.items[]|[{"name": .metadata.name,
	"volumes":.spec.template.spec.volumes[]?|select(.|has("configMap"))|.configMap.name|select(. == "'${configName}'")}]|.[].name'|  tr "\n" " ")
		if [[ $(echo "${deployment}" | sed '/^\s*$/d' | wc -l) -gt 0 ]]; then
			echo "Starting rollout for $deployment"
			kubectl rollout restart deployment $(echo $deployment)
		fi
	fi
fi
