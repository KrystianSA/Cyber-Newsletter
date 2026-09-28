<script setup>
import { computed, ref } from 'vue'

const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

const email = ref('')
const status = ref('idle') // idle | loading | success | error
const errorMessage = ref('')

const isLoading = computed(() => status.value === 'loading')
const isSuccess = computed(() => status.value === 'success')

async function handleSubmit() {
  const value = email.value.trim()

  if (!value) {
    status.value = 'error'
    errorMessage.value = 'Podaj adres e-mail.'
    return
  }

  if (!EMAIL_PATTERN.test(value)) {
    status.value = 'error'
    errorMessage.value = 'Ten adres e-mail wygląda na nieprawidłowy.'
    return
  }

  status.value = 'loading'
  errorMessage.value = ''

  try {
    const res = await fetch(`${API_URL}/subscribers`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: value }),
    })

    if (res.status === 409) {
      status.value = 'error'
      errorMessage.value = 'Ten adres e-mail jest już zapisany.'
      return
    }

    if (!res.ok) {
      status.value = 'error'
      errorMessage.value = 'Coś poszło nie tak. Spróbuj ponownie.'
      return
    }

    status.value = 'success'
  } catch {
    status.value = 'error'
    errorMessage.value = 'Brak połączenia z serwerem. Spróbuj ponownie.'
  }
}

function handleReset() {
  email.value = ''
  status.value = 'idle'
  errorMessage.value = ''
}
</script>

<template>
  <div class="signup-card">
    <template v-if="!isSuccess">
      <form class="signup-form" novalidate @submit.prevent="handleSubmit">
        <label class="field-label" for="email">Adres e-mail</label>
        <div class="field-row">
          <div class="input-wrap" :class="{ 'input-wrap--error': status === 'error' }">
            <span class="prompt" aria-hidden="true">&gt;</span>
            <input
              id="email"
              v-model="email"
              type="email"
              name="email"
              autocomplete="email"
              placeholder="ty@firma.pl"
              :disabled="isLoading"
              :aria-invalid="status === 'error'"
              aria-describedby="email-error"
              @input="status === 'error' && (status = 'idle')"
            />
          </div>
          <button type="submit" class="submit-btn" :disabled="isLoading">
            <span v-if="!isLoading">Zapisz się</span>
            <span v-else>Zapisywanie…</span>
          </button>
        </div>
        <p v-if="status === 'error'" id="email-error" class="field-error" role="alert">
          {{ errorMessage }}
        </p>
      </form>
      <p class="disclaimer">
        Zero spamu. ~1 e-mail tygodniowo. Rezygnacja jednym kliknięciem.
      </p>
    </template>

    <div v-else class="success-state" role="status">
      <div class="success-icon" aria-hidden="true">✓</div>
      <h3>Jesteś zapisany/a</h3>
      <p>Potwierdziliśmy adres <strong>{{ email }}</strong> na liście. Pierwszy przegląd zagrożeń wkrótce w Twojej skrzynce.</p>
      <button type="button" class="link-btn" @click="handleReset">Zapisz inny adres</button>
    </div>
  </div>
</template>

<style scoped>
.signup-card {
  width: 100%;
  max-width: 480px;
  margin: 0 auto;
}

.signup-form {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.field-label {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
}

.field-row {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.input-wrap {
  flex: 1 1 220px;
  display: flex;
  align-items: center;
  gap: 8px;
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 0 14px;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.input-wrap:focus-within {
  border-color: var(--accent-border);
  box-shadow: 0 0 0 3px var(--accent-bg);
}

.input-wrap--error {
  border-color: var(--danger);
}

.prompt {
  font-family: var(--mono);
  color: var(--accent);
  font-size: 15px;
}

.input-wrap input {
  flex: 1;
  min-width: 0;
  background: transparent;
  border: none;
  outline: none;
  color: var(--text-h);
  font-family: var(--mono);
  font-size: 15px;
  padding: 14px 0;
}

.input-wrap input::placeholder {
  color: var(--text-dim);
}

.submit-btn {
  flex: 0 0 auto;
  background: var(--accent);
  color: #04150c;
  font-weight: 600;
  font-size: 15px;
  border: 1px solid var(--accent);
  border-radius: 10px;
  padding: 0 22px;
  cursor: pointer;
  transition: background 0.2s, box-shadow 0.2s, transform 0.1s;
}

.submit-btn:hover:not(:disabled) {
  background: var(--accent-strong);
  box-shadow: 0 0 24px rgba(62, 224, 139, 0.35);
}

.submit-btn:active:not(:disabled) {
  transform: translateY(1px);
}

.submit-btn:disabled {
  opacity: 0.65;
  cursor: progress;
}

.field-error {
  color: var(--danger);
  font-size: 13px;
  font-family: var(--mono);
  margin: 2px 2px 0;
}

.disclaimer {
  margin-top: 14px;
  text-align: center;
  font-size: 13px;
  color: var(--text-dim);
}

.success-state {
  text-align: center;
  border: 1px solid var(--accent-border);
  background: var(--accent-bg);
  border-radius: 14px;
  padding: 32px 28px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.success-icon {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: var(--accent);
  color: #04150c;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  font-weight: 700;
}

.success-state h3 {
  font-size: 20px;
}

.success-state p {
  color: var(--text);
  font-size: 14px;
  max-width: 36ch;
}

.link-btn {
  margin-top: 6px;
  background: none;
  border: none;
  color: var(--accent);
  font-family: var(--mono);
  font-size: 13px;
  text-decoration: underline;
  cursor: pointer;
  padding: 4px;
}

@media (max-width: 480px) {
  .field-row {
    flex-direction: column;
  }

  .submit-btn {
    padding: 14px;
  }
}
</style>
