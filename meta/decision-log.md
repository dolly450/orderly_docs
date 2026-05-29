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

### 2026-04-18 - Επιλογή Local-First Database
- **Απόφαση / Σύνοψη:** Επιλογή του Turso / libSQL (με embedded replicas) ως η βέλτιστη λύση για το local-first setup (και εναλλακτικά το PocketBase), προσφέροντας microsecond reads τοπικά και αυτόματο fallback sync στο cloud.
- **Αρχεία που ενημερώθηκαν:** [[architecture/technical_stack.md]], [[design/features.md]]
- **Σημείωση για Implementation:** Όταν προχωρήσουμε στο phase 2 local-first με Tauri/Golang, η database να χτυπάει πρώτα τοπικά `file:local.db?syncUrl=libsql://...` και η εγκατάσταση σε μαγαζιά να γίνεται με 1-Click script (Docker/Podman).
