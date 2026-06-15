# Τεχνική Αρχιτεκτονική (Technical Stack)

Η τρέχουσα υλοποίηση είναι web-first και βελτιστοποιημένη για γρήγορη ανάπτυξη, καθαρό domain separation και εύκολη επέκταση ανά feature.

## 1. Τρέχον MVP Stack

- **Frontend:** SvelteKit 2, Svelte 5, Tailwind CSS 4
- **Routing / App Shell:** route groups για customer, staff, kitchen και admin
- **Auth:** Better Auth
- **Data:** Drizzle ORM + libSQL/Turso-style storage layer
- **Realtime:** SSE για orders, waiter calls, reservations, tabs και occupancy
- **i18n:** Paraglide JS
- **Testing:** Vitest
- **Tooling:** Bun

## 2. Τι δεν είναι baseline ακόμα

- Local-first packaging με Tauri v2+ δεν είναι το τρέχον shipping model.
- Embedded replicas / local gateway είναι future-phase κατεύθυνση, όχι baseline που στηρίζεται το repo σήμερα.
- Offline sync και local device routing παραμένουν strategic research, όχι production default.

## 3. Analytics & Tracking

- Το strategy doc έχει επιλέξει PostHog ως πιθανή λύση για anonymous conversion tracking.
- Το repo πρέπει να το αντιμετωπίζει ως επόμενη ενσωμάτωση, όχι ως δεδομένο ήδη wired-in stack component.

## 4. Deployment Logic

- Το app τρέχει ως web application και το backend logic μένει στο SvelteKit server layer.
- Τα feature-specific modules παραμένουν απομονωμένα μέσα στο feature registry και τα route orchestrators.

## Σχετικές Σημειώσεις

- [[overview]] — High-level architecture.
- [[system_architecture]] — Διάγραμμα ροής.
- [[pos_compliance]] — Φάσεις POS / fiscal integration.

## 5. Βάση Δεδομένων (Database) - Local-First (Μελλοντική Φάση)

- **Απόφαση:** Επιλέχθηκε Turso/libSQL λόγω χαμηλού overhead, υποστήριξης embedded replicas (τοπικά αντίγραφα) και εύκολου scaling. Η Supabase απορρίφθηκε ως "βαριά" για low-power συσκευές καταστημάτων.
- **ORM:** Drizzle ORM για type-safe (ασφαλή ως προς τους τύπους) ερωτήματα, ειδικά στο SvelteKit.
- **Sync:** Τα δεδομένα γράφονται στο cloud και συγχρονίζονται τοπικά, επιτρέποντας στο μαγαζί να δουλεύει 100% offline με microsecond latency στα reads (αναγνώσεις).
- **Περιορισμοί:** Το libSQL δεν έχει native RLS (Row Level Security - Ασφάλεια επιπέδου γραμμής) ή SSE (Server-Sent Events). Αν χρειαστεί RLS, θα υλοποιηθεί στο application layer. Το SSE υλοποιείται μέσω custom Go backend.
