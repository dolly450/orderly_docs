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

### 2026-04-18 - Επιλογή Βάσης Δεδομένων (Database)
- **Απόφαση / Σύνοψη:** Επιλέχθηκε η Turso / libSQL για την υποστήριξη του future local-first setup με embedded replicas και φθηνό active DB scaling.
- **Αρχεία που ενημερώθηκαν:** [[architecture/technical_stack.md]]
- **Σημείωση για Implementation:** Θα χρειαστεί custom υλοποίηση SSE για realtime updates και χειρισμός RLS σε επίπεδο εφαρμογής ή μέσω database-per-tenant.

### 2026-04-18 - Στρατηγική Πωλήσεων (Phase 2 MVP Sales)
- **Απόφαση / Σύνοψη:** Δεν θα αντικαταστήσουμε τα υπάρχοντα PDA. Θα λειτουργούμε ως self-service layer στέλνοντας τις παραγγελίες κατευθείαν στο POS, προωθώντας την εφαρμογή μέσω "Direct sales (walking in)".
- **Αρχεία που ενημερώθηκαν:** [[business/market_strategy.md]]
- **Σημείωση για Implementation:** Το sales pitch πρέπει να εστιάζει στη λειτουργική ηρεμία και την αύξηση τζίρου χωρίς να διαταράσσει το υφιστάμενο σύστημα.
