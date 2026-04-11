### Ερωτήσεις Σήμερα – 2026-04-09

**3. Ερώτηση:** Ποιο θα είναι το όνομα του startup μας;
**Γιατί είναι κρίσιμη:** Έχουμε καταλήξει ότι το "Orderly" είναι πολύ safe και ότι χρειαζόμαστε κάτι που να εκπέμπει ταχύτητα και καλοκαίρι. Χωρίς brand name δυσκολευόμαστε να φτιάξουμε τα pitch decks.
**Επίπεδο:** High
**Πεδίο:** Branding
**Απάντηση:** Ο χρήστης δεν θυμάται ακριβώς, αλλά έχει σημειώσει προηγουμένως ιδέες (TapServe, EasyTab, QResto, Breeze, Velo, Kima, Lio, Zeno). Χρειάζεται τελική επιλογή (π.χ. με ψηφοφορία στην ομάδα).

**Prompt για AI έρευνα (copy-paste ready):**
> Φτιάχνουμε ένα B2B2C startup για QR ordering σε beach bars, χωρίς app install (web). Ψάχνουμε για 1-3 συλλαβές brand names που να είναι "Airplane test approved" (να καταλαβαίνει κάποιος πώς γράφεται αν το ακούσει στο τηλέφωνο). Δώσε μου 5 επιλογές με διαθέσιμα .io ή .com domains.

**4. Ερώτηση:** Πώς θα διαχειριστούμε την επιστροφή χρημάτων (refunds) και το payment routing;
**Γιατί είναι κρίσιμη:** Πώς θα διαχειριστούμε την επιστροφή χρημάτων (refunds) αν ο πελάτης ακυρώσει ή αν το προϊόν δεν υπάρχει, χωρίς να έχουμε εμείς την ευθύνη των χρημάτων (liability);
**Επίπεδο:** High
**Πεδίο:** Business/Finance
**Απάντηση:** →

**Prompt για AI έρευνα (copy-paste ready):**
> Είμαστε ένα marketplace ordering platform όπου ο πελάτης πληρώνει μέσω κινητού. Ποιος είναι ο καλύτερος τρόπος να γίνει το payment routing (π.χ. Stripe Connect, Viva Wallet) ώστε τα χρήματα να πηγαίνουν απευθείας στο κατάστημα και οι ακυρώσεις να βαρύνουν εκείνο, κρατώντας εμείς μόνο ένα fee;
**6. Ερώτηση:** Διαχωρισμός χαρακτηριστικών στις βαθμίδες συνδρομής (Tiered Pricing Features)
**Γιατί είναι κρίσιμη:** Έχουμε ορίσει tiers (€0/€19/€39/€69) αλλά πρέπει να αποφασίσουμε ποια ακριβώς features μπαίνουν πού για να υπάρχει σωστό upselling motivation.
**Επίπεδο:** Medium
**Πεδίο:** Business
**Απάντηση:** →

**Prompt για AI έρευνα (copy-paste ready):**
> Για ένα B2B SaaS εστίασης με QR ordering, πρότεινε έναν διαχωρισμό χαρακτηριστικών (features) για 4 tiers (Free, Basic, Pro, Enterprise). Λάβε υπόψη features όπως: Digital Menu, Ordering, POS Integration, Analytics, Multi-location, Staff Accounts, Custom Branding.

---
### Αρχειοθετημένες Ερωτήσεις & Απαντήσεις

**3. Analytics Setup (Data Tracking) - 2026-04-10**

Απάντηση: Επιλέχθηκε το PostHog για το zero-friction tracking του OMTM (Scan-to-order rate).

Insights / Επιπτώσεις: Θα ενσωματωθεί στο SvelteKit frontend για anonymous tracking.

**Reference:**
- `meta/decision-log.md`
- `architecture/technical_stack.md`

**4. Στρατηγική Προσέγγισης Πελατών (Phase 1 Sales) - 2026-04-10**

Απάντηση: Επιλέχθηκε το Direct Sales (Walking in).

Insights / Επιπτώσεις: Θα παρουσιάζουμε ένα "Fake MVP" demo κατευθείαν στο κινητό του manager του beach bar/φεστιβάλ. Δεν θα μπλέξουμε με πολύπλοκα automated emails σε αυτή τη φάση.

**Reference:**
- `meta/decision-log.md`
- `business/market_strategy.md`

**1. Ποιο είναι το ιδανικό brand name (Brand Name) για το startup μας; – 2026-04-08**

Απάντηση: Το όνομα "Orderly" είναι ασφαλές, αλλά λείπει ίσως το συναίσθημα. Έγινε brainstorming με βάση το Relevance workshop (1-3 συλλαβές, Airplane Test). Ιδέες: TapServe, EasyTab, QResto, Breeze, Velo, Kima.

Insights / Επιπτώσεις: Χρειαζόμαστε ένα brand name που να δείχνει ταχύτητα, καλοκαίρι και λειτουργικότητα, χωρίς να είναι περιοριστικό.

**Reference:**
- `meta/decision-log.md`
- `notes/Business Model Canvas Initial Plan.md`

**2. Τοπική Αρχιτεκτονική MVP (Local-first MVP Architecture) - 2026-04-10**

Απάντηση: Επιλογή του Tauri v2+ για την υλοποίηση του local-first ordering setup (με server και DB), ως ένα απλό, cross-platform εκτελέσιμο (one-click install) χωρίς να χρειάζεται περίπλοκο setup. Για DB επιλέχθηκε Turso/libSQL cloud με embedded replicas τοπικά.

Insights / Επιπτώσεις: Ξεκινάμε με SvelteKit Cloud-only (V1) και προσθέτουμε το Tauri v2 local-first αργότερα (V2) χωρίς αλλαγές στο web frontend.

**Reference:**
- `meta/decision-log.md`
- `architecture/technical_stack.md`
