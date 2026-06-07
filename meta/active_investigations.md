# Ενεργές Έρευνες (Active Investigations)

Οι παρακάτω ερωτήσεις/αναλύσεις κρατιούνται ως ιστορικό ερευνητικό υλικό. Το current product baseline είναι cloud-first web app, άρα το local-first/Tauri μέρος δεν πρέπει να διαβάζεται σαν τρέχουσα υλοποίηση.

---
### Τρέχουσες Ανοιχτές Ερωτήσεις (Top 5)

- **Τίτλος Έρευνας:** Διαχείριση επιστροφής χρημάτων (Refunds) & Payment Routing
- **Γιατί είναι κρίσιμη:** Πώς θα διαχειριστούμε την επιστροφή χρημάτων αν ο πελάτης ακυρώσει ή αν το προϊόν δεν υπάρχει, χωρίς να έχουμε εμείς την ευθύνη των χρημάτων (liability);
- **AI Prompt:** Είμαστε ένα marketplace ordering platform όπου ο πελάτης πληρώνει μέσω κινητού. Ποιος είναι ο καλύτερος τρόπος να γίνει το payment routing (π.χ. Stripe Connect, Viva Wallet) ώστε τα χρήματα να πηγαίνουν απευθείας στο κατάστημα και οι ακυρώσεις να βαρύνουν εκείνο, κρατώντας εμείς μόνο ένα fee;
- **Απάντηση / Δεδομένα:** →

- **Τίτλος Έρευνας:** Στρατηγική Προϊόντος: Αντικατάσταση ή Ενσωμάτωση PDA;
- **Γιατί είναι κρίσιμη:** Αν προσπαθήσουμε να αντικαταστήσουμε τα υπάρχοντα PDA, μπαίνουμε σε ευθεία σύγκρουση με τους παρόχους POS. Αν ενσωματωθούμε, λειτουργούμε ως add-on. Αυτό καθορίζει το Phase 2 MVP.
- **AI Prompt:** Είμαστε startup παραγγελιοληψίας με QR. Στην ελληνική αγορά, είναι καλύτερο να προσπαθήσουμε να αντικαταστήσουμε τα υπάρχοντα PDA των σερβιτόρων με δικό μας interface (Staff Dashboard), ή να στέλνουμε τις παραγγελίες κατευθείαν στο υπάρχον POS (π.χ. Epsilon Net) και να λειτουργούμε μόνο ως self-service layer; Ποιο έχει το μικρότερο friction adoption;
- **Απάντηση / Δεδομένα:** → Direct sales.

- **Τίτλος Έρευνας:** Διαχωρισμός χαρακτηριστικών στις βαθμίδες συνδρομής (Tiered Pricing Features)
- **Γιατί είναι κρίσιμη:** Έχουμε ορίσει tiers (€0/€19/€39/€69) αλλά πρέπει να αποφασίσουμε ποια ακριβώς features μπαίνουν πού για να υπάρχει σωστό upselling motivation.
- **AI Prompt:** Για ένα B2B SaaS εστίασης με QR ordering, πρότεινε έναν διαχωρισμό χαρακτηριστικών (features) για 4 tiers (Free, Basic, Pro, Enterprise). Λάβε υπόψη features όπως: Digital Menu, Ordering, POS Integration, Analytics, Multi-location, Staff Accounts, Custom Branding.
- **Απάντηση / Δεδομένα:** →

- **Τίτλος Έρευνας:** Ποιο είναι το πραγματικό «σημείο πόνου» (Pain Point) του μαγαζιού;
- **Γιατί είναι κρίσιμη:** Θα καθορίσει αν εστιάζουμε το marketing στο κόστος του λογισμικού, στον δισταγμό του manager ή αλλού.
- **AI Prompt:** Για καταστήματα εστίασης (beach bars, festivals) που διστάζουν να υιοθετήσουν QR ordering, ποιο είναι συνήθως το μεγαλύτερο pain point τους (π.χ. υψηλό κόστος λογισμικού, φόβος απώλειας πελατειακής επαφής); Δώσε μου επιχειρήματα για να το ανατρέψω.
- **Απάντηση / Δεδομένα:** →

- **Τίτλος Έρευνας:** Ένταξη AI στο MVP (Artificial Intelligence Implementation)
- **Γιατί είναι κρίσιμη:** Πρέπει να βρούμε την ισορροπία μεταξύ ενός εντυπωσιακού pitch (AI features) και ενός απλού προϊόντος που δεν τρομάζει τον χρήστη.
- **AI Prompt:** Πώς μπορούμε να ενσωματώσουμε βασικές AI λειτουργίες (όπως αυτόματες μεταφράσεις, dynamic menu ordering, recommendation engine) σε ένα QR ordering MVP χωρίς να προσθέσουμε πολυπλοκότητα στο interface για τον πελάτη και τον manager;
- **Απάντηση / Δεδομένα:** →

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

Απάντηση: Το όνομα "Orderly" είναι ασφαλές, αλλά λείπει ίσως το συναίσθημα. Έγινε brainstorming με βάση το Relevance workshop (1-3 συλλαβές, Airplane Test). Ιδέες: TapServe, EasyTab, QResto, Breeze, Velo, Kima. (Νέες ιδέες: skipq.menu, ordersnap, waitease, κλπ).

Insights / Επιπτώσεις: Χρειαζόμαστε ένα brand name που να δείχνει ταχύτητα, καλοκαίρι και λειτουργικότητα, χωρίς να είναι περιοριστικό. Θα γίνει ψηφοφορία για την τελική επιλογή.

**Reference:**
- `meta/decision-log.md`
- `notes/Business Model Canvas Initial Plan.md`
- `business/logo and branding.md`

**2. Τοπική Αρχιτεκτονική MVP (Local-first MVP Architecture) - 2026-04-10**

Απάντηση: Επιλογή του Tauri v2+ για την υλοποίηση του local-first ordering setup (με server και DB), ως ένα απλό, cross-platform εκτελέσιμο (one-click install) χωρίς να χρειάζεται περίπλοκο setup. Για DB επιλέχθηκε Turso/libSQL cloud με embedded replicas τοπικά.

Insights / Επιπτώσεις: Ξεκινάμε με SvelteKit Cloud-only (V1) και προσθέτουμε το Tauri v2 local-first αργότερα (V2) χωρίς αλλαγές στο web frontend.

**Reference:**
- `meta/decision-log.md`
- `architecture/technical_stack.md`
