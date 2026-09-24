<script setup>
import NewsletterSignup from './components/NewsletterSignup.vue'
</script>

<template>
  <header class="topbar">
    <div class="brand">
      <svg class="brand-icon" viewBox="0 0 32 32" aria-hidden="true">
        <path
          d="M16 5.5 25 9v6.2c0 6.1-3.8 10.9-9 12.3-5.2-1.4-9-6.2-9-12.3V9z"
          fill="none"
          stroke="currentColor"
          stroke-width="1.6"
          stroke-linejoin="round"
        />
        <path
          d="M11.8 16.2l3 3 5.4-6"
          fill="none"
          stroke="currentColor"
          stroke-width="1.8"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
      </svg>
      <span>CyberNewsletter</span>
    </div>
  </header>

  <main class="hero">
    <p class="eyebrow">&gt; cotygodniowy przegląd zagrożeń_</p>
    <h1>
      Bądź o krok przed zagrożeniami,<br />
      zanim staną się problemem.
    </h1>
    <p class="subhead">
      Najważniejsze podatności, incydenty i praktyczne porady z branży
      cyberbezpieczeństwa — w jednej, zwięzłej wiadomości raz w tygodniu.
    </p>

    <NewsletterSignup class="hero-form" />

    <ul class="trust-row">
      <li>🛡️ Bez spamu</li>
      <li>⚡ ~1 e-mail / tydzień</li>
      <li>✕ Rezygnacja jednym kliknięciem</li>
    </ul>
  </main>

  <footer class="footer">
    <p>&copy; {{ new Date().getFullYear() }} CyberNewsletter. Wszystkie prawa zastrzeżone.</p>
  </footer>
</template>

<style scoped>
.topbar {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px 20px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: var(--mono);
  font-size: 15px;
  color: var(--text-h);
  letter-spacing: -0.2px;
}

.brand-icon {
  width: 22px;
  height: 22px;
  color: var(--accent);
  flex-shrink: 0;
}

.hero {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 24px;
  padding: 48px 20px 80px;
  max-width: 720px;
  margin: 0 auto;
  width: 100%;
}

.eyebrow {
  font-family: var(--mono);
  font-size: 13px;
  color: var(--accent);
  letter-spacing: 0.5px;
}

.hero h1 {
  font-size: 44px;
  line-height: 1.15;
  letter-spacing: -1px;
  font-weight: 600;
}

.subhead {
  font-size: 17px;
  color: var(--text);
  max-width: 52ch;
}

.hero-form {
  margin-top: 12px;
  width: 100%;
}

.trust-row {
  list-style: none;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px 20px;
  padding: 0;
  margin: 4px 0 0;
  font-size: 13px;
  color: var(--text-dim);
  font-family: var(--mono);
}

.footer {
  text-align: center;
  padding: 24px 20px;
  border-top: 1px solid var(--border);
  font-size: 13px;
  color: var(--text-dim);
}

@media (max-width: 640px) {
  .hero h1 {
    font-size: 32px;
  }

  .subhead {
    font-size: 15px;
  }
}
</style>
