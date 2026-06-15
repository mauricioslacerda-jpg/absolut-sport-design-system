# ABSOLUT SPORT — Design Token Taxonomy
**Design System | Versão 1.0 | Marketing & Produto | Maio 2025**

---

## 1. Objetivo do Documento

Este documento define a taxonomia oficial de design tokens da ABSOLUT Sport. Seu propósito é estabelecer uma linguagem comum entre designers, desenvolvedores e gestores de produto, garantindo que todos os elementos visuais da marca sejam nomeados de forma previsível, escalável e consistente em todos os canais digitais da ASB.

Um design token é a menor unidade de decisão visual de um produto. Cada cor, espaço, fonte ou raio de borda que aparece em qualquer interface da ASB deve corresponder a um token nomeado, nunca a um valor hardcoded. Isso garante que o sistema seja temático, auditável e evolutivo.

---

## 2. Por que Nomenclatura Semântica Importa

A maioria dos sistemas de design começa com nomenclatura literal: `azul-500`, `cinza-escuro`, `rosa-primario`. Essa abordagem parece funcional no início, mas gera três problemas estruturais conforme o produto cresce.

O primeiro é o **acoplamento visual**: quando o desenvolvedor vê `azul-500` no código, ele precisa abrir o Figma para entender o contexto de uso. O nome não carrega o contrato. O segundo é a **fragilidade temática**: se a marca evoluir ou precisar de um modo escuro, todos os valores precisam ser remapeados componente a componente. O terceiro é a **auditoria impossível**: sem semântica, não há como saber quantos valores de cor diferentes existem no sistema ou quais estão em uso.

A nomenclatura semântica resolve os três problemas ao mesmo tempo. Quando um token se chama `color-bg-surface-secondary-hover`, o nome por si só diz onde usar (background), qual tipo de superfície (surface), qual hierarquia (secondary) e em que momento (hover). O valor hex pode mudar. O nome permanece como contrato.

> **Referência histórica:** O Spotify enfrentou uma migração massiva e custosa do seu design system por não ter adotado essa disciplina desde o início. O custo de refatoração é exponencialmente maior do que o custo de estruturação preventiva.

---

## 3. Anatomia do Token

Todo token de cor da ASB segue uma estrutura de três camadas separadas por hífen:

```
color - [elemento de UI] - [hierarquia/tipo] - [estado]
```

| Camada | Nome | Responde à pergunta |
|--------|------|----------------------|
| **1** | Elemento de UI | Onde o token é aplicado? |
| **2** | Hierarquia / Tipo | Qual o peso ou papel? |
| **3** | Estado | Em que momento aparece? |

### Exemplos de tokens bem formados

| Token | Leitura semântica |
|-------|-------------------|
| `color-bg` | Cor de fundo base da aplicação |
| `color-bg-surface-secondary-hover` | Fundo de superfície secundária em hover |
| `color-bg-fill-primary-active` | Preenchimento primário no estado ativo |
| `color-text-primary-disabled` | Texto primário desabilitado |
| `color-border-tertiary-default` | Borda terciária no estado padrão |
| `color-icon-secondary-hover` | Ícone secundário em hover |

O prefixo `color-` é sempre obrigatório. Tokens que se referem apenas ao elemento base, sem hierarquia ou estado, podem omitir as camadas subsequentes. Por exemplo, `color-bg` é válido como token base de fundo.

---

## 4. Taxonomia Completa

### 4.1 Camada 1: Elementos de UI

Os elementos de UI definem onde o token será aplicado. Cada elemento mapeia para uma categoria funcional de interface, não para um componente específico, garantindo que o token seja reutilizável em múltiplos contextos.

| Elemento | Uso | Exemplo de contexto |
|----------|-----|---------------------|
| `bg` | Cor de fundo de páginas e containers | Fundo da homepage, fundo de cards |
| `surface` | Fundo de superfícies elevadas | Modais, dropdowns, painéis flutuantes |
| `fill` | Preenchimento de elementos interativos | Botões, tags, badges |
| `text` | Cor de qualquer texto | Títulos, parágrafos, labels, placeholders |
| `border` | Bordas e separadores | Inputs, cards, divisores |
| `icon` | Cor de ícones e glifos | Ícones de navegação, ações, status |
| `overlay` | Camadas de sobreposição | Backdrops de modais, tooltips |
| `shadow` | Sombras e elevação | Box-shadow de cards e componentes flutuantes |

