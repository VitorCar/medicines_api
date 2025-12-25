#  Padrão Oficial de Documentação – Medicines API

Este documento define o **padrão oficial de documentação** da *Medicines API*. Ele deve ser seguido por todos os endpoints, serializers e features do projeto, garantindo consistência, clareza e padrão profissional.

---

##  Objetivos da documentação

* Ser a **fonte única de verdade** da API
* Facilitar o consumo por Frontend, Mobile e QA
* Padronizar endpoints, respostas e erros
* Integrar **Swagger (OpenAPI)** e **Postman**
* Servir como referência de portfólio profissional

---

##  Arquitetura da Documentação

A documentação da Medicines API é composta por **três camadas complementares**:

1. **Swagger / OpenAPI (drf-spectacular)** → contrato oficial
2. **Postman Collection** → testes e exemplos reais
3. **README.md** → visão geral e onboarding

>  Regra de ouro: **Swagger é a fonte da verdade**. Postman é sempre gerado a partir dele.

---

##  Endpoints Base

```
Base URL: http://localhost:8000/api/v1/
Schema OpenAPI: /api/schema/
Swagger UI: /api/schema/swagger/
```

---

##  Autenticação

### Tipo

* JWT (JSON Web Token)

### Endpoints

```
POST /authentication/token/
POST /authentication/token/refresh/
POST /authentication/token/verify/
```

### Header padrão

```
Authorization: Bearer <token>
```

---

##  Padrão de Documentação dos Endpoints

Todo endpoint **OBRIGATORIAMENTE** deve conter:

* `@extend_schema` ou `@extend_schema_view`
* `tags`
* `description`
* `request` (quando aplicável)
* `responses`

### Exemplo (Retrieve / Update / Delete)

```python
@extend_schema_view(
    get=extend_schema(
        tags=['Manufacturers'],
        description='Retorna os dados de um fabricante específico',
        responses={200: ManufacturersSerializer}
    ),
    put=extend_schema(
        description='Atualiza todos os dados de um fabricante',
        request=ManufacturersSerializer,
        responses={200: ManufacturersSerializer}
    ),
    patch=extend_schema(
        description='Atualiza parcialmente os dados de um fabricante',
        request=ManufacturersSerializer,
        responses={200: ManufacturersSerializer}
    ),
    delete=extend_schema(
        description='Remove um fabricante do sistema',
        responses={204: None}
    ),
)
```

---

##  Padrão de Respostas HTTP

| Código | Significado               |
| ------ | ------------------------- |
| 200    | Sucesso (GET, PUT, PATCH) |
| 201    | Criado com sucesso        |
| 204    | Removido com sucesso      |
| 400    | Erro de validação         |
| 401    | Não autenticado           |
| 403    | Sem permissão             |
| 404    | Recurso não encontrado    |

---

##  Padrão de Erros

```json
{
  "detail": "Você não tem permissão para executar esta ação."
}
```

Erros de validação:

```json
{
  "field_name": ["Este campo é obrigatório."]
}
```

---

##  Endpoints Especiais (fora do CRUD)

Todo endpoint especial deve:

* Usar `@action` ou `APIView`
* Ser documentado com `@extend_schema`
* Ter descrição clara do retorno

### Exemplo: Estatísticas

```python
@extend_schema(
    tags=['Drugs'],
    description='Retorna estatísticas gerais dos medicamentos',
    responses={
        200: {
            'type': 'object',
            'properties': {
                'total': {'type': 'integer'},
                'with_prescription': {'type': 'integer'},
            }
        }
    }
)
```

---

##  Endpoints de IA (Gemini)

### Pharmacy Information

```
POST /ai/pharmacy/
```

Request:

```json
{
  "city": "São Paulo",
  "state": "SP"
}
```

### Medicine Leaflet

```
POST /ai/leaflet/
```

Request:

```json
{
  "remedy": "Dipirona"
}
```

---

##  Integração Swagger ↔ Postman

### Regra Oficial

* ❌ Nunca editar requests manualmente no Postman
* ✅ Sempre importar a partir do OpenAPI

### Processo

1. Atualizar código
2. Conferir Swagger
3. Reimportar Collection no Postman

---

##  Versionamento

* URLs versionadas (`/api/v1/`)
* Mudanças incompatíveis geram nova versão

---

##  Testes

* Testes automatizados (DRF APITestCase)
* Postman usado para testes manuais

---

##  Boas Práticas Obrigatórias

* Nomes claros e consistentes
* Descrições objetivas
* Responses sempre documentados
* Autenticação explícita
* Tags bem definidas

---

##  Conclusão

Este padrão garante que a **Medicines API** seja:

* Profissional
* Escalável
* Bem documentada
* Fácil de manter
* Pronta para consumo externo

>  Qualquer novo endpoint **deve seguir este documento**.
