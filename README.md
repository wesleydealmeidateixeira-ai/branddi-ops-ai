
# Branddi Ops AI

Agente de Inteligência Artificial para análise de capacidade, produtividade e recuperação operacional em ambientes SaaS.

## 1. Objetivo

O Branddi Ops AI é um protótipo de apoio à decisão gerencial que combina cálculos operacionais determinísticos com análises consultivas de Inteligência Artificial.

O projeto busca apoiar gestores na identificação de gargalos, avaliação de capacidade, dimensionamento de recursos e planejamento da recuperação de filas de atendimento.

## 2. Funcionalidades

- Simulação de capacidade operacional de suporte N1 e N2.
- Comparação entre cenários atuais e crescimento de demanda.
- Identificação de déficits e excedentes de capacidade.
- Cálculo de utilização operacional.
- Simulação de recuperação de backlog.
- Avaliação de alternativas de contratação, produtividade e automação.
- Análise consultiva com IA generativa utilizando Google Gemini.
- Identificação de determinadas afirmações financeiras e prazos que exigem validação.
- Registro de decisões gerenciais em banco SQLite.
- Consulta ao histórico de decisões.

## 3. Arquitetura

O projeto utiliza Python e Streamlit.

Componentes principais:

- `app.py`: interface da aplicação.
- `capacity.py`: cálculos de capacidade operacional.
- `recommendations.py`: cálculo de alternativas operacionais.
- `recovery.py`: simulação de recuperação de filas.
- `ai_agent.py`: integração com Gemini e geração de análises consultivas.
- `database.py`: persistência de decisões gerenciais em SQLite.

A Inteligência Artificial interpreta os indicadores calculados pelo sistema, mas não substitui o motor matemático.

## 4. Governança

O agente foi projetado para apoiar decisões, não para executá-las automaticamente.

Diretrizes:

- Preservar os resultados dos cálculos operacionais.
- Diferenciar dados, hipóteses e recomendações.
- Não presumir custos ou resultados financeiros sem evidências.
- Tratar alternativas de recuperação como opções independentes quando aplicável.
- Sinalizar determinadas afirmações que exigem validação adicional.
- Manter aprovação e execução sob responsabilidade humana.

A validação automática utiliza regras textuais e não garante a detecção de todas as inconsistências.

## 5. Tecnologias

- Python
- Streamlit
- Google Gemini API
- SQLite
- Git e GitHub

## 6. Instalação

Clone o repositório:

```bash
git clone https://github.com/wesleydealmeidateixeira-ai/branddi-ops-ai.git
```

Entre na pasta:

```bash
cd branddi-ops-ai
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Crie um arquivo `.env` na raiz do projeto:

```env
GEMINI_API_KEY=SUA_CHAVE_API
```

Nunca publique sua chave de API.

## 7. Execução

Inicie a aplicação:

```bash
python -m streamlit run app.py
```

O Streamlit apresentará o endereço local da aplicação no terminal.

## 8. Testes

Execute os testes de cálculo:

```bash
python teste_capacity.py
python teste_recommendations.py
python teste_recovery.py
```

Esses scripts permitem verificar os resultados dos cenários operacionais implementados.

## 9. Limitações

- Protótipo demonstrativo, não homologado para produção.
- Cenários operacionais dependem dos dados e premissas informados.
- Recomendações da IA podem conter imprecisões.
- Não há integração automática com sistemas reais de tickets.
- A disponibilidade da análise por IA depende da API do Gemini.
- Custos e viabilidade de implementação precisam ser avaliados separadamente.

## 10. Finalidade

Projeto demonstrativo desenvolvido para apresentação de um case de gestão operacional SaaS.

Seu foco é demonstrar a aplicação conjunta de processos, indicadores, simulações e Inteligência Artificial na tomada de decisão gerencial.