### 4.2 Camada 2: Hierarquia e Tipo

A segunda camada define a posição hierárquica do token dentro do elemento. Ela responde à pergunta: qual é o peso visual ou o papel funcional desse token em relação aos seus pares?

| Hierarquia | Peso visual | Quando usar |
|------------|-------------|-------------|
| `primary` | Mais proeminente | Ação principal, texto de maior leitura |
| `secondary` | Moderado | Ações de apoio, textos de suporte |
| `tertiary` | Sutil | Elementos de terceiro plano, bordas suaves |
| `inverse` | Invertido / sobre escuro | Texto branco sobre fundo escuro |
| `brand` | Cor de marca | Acentos ASB Gold, elementos identitários |
| `danger` | Alerta crítico | Erros, exclusões, ações destrutivas |
| `warning` | Atenção moderada | Avisos, pendências, alertas não críticos |
| `success` | Confirmação positiva | Confirmações, pagamentos aprovados |
| `info` | Informativo neutro | Tooltips, notas, dicas de uso |

### 4.3 Camada 3: Estado

A terceira camada mapeia o estado de interação do componente no momento em que o token é exibido.

| Estado | Acionado quando | Gatilho típico |
|--------|-----------------|----------------|
| `default` | Elemento em repouso | Sem interação do usuário |
| `hover` | Cursor sobre o elemento | mouseover |
| `active` | Elemento pressionado | mousedown / touchstart |
| `focus` | Elemento com foco de teclado | tab / click em input |
| `selected` | Elemento escolhido | Opção ativa em filtro ou menu |
| `disabled` | Elemento inativo | prop disabled / regra de negócio |
| `loading` | Aguardando resposta | Spinner, skeleton, fetch em curso |
| `error` | Estado inválido | Validação de formulário falhou |
| `visited` | Link já acessado | Histórico de navegação |

---

## 5. Tokens de Cor da Marca ABSOLUT Sport

### 5.1 Paleta Base

| Token | Hex | Papel | Tema |
|-------|-----|-------|------|
| `color-brand-primary-default` | `#C9A84C` | ASB Gold — cor identitária principal | Global |
| `color-brand-secondary-default` | `#1A1A1A` | Preto profundo — fundos premium | Global |
| `color-bg-default` | `#FFFFFF` | Fundo base — tela principal | Light |
| `color-bg-surface-primary-default` | `#F5F5F5` | Superfície de cards e painéis | Light |
| `color-bg-default` | `#111111` | Fundo base — modo escuro | Dark |
| `color-bg-surface-primary-default` | `#1E1E1E` | Superfície de cards — modo escuro | Dark |
| `color-text-primary-default` | `#1A1A1A` | Texto principal em fundo claro | Light |
| `color-text-primary-default` | `#F0F0F0` | Texto principal em fundo escuro | Dark |
| `color-text-secondary-default` | `#666666` | Texto de suporte e metadados | Light |
| `color-border-primary-default` | `#D4C5A0` | Bordas de containers e inputs | Light |

### 5.2 Tokens de Status

| Token | Hex | Uso |
|-------|-----|-----|
| `color-fill-success-default` | `#2D8A4E` | Pagamento confirmado, reserva aprovada |
| `color-fill-danger-default` | `#C0392B` | Erro crítico, cancelamento, alerta |
| `color-fill-warning-default` | `#D4860A` | Pendência, prazo próximo, atenção |
| `color-fill-info-default` | `#2474A4` | Informações e dicas contextuais |

---

## 6. Taxonomia de Espaçamento

Tokens de espaçamento seguem a mesma lógica semântica das cores, com uma convenção de escala numérica. A base é 4px. Cada nível multiplica a base, criando uma progressão harmônica que cobre da menor margem interna até os espaçamentos de layout.

