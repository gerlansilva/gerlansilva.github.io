# gerlansilva.github.io

Página pessoal de pesquisador hospedada no GitHub Pages.

## 🚀 Como publicar no GitHub

### 1. Criar o repositório

1. Acesse [github.com/new](https://github.com/new)
2. Nome do repositório: **`gerlansilva.github.io`** (exatamente assim)
3. Visibilidade: **Public**
4. Clique em **Create repository**

---

### 2. Enviar os arquivos

No terminal, dentro da pasta do projeto:

```bash
git init
git add .
git commit -m "🚀 Primeiro commit"
git branch -M main
git remote add origin https://github.com/gerlansilva/gerlansilva.github.io.git
git push -u origin main
```

---

### 3. Ativar o GitHub Pages

1. No repositório, vá em **Settings → Pages**
2. Em *Source*, selecione **Deploy from a branch**
3. Branch: **main** / pasta: **/ (root)**
4. Clique em **Save**

Aguarde 1–2 minutos. O site estará em:
**https://gerlansilva.github.io**

---

### 4. Ativar permissões para o GitHub Actions

1. Vá em **Settings → Actions → General**
2. Em *Workflow permissions*, selecione:
   - ✅ **Read and write permissions**
3. Clique em **Save**

---

### 5. Adicionar sua foto

1. Coloque sua foto em `assets/img/foto.jpg`
2. No `index.html`, substitua o bloco:
   ```html
   <span class="placeholder">👤</span>
   ```
   Por:
   ```html
   <img src="assets/img/foto.jpg" alt="Gerlan Silva da Silva" />
   ```
3. Faça `git add . && git commit -m "Adiciona foto" && git push`

---

## 📁 Estrutura do projeto

```
gerlansilva.github.io/
├── index.html                        ← site principal
├── assets/
│   └── img/
│       └── foto.jpg                  ← sua foto (adicionar)
├── scripts/
│   └── fetch_orcid.py                ← busca publicações do ORCID
├── _bibliography/
│   └── papers.bib                    ← gerado automaticamente
├── .github/
│   └── workflows/
│       └── update_publications.yml   ← automação semanal
└── README.md
```

---

## 🔄 Atualização automática de publicações

O workflow `update_publications.yml` roda toda **segunda-feira às 8h (Brasília)**:
- Busca seus artigos na API do ORCID
- Atualiza o `_bibliography/papers.bib`
- Faz commit automático se houver novidades

Para rodar manualmente: **Actions → 🔄 Atualizar Publicações → Run workflow**

---

## ✏️ Como editar o site

Todos os textos estão no `index.html`. Basta editar e fazer push:

```bash
git add index.html
git commit -m "Atualiza bio"
git push
```

O GitHub Pages atualiza em 1–2 minutos.
