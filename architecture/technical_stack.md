# Τεχνική Αρχιτεκτονική (Technical Stack)

Η τρέχουσα υλοποίηση είναι web-first και βελτιστοποιημένη για γρήγορη ανάπτυξη, καθαρό domain separation και εύκολη επέκταση ανά feature.

## 1. Τρέχον MVP (Minimum Viable Product - Ελάχιστο Βιώσιμο Προϊόν) Stack

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

### Υλοποίηση Βάσης Δεδομένων (Database Implementation)

*   **Επιλογή:** Turso / libSQL (με SQLite) έναντι Supabase / CockroachDB.
*   **Γιατί:** Ιδανικό για local-first QR ordering (μελλοντική φάση με Tauri v2+). Επιτρέπει embedded replicas, τοπικά reads (microsecond) και αυτόματο cloud sync. Ελαφρύ (low resources) για Raspberry Pi / Android.
*   **Κόστος & Scaling:** Developer tier καλύπτει άνετα. Το storage είναι φθηνό. Το limit είναι τα active databases, όχι το συνολικό πλήθος. Μπορεί να επεκταθεί (scale) με database-per-tenant.
*   **Περιορισμοί & Workarounds:**
    *   *Realtime / SSE:* Υλοποίηση SSE χειροκίνητα στο backend (δεν υπάρχει native).
    *   *RLS (Row Level Security):* Χρήση database-per-tenant ή application-level ελέγχους, καθώς δεν υπάρχει native RLS.
    *   *Auth:* Χρήση εξωτερικού provider (Better Auth) με JWT.
*   **Εναλλακτική:** Self-hosted `libsql-server` (VPS) για εξοικονόμηση κόστους σε 1000+ καταστήματα.

### Οπτικοποίηση: Turso DB Flow (Μελλοντική Φάση Local-first)

```mermaid
flowchart TD
    subgraph Τοπικό Δίκτυο (Local Network)
        Client[Κινητό / Tablet] -->|Reads / Writes| LocalDB[(Embedded Replica - SQLite)]
    end
    subgraph Cloud
        LocalDB -.->|Sync| Turso[(Turso Cloud / libsql-server)]
    end
```
