# IA para Times — Higgsfield Enterprise
> **Uso Interno** · Guia Educacional · [MIT AI & ML for Business] [Claude Certified] [Keter System]

**Autor:** Mauricio Lacerda — AI Strategist & Operador de Sistemas Inteligentes · Higgsfield Enterprise  
**Base:** Estudos pessoais aprofundados e certificação **MIT AI & ML for Business**  
**Data:** 2026

---

## Por que a sua empresa precisa de IA agora

Não se trata de substituir pessoas. Trata-se de dar a cada pessoa a capacidade de um time inteiro.

| # | Pilar | O que significa |
|---|-------|-----------------|
| ⚡ | **Velocidade** | Tarefas de horas — análise, redação, pesquisa, código — entregues em minutos com o contexto certo |
| 🔁 | **Escala** | Um único operador conduz múltiplos agentes em paralelo, amplificando a capacidade sem aumentar headcount |
| 🎯 | **Consistência** | Com Projects + Skills + Specs, o output é consistente — não depende do humor ou memória de ninguém |

---

## Configuração de Contas — Higgsfield Global

### Estrutura Recomendada

| Nível | Plano | Para quem | Custo aprox. | Diferencial |
|-------|-------|-----------|-------------|-------------|
| Hub / Estratégia | **Claude MAX** | AI Strategist, Leads de Área | ~$100/mês por pessoa | Contexto máximo, Claude Code, modelos mais recentes com prioridade |
| Colaborador | **Claude Pro** | Uso regular de negócio | ~$20/mês por pessoa | 5× mais uso que free, Projects, acesso aos modelos principais |
| Exploração | **Claude Free** | Onboarding inicial | Gratuito | Testar antes de decidir — **não usar com dados da empresa** |

### Regras de Ouro

- 🚫 **Nunca compartilhe login.** 1 conta = 1 pessoa. Compartilhar viola os termos e compromete a segurança.
- 📁 **Crie Projects por cliente/projeto.** Contexto isolado, reutilizável e consistente para o time inteiro.
- 🔑 **O Time Lead é o guardião do Project.** Responsável pelas instruções iniciais e qualidade do contexto.
- 📊 **MAX vs Pro:** MAX para quem usa IA como ferramenta central. Pro para uso regular. Free apenas para exploração.

---

## Organização Visual — Como Estruturamos a IA

```
┌──────────────────────────────────────────────────────────┐
│               ⬡  HIGGSFIELD AI HUB                       │
│         Mauricio Lacerda — AI Strategist                 │
│                    Claude MAX                            │
└────────────────────────┬─────────────────────────────────┘
                         │
          ┌──────────────┼──────────────┬──────────────┐
          │              │              │              │
   ┌──────▼──────┐ ┌────▼──────┐ ┌────▼──────┐ ┌────▼──────────┐
   │  Marketing  │ │   Sales   │ │Operations │ │  Tech / Dev   │
   │  MAX Lead   │ │  MAX Lead │ │  MAX Lead │ │MAX + Cod Code │
   └──────┬──────┘ └────┬──────┘ └────┬──────┘ └────┬──────────┘
          │              │              │              │
       Pro ×N         Pro ×N        Pro ×N         Pro ×N
      (time)          (time)        (time)         (time)

Cada departamento possui um Project dedicado com contexto isolado.
Escalável conforme o crescimento da empresa.
```

---

## Boas Práticas para o Time

### 🔒 Segurança e Privacidade

- **Nunca coloque senhas, tokens ou chaves de API em prompts.** Use variáveis de ambiente — nunca texto direto.
- **Não use conta Free para dados confidenciais da empresa.** No plano Free, o histórico pode ser usado para treinar modelos.
- **Use Projects para isolar contextos.** Dados de um cliente não devem vazar para o projeto de outro.
- **Revise antes de enviar para clientes.** A IA não conhece seus relacionamentos — valide o tom e os fatos.
- **Dados pessoais de terceiros? Nunca no prompt.** CPFs, números de cartão, dados médicos — nunca.

> **Regra de ouro:** Se você não colocaria essa informação num email corporativo sem criptografia, não coloque na IA.

---

### 💬 Como Conversar com IA

- **Dê um papel:** *"Você é um especialista em logística internacional com foco em compliance..."* — contexto muda tudo.
- **Seja específico:** *"Escreva um email de 3 parágrafos, tom profissional mas caloroso, para o cliente João que pediu prazo estendido."*
- **Dê exemplos (few-shot):** *"Aqui está um email no tom que queremos: [exemplo]. Agora escreva um similar sobre..."*
- **Itere:** Nunca aceite o primeiro resultado sem ajustes. Peça: *"Torne mais conciso"*, *"Adicione urgência"*, *"Reformule o 2º parágrafo."*
- **Use Artifacts:** Para tabelas, documentos e código — peça output estruturado, não paredes de texto.

