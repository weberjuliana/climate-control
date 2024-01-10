# Climate Control API - Backend Python Application

## Descrição

Climate Control é uma aplicação de backend desenvolvida para fornecer informações sobre a previsão do tempo para os próximos dias. 

Utilizando a API de previsão do tempo de 5 dias do [OpenWeatherMap](https://openweathermap.org/), esta aplicação não só busca dados atualizados sobre o clima, mas também armazena o histórico de chamadas para consultas posteriores. A aplicação é ideal para aqueles que precisam de informações rápidas e confiáveis sobre as condições meteorológicas.

## Requisitos e Bônus do Desafio Técnico

### Requisitos Completos

- [x] **Linguagem de Programação Python**: Desenvolvida inteiramente em Python.
- [x] **Banco de Dados Não Relacional**: Utilização do MongoDB, um banco de dados não relacional.
- [x] **Bibliotecas e Frameworks Livres**: Usado FastApi pela capacidade de uso com banco nosql, arquitetura customizável.
- [x] **Chamadas de API Diretas**: API do OpenWeatherMap utilizada também diretamente com postman e swagger.
- [x] **README com Instruções**: Documentação detalhada sobre como configurar e executar a aplicação.

### Bônus Completos

- [x] **Testes unitários**: Inclusão de testes unitários no repositório.
- [x] **Collections Postman**: Inclusão de collections do Postman.

### Extras

- [x] ** Commits semânticos**: melhor organização, padronização e transparência ao que foi feito.
- [x] ** Uso de Gitflow**: para melhor visualização de trabalho em equipe.
- [x] ** Containerização**: aplicação fácil de executar, portátil, consistente, eficiente e simples.

# Como rodar a aplicação

#### Requisitos mínimos

- Docker/Docker-compose
- Client mongodb(compass), caso queira acessar o banco manualmente.

Obs.: há também endpoints onde os dados do banco de dados são retornados, nao se fazendo necessario o uso do client.

## Instruções para Clonar e Executar a Aplicação

1.  **Clonar o Repositório**:

```bash
git clone https://github.com/weberjuliana/climate-control.git
```

```bash
cd climate
```

2.  **Arquivo .env**:
    - Crie um arquivo chamado .env e insira todas informações que constam em `.env-example`
3.  **Executar**:
    - Utilize para construir/executar a aplicação o comando:
    ```bash
    docker-compose up --build
    ```
4.  **Swagger da API**:
    - Agora você pode acessar [http://localhost:8000/docs](http://localhost:8000/docs) para testar os endpoints manualmente.
5.  **Login e Autenticação**:
    - Clique no endpoint `/login`.
    - Clique em "Try it out".
    - Insira `username` e `password`, contidos em sua .env, e clique em "Execute".
    - Você receberá um `access_token`: copie-o.
    - No topo da página, no lado direito, clique em "Authorize" e cole o token, em seguida clique em "Authorize".
6.  **Uso dos Endpoints Autenticados**:
    - Agora você pode usar todos os endpoints autenticados (tempo de expiração do token é de 20 minutos).

## Postman

Na pasta raiz do projeto você encontra um arquivo para importar no postman com as collections , o arquivo se chama "OpenWeather.postman_collection"

# Como rodar os testes

Em um terminal, independente de ja estar rodando a aplicação ou não, execute:

```bash
docker-compose up --build test
```

# Endpoints da API


1.  POST `/login` - Login (parâmetros: `username`, `password`)
2.  GET `/forecast` - Obter previsão do tempo (parâmetros opcionais: `city`, `lat`, `lon`)
3.  GET `/all` - Obter todos os dados de previsão do tempo
4.  GET `/by-id/{document_id}` - Obter dados de previsão do tempo por ID do documento
5.  DELETE `/delete-all` - Deletar todos os dados de previsão do tempo
6.  DELETE `/delete-by-id/{document_id}` - Deletar dados de previsão do tempo por ID do documento

### 1. Login

- **Método e Caminho**: `POST /login`
- **Parâmetros**:
  - `username`: Nome de usuário para login.
  - `password`: Senha para login.
- **Descrição**: Endpoint para realizar o login. Retorna um token JWT se o login for bem-sucedido.

### 2. Previsão do Tempo por Cidade ou Coordenadas

- **Método e Caminho**: `GET /forecast`
- **Parâmetros**:
  - `city` (opcional): Nome da cidade para a previsão do tempo.
  - `lat` (opcional): Latitude para a previsão do tempo.
  - `lon` (opcional): Longitude para a previsão do tempo.
- **Descrição**: Retorna a previsão do tempo com base no nome da cidade ou nas coordenadas de latitude e longitude fornecidas.

### 3. Obter Todos os Dados de Previsão do Tempo

- **Método e Caminho**: `GET /all`
- **Descrição**: Recupera todos os dados de previsão do tempo armazenados no banco de dados.

### 4. Obter Dados de Previsão do Tempo por ID

- **Método e Caminho**: `GET /by-id/{document_id}`
- **Parâmetros**:
  - `document_id`: ID do documento a ser recuperado do banco de dados.
- **Descrição**: Busca e retorna os dados de previsão do tempo associados ao ID do documento especificado.

### 5. Deletar Todos os Dados de Previsão do Tempo

- **Método e Caminho**: `DELETE /delete-all`
- **Descrição**: Remove todos os dados de previsão do tempo do banco de dados.

### 6. Deletar Dados de Previsão do Tempo por ID

- **Método e Caminho**: `DELETE /delete-by-id/{document_id}`
- **Parâmetros**:
  - `document_id`: ID do documento a ser removido do banco de dados.
- **Descrição**: Remove um documento de previsão do tempo específico, identificado pelo ID fornecido.

# Arquitetura
A arquitetura segue princípios de design de software limpo e modular, com vários benefícios em manutenção, escalabilidade e clareza. 

### 📦climatecontrol

Estrutura Raiz do projeto.

#### ┣ 📂src

Diretório de código-fonte principal.

-   **Benefícios**:
    -   **Centralização**: Mantém todo o código-fonte em um local único, facilitando a navegação e o gerenciamento.

#### ┃ ┣ 📂interfaces

Contém a interface da API e as rotas.

-   **v1**: Versão específica da API, facilitando a gestão de versões e atualizações futuras.
    
-   **authentication**: Lógica de autenticação, isolando preocupações de segurança.
    
-   **routes**: Endpoints da API, promovendo clareza na definição das rotas.
    
-   **Benefícios**:
    
    -   **Modularidade**: Facilita a extensão e manutenção da API.
    -   **Segregação de Responsabilidades**: Cada parte da API é mantida isoladamente.

#### ┃ ┣ 📂config

Configurações do projeto, como variáveis de ambiente e parâmetros de conexão.

-   **Benefícios**:
    -   **Manutenção Facilitada**: Centraliza as configurações, tornando mais fácil gerenciar e alterar as definições do projeto.

#### ┃ ┣ 📂repository

Lógica de acesso e manipulação do banco de dados.

-   **Benefícios**:
    -   **Abstração de Dados**: Isola a camada de dados do restante do aplicativo, facilitando mudanças na base de dados ou ORM sem afetar outras partes do código.

#### ┃ ┣ 📂entities

Modelos e esquemas de dados.

-   **Benefícios**:
    -   **Reusabilidade**: Centraliza modelos e tipos de dados, facilitando a reutilização em todo o projeto.
    -   **Validação**: Define claramente a estrutura de dados usada em toda a aplicação.

#### ┃ ┣ 📂logic

Contém a lógica de negócios da aplicação.

-   **Benefícios**:
    -   **Separação de Concerns**: Mantém a lógica de negócios separada da interface e camada de dados, promovendo a manutenção e testabilidade.

#### ┃ ┣ 📂testing

Testes do projeto.

-   **Benefícios**:
    -   **Qualidade do Código**: Facilita o desenvolvimento e manutenção de testes, garantindo a robustez do código.

#### ┃ ┣ 📜server.py

Ponto de entrada da aplicação.

-   **Benefícios**:
    -   **Clareza**: Define claramente o ponto de início da aplicação, facilitando o entendimento do fluxo do programa.

#### ┗ Outros Arquivos (`.env`, `.gitignore`, `Dockerfile`, etc.)

Configurações auxiliares e de ambiente, como variáveis de ambiente, regras de versionamento, configuração para contêineres, etc.

-   **Benefícios**:
    -   **Ambiente Controlado**: Garante que a aplicação seja executada em um ambiente configurado de forma consistente.
    -   **Segurança e Conformidade**: Mantém segredos e configurações sensíveis fora do código fonte.