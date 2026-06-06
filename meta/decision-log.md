# Ημερολόγιο Αποφάσεων (Decision Log)

### 2026-04-10 - Αρχιτεκτονική MVP (Cloud-first Web App)
- **Απόφαση / Σύνοψη:** Το τρέχον baseline του προϊόντος είναι cloud-first web εφαρμογή σε SvelteKit. Η local-first / Tauri κατεύθυνση παραμένει ερευνητική επιλογή για μελλοντική φάση, όχι το shipped μοντέλο.
- **Αρχεία που ενημερώθηκαν:** [[architecture/technical_stack.md]], [[architecture/system_architecture.md]], [[meta/active_investigations.md]]
- **Σημείωση για Implementation:** Κρατάμε το web frontend ως κύρια βάση και αφήνουμε το local-first packaging για ξεχωριστή φάση όταν το ζητήσει το προϊόν.
### 2026-04-10 - Analytics Setup (Data Tracking)
- **Απόφαση / Σύνοψη:** Επιλογή του PostHog για το track-άρισμα του conversion rate (OMTM) ανώνυμα χωρίς login.
- **Αρχεία που ενημερώθηκαν:** [[architecture/technical_stack.md]], [[notes/Product Design.md]]
- **Σημείωση για Implementation:** Χρήση distinct IDs στο SvelteKit frontend (χωρίς Auth requirement).

### 2026-04-10 - Στρατηγική Πωλήσεων Φάσης 1 (Phase 1 Sales)
- **Απόφαση / Σύνοψη:** Επιλογή του "Direct sales (walking in)" με ένα "Fake MVP" demo.
- **Αρχεία που ενημερώθηκαν:** [[business/market_strategy.md]]
- **Σημείωση για Implementation:** Δεν χρησιμοποιούμε automated emails ακόμα. Tracking μέσω απλού CRM (Planka).


### [2026-04-27] - Επιλογή Βάσης Δεδομένων (Database) για Local-First Requirement
- **Απόφαση / Σύνοψη:** Επιλέχθηκε το Turso/libSQL λόγω της εγγενούς υποστήριξης embedded replicas (SQLite) για offline λειτουργία, μικρού footprint για edge devices, και άψογης συμβατότητας με SvelteKit/Drizzle. Το Supabase/CockroachDB απορρίφθηκαν ως πολύ "βαριά" για low-end hardware.
- **Αρχεία που ενημερώθηκαν:** [[architecture/technical_stack.md]], [[architecture/data_model.md]]
- **Σημείωση για Implementation:** Χρησιμοποιούμε "database-per-tenant" model (1 DB/κατάστημα) για data isolation, καθώς η libSQL δεν έχει native RLS. Τα reads είναι τοπικά, τα writes πάνε cloud+local sync. Drizzle ORM για TS support.
