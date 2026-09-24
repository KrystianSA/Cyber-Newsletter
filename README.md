# Cyber Newsletter

Statyczna strona z formularzem zapisu do newslettera o cyberbezpieczeństwie. Zbudowana w Vue 3 + Vite.

## Uruchomienie

```bash
npm install
npm run dev
```

Domyślnie strona wystartuje pod `http://localhost:5173`.

## Build produkcyjny

```bash
npm run build
```

Wynik trafia do `dist/` — to czysto statyczne pliki, które można wdrożyć na dowolnym hostingu statycznym (Vercel, Netlify, GitHub Pages itp.), bez potrzeby uruchamiania serwera Node.

## Podłączenie realnego newslettera

Formularz w `src/components/NewsletterSignup.vue` na razie **symuluje** zapis adresu e-mail (funkcja `handleSubmit`, `setTimeout` zastępujący prawdziwe wywołanie sieciowe) — nie wysyła danych nigdzie na zewnątrz. Żeby podłączyć realny zapis, w `handleSubmit` zamień blok `await new Promise(...)` na wywołanie wybranej usługi, np.:

- **Buttondown / ConvertKit / Mailchimp** — wywołanie ich API zapisu subskrybenta (`fetch` z kluczem API; klucz API najlepiej trzymać po stronie prostej funkcji serverless, nie w kodzie frontendu).
- **Formspree** lub podobna usługa form-backend — `fetch` na endpoint formularza podany przez usługę.
- **Własna funkcja serverless** (np. Vercel/Netlify Function) zapisująca adres do bazy danych (np. Supabase) — frontend woła własny endpoint, endpoint zapisuje rekord.

W każdym z powyższych przypadków warto też obsłużyć realny stan błędu odpowiedzi API (np. duplikat adresu, limit zapytań) w istniejącej gałęzi `status = 'error'`.
