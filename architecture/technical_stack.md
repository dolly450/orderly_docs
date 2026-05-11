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

## 5. Βάση Δεδομένων & Local-First (Έρευνα & Στρατηγική)

Βάσει της πρόσφατης ανάλυσης για την υλοποίηση της offline/local-first απαίτησης (όταν αυτή ενεργοποιηθεί), η στρατηγική είναι η εξής:

### Προτεινόμενη Λύση: Turso / libSQL
Αποτελεί την κορυφαία επιλογή για το συγκεκριμένο μοντέλο (SvelteKit + Golang API) χάρη στα Embedded Replicas.
- **Εγκατάσταση:** Docker container (`ghcr.io/tursodatabase/libsql-server`) ή single binary/embed στο Go app.
- **Πόροι:** Πολύ ελαφρύ (~10-50MB RAM), ιδανικό για Raspberry Pi ή Android (μέσω Termux).
- **Συγχρονισμός (Sync):** Αυτόματος συγχρονισμός (built-in offline-first). Τα microsecond reads γίνονται τοπικά στο SQLite file, και τα writes στέλνονται ταυτόχρονα στο cloud (Turso) και στην τοπική βάση.
- **Υποστήριξη (SDK):** Άψογη υποστήριξη με `libsql/client-go` για Golang και `@libsql/client` (μέσω Drizzle ORM) για το SvelteKit (πλήρης type-safety, migrations).

### Εναλλακτική Επιλογή: PocketBase
Μια εξαιρετική, πιο «plug & play» εναλλακτική.
- **Εγκατάσταση:** Ένα μόνο εκτελέσιμο αρχείο (~15MB), τρέχει χωρίς πρόβλημα σε συσκευές με ελάχιστους πόρους (π.χ., Raspberry Pi 3).
- **Λειτουργίες:** Περιλαμβάνει Auth, Realtime (SSE), Admin UI, και File storage.
- **Συγχρονισμός:** Ενσωμάτωση με Litestream ή Turso modules για σύνδεση με το cloud.
- **Επεκτασιμότητα:** Native υποστήριξη για Go (μέσω Go hooks).

### Απορριφθείσες Λύσεις
- **Supabase Local/Self-hosted:** Αν και ισχυρή επιλογή (Postgres, Auth, Realtime, Edge Functions), είναι πολύ βαριά για παλιές/embedded συσκευές (απαιτεί πολλαπλά containers, >500MB-1GB+ RAM idle). Ο τοπικός <-> cloud συγχρονισμός απαιτεί manual logical replication.
- **CockroachDB (single-node):** Distributed SQL που προσφέρει multi-node native υποστήριξη, αλλά είναι πολύ βαρύ (απαιτεί >4+ vCPU, 4GB+ RAM, υψηλό idle CPU) και περίπλοκο για εγκατάσταση από μη-τεχνικό χρήστη.

### Implementation Notes για το μέλλον
- **Κόστος:** Η λύση της Turso προσφέρει δωρεάν τα Embedded Replicas (ανεξαρτήτως tier), χρεώνοντας μόνο το synchronization. Η λύση είναι δωρεάν για τα πρώτα 500 καταστήματα.
- **Realtime (SSE):** Καθώς το Turso/libSQL δεν διαθέτει built-in realtime (όπως π.χ. η Supabase), το SSE πρέπει να υλοποιηθεί στο επίπεδο του Golang backend ή να γίνει custom polling.
- **Ασφάλεια (RLS):** Δεν υποστηρίζεται Row Level Security εγγενώς. Η προσέγγιση της Turso είναι "database-per-tenant" (1 βάση δεδομένων ανά κατάστημα) εξασφαλίζοντας πλήρη απομόνωση (isolation).
- **Αυθεντικοποίηση (Auth):** Χρειάζεται εξωτερικός πάροχος (π.χ. Better Auth) και χρήση JWT tokens που θα διαβιβάζονται στο libSQL driver.
