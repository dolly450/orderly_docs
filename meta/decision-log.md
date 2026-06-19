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

### 2026-06-19 - Local-First Database Choice
- **Απόφαση / Σύνοψη:** Επιλογή Turso/libSQL με embedded replicas για local-first λειτουργία. Το PocketBase λειτουργεί ως alternative plug & play επιλογή.
- **Αρχεία που ενημερώθηκαν:** [[architecture/technical_stack.md]]
- **Σημείωση για Implementation:** Θα χρησιμοποιηθούν official SDKs (@libsql/client) και Drizzle ORM. Custom implementation για SSE.

### 2026-06-19 - Στρατηγική Ενσωμάτωσης POS (PDA vs Add-on)
- **Απόφαση / Σύνοψη:** Η εφαρμογή θα λειτουργήσει ως add-on/self-service layer και δεν θα αντικαταστήσει τα υπάρχοντα PDA των σερβιτόρων για να μειώσει το friction adoption.
- **Αρχεία που ενημερώθηκαν:** [[business/market_strategy.md]]
- **Σημείωση για Implementation:** Η προσέγγιση θα είναι direct sales παρουσιάζοντας zero-friction self-service.
