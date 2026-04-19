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


### Επιλογή Βάσης Δεδομένων (Database Details)
- **Turso (libSQL):** Επιλέχθηκε για την υποστήριξη embedded replicas που προσφέρουν microsecond reads τοπικά, επιτρέποντας δωρεάν syncing για local-first λειτουργία στο μέλλον.
- **Κόστος & Scaling:** Ιδιαίτερα cost-effective για >500 καταστήματα σε σύγκριση με Supabase ή PocketBase, καθώς το pricing model βασίζεται σε active DBs.
- **Περιορισμοί:**
  - **RLS:** Δεν υπάρχει native Row Level Security. Η προτεινόμενη λύση είναι **database-per-tenant** για πλήρη απομόνωση.
  - **Realtime:** Δεν έχει built-in SSE/Realtime (όπως η Supabase). Απαιτείται custom SSE υλοποίηση στο Go backend.
- **SDKs:** Πλήρης υποστήριξη Type-safe Drizzle ORM για το SvelteKit και `@libsql/client-go` για το Go.
- **Self-Hosting:** Διαθέσιμη επιλογή self-hosting με `libsql-server` για περαιτέρω μείωση κόστους στο scale (1.000+ καταστήματα).

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
