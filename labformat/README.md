# Site do LabForMat

Site institucional do **LabForMat — Laboratório de Formação Docente e Pesquisa em Educação Matemática (UFSC)**.

É um site 100% estático (HTML + CSS + um pouco de JS), sem necessidade de build, framework ou servidor — por isso funciona muito bem no **GitHub Pages**.

## Estrutura de pastas

```
labformat/
├── index.html          → Início
├── sobre.html           → Sobre o LabForMat
├── equipe.html          → Equipe (pesquisadoras/pesquisadores)
├── pesquisa.html         → Linhas de pesquisa e publicações
├── formacao.html         → Formação inicial/continuada (PROFC)
├── extensao.html         → Ações de extensão
├── contato.html          → Contato (formulário de exemplo)
├── assets/
│   ├── css/style.css    → todo o estilo do site (cores, tipografia, layout)
│   ├── js/main.js       → menu mobile + comportamento do formulário
│   └── img/
│       ├── logo-labformat.png
│       └── equipe/      → fotos recortadas dos flyers de cada integrante
└── README.md
```

## Como publicar no GitHub Pages

1. Crie um repositório novo no GitHub (ex: `labformat-ufsc`).
2. Coloque todos os arquivos desta pasta na raiz do repositório (ou dentro de uma pasta `docs/`, se preferir).
3. No GitHub: **Settings → Pages**.
4. Em **Source**, selecione a branch (geralmente `main`) e a pasta (`/root` ou `/docs`).
5. Salve. Em alguns minutos o site estará em algo como:
   `https://SEU-USUARIO.github.io/labformat-ufsc/`

Se quiser um domínio próprio (ex: `labformat.ced.ufsc.br`), dá para configurar um domínio customizado nas mesmas configurações de Pages — mas isso normalmente depende da TI da UFSC liberar o DNS.

## O que ainda precisa de atenção antes de publicar

Alguns conteúdos foram deixados como **placeholder** e devem ser substituídos por informações reais:

- **`contato.html`**: o e-mail `labformat@contato.ufsc.br` e o link do Instagram `@PROFC.UFSC` são exemplos — troque pelos contatos reais do laboratório.
- **`contato.html`**: o formulário é apenas visual. Um site estático não tem como enviar e-mails por conta própria. Para ele funcionar de verdade, duas opções simples:
  - Usar um serviço gratuito como [Formspree](https://formspree.io) ou [Web3Forms](https://web3forms.com) — você só troca o `action` do `<form>` e cola uma chave.
  - Ou simplificar para um botão "mailto:" que abre o cliente de e-mail da pessoa.
- **`pesquisa.html`**: a seção de publicações está vazia de propósito — é só adicionar os itens reais dentro de `.pub-list` seguindo o mesmo padrão de `.pub-item`.
- **Fotos da equipe**: foram recortadas automaticamente dos flyers que você enviou. Se tiver fotos em melhor resolução, é só substituir os arquivos em `assets/img/equipe/` (mantendo os mesmos nomes: `everaldo.png`, `viviane.png`, `regina.png`, `lais.png`).
- **Novos integrantes**: para adicionar alguém à equipe, duplique um `<article class="team-card">` inteiro dentro de `equipe.html` e troque o conteúdo.

## Sobre o design

- **Cores**: extraídas da própria logo do LabForMat — azul-marinho, azul royal, verde-água e dourado (variáveis CSS no topo de `assets/css/style.css`).
- **Tipografia**: título em Fraunces (serifada, com personalidade), texto em Source Sans 3.
- **Elemento de assinatura**: o "fio pontilhado" que aparece na página inicial é uma referência direta ao fio da pipa do logo — e também uma metáfora visual para "rede colaborativa", o conceito central do laboratório.

## Como adicionar uma página nova

1. Copie um arquivo `.html` existente (ex: `extensao.html`) como base.
2. Troque o `<title>`, o conteúdo entre `<section class="page-hero">` e o rodapé.
3. Adicione o link dela em `<nav class="main-nav">` — **em todas as páginas** (já que não há um sistema de "include" automático neste site estático simples).
