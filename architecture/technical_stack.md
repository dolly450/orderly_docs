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


## 5. Έρευνα για Τοπική Βάση Δεδομένων (Local-First Database Research) - Ιστορικό / Μελλοντική Φάση (Future Phase)
- **Έρευνα για Local-first DB:** Η καλύτερη λύση για την τοπική (local-first) εφαρμογή παραγγελιών QR (QR ordering app) με SvelteKit + Go στο μέλλον είναι το **Turso/libSQL** ή το **PocketBase**. Το Turso/libSQL είναι η κορυφαία επιλογή λόγω των **Ενσωματωμένων Αντιγράφων (Embedded Replicas)** που συγχρονίζονται (sync) αυτόματα (εξαιρετικά γρήγορες αναγνώσεις τοπικά, εγγραφές στο σύννεφο και τοπικά - microsecond reads τοπικά, writes σε cloud + local).
- **Γιατί απορρίφθηκαν τα Supabase/CockroachDB:** Είναι πολύ βαριά για εξοπλισμό χαμηλών επιδόσεων (low-end hardware, π.χ. Raspberry Pi / παλιό κινητό) και δεν έχουν ενσωματωμένο (built-in) το μοντέλο εναλλακτικής λύσης από τοπικό σε σύννεφο (local<->cloud fallback) με την ίδια ευκολία.
- **Κόστος:** Το Turso Cloud (επίπεδο προγραμματιστή - Developer tier στα $4.99) επιτρέπει 500 ενεργές βάσεις (Active DBs), ενώ τα ενσωματωμένα αντίγραφα (Embedded Replicas) είναι δωρεάν, καθιστώντας το πολύ αποδοτικό για επέκταση (scale).
- **Εναλλακτική:** Το PocketBase προσφέρει μια εμπειρία ενός εκτελέσιμου (single-binary experience - εξαιρετικά απλό) που ίσως εξυπηρετεί καλύτερα συγκεκριμένα σενάρια εγκατάστασης (deployment scenarios, π.χ. Android μέσω Termux).
