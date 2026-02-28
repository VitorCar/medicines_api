# 💊 Medicines API

[![CI – Medicines API (Docker)](https://github.com/VitorCar/medicines_api/actions/workflows/ci.yml/badge.svg)](https://github.com/VitorCar/medicines_api/actions/workflows/ci.yml)

API RESTful para gerenciamento completo de **medicamentos**, desenvolvida com **Django**, **Django Rest Framework (DRF)** e boas práticas profissionais de backend.

Este projeto foi pensado como **API de nível mercado**, com autenticação JWT, versionamento, documentação completa e integração com ferramentas modernas.

---

## 🚀 Tecnologias Utilizadas

* Python 3
* Django
* Django Rest Framework (DRF)
* Simple JWT
* Gemini
* drf-spectacular (Swagger / OpenAPI)
* Docker & Docker Compose
* MySQL
* GitHub Actions (CI/CD)
* Postman
* MkDocs (Documentação)

---

## 🧠 Conceito do Projeto

A **Medicines API** centraliza informações detalhadas sobre medicamentos, incluindo:

* Tipos de medicamentos (Referência, Genérico, Similar)
* Formas farmacêuticas
* Vias de administração
* Fabricantes
* Identificação completa do medicamento
* Integração com IA (Gemini) para:

  * Informações de farmácias
  * Consulta de bula
* Geração de PDF de bula via comando Django

---

## 🌐 Versionamento da API

```
Base URL: http://localhost:8000/api/v1/
```

Toda evolução incompatível da API gera uma nova versão (`v2`, `v3`, etc.).

---

## 🔐 Autenticação

A API utiliza **JWT (JSON Web Token)**.

### Endpoints

```
POST /authentication/token/
POST /authentication/token/refresh/
POST /authentication/token/verify/
```

### Header obrigatório

```http
Authorization: Bearer <token>
```


---

## 📘 Documentação Oficial

A documentação do projeto é composta por **três camadas complementares**:

### 1️⃣ Swagger / OpenAPI (Contrato da API)

* Swagger UI: `http://localhost:8000/api/schema/swagger/`
* Schema OpenAPI: `http://localhost:8000/api/schema/`

➡️ **Swagger é a fonte única da verdade da API**. Todos os endpoints são documentados usando `@extend_schema`.

---

### 2️⃣ Postman (Testes e Uso Prático)

O projeto disponibiliza uma **collection oficial do Postman**, sempre sincronizada com o Swagger.

📁 Local no projeto:

```
postman/
├── collections/
│   └── medicines_api.postman_collection.json
├── environments/
│   └── local.postman_environment.json
└── README.md
```

#### Como usar

1. Importar a collection no Postman
2. Importar o environment
3. Autenticar via JWT
4. Testar endpoints

➡️ **Nunca editar requests manualmente**. A collection é sempre gerada a partir do OpenAPI.

---

### 3️⃣ MkDocs (Documentação Explicativa)

A documentação detalhada e explicativa do projeto está disponível via **MkDocs**.

#### Rodar localmente

```bash
mkdocs serve
```

Acesse:

```
http://127.0.0.1:8001
```

O MkDocs contém:

* Visão geral da API
* Padrão oficial de documentação
* Autenticação
* Endpoints organizados por domínio
* Integração com Swagger e Postman

---

## 📐 Padrão Oficial de Documentação

O projeto segue um **padrão oficial de documentação**, garantindo consistência e qualidade.

Regras principais:

* Swagger é a fonte da verdade
* Todo endpoint deve usar `@extend_schema`
* Responses HTTP sempre documentados
* Postman sempre sincronizado com OpenAPI

📘 Documento completo disponível no MkDocs.

---

## 📊 Endpoints Principais

| Recurso                  | Endpoint           |
| ------------------------ | ------------------ |
| Manufacturers            | `/manufacturers/`  |
| Pharmaceutical Forms     | `/pharmaceutical/` |
| Routes of Administration | `/administration/` |
| Drug Identification      | `/drug/`           |
| Estatísticas             | `/drug/stats/`     |
| IA – Farmácias           | `/ai/pharmacy/`    |
| IA – Bula                | `/ai/leaflet/`     |

---

## 🤖 Integração com IA (Google Gemini)

A **Medicines API** conta com integração com **IA generativa (Google Gemini)** para fornecer informações inteligentes e contextualizadas, indo além de um simples CRUD.

Essa integração foi projetada como um **serviço complementar**, desacoplado do domínio principal da API, seguindo boas práticas de arquitetura.

---

### 🎯 Objetivos da Integração com IA

* Enriquecer a experiência do usuário
* Automatizar consultas textuais complexas
* Demonstrar uso real de IA em APIs REST
* Tornar a API mais inteligente e contextual

---

### 🏥 Endpoint: Informações de Farmácias

```
POST /api/v1/ai/pharmacy/
```

#### Descrição

Retorna uma lista de **farmácias** com base na cidade e estado informados pelo usuário, utilizando IA para gerar respostas contextualizadas.

#### Request

```json
{
  "city": "São Paulo",
  "state": "SP"
}
```

#### Response (exemplo)

```json
{
  "pharmacies": [
    "Farmácia Central – Centro",
    "Drogaria Saúde Total",
    "Farmácia Popular Paulista",
    "Rede Vida Farma",
    "Drogaria Bem Estar"
  ]
}
```

---

### 💊 Endpoint: Consulta de Bula de Medicamento

```
POST /api/v1/ai/leaflet/
```

#### Descrição

Retorna um **resumo estruturado da bula** de um medicamento informado pelo usuário, utilizando IA generativa.

As informações incluem:

* Indicações
* Contraindicações
* Reações adversas
* Precauções

#### Request

```json
{
  "remedy": "Dipirona"
}
```

#### Response (exemplo)

```json
{
  "name": "Dipirona",
  "indications": "Alívio da dor e redução da febre",
  "contraindications": "Hipersensibilidade à dipirona",
  "adverse_reactions": "Náusea, tontura",
  "precautions": "Evitar uso prolongado sem orientação médica"
}
```

---

### 🧠 Arquitetura da Integração com IA

* A IA **não altera dados persistidos** no banco
* Atua apenas como **serviço de consulta**
* Comunicação via serviço dedicado
* Isolada do domínio principal (medicamentos)

Fluxo simplificado:

```
User → API → Serviço de IA (Gemini) → API → User
```

---

### 🔐 Segurança e Boas Práticas

* Endpoints protegidos por autenticação JWT
* Prompts controlados e sanitizados
* Nenhuma informação sensível do usuário é armazenada
* Arquitetura preparada para troca de provedor de IA

---

---|--------|
| Manufacturers | `/manufacturers/` |
| Pharmaceutical Forms | `/pharmaceutical/` |
| Routes of Administration | `/administration/` |
| Drug Identification | `/drug/` |
| Estatísticas | `/drug/stats/` |
| IA – Farmácias | `/ai/pharmacy/` |
| IA – Bula | `/ai/leaflet/` |

---

## 🧪 Testes

* Testes automatizados com `APITestCase`
* Testes manuais via Postman

---

## 🛠️ Comandos Customizados

### Listar medicamentos cadastrados

```bash
python manage.py get_id
```

### Gerar PDF da bula

```bash
python manage.py export <id_do_medicamento>
```

---

## 🐳 Docker (Execução Profissional)

Este projeto utiliza **Docker** para garantir:

* Ambiente padronizado
* Facilidade de execução em qualquer máquina
* Isolamento de dependências
* Integração automática com MySQL

### 📦 Containers utilizados

* **medicines_api_web** → Django + DRF
* **medicines_api_db** → MySQL

---

### ▶️ Como rodar o projeto com Docker

#### 1️⃣ Clonar o repositório

```bash
git clone https://github.com/seu-usuario/medicines_api.git
cd medicines_api
```

---

#### 2️⃣ Criar arquivo `.env`

Crie um arquivo `.env` baseado no exemplo:

```bash
cp .env.example .env
```

Edite se necessário:

```env
GEMINI_API_KEY=CHANGE-ME
SECRET_KEY=django-insecure-change-this-key
DEBUG=1
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=medicines_api
DB_USER=mysql
DB_PASSWORD=mysql
DB_HOST=medicines_api_db
DB_PORT=3306
```

---

#### 3️⃣ Subir os containers

```bash
docker-compose up --build
```

A API ficará disponível em:

```
http://localhost:8000
```

---

### 🧪 Comandos Django (via Docker)

Todos os comandos Django devem ser executados **via container**:

```bash
docker-compose run medicines_api_web python manage.py migrate
```

```bash
docker-compose run medicines_api_web python manage.py createsuperuser
```

```bash
docker-compose run medicines_api_web python manage.py makemigrations
```

---

⚠️ **Regra importante**

> Em projetos dockerizados, **não utilize **``** localmente**. O Docker é a fonte da verdade do ambiente.

---

## 🔄 Integração Contínua (CI)

Este projeto utiliza GitHub Actions para Integração Contínua (CI), garantindo qualidade e estabilidade do código.

A cada push ou pull request para a branch main, o pipeline executa automaticamente:

Build da aplicação via Docker

Subida dos serviços com docker-compose

Execução de migrations

Execução de testes automatizados

Validação da integração com MySQL

📌 O CI utiliza a mesma configuração Docker do ambiente local, garantindo consistência entre desenvolvimento e integração.

---

## 🎯 Status do Projeto

🚧 Em desenvolvimento contínuo

---

## 👨‍💻 Autor

**Vitor Carvalho**
Backend Developer | Python | Django | DRF

---

## ⭐ Considerações Finais

Este projeto foi desenvolvido com foco em:

* Boas práticas de backend
* Organização e escalabilidade
* Dockerização profissional
* Documentação profissional
* Uso real de ferramentas de mercado
