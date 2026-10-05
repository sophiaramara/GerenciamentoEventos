# Sistema de Gestão de Eventos Acadêmicos (API)

## 1. Contexto do Problema e Introdução
Atualmente, o gerenciamento de eventos acadêmicos, inscrições de participantes, controle de presença e emissão de certificados na instituição é feito por meio de planilhas manuais e processos descentralizados. Isso gera ineficiência, inconsistência de dados, risco de inscrições duplicadas e superação da capacidade de vagas.

- **Objetivo da API:** Disponibilizar uma API RESTful centralizada, performática e segura para gerenciar eventos acadêmicos, inscrições, perfis de usuários e automação da emissão de certificados.
- **Escopo do MVP (Versão 1.0):** Gerenciamento e listagem de eventos, controle de inscrições, validação rigorosa de regras de negócio e controle de capacidade máxima dos eventos.

---

## 2. Perfis de Usuário (Atores)
| Perfil | Descrição | 
| :--- | :--- |
| **Administrador** | Gerencia usuários, eventos, inscrições e certificados do sistema. |
| **Organizador** | Cria e gerencia eventos de sua responsabilidade. |
| **Participante** | Consulta eventos abertos, realiza inscrições e consulta seus certificados. |

---

## 3. Regras de Negócio (RN)
* **RN01 - E-mail Único e Válido:** Não é permitido cadastrar mais de um usuário/participante com o mesmo e-mail, devendo respeitar o formato de e-mail válido.
* **RN02 - Inscrição Única:** Um participante não pode se inscrever duas vezes no mesmo evento.
* **RN03 - Limite de Capacidade:** Um evento não pode ultrapassar sua capacidade máxima de inscritos (Caso a capacidade não seja informada, o sistema assume o padrão de 50 vagas).
* **RN04 - Exclusão Restrita de Eventos:** Apenas Administradores e Organizadores têm permissão para excluir ou cancelar eventos.
* **RN05 - Cancelamento Próprio:** Um participante só pode cancelar a sua própria inscrição.
* **RN06 - Eventos em Datas Futuras:** Não é permitido cadastrar ou editar um evento com data passada.
* **RN07 - Requisito para Certificado:** Um certificado só pode ser emitido para um participante com inscrição confirmada e presença registrada.
* **RN08 - Validação de Inscrição Ativa:** Não é possível inscrever-se em eventos cancelados ou com status inativo.
* **RN09 - Chave do Certificado:** Cada certificado deve conter um código validador único e imutável.
* **RN10 - Edição do Evento pelo Criador:** Organizadores só podem editar ou gerenciar eventos criados por eles mesmos.

---

## 4. Dicionário de Dados

### Tabela: `eventos`
| Campo | Tipo | Obrigatório | Regra / Descrição |
| :--- | :--- | :---: | :--- |
| `id` | BigInt (PK) | Sim | Chave Primária Autoincrementada |
| `created_at` | Timestamptz | Sim | Data/Hora de registro no banco |
| `titulo` | String(150) | Sim | Título legível do evento |
| `descricao` | Text | Não | Detalhes sobre a programação |
| `data_evento` | DateTime | Sim | Data de realização (Não pode ser no passado) |
| `capacidade` | Integer | Sim | Limite máximo de inscritos (Padrão: 50) |
| `status` | String(20) | Sim | Status do evento (ATIVO, CANCELADO, CONCLUIDO) |

### Tabela: `inscricoes`
| Campo | Tipo | Obrigatório | Regra / Descrição |
| :--- | :--- | :---: | :--- |
| `id` | BigInt (PK) | Sim | Chave Primária Autoincrementada |
| `created_at` | Timestamptz | Sim | Data/Hora de registro da inscrição |
| `nome_participante` | String(100) | Sim | Nome completo do participante |
| `email_participante` | String(150) | Sim | E-mail do participante (Formato válido) |
| `evento_id` | BigInt (FK) | Sim | Chave Estrangeira apontando para `eventos.id` |
| `status` | String(20) | Sim | Status da inscrição (ATIVA, CANCELADA) |

---

## 5. Matriz de Permissões
| Funcionalidade / Rota | Admin | Organizador | Participante |
| :--- | :---: | :---: | :---: |
| Criar Evento (`POST /eventos`) | Sim | Sim | Não |
| Editar Evento (`PUT /eventos/{id}`) | Sim | Sim (próprio) | Não |
| Excluir Evento (`DELETE /eventos/{id}`) | Sim | Não | Não |
| Listar Eventos (`GET /eventos`) | Sim | Sim | Sim |
| Inscrever-se em Evento (`POST /inscricoes`) | Não | Não | Sim |
| Cancelar Inscrição (`DELETE /inscricoes/{id}`) | Sim | Não | Sim (próprio) |

---

## 6. Status Codes da API
| Código | Situação |
| :---: | :--- |
| `200 OK` | Consulta ou atualização realizada com sucesso. |
| `201 Created` | Registro de evento ou inscrição criado com sucesso. |
| `204 No Content` | Exclusão/cancelamento realizado com sucesso. |
| `400 Bad Request` | Violação de regra de negócio (ex: evento lotado ou inscrição duplicada). |
| `401 Unauthorized` | Usuário não autenticado. |
| `403 Forbidden` | Sem permissão para realizar a ação. |
| `404 Not Found` | Recurso (evento ou inscrição) não encontrado. |
| `422 Unprocessable Entity` | Erro de validação nos dados enviados (ex: e-mail inválido ou data no passado). |

---

## 7. Backlog do Projeto e Critérios de Aceitação

| ID | História de Usuário (User Story) | Prioridade | Critérios de Aceitação |
| :--- | :--- | :---: | :--- |
| **US01** | Como participante, quero me cadastrar para acessar eventos. | Alta | Exige nome, e-mail e senha. Retorna `201`. Retorna `422` em e-mail inválido. |
| **US02** | Como administrador, quero criar eventos acadêmicos. | Alta | Exige título e data futura. Assume 50 vagas se omitido. Retorna `201`. |
| **US03** | Como participante, quero me inscrever em um evento. | Alta | Valida se o evento existe (`404`), se está ativo (`400`) e se há vagas (`400`). Retorna `201`. |
| **US04** | Como participante, quero consultar meus eventos inscritos. | Média | Retorna status `200` com a lista detalhada das inscrições do usuário. |
| **US05** | Como organizador, quero listar inscritos no meu evento. | Média | Retorna `200` com os dados dos inscritos do evento informado. |
| **US06** | Como participante, quero cancelar minha inscrição. | Média | Cancela a inscrição existente e retorna status `204`. |
| **US07** | Como admin, quero desativar/excluir um evento. | Alta | Remove o evento do sistema e retorna status `204`. |