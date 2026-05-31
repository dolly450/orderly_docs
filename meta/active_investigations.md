# Ενεργές Έρευνες (Active Investigations)

Εδώ διατηρούνται αυστηρά **μόνο οι 5 πιο επείγουσες ανοιχτές ερωτήσεις**.

**1. Ερώτηση:** Πώς θα διαχειριστούμε την επιστροφή χρημάτων (Refunds) και το Payment Routing;
**Γιατί είναι κρίσιμη:** Πώς θα διαχειριστούμε την επιστροφή χρημάτων αν ο πελάτης ακυρώσει ή αν το προϊόν δεν υπάρχει, χωρίς να έχουμε εμείς την ευθύνη των χρημάτων (liability);
**AI Prompt:**
> Είμαστε ένα marketplace ordering platform όπου ο πελάτης πληρώνει μέσω κινητού. Ποιος είναι ο καλύτερος τρόπος να γίνει το payment routing (π.χ. Stripe Connect, Viva Wallet) ώστε τα χρήματα να πηγαίνουν απευθείας στο κατάστημα και οι ακυρώσεις να βαρύνουν εκείνο, κρατώντας εμείς μόνο ένα fee;
**Απάντηση / Δεδομένα:** →

**2. Ερώτηση:** Διαχωρισμός χαρακτηριστικών στις βαθμίδες συνδρομής (Tiered Pricing Features)
**Γιατί είναι κρίσιμη:** Έχουμε ορίσει tiers (€0/€19/€39/€69) αλλά πρέπει να αποφασίσουμε ποια ακριβώς features μπαίνουν πού για να υπάρχει σωστό upselling motivation.
**AI Prompt:**
> Για ένα B2B SaaS εστίασης με QR ordering, πρότεινε έναν διαχωρισμό χαρακτηριστικών (features) για 4 tiers (Free, Basic, Pro, Enterprise). Λάβε υπόψη features όπως: Digital Menu, Ordering, POS Integration, Analytics, Multi-location, Staff Accounts, Custom Branding.
**Απάντηση / Δεδομένα:** →

**3. Ερώτηση:** Χρηματοδοτικό Μοντέλο: Bootstrapping ή VC Funding;
**Γιατί είναι κρίσιμη:** Πρέπει να αποφασιστεί αν θα κυνηγήσουμε χρηματοδότηση Pre-Seed (δίνοντας equity) ή αν θα αναπτυχθούμε οργανικά, ώστε να προσαρμοστεί η στρατηγική του Pitch Deck (Milestones).
**AI Prompt:**
> Είμαστε μια startup παραγγελιοληψίας με QR στην Ελλάδα (B2B2C). Ποια είναι τα πλεονεκτήματα του Bootstrapping έναντι της άντλησης κεφαλαίων από VC (Pre-Seed) στη φάση του MVP, και ποια metrics χρειάζεται να αποδείξουμε για να σηκώσουμε χρηματοδότηση;
**Απάντηση / Δεδομένα:** →

**4. Ερώτηση:** Metrics απόδοσης και Validation (Pilot Metrics)
**Γιατί είναι κρίσιμη:** Χρειαζόμαστε 3-4 μετρήσιμα KPIs που να αποδεικνύουν άμεσα στο κατάστημα (Owner) την αξία μας (μείωση ουράς, αύξηση παραγγελιών), ώστε να μετατρέπουμε τα δωρεάν pilots σε πληρωμένους πελάτες.
**AI Prompt:**
> Για ένα QR ordering system σε beach bars, ποια είναι τα 4 πιο κρίσιμα KPIs που πρέπει να μετρήσουμε κατά τη διάρκεια ενός δωρεάν pilot 7 ημερών για να πείσουμε τον ιδιοκτήτη να πληρώσει; Πώς μεταφράζουμε αυτά τα metrics σε μείωση εργατοωρών και αύξηση κέρδους;
**Απάντηση / Δεδομένα:** →

**5. Ερώτηση:** Τεχνική προσέγγιση για Multi-Tenant Auth χωρίς Login πελατών
**Γιατί είναι κρίσιμη:** Οι πελάτες δεν πρέπει να κάνουν login (Anonymous by default), αλλά το προσωπικό πρέπει να έχει role-based access ανά κατάστημα (Tenant). Πώς το υλοποιούμε αποδοτικά στο SvelteKit;
**AI Prompt:**
> Σχεδιάζω μια εφαρμογή παραγγελιοληψίας (SvelteKit, libSQL, Better Auth). Ο πελάτης (Customer) πρέπει να λειτουργεί πλήρως ανώνυμα χωρίς login. Το προσωπικό (Staff/Admin) χρειάζεται RBAC και σύνδεση σε συγκεκριμένα καταστήματα (Multi-tenant). Ποιο είναι το βέλτιστο auth/session model για να απομονώσω τα δεδομένα ανά κατάστημα διατηρώντας το ανώνυμο checkout του πελάτη;
**Απάντηση / Δεδομένα:** →

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

Απάντηση: Το όνομα "SkipQ" είναι ασφαλές, αλλά λείπει ίσως το συναίσθημα. Έγινε brainstorming με βάση το Relevance workshop (1-3 συλλαβές, Airplane Test).

Insights / Επιπτώσεις: Χρειαζόμαστε ένα brand name που να δείχνει ταχύτητα, καλοκαίρι και λειτουργικότητα, χωρίς να είναι περιοριστικό.

**Reference:**
- `meta/decision-log.md`
- `business/logo and branding.md`

**2. Τοπική Αρχιτεκτονική MVP (Local-first MVP Architecture) - 2026-04-10**

Απάντηση: Επιλογή του Tauri v2+ για την υλοποίηση του local-first ordering setup (με server και DB), ως ένα απλό, cross-platform εκτελέσιμο (one-click install) χωρίς να χρειάζεται περίπλοκο setup. Για DB επιλέχθηκε Turso/libSQL cloud με embedded replicas τοπικά.

Insights / Επιπτώσεις: Ξεκινάμε με SvelteKit Cloud-only (V1) και προσθέτουμε το Tauri v2 local-first αργότερα (V2) χωρίς αλλαγές στο web frontend.

**Reference:**
- `meta/decision-log.md`
- `architecture/technical_stack.md`

**5. Στρατηγική Αποθήκευσης Δεδομένων (Database: Turso vs Supabase) - 2026-05-31**

Απάντηση: Επιλέχθηκε το Turso (libSQL) αντί του Supabase λόγω χαμηλότερου κόστους σε multi-tenant scale και των δωρεάν embedded replicas. Η δομή θα είναι database-per-tenant.

Insights / Επιπτώσεις: Δεν έχουμε out-of-the-box Auth ή Realtime (όπως στο Supabase), οπότε το Better Auth και το SSE πρέπει να υλοποιηθούν custom.

**Reference:**
- `meta/decision-log.md`
- `architecture/data_layer_tech.md`
