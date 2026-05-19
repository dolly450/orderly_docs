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

### 2026-05-19 - Στρατηγική Βάσης Δεδομένων (Database Strategy) & Fallback
- **Απόφαση / Σύνοψη:** Επιλογή Turso (libSQL) cloud ως κύρια βάση δεδομένων με Drizzle ORM και custom Server-Sent Events (SSE). Αποτελεί τη βάση για μελλοντικά embedded replicas και local-first υλοποίηση με το Tauri V2.
- **Αρχεία που ενημερώθηκαν:** [[architecture/technical_stack.md]], [[meta/active_investigations.md]]
- **Σημείωση για Implementation:** Θα χρησιμοποιηθεί το Developer tier της Turso (database-per-tenant isolation χωρίς native RLS) και το Drizzle ORM στο SvelteKit Edge. Δεν έχει native realtime, οπότε θα υλοποιηθεί SSE λογική στο server.
