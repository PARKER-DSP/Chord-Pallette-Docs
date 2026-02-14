window.addEventListener('DOMContentLoaded', () => {
  if (typeof mermaid === 'undefined') {
    return;
  }

  mermaid.initialize({
    startOnLoad: true,
    securityLevel: 'loose',
    theme: 'default',
  });
});
