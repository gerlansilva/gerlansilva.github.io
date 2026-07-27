// LabForMat — comportamentos globais do site
document.addEventListener('DOMContentLoaded', function () {
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.main-nav');

  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var isOpen = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });
  }

  // Formulário de contato: como é um site estático (GitHub Pages),
  // não há back-end. Isso apenas evita envio real e orienta o uso
  // de mailto ou de um serviço de formulários (ver contato.html).
  var form = document.querySelector('#form-contato');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var status = document.querySelector('#form-status');
      if (status) {
        status.textContent = 'Este formulário é apenas um modelo visual. Configure um serviço como Formspree, ou use o e-mail/WhatsApp indicados ao lado, para receber as mensagens de verdade.';
        status.style.display = 'block';
      }
    });
  }
});
