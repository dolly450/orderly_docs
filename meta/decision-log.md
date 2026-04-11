# Ημερολόγιο Αποφάσεων (Decision Log)

### 2026-04-10 - Επιλογή Βάσης Δεδομένων (Database Selection for Local-First)
- **Απόφαση / Σύνοψη:** Επιλογή του Turso/libSQL με embedded replicas για την υποστήριξη του local-first ordering. Επιτρέπει εγκατάσταση με ένα binary, microsecond reads τοπικά, και αυτόματο cloud sync. Το Supabase θεωρήθηκε βαρύ για τα local requirements (Pi/Android), ενώ το CockroachDB απορρίφθηκε ως υπερβολικό.
- **Αρχεία που ενημερώθηκαν:** [[architecture/technical_stack.md]]
- **Σημείωση για Implementation:** Θα χρησιμοποιηθεί Drizzle ORM για το SvelteKit (αν χρειαστεί TS) ή native `database/sql` + `sqlc` στο Golang backend. Δεν υπάρχει native SSE, άρα θα υλοποιηθεί στο Go API. RLS (Row Level Security) υλοποιείται μέσω "database-per-tenant" ή σε επίπεδο εφαρμογής.

### 2026-04-10 - Στρατηγική Προϊόντος (Product Strategy: Integration vs Replacement)
- **Απόφαση / Σύνοψη:** Στρατηγική Direct Sales & Integration. Το σύστημα θα στέλνει παραγγελίες κατευθείαν στο υπάρχον POS (π.χ., Epsilon Net) λειτουργώντας ως self-service layer, αντί να αντικαταστήσει τα υπάρχοντα PDA του προσωπικού, μειώνοντας δραστικά το friction της πώλησης (adoption friction).
- **Αρχεία που ενημερώθηκαν:** [[business/market_strategy.md]]
- **Σημείωση για Implementation:** Το Phase 2 MVP θα εστιάσει στο API integration με τα POS. Δεν απαιτείται πλήρες Staff Dashboard για παραγγελιοληψία από σερβιτόρους, παρά μόνο για διαχείριση εκκρεμοτήτων.

### 2026-04-10 - Τοπική Αρχιτεκτονική MVP (Local-first MVP Architecture)
- **Απόφαση / Σύνοψη:** Επιλογή του Tauri v2+ για την υλοποίηση του local-first ordering setup (με server και DB), ως ένα απλό, cross-platform εκτελέσιμο (one-click install) χωρίς να χρειάζεται περίπλοκο setup. Για DB επιλέχθηκε Turso/libSQL cloud με embedded replicas τοπικά.
- **Αρχεία που ενημερώθηκαν:** [[architecture/technical_stack.md]], [[architecture/system_architecture.md]], [[meta/active_investigations.md]]
- **Σημείωση για Implementation:** Ξεκινάμε με SvelteKit Cloud-only (V1) και προσθέτουμε το Tauri v2 local-first αργότερα (V2) χωρίς αλλαγές στο web frontend.
### 2026-04-10 - Analytics Setup (Data Tracking)
- **Απόφαση / Σύνοψη:** Επιλογή του PostHog για το track-άρισμα του conversion rate (OMTM) ανώνυμα χωρίς login.
- **Αρχεία που ενημερώθηκαν:** [[architecture/technical_stack.md]], [[notes/Product Design.md]]
- **Σημείωση για Implementation:** Χρήση distinct IDs στο SvelteKit frontend (χωρίς Auth requirement).

### 2026-04-10 - Στρατηγική Πωλήσεων Φάσης 1 (Phase 1 Sales)
- **Απόφαση / Σύνοψη:** Επιλογή του "Direct sales (walking in)" με ένα "Fake MVP" demo.
- **Αρχεία που ενημερώθηκαν:** [[business/market_strategy.md]]
- **Σημείωση για Implementation:** Δεν χρησιμοποιούμε automated emails ακόμα. Tracking μέσω απλού CRM (Planka).