> **Método RPI:** Research → Plan → Implement. Nunca pule direto para a execução.

---

### ⚡ Economia de Tokens

- **Use Projects com instruções fixas.** Uma vez configurado, você não repete o contexto em cada conversa.
- **Resuma conversas longas.** Antes de continuar: *"Resuma em 5 pontos o que decidimos até agora"* → nova conversa.
- **Modelos certos para as tarefas certas:**
  - **Haiku** → triagem e rascunhos rápidos
  - **Sonnet** → trabalho complexo (padrão recomendado)
  - **Opus** → decisões estratégicas e análise profunda
- **Não carregue arquivos desnecessários.** O contexto é finito — só inclua o que é realmente relevante.
- **Regra dos 40%:** Máximo 40% do contexto deve ser histórico de conversa. 60% deve ser instrução estruturada.

> Projects + Regra dos 40% = contexto sempre fresco. Qualidade consistente sem desperdício.

---

### 🚀 Como Extrair o Máximo

- **Método RPI:**
  1. **Research** — explore com IA livre, anote as melhores sínteses
  2. **Plan** — estruture o que aprendeu em especificações claras
  3. **Implement** — execute com contexto limpo e instrução precisa
- **Use Research Mode do Claude** para tarefas que precisam de fontes externas verificadas.
- **NotebookLM para base de conhecimento interna.** Coloque manuais, processos e PDFs — a IA responde com base nos seus documentos, não em suposições.
- **Crie Skills reutilizáveis.** Tarefas recorrentes do time viram instruções salvas: email de follow-up, proposta comercial, análise de métricas.
- **Valide sempre:** IA pode alucinar. Use como acelerador inteligente, não como fonte final de verdade.

> NotebookLM com os documentos da Higgsfield = IA que fala a linguagem da empresa, não do mundo genérico.

---

## Arsenal de IA — O que Usamos

| Ferramenta | Uso |
|-----------|-----|
| 🧠 **Claude.ai Projects** | Contexto persistente por cliente ou projeto. O time acessa o mesmo "cérebro" compartilhado. |
| ⌨️ **Claude Code** | Automação, desenvolvimento e operações avançadas. Para os tech leads do time. |
| 📚 **NotebookLM** | Base de conhecimento interna. Faça perguntas sobre os documentos da empresa com respostas citadas. |
| 🔍 **Perplexity / Research Mode** | Pesquisa com fontes verificadas. Para quando você precisa de dados reais, não síntese de treinamento. |
| 📱 **ManyChat + Meta AI** | Automação de WhatsApp e Instagram. Fluxos inteligentes sem código para escalar atendimento. |
| 🎨 **Canva AI / Figma AI** | Design assistido por IA. Criativos em minutos com identidade visual consistente. |
| 📋 **Claude Artifacts** | Output estruturado renderizável: planilhas, dashboards, landing pages, documentos — direto no chat. |
| 🤖 **Agentes Multi-Step** | Sequências automáticas: pesquisa → análise → relatório → envio. Um comando, resultado completo. |

---

## Posso Ajudar o Seu Time

**Mauricio Lacerda** — AI Strategist & Operador de Sistemas Inteligentes  
📜 MIT AI & ML for Business · 12+ meses em produção  
✉️ [mauricio.s.lacerda@gmail.com](mailto:mauricio.s.lacerda@gmail.com)

### Áreas de suporte disponíveis

Selecione os tópicos abaixo e me envie um email com o assunto:  
`Higgsfield AI — [tópicos de interesse]`

- [ ] Configuração Claude MAX & Accounts
- [ ] Treinamento do Time
- [ ] Automação de Workflows
- [ ] Criação de Agentes IA
- [ ] Segurança & Compliance
- [ ] NotebookLM & Base de Conhecimento
- [ ] Arquitetura de Prompts
- [ ] Claude Code & Desenvolvimento
- [ ] Estratégia de IA para o Time

**→ [Enviar email para Mauricio](mailto:mauricio.s.lacerda@gmail.com?subject=Higgsfield%20AI%20%E2%80%94%20Suporte&body=Ol%C3%A1%20Mauricio%2C%0A%0AEstou%20interessado%20em%20suporte%20nos%20seguintes%20t%C3%B3picos%3A%0A%0A%5Bdescreva%20aqui%5D%0A%0A%5BSeu%20nome%20e%20departamento%5D)**

---

*Guia baseado em estudos pessoais e na certificação MIT AI & ML for Business.*  
*Keter System — Segundo Cérebro Operacional · Mauricio Lacerda · © 2026 Higgsfield Enterprise*