| Token | Valor (px) | Valor (rem) | Uso típico |
|-------|-----------|------------|------------|
| `spacing-1` | 4px | 0.25rem | Padding interno mínimo de ícones |
| `spacing-2` | 8px | 0.5rem | Gap entre ícone e label |
| `spacing-3` | 12px | 0.75rem | Padding de badges e chips |
| `spacing-4` | 16px | 1rem | Padding padrão de botões e inputs |
| `spacing-5` | 20px | 1.25rem | Espaço entre itens de lista |
| `spacing-6` | 24px | 1.5rem | Padding de cards |
| `spacing-8` | 32px | 2rem | Espaço entre seções de formulário |
| `spacing-10` | 40px | 2.5rem | Margens de seções de página |
| `spacing-12` | 48px | 3rem | Altura de headers de seção |
| `spacing-16` | 64px | 4rem | Espaçamento maior entre blocos de layout |

---

## 7. Regras de Governança

### 7.1 Princípios Inegociáveis

**Regra 1:** Nenhum valor de cor, espaçamento ou tipografia deve ser escrito de forma hardcoded em componentes de produção. Todo valor visual precisa referenciar um token.

**Regra 2:** Novos tokens só podem ser criados mediante justificativa semântica documentada. A duplicidade de tokens para o mesmo propósito é considerada débito técnico.

**Regra 3:** O nome do token é imutável após publicação. O valor que ele referencia pode evoluir; o nome não. Renomear um token exige versão maior (v2.0).

**Regra 4:** Tokens de marca (`color-brand-*`) só podem ter seus valores alterados pelo time de branding, mediante aprovação do responsável de marketing.

**Regra 5:** Todo token deve ser documentado com pelo menos um exemplo de uso antes de ser publicado no sistema.

### 7.2 Processo de Adição de Tokens

Quando um designer ou desenvolvedor identifica a necessidade de um novo token, o fluxo é o seguinte: o solicitante verifica se já existe um token semanticamente equivalente. Se existir, usa o token existente. Se não existir, propõe o nome seguindo a taxonomia e documenta o uso. O responsável pelo design system revisa e aprova. O token é adicionado ao Figma e ao repositório de código de forma sincronizada.

### 7.3 Depreciação de Tokens

Um token em desuso deve ser marcado como `deprecated` por pelo menos um ciclo de versão (minor release) antes de ser removido. O token deprecated continua funcional durante o período de transição. A documentação deve registrar qual token o substitui.

---

## 8. Exemplos Práticos por Produto ASB

### 8.1 E-commerce DTC (Shopify)

| Componente | Token aplicado | Elemento |
|------------|----------------|----------|
| Botão Comprar | `color-fill-primary-default` | Background do botão |
| Botão Comprar (hover) | `color-fill-primary-hover` | Background no hover |
| Preço do pacote | `color-brand-primary-default` | Texto do valor em gold |
| Erro de pagamento | `color-fill-danger-default` | Banner de erro |
| Reserva confirmada | `color-fill-success-default` | Notificação de sucesso |

### 8.2 CRM e Customer Success

| Componente | Token aplicado | Elemento |
|------------|----------------|----------|
| Status: ativo | `color-fill-success-default` | Badge de status |
| Status: pendente | `color-fill-warning-default` | Badge de atenção |
| Status: cancelado | `color-fill-danger-default` | Badge crítico |
| Label de segmento VIP | `color-brand-primary-default` | Tag gold para clientes premium |
| Fundo de painel de dados | `color-bg-surface-primary-default` | Container de métricas |

---

## 9. Responsáveis e Versionamento

| Área | Responsabilidade | Contato |
|------|-----------------|---------|
| Marketing Americas | Aprovação de tokens de marca e paleta gold | Head of Marketing |
| Produto & Tech | Implementação e sincronização Figma/código | Tech Lead |
| Design System Owner | Governança, versionamento e documentação | Design Lead |

**Versão atual:** 1.0  
**Data:** Maio 2025  
**Próxima revisão:** Agosto 2025

---

*ABSOLUT Sport | Design System | Documento Interno Confidencial*
