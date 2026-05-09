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

### 2026-04-18 - Επιλογή Βάσης Δεδομένων
- **Απόφαση / Σύνοψη:** Επιλέχθηκε η Turso/libSQL με embedded replicas για την ερευνητική κατεύθυνση του local-first fallback sync.
- **Αρχεία που ενημερώθηκαν:** [[architecture/technical_stack.md]]
- **Σημείωση για Implementation:** Χρήση `@libsql/client`. Δεν διαθέτει native SSE/Auth, άρα η λύση στηρίζεται σε Better Auth και custom real-time events.

### 2026-04-18 - Επιλογή Ονόματος (Brand Name)
- **Απόφαση / Σύνοψη:** Καταγράφηκαν εναλλακτικές 1-3 συλλαβών (π.χ. ordersnap, waitease, zeroq) για πιθανή αντικατάσταση του "Orderly".
- **Αρχεία που ενημερώθηκαν:** [[business/logo and branding.md]]
- **Σημείωση για Implementation:** Θα χρειαστεί τελική απόφαση πριν τη δημιουργία του επίσημου branding.

### 2026-04-18 - Στρατηγική Προϊόντος: Ενσωμάτωση (Add-on)
- **Απόφαση / Σύνοψη:** Δεν στοχεύουμε σε αντικατάσταση των PDAs αλλά σε ενσωμάτωση ως add-on self-service layer (για να μειωθεί η τριβή με παρόχους POS).
- **Αρχεία που ενημερώθηκαν:** [[business/market_strategy.md]]
- **Σημείωση για Implementation:** Direct sales προσέγγιση σε καταστηματάρχες.
