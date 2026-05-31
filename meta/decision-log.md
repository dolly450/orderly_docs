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

### 2026-05-31 - Brand Name
- **Απόφαση / Σύνοψη:** Εδραίωση του ονόματος "SkipQ" ως την τελική επιλογή (πρώην Orderly).
- **Αρχεία που ενημερώθηκαν:** [[business/logo and branding.md]], [[pitch/deck - φαμφάρες type shit.md]]
- **Σημείωση για Implementation:** Θα πρέπει σταδιακά να ενημερωθούν όλα τα assets (canvases, codebase) με το νέο όνομα.

### 2026-05-31 - Στρατηγική Προϊόντος (Αντικατάσταση vs Ενσωμάτωση PDA)
- **Απόφαση / Σύνοψη:** Η πλατφόρμα θα λειτουργήσει αρχικά ως self-service layer (Direct Sales) χωρίς να αντικαταστήσει τα υπάρχοντα PDA.
- **Αρχεία που ενημερώθηκαν:** [[architecture/pos_compliance.md]], [[business/market_strategy.md]]
- **Σημείωση για Implementation:** Η ροή (Phase 1 MVP) στέλνει την παραγγελία στο δικό μας Staff Dashboard, ανεξάρτητα από τα POS, για γρήγορο deployment.

### 2026-05-31 - Στρατηγική Αποθήκευσης Δεδομένων (Database: Turso vs Supabase)
- **Απόφαση / Σύνοψη:** Επιλογή του Turso (libSQL) αντί του Supabase, χρησιμοποιώντας το μοντέλο database-per-tenant, με Drizzle ORM και custom Better Auth/SSE.
- **Αρχεία που ενημερώθηκαν:** [[architecture/data_layer_tech.md]]
- **Σημείωση για Implementation:** Το Turso επιλέχθηκε λόγω κόστους σε scale και των embedded replicas. Το Auth (Better Auth) και το Realtime (SSE) θα πρέπει να υλοποιηθούν custom, καθώς δεν παρέχονται out-of-the-box όπως στο Supabase.
