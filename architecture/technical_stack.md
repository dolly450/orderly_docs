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

## 5. Βάση Δεδομένων & Τοπικός Συγχρονισμός (Database & Local Sync)

- **Cloud DB:** Turso (libSQL) στο Developer tier προσφέρει επαρκές capacity με πολύ χαμηλό κόστος (>$5/μήνα για μέχρι 500 active DBs) και απρόσκοπτο scaling.
- **Local-first Data:** Υποστήριξη για Embedded Replicas (απεριόριστα δωρεάν), τα οποία συγχρονίζουν με το Cloud και προσφέρουν microsecond reads τοπικά.
- **ORM:** Drizzle ORM για type-safe queries. Επίσημη υποστήριξη για libSQL/Turso (TS) σε SvelteKit server+edge.
- **Self-hosted Fallback:** Δυνατότητα εύκολης μετάβασης σε self-hosted libsql-server (πρώην sqld) σε VPS για μεγαλύτερα scales (1.000+ καταστήματα) χωρίς αλλαγή του protocol ή του κώδικα.
- **Σημείωση για SSE & Auth:** Το libSQL είναι lightweight και δεν διαθέτει built-in Realtime ή Auth. Αυτά αντιμετωπίζονται application-level: Custom Auth μέσω JWT (π.χ. Better Auth) και SSE connections διαχειριζόμενα απευθείας στο web layer.
