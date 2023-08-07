#!/usr/bin/env python3

# данных хук создан просто для изучения содержимого BINDING_CONTEXT_PATH
import sys
import os
import json

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--config":
        # обратите внимение - конфиг в формате словаря. Его возможно для удобства можно держать отдельным файлом и просто импортировать при
        # запуске
        config = {
                "configVersion": "v1",
                "kubernetes": [
                    {
                        "apiVersion": "v1",
                        "kind": "Pod",
                        "executeHookOnEvent": ["Added", "Modified"]
                        }
                    ]
                }
        json_config = json.dumps(config)
        print(json_config)
    else:
        # загоняем в try, так как при первом запуске создается неверный BINDING_CONTEXT_PATH, и в логах ошибка, что неприятно. Думаю это
        # можно отлавливать удобней чем конструкцией try, но как тестовый вариант покатит.
        try:
            print("OnStartup Python powered hook")
            # context = os.getenv('BINDING_CONTEXT_PATH')
            f = open(os.getenv('BINDING_CONTEXT_PATH'))
            data = json.load(f)
            print("RESULTS-------------")
            # print(len(data))
            # print(data[0].keys())
            # dict_keys(['binding', 'object', 'type', 'watchEvent'])
            if "object" in data[0]:
                print(data[0]["object"]["metadata"]["name"])
            # print(data[0]["watchEvent"])
            # print(data[1])
            print("END-------------")
        except:
            print("some fucking error")

