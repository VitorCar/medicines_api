# Postman – Medicines API

Este diretório contém as collections oficiais da Medicines API.

##  Importação
1. Abra o Postman
2. Import → File
3. Selecione:
   - collections/medicines_api.postman_collection.json
   - environments/local.postman_environment.json

##  Sincronização
As collections são geradas a partir do Swagger (OpenAPI).

Sempre que um endpoint for alterado:
1. Atualize o código
2. Verifique o Swagger
3. Reimporte o schema no Postman
4. Exporte novamente a collection
