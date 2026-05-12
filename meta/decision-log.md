# Ημερολόγιο Αποφάσεων (Decision Log)

### 2026-04-18 - Brand Name Status
- **Απόφαση / Σύνοψη:** Η τελική ονομασία δεν έχει αποφασιστεί ακόμα (ανοιχτό για ψηφοφορία). Προτάσεις: TapServe, EasyTab, QResto, Breeze, κλπ.
- **Αρχεία που ενημερώθηκαν:** [[business/logo and branding.md]], [[meta/active_investigations.md]]
- **Σημείωση για Implementation:** Αναμονή τελικής ψηφοφορίας πριν την ενοποίηση του domain και του branding.

### 2026-04-18 - Direct Sales (Αντικατάσταση vs Ενσωμάτωση)
- **Απόφαση / Σύνοψη:** Για το Phase 1, προτιμούμε τα Direct Sales και δεν μπαίνουμε στη διαδικασία αντικατάστασης υφιστάμενων PDA αμέσως.
- **Αρχεία που ενημερώθηκαν:** [[business/market_strategy.md]], [[meta/active_investigations.md]]
- **Σημείωση για Implementation:** Θα παρουσιάζουμε το προϊόν ως "self-service layer" (add-on) και όχι ως άμεσο αντικαταστάτη ολόκληρου του POS συστήματος για να μειώσουμε το friction στην πώληση.

### 2026-04-18 - Local-First Database Solution (Future Phase)
- **Απόφαση / Σύνοψη:** Επιλογή του Turso/libSQL (με embedded replicas) ως τη μελλοντική λύση βάσης δεδομένων για την local-first λειτουργικότητα.
- **Αρχεία που ενημερώθηκαν:** [[architecture/technical_stack.md]], [[meta/active_investigations.md]]
- **Σημείωση για Implementation:** Προτιμάται η χρήση Turso αντί Supabase λόγω χαμηλότερων απαιτήσεων σε πόρους και native offline sync (embedded replicas). To Auth/SSE θα πρέπει να υλοποιηθεί custom στο Golang backend.

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
