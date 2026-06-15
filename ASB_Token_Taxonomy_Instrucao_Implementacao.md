# Como introduzir a Taxonomia de Design Tokens no ASB Design System
**Instrução de implementação — Mauricio Lacerda × Raphael Ferreira**  
**Referência: `ASB_Design_Token_Taxonomy_v1.md` | Design System v1.0**

---

## Contexto e ponto de partida

Este documento é uma instrução de implementação. Ele responde à pergunta: dado que o ASB Design System (https://mauricioslacerda-jpg.github.io/absolut-sport-design-system/) já existe e está vivo em v1.0, como introduzimos a taxonomia semântica de três camadas sem quebrar nada que já funciona?

A resposta curta é: o sistema já está na metade do caminho. O `colors-semantic.html` já usa nomes funcionais como `--bg-surface`, `--fg-primary`, `--accent-gold` e `--status-success`. Isso é uma convenção de duas camadas. A taxonomia completa adiciona uma terceira — o estado — e padroniza o prefixo `color-` em toda a arquitetura. A migração é cirúrgica, não uma refatoração destrutiva.

---

## Passo 1: Diagnóstico — mapear o que já existe

Antes de tocar em qualquer arquivo, o Rafa e o dev responsável precisam fazer um inventário completo dos tokens ativos em `colors_and_type.css` (publicado em `design.absolut-sport.com.br/colors_and_type.css`). O objetivo é ter uma planilha de mapeamento com três colunas: o nome atual do token, o nome novo na taxonomia e o valor hex que permanece intacto.

O mapeamento dos tokens já visíveis no design system é o seguinte:

**Backgrounds**

| Token atual | Token novo (taxonomia) | Valor |
|-------------|------------------------|-------|
| `--bg-base` | `--color-bg-default` | `#FAFAFA` |
| `--bg-surface` | `--color-bg-surface-primary-default` | (verificar no CSS) |
| `--bg-card` | `--color-bg-surface-secondary-default` | (verificar no CSS) |
| `--bg-brand` | `--color-bg-brand-default` | `#155F97` |
| `--bg-dark` | `--color-bg-inverse-default` | `#0D0D0D` |

**Texto (Foregrounds)**

| Token atual | Token novo (taxonomia) | Valor |
|-------------|------------------------|-------|
| `--fg-primary` | `--color-text-primary-default` | (verificar no CSS) |
| `--fg-secondary` | `--color-text-secondary-default` | (verificar no CSS) |
| `--fg-muted` | `--color-text-tertiary-default` | (verificar no CSS) |
| `--fg-inverse` | `--color-text-inverse-default` | (verificar no CSS) |

**Acentos e interação**

| Token atual | Token novo (taxonomia) | Valor |
|-------------|------------------------|-------|
| `--accent-primary` | `--color-fill-primary-default` | `#155F97` |
| `--accent-highlight` | `--color-fill-primary-hover` | `#2857F7` |
| `--accent-gold` | `--color-fill-brand-vip-default` | `#C9A84C` |
| `--accent-gray` | `--color-border-secondary-default` | `#C0C0C0` |

**Status**

| Token atual | Token novo (taxonomia) | Valor |
|-------------|------------------------|-------|
| `--status-success` | `--color-fill-success-default` | `#22C55E` |
| `--status-warning` | `--color-fill-warning-default` | (verificar no CSS) |
| `--status-error` | `--color-fill-danger-default` | `#E3001B` |

**Espaçamento** — a convenção atual (`--space-1` a `--space-24`) já está alinhada com a taxonomia e não precisa ser renomeada. A escala de 4px está correta. Nenhuma alteração necessária aqui.

**Motion** — os tokens `--transition-fast`, `--transition-default` e `--transition-slow` também estão corretos e não precisam ser migrados.

---

## Passo 2: Decisão de arquitetura — migração ou camada adicional?

Existem dois caminhos possíveis e é preciso escolher um antes de qualquer implementação.

**Caminho A — Migração direta (recomendado para v1.0 → v1.1):** renomear os tokens no CSS e atualizar todas as referências nos componentes. Como o sistema está em v1.0 e relativamente novo, o número de referências ainda é controlável. A vantagem é que o sistema fica limpo e sem aliases. A desvantagem é que qualquer código que já usa os tokens antigos em produtos externos (Shopify, landing pages, e-mails) precisa ser atualizado simultaneamente.

**Caminho B — Aliases transitórios (estratégia de zero-downtime):** manter os tokens antigos funcionando e apontar os novos nomes para os mesmos valores. O CSS ficaria assim:

```css
/* Novo token canônico */
--color-bg-surface-primary-default: #F5F5F5;

/* Alias de compatibilidade — marcado como deprecated */
--bg-surface: var(--color-bg-surface-primary-default); /* @deprecated v1.1 */
```

Essa abordagem permite que os times de produto migrem no próprio ritmo sem quebrar nada imediatamente. O alias é removido na v2.0.

**Recomendação:** usar o Caminho B para a primeira publicação da taxonomia, com prazo de 60 dias para os times migrarem antes de remover os aliases na v2.0.

---

## Passo 3: Adicionar os tokens de estado que estão faltando

O diagnóstico mostra que o sistema atual não tem tokens para os estados `hover`, `active`, `focus` e `disabled`. Esses tokens precisam ser criados do zero, não migrados. A fonte de verdade para os valores deve ser os componentes do Figma que o Rafa mantém.

Para cada token de interação no sistema, os valores de estado seguem uma lógica de manipulação de luminosidade: `hover` é tipicamente 10% mais claro ou mais escuro que `default`, e `active` é 15% na direção contrária. Para a paleta ASB:

```css
/* Exemplo de cadeia completa para o botão primário */
--color-fill-primary-default:  #155F97;
--color-fill-primary-hover:    #1E7ABE;  /* Azul Mid — já existe na blue scale */
--color-fill-primary-active:   #0F4A75;  /* Azul Dark — já existe na blue scale */
--color-fill-primary-disabled: #8BAFC8;  /* 50% opacidade do Azul ASB */
--color-fill-primary-focus:    #155F97;  /* igual ao default, com outline externo */
```

Isso significa que a blue scale que já existe no brand core (`Azul Dark #0F4A75`, `Azul ASB #155F97`, `Azul Mid #1E7ABE`, `Highlight #2857F7`) já é a fonte para preencher esses estados. Não é necessário criar valores novos — é necessário nomear os valores existentes de forma que o estado fique explícito.

---

## Passo 4: Atualizar o arquivo `colors_and_type.css`

Essa é a única alteração de código real necessária para que a taxonomia entre em vigor. O arquivo deve ser estruturado em blocos comentados que espelham a taxonomia:

```css
/* ============================================================
   ABSOLUT SPORT — Design Tokens v1.1
   Taxonomia: color-[elemento]-[hierarquia]-[estado]
   Maintainer: Raphael Ferreira · raphael.ferreira@absolut-sport.com.br
   ============================================================ */

/* --- BRAND --- */
:root {
  --color-brand-primary-default:   #155F97;
  --color-brand-highlight-default: #2857F7;
  --color-brand-vip-default:       #C9A84C;  /* Gold */
  --color-brand-gray-default:      #C0C0C0;

  /* --- BACKGROUND --- */
  --color-bg-default:                       #FAFAFA;
  --color-bg-surface-primary-default:       /* valor do Figma */;
  --color-bg-surface-secondary-default:     /* valor do Figma */;
  --color-bg-brand-default:                 #155F97;
  --color-bg-inverse-default:               #0D0D0D;

  /* --- TEXT --- */
  --color-text-primary-default:   /* valor do Figma */;
  --color-text-secondary-default: /* valor do Figma */;
  --color-text-tertiary-default:  /* valor do Figma */;
  --color-text-inverse-default:   /* valor do Figma */;

  /* --- FILL (botões, badges, interativos) --- */
  --color-fill-primary-default:   #155F97;
  --color-fill-primary-hover:     #1E7ABE;
  --color-fill-primary-active:    #0F4A75;
  --color-fill-primary-disabled:  #8BAFC8;

  /* --- BORDER --- */
  --color-border-primary-default:   /* valor do Figma */;
  --color-border-secondary-default: #C0C0C0;

  /* --- STATUS --- */
  --color-fill-success-default: #22C55E;
  --color-fill-warning-default: /* valor do Figma */;
  --color-fill-danger-default:  #E3001B;

  /* --- ALIASES DE COMPATIBILIDADE (remover na v2.0) --- */
  --bg-base:         var(--color-bg-default);
  --bg-surface:      var(--color-bg-surface-primary-default);
  --fg-primary:      var(--color-text-primary-default);
  --accent-primary:  var(--color-fill-primary-default);
  --accent-gold:     var(--color-brand-vip-default);
  --status-success:  var(--color-fill-success-default);
  --status-error:    var(--color-fill-danger-default);
}
```

Os valores marcados como "valor do Figma" precisam ser preenchidos pelo Rafa exportando o token value diretamente do arquivo Figma de referência, garantindo que o CSS e o Figma estejam em sincronia perfeita.

---

## Passo 5: Criar a nova seção "Tokens" no `index.html`

A página principal do design system já tem um âncora `#tokens` no rodapé mas não tem uma seção dedicada à taxonomia no corpo da página. A instrução é adicionar uma seção entre o bloco de Cores (`#cores`) e o bloco de Tipografia (`#tipografia`), com âncora `#tokens`.

A seção deve conter três elementos visuais: um diagrama de anatomia do token mostrando as três camadas com codificação de cor (o mesmo conceito do post do Memorisely), uma tabela de todos os tokens canônicos da ASB com o nome, o valor e o papel, e um bloco de código copiável mostrando o padrão de uso correto versus o anti-padrão hardcoded.

O padrão visual da seção deve seguir exatamente o padrão das outras seções do site: fundo alternando entre claro e escuro, headline em SoulCraft, grid de cards para os tokens, e o padrão de codificação "Clique para copiar" que já existe nas seções de cores.

---

## Passo 6: Criar a página `preview/token-taxonomy.html`

Seguindo o padrão das 13 páginas de preview que já existem (como `preview/colors-semantic.html` e `preview/spacing-tokens.html`), é necessário criar uma nova página de preview dedicada à taxonomia. Essa página deve ser adicionada ao catálogo de componentes do `index.html` como o 14º card.

O conteúdo da página de preview deve seguir a estrutura da `colors-semantic.html` como referência direta, mas expandida para mostrar as cadeias de estado completas. Para cada elemento de UI (bg, text, fill, border, icon), a página deve renderizar todos os estados em sequência: default, hover, active, disabled.

O cartão no catálogo de componentes do `index.html` deve ter o mesmo formato dos outros 13, com o seguinte conteúdo:

```html
<a href="preview/token-taxonomy.html">
  <span class="card-icon">⬡</span>
  <span class="card-category">Tokens</span>
  <span class="card-name">Token Taxonomy</span>
  <span class="card-cta">Ver preview</span>
</a>
```

---

## Passo 7: Atualizar a seção "Para Devs"

A seção de implementação para desenvolvedores (`#devs`) no `index.html` atualmente mostra três exemplos de uso de tokens: `--color-blue`, `--color-white` e `--font-display`. Esses três exemplos precisam ser atualizados para refletir a nova nomenclatura de três camadas e mostrar um exemplo de cadeia de estados.

O bloco de código atualizado deve ficar assim:

```css
/* Antes: nomenclatura parcial */
.cta {
  background: var(--color-blue);     /* sem camada de estado */
  color: var(--color-white);         /* sem semântica de uso */
}

/* Depois: taxonomia completa */
.cta {
  background: var(--color-fill-primary-default);
  color:       var(--color-text-inverse-default);
  font-family: var(--font-display);
  padding:     var(--space-3) var(--space-6);
  border-radius: var(--radius-sm);
}

.cta:hover {
  background: var(--color-fill-primary-hover);    /* estado explícito */
}

.cta:active {
  background: var(--color-fill-primary-active);   /* estado explícito */
}

.cta:disabled {
  background: var(--color-fill-primary-disabled); /* estado explícito */
  cursor: not-allowed;
}
```

Esse bloco faz dois trabalhos ao mesmo tempo: mostra a nova convenção de nomenclatura e mostra que cada estado de interação tem um token próprio, o que é o comportamento esperado de um sistema maduro.

---

## Passo 8: Atualizar o AI Playbook

O AI Playbook (`playbooks/ai-marketing.html`) já tem um item marcado como "Em progresso" chamado "Design System como contexto AI". A introdução da taxonomia é exatamente o que completa esse item. Quando os tokens estiverem nomeados de forma semântica e documentados na página de preview, o bloco de contexto que qualquer pessoa do time pode colar num prompt de AI ficará assim:

```
Design System ABSOLUT Sport — Taxonomia de Tokens
Fonte: design.absolut-sport.com.br/colors_and_type.css

BRAND: --color-brand-primary-default: #155F97 (Azul ASB)
       --color-brand-vip-default: #C9A84C (Gold VIP)

FILL:  --color-fill-primary-default: #155F97
       --color-fill-primary-hover: #1E7ABE
       --color-fill-success-default: #22C55E
       --color-fill-danger-default: #E3001B

TEXT:  --color-text-primary-default: [valor]
       --color-text-inverse-default: #FAFAFA

SPACE: --space-4: 16px | --space-6: 24px | --space-8: 32px
```

Esse bloco deve ser adicionado ao Playbook como um terceiro link ao lado do Global Asset List e do Design System, com o título "Token Context Block" e a instrução: "Cole isso no início de qualquer prompt que precise gerar HTML, CSS ou Figma alinhado à marca."

O status do item no AI Playbook muda de "Em progresso" para "Concluído" após os passos 4 a 7 deste documento serem executados.

---

## Ordem de execução recomendada

A sequência importa porque alguns passos dependem de outros. O passo 1 (diagnóstico e mapeamento) é bloqueante para todos os outros — sem a planilha de mapeamento completa com os valores reais do CSS, nenhum outro passo pode ser executado com segurança.

O passo 4 (atualizar o CSS) deve ser feito em staging antes de publicar, porque é a única alteração que pode impactar produtos que já usam os tokens antigos. Os aliases de compatibilidade são exatamente a rede de segurança para esse momento.

Os passos 5, 6 e 7 (seção no index, nova página de preview, atualização da seção devs) são puramente aditivos — não modificam nada existente, apenas adicionam conteúdo novo. Podem ser feitos em qualquer ordem depois que o CSS estiver em produção.

O passo 8 (AI Playbook) é o último porque depende de tudo anterior estar publicado para que o bloco de contexto seja real e não aspiracional.

**Resumo da sequência:**

1. Rafa exporta valores reais do Figma e preenche a planilha de mapeamento
2. Criar a planilha de mapeamento com os aliases de compatibilidade
3. Atualizar `colors_and_type.css` em staging e validar que nenhum componente quebra
4. Publicar CSS atualizado em produção
5. Adicionar seção `#tokens` no `index.html`
6. Criar `preview/token-taxonomy.html` e adicionar ao catálogo
7. Atualizar bloco de código na seção "Para Devs"
8. Atualizar o AI Playbook e marcar item como concluído

**Prazo estimado para execução completa:** 2 a 3 dias de trabalho do Rafa, dado que todos os valores do Figma já existem e o padrão visual das páginas de preview é um template estabelecido.

---

## O que não mudar

Três coisas no sistema atual estão corretas e não precisam ser tocadas:

A escala de espaçamento (`--space-1` a `--space-24`) já segue a lógica de múltiplos de 4px e os nomes numéricos são suficientemente universais para não precisar de semântica adicional. Renomear para `--spacing-1` seria uma mudança cosmética sem ganho real.

Os tokens de motion (`--transition-fast`, `--transition-default`, `--transition-slow`) são semanticamente corretos e amplamente compreendidos por qualquer desenvolvedor sem necessidade de documentação adicional.

A convenção de border radius (`sm`, `md`, `lg`, `xl`, `pill`) também está correta e não precisa de migração.

---

*Instrução criada por Mauricio Lacerda — Head of Marketing Americas*  
*Para execução por Raphael Ferreira — Design Lead*  
*Referência: `ASB_Design_Token_Taxonomy_v1.md` na mesma pasta*  
*Versão: 1.0 | Maio 2025*
