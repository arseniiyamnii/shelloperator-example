FROM flant/shell-operator:v1.2.1
ADD hooks /hooks
RUN apk --no-cache add python3 py3-pip
RUN pip install kubernetes
