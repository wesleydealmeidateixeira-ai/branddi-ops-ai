# Branddi Ops AI

Protótipo funcional de **inteligência operacional e apoio à decisão gerencial**, criado para o case fictício de Gerente Operacional de SaaS da Branddi.

**Demonstração:** https://branddi-ops-ai.streamlit.app

## Problema e solução

Avaliar a capacidade dos níveis N1/N2, uma proposta de redução de equipe, crescimento de demanda de 20%, backlog e alternativas de recuperação, sem confundir ganho hipotético com evidência real. O sistema combina **cálculos determinísticos em Python**, dashboard Streamlit, **parecer textual via Google Gemini** e **revisão humana** com registro local de decisões.

O sistema não toma decisões de pessoal, não executa ações em clientes e não integra sistemas reais.

## Arquivos principais

- `app.py` — interface Streamlit, simulações, parecer e revisão humana.
- `capacity.py` — cálculo de capacidade e cenários.
- `recommendations.py` — alternativas de capacidade.
- `recovery.py` — plano de recuperação de fila.
- `ai_agent.py` — Gemini, instruções e validação de resposta.
- `database.py` — registro de decisões SQLite.
- `requirements.txt` — dependências Python.
- `PROJETO.md` — diagnóstico, memória de cálculo, fluxos, decisão e piloto.
- `USO_DE_IA.md` — ferramentas, prompts, revisões e limites.
- `TESTES.md` — cenários, evidências e lacunas.

## Pré-requisitos

Python 3.12 recomendado, Git opcional para clonar, conexão de rede e chave de API Gemini para gerar parecer por IA. Dependências instaladas por `requirements.txt` (incluindo Streamlit, `google-genai` e `python-dotenv`). A interface e cálculos podem ser executados localmente; o módulo de IA depende de chave válida, e a implementação pode exigir chave já na inicialização.

## Instalação e execução — Windows PowerShell

```powershell
git clone https://github.com/wesleydealmeidateixeira-ai/branddi-ops-ai.git
cd branddi-ops-ai
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Crie `.env` **localmente** na raiz (não faça commit):

```dotenv
GEMINI_API_KEY=COLE_AQUI_SUA_CHAVE_PRIVADA
```

Inicie:

```powershell
streamlit run app.py
```

Abra o endereço local informado pelo Streamlit. Para testes incluídos no repositório, consulte os scripts `test_*.py` e `TESTES.md`; execute-os conforme seus respectivos pontos de entrada.

## Exemplo reproduzível

Dados fictícios N2: 9 analistas, 40 horas semanais, 65% produtivas, 3 ações humanas/caso, 12 minutos/ação, 420 casos de entrada por semana e fila inicial 180. Resultado esperado: **390 casos/semana de capacidade**, **107,69% de utilização**, **déficit de 30 casos/semana**. Para eliminar fila de 180 em quatro semanas, mantendo entrada de 420/semana: capacidade-alvo **465 casos/semana**.

A aplicação também compara N1 e N2 com sete analistas por nível, tempos futuros hipotéticos e crescimento de 20%.

## Limitações e segurança

- Cenário integralmente fictício; os dados não são da operação real da Branddi.
- Ganhos de tempo futuro são hipóteses; não há medição de produtividade antes/depois em amostra real.
- O parecer da IA é interpretativo e pode errar; cálculos são determinísticos e decisões exigem revisão humana.
- O SQLite local no Streamlit Community Cloud **não garante persistência durável** entre reinicializações/redeploys; não usar como trilha de auditoria de produção.
- Não há autenticação corporativa, integração SaaS, execução automática de contratações ou alterações em operações reais.
- **Custos/dependências externas:** hospedagem Streamlit Community Cloud sujeita às condições do serviço; Gemini API requer chave, acesso à rede e está sujeito a cotas e possível cobrança conforme plano/uso. Não é necessário contratar serviço pago para reproduzir os cálculos, mas o parecer online depende da API.
- Nunca publicar `.env`, tokens, chaves, dados pessoais ou credenciais.

## Entregáveis

Leia `PROJETO.md`, `USO_DE_IA.md` e `TESTES.md` antes da apresentação. A demonstração online complementa, mas não substitui, o repositório reproduzível.
