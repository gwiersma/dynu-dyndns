FROM python:3

WORKDIR /usr/src/app

ENV API_URL=api \
    API_KEY=key \
    DOMAIN_URL=domain
    

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY updateIpDNS.py ./ 

CMD [ "python", "./updateIpDNS.py -s ${API_URL} -t ${API_KEY} -d ${DOMAIN_URL}"]
