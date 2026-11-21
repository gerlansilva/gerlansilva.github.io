/* Seletor de idioma: mantém a navegação dentro do idioma escolhido */
(function () {
  var html = document.documentElement;
  var lang = (html.getAttribute("lang") || "pt").toLowerCase().slice(0, 2);
  if (["pt", "en", "es"].indexOf(lang) < 0) lang = "pt";

  var labels = {
    pt: { home: "Início", sobre: "Sobre", pesquisas: "Pesquisas", publicacoes: "Publicações", projetos: "Projetos", apresentacoes: "Apresentações", built: "Feito com", contato: "Contato", sobreFooter: "Sobre", publicacoesFooter: "Publicações" },
    en: { home: "Home", sobre: "About", pesquisas: "Research", publicacoes: "Publications", projetos: "Projects", apresentacoes: "Presentations", built: "Built with", contato: "Contact", sobreFooter: "About", publicacoesFooter: "Publications" },
    es: { home: "Inicio", sobre: "Sobre mí", pesquisas: "Investigación", publicacoes: "Publicaciones", projetos: "Proyectos", apresentacoes: "Presentaciones", built: "Hecho con", contato: "Contacto", sobreFooter: "Sobre mí", publicacoesFooter: "Publicaciones" }
  };

  var sections = {
    "/": "home",
    "/sobre/": "sobre",
    "/pesquisas/": "pesquisas",
    "/publicacoes/": "publicacoes",
    "/projetos/": "projetos",
    "/apresentacoes/": "apresentacoes"
  };

  function norm(path) {
    var p = String(path || "/");
    try {
      p = new URL(p, location.href).pathname;
    } catch (e) {
      p = p.split("?")[0].split("#")[0];
    }
    p = p.replace(/\/index\.html$/, "/");
    p = p.replace(/^\/(en|es)(?=\/|$)/, "") || "/";
    if (p === "") p = "/";
    if (p.charAt(0) !== "/") p = "/" + p;
    return p;
  }

  function prefixFor(l) {
    return l === "pt" ? "" : "/" + l;
  }

  var prefix = prefixFor(lang);
  var here = norm(location.pathname);

  // Botões de idioma: PT, EN e ES sempre visíveis, apontando para a mesma página
  var codes = { pt: "PT", en: "EN", es: "ES" };
  var langLinks = [];
  document.querySelectorAll(".navbar a.nav-link").forEach(function (a) {
    var code = a.textContent.trim().toLowerCase();
    if (!codes[code]) return;
    langLinks.push(a);
    a.dataset.langToggle = "true";
    a.dataset.lang = code;
    a.setAttribute("href", prefixFor(code) + here);
    if (a.parentElement) a.parentElement.classList.add("lang-nav-item");
    if (code === lang) {
      a.dataset.langActive = "true";
      a.setAttribute("aria-current", "true");
    } else {
      a.setAttribute("aria-label", { pt: "Português", en: "English", es: "Español" }[code]);
      a.setAttribute("title", { pt: "Português", en: "English", es: "Español" }[code]);
    }
  });
  if (langLinks.length) {
    langLinks[0].dataset.langFirst = "true";
    langLinks[langLinks.length - 1].dataset.langLast = "true";
  }

  // Navegação principal
  document.querySelectorAll(".navbar a.nav-link").forEach(function (a) {
    if (a.classList.contains("dropdown-toggle") || a.dataset.langToggle) return;
    var url;
    try { url = new URL(a.getAttribute("href"), location.href); } catch (e) { return; }
    if (url.host !== location.host) return;
    var key = sections[norm(url.pathname)];
    if (!key) return;
    a.setAttribute("href", prefix + (key === "home" ? "/" : norm(url.pathname)));
    var span = a.querySelector(".menu-text");
    if (span) span.textContent = labels[lang][key];
    else a.textContent = labels[lang][key];
    if (norm(url.pathname) === here) a.classList.add("active");
  });

  // Marca do site
  var brand = document.querySelector(".navbar-brand");
  if (brand) brand.setAttribute("href", prefix + "/");

  // Rodapé
  var footer = document.querySelector(".gs-footer");
  if (footer) {
    var left = footer.querySelector(".gs-footer-left");
    if (left) {
      left.innerHTML = left.innerHTML.replace(/Feito com|Built with|Hecho con/, labels[lang].built);
    }
    var right = footer.querySelector(".gs-footer-right");
    if (right) {
      right.querySelectorAll("a").forEach(function (a) {
        var key = norm(a.getAttribute("href") || "");
        if (key === "/contato.html" || key === "/contato/") {
          a.setAttribute("href", prefix + "/contato.html");
          a.textContent = labels[lang].contato;
        } else if (key === "/publicacoes/") {
          a.setAttribute("href", prefix + "/publicacoes/");
          a.textContent = labels[lang].publicacoesFooter;
        } else if (key === "/sobre/") {
          a.setAttribute("href", prefix + "/sobre/");
          a.textContent = labels[lang].sobreFooter;
        }
      });
    }
  }
})();
