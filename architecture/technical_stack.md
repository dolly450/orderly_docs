# Τεχνική Αρχιτεκτονική (Technical Stack)

Η τρέχουσα υλοποίηση είναι web-first και βελτιστοποιημένη για γρήγορη ανάπτυξη, καθαρό domain separation και εύκολη επέκταση ανά feature. Τοπική αρχιτεκτονική και διαχείριση βάσης δεδομένων ερευνώνται για μελλοντικές φάσεις λειτουργίας (offline-first).

## 1. Τρέχον MVP Stack

- **Frontend:** SvelteKit 2, Svelte 5, Tailwind CSS 4
- **Routing / App Shell:** route groups για customer, staff, kitchen και admin
- **Auth:** Better Auth (Εξωτερική λύση Auth καθώς το Turso δεν παρέχει native)
- **Data:** Drizzle ORM + libSQL/Turso Cloud (Developer Tier). Το Drizzle παρέχει type-safety σε TypeScript/SvelteKit.
- **Realtime:** SSE για orders, waiter calls, reservations, tabs και occupancy. Το SSE στήνεται στο backend καθώς η libSQL δεν έχει native realtime endpoints (όπως η Supabase).
- **i18n:** Paraglide JS
- **Testing:** Vitest
- **Tooling:** Bun

## 2. Βάση Δεδομένων & Local-First Architecture (Turso/libSQL)

Για την αντιμετώπιση του offline προβλήματος στα νησιά, επιλέχθηκε το **Turso / libSQL**.
- **Embedded Replicas:** Τα αρχεία SQLite αποθηκεύονται τοπικά (local) στις συσκευές και συγχρονίζονται ασύγχρονα με το Turso Cloud, εξασφαλίζοντας μηδενικό latency και offline λειτουργία.
- **Κόστος & Scaling:** Το Developer tier ($4.99) παρέχει απεριόριστα (unlimited) Embedded Replicas. Τα syncs κοστίζουν ελάχιστα.
- **Μειονεκτήματα προς Διαχείριση:**
  - Δεν υπάρχει native Row Level Security (RLS). Λύση: Database-per-tenant (1 DB ανά κατάστημα) για πλήρη απομόνωση (isolation).
  - Δεν υπάρχει native Auth. Η διαχείριση γίνεται σε application level (Better Auth).
  - Εναλλακτική μελλοντική φάση είναι το Self-hosted `libsql-server` σε VPS.

## 3. Τι δεν είναι baseline ακόμα

- Local-first packaging με Tauri v2+ δεν είναι το τρέχον shipping model.
- Embedded replicas / local gateway είναι future-phase κατεύθυνση, όχι baseline που στηρίζεται το repo σήμερα.
- Offline sync και local device routing παραμένουν strategic research, όχι production default.

## 4. Analytics & Tracking

- Το strategy doc έχει επιλέξει PostHog ως πιθανή λύση για anonymous conversion tracking.
- Το repo πρέπει να το αντιμετωπίζει ως επόμενη ενσωμάτωση, όχι ως δεδομένο ήδη wired-in stack component.

## 5. Deployment Logic

- Το app τρέχει ως web application και το backend logic μένει στο SvelteKit server layer.
- Τα feature-specific modules παραμένουν απομονωμένα μέσα στο feature registry και τα route orchestrators.

## Σχετικές Σημειώσεις

- [[overview]] — High-level architecture.
- [[system_architecture]] — Διάγραμμα ροής.
- [[pos_compliance]] — Φάσεις POS / fiscal integration.