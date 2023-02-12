# zapy-simplified
## Ferramenta forense para a organização dos metadados do WhatsApp em planilha
- - - 
### Introdução

O WhatsApp fornece por e-mail os metadados das comunicações realizadas pelo app, em atendimento à ordem judicial de afastamento do sigilo telemático.

O programa lê o arquivo texto resultante da exportação desses e-mails pelo Outlook e organiza toda a informação numa planilha Excel para facilitar a análise pelo investigador. 

Também consulta a api do Ipapi (https://ipapi.com) para a obtenção de informações adicionais relacionadas aos IPs coletados, tais como 'hostname', 'latitude', 'longitude', 'cidade' e 'região'.

> O programa perguntará se você deseja restringir a consulta da API, para economizar o consumo.
