# Τεχνική Αρχιτεκτονική (Technical Stack)

Η τρέχουσα υλοποίηση είναι web-first (αρχικά εστιασμένη στο διαδίκτυο) και βελτιστοποιημένη για γρήγορη ανάπτυξη, καθαρό domain separation (διαχωρισμό τομέων) και εύκολη επέκταση ανά χαρακτηριστικό (feature).

## 1. Τρέχον MVP Stack

- **Frontend:** SvelteKit 2, Svelte 5, Tailwind CSS 4
- **Routing / App Shell:** route groups για customer, staff, kitchen και admin
- **Auth:** Better Auth
- **Data:** Drizzle ORM + libSQL/Turso
- **Realtime:** SSE για παραγγελίες, κλήσεις σερβιτόρου (waiter calls), κρατήσεις (reservations), λογαριασμούς (tabs) και πληρότητα (occupancy)
- **i18n:** Paraglide JS
- **Testing:** Vitest
- **Tooling:** Bun

## 2. Βάση Δεδομένων & Στρατηγική Αποθήκευσης (Database & Storage Strategy)

Η εφαρμογή χρησιμοποιεί **Turso Cloud (libSQL)** για τα δεδομένα της. Αυτό επιτρέπει μελλοντική εύκολη μετάβαση σε **Local-First (τοπικά πρώτα)** υποδομή χωρίς αλλαγή του κώδικα (codebase).

### Implementation Logic:
- **Cloud-First Baseline:** Σήμερα χρησιμοποιούμε Turso Cloud (Developer Tier). Κάθε πελάτης (κατάστημα) θα μπορεί να απομονωθεί σε δική του βάση (database-per-tenant) για πλήρη διαχωρισμό (isolation).
- **Embedded Replicas:** Τα δεδομένα συγχρονίζονται τοπικά. Όταν ενεργοποιηθεί η **Tauri V2+** υποδομή στο μέλλον, το τοπικό κατάστημα θα μπορεί να τρέχει τη δική του libSQL replica τοπικά με microsecond reads και να γίνεται συγχρονισμός (sync) στο Turso cloud.
- **Type-Safety:** Χρησιμοποιείται το **Drizzle ORM** (v0.30+) με το `@libsql/client` (TypeScript) για πλήρη προστασία τύπων (type-safety) στο SvelteKit edge/server.
- **Real-Time (SSE):** Καθώς το Turso δεν έχει native realtime features, τα live updates γίνονται μέσω Server-Sent Events (SSE) από το SvelteKit / Golang layer.
- **Self-Hosted Fallback:** Αν ο αριθμός των καταστημάτων αυξηθεί κατακόρυφα (>1000) και το κόστος ανέβει, υπάρχει η επιλογή self-hosting του `libsql-server` (sqld) σε δικά μας VPS χωρίς αλλαγή του κώδικα (ίδιο πρωτόκολλο).

## 3. Τι δεν είναι baseline ακόμα

- Η τοπική συσκευασία (Local-first packaging) με **Tauri v2+** δεν είναι το τρέχον shipping model (μοντέλο διάθεσης).
- Embedded replicas / local gateway (τοπική πύλη) είναι future-phase κατεύθυνση, όχι baseline που στηρίζεται το repo σήμερα. Το app εξυπηρετείται ως cloud-first web app.
- Ενσωματώσεις POS (Ταμειακών Μηχανών) και φορολογικών μηχανισμών είναι σε φάση έρευνας (strategic research).

## 4. Analytics & Tracking

- Το strategy doc έχει επιλέξει **PostHog** ως πιθανή λύση για anonymous conversion tracking (ανώνυμη ιχνηλάτηση μετατροπών).
- Το repo πρέπει να το αντιμετωπίζει ως επόμενη ενσωμάτωση, όχι ως δεδομένο ήδη wired-in stack component.

## 5. Deployment Logic (Λογική Ανάπτυξης)

- Το app τρέχει ως διαδικτυακή εφαρμογή (web application) και το backend logic μένει στο SvelteKit server layer.
- Τα feature-specific modules παραμένουν απομονωμένα μέσα στο feature registry και τα route orchestrators.

## Σχετικές Σημειώσεις

- [[overview]] — High-level architecture.
- [[system_architecture]] — Διάγραμμα ροής.
- [[pos_compliance]] — Φάσεις POS / fiscal integration.
