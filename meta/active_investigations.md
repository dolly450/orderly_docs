# Ενεργές Έρευνες (Active Investigations)

Εδώ διατηρούνται οι **5 πιο επείγουσες ανοιχτές έρευνες/ερωτήσεις**. Μόλις απαντηθούν, η απόφαση περνάει στο `decision-log.md` και η ερώτηση αφαιρείται από εδώ.

---

**1. Ερώτηση:** Ποιο είναι το ιδανικό Value Proposition για να κλείσουμε τα πρώτα 5 demos;
**Γιατί είναι κρίσιμη:** Έχουμε δύο προσεγγίσεις ("Λειτουργική Ηρεμία" vs "Αύξηση Τζίρου") και πρέπει να ξέρουμε ποια "πουλάει" καλύτερα στο cold outreach.
**Επίπεδο:** High
**Πεδίο:** Marketing/Sales
**Απάντηση:** →

**Prompt για AI έρευνα (copy-paste ready):**
> Είμαστε B2B SaaS εστίασης στην Ελλάδα. Θέλουμε να κάνουμε A/B test το Value Proposition μας σε ιδιοκτήτες Beach Bars. Το Α είναι "Αυξήστε τον τζίρο σας κατά 20% με ταχύτερες παραγγελίες" και το Β είναι "Μειώστε το χάος και τα λάθη, προσφέροντας λειτουργική ηρεμία στο προσωπικό σας". Σχεδίασε ένα πείραμα επικύρωσης (validation experiment) χρησιμοποιώντας cold outreach (τηλέφωνο ή επίσκεψη) για να μετρήσουμε ποιο value proposition έχει καλύτερο conversion rate στο να κλείσει ραντεβού/demo. Δώσε συγκεκριμένα metrics.

**2. Ερώτηση:** Τι data tracking/analytics setup (π.χ. PostHog vs Mixpanel) χρειάζεται το MVP μας για να μετρήσουμε αξιόπιστα το OMTM (scan-to-order rate) χωρίς backend από την πρώτη μέρα;
**Γιατί είναι κρίσιμη:** Αν δεν μετρήσουμε, δεν μπορούμε να τρέξουμε Lean Startup (Build-Measure-Learn).
**Επίπεδο:** High
**Πεδίο:** Development/Architecture
**Απάντηση:** →

**Prompt για AI έρευνα (copy-paste ready):**
> Φτιάχνουμε frontend-heavy PWA ordering app (Svelte / SvelteKit). Θέλουμε να κάνουμε track conversion events (QR scan, add to cart, checkout error) με έμφαση στο zero-friction (no login). Σύγκρινε τεχνικά και κοστολογικά το PostHog με το Mixpanel για early stage startups και δώσε μου το ιδανικό architecture schema.

**3. Ερώτηση:** Ποιο θα είναι το όνομα του startup μας;
**Γιατί είναι κρίσιμη:** Έχουμε καταλήξει ότι το "Orderly" είναι πολύ safe και ότι χρειαζόμαστε κάτι που να εκπέμπει ταχύτητα και καλοκαίρι. Χωρίς brand name δυσκολευόμαστε να φτιάξουμε τα pitch decks.
**Επίπεδο:** High
**Πεδίο:** Branding
**Απάντηση:** →

**Prompt για AI έρευνα (copy-paste ready):**
> Φτιάχνουμε ένα B2B2C startup για QR ordering σε beach bars, χωρίς app install (web). Ψάχνουμε για 1-3 συλλαβές brand names που να είναι "Airplane test approved" (να καταλαβαίνει κάποιος πώς γράφεται αν το ακούσει στο τηλέφωνο). Δώσε μου 5 επιλογές με διαθέσιμα .io ή .com domains.

**4. Ερώτηση:** Πώς θα διαχειριστούμε την επιστροφή χρημάτων (refunds) και το payment routing;
**Γιατί είναι κρίσιμη:** Πώς θα διαχειριστούμε την επιστροφή χρημάτων (refunds) αν ο πελάτης ακυρώσει ή αν το προϊόν δεν υπάρχει, χωρίς να έχουμε εμείς την ευθύνη των χρημάτων (liability);
**Επίπεδο:** High
**Πεδίο:** Business/Finance
**Απάντηση:** →

**Prompt για AI έρευνα (copy-paste ready):**
> Είμαστε ένα marketplace ordering platform όπου ο πελάτης πληρώνει μέσω κινητού. Ποιος είναι ο καλύτερος τρόπος να γίνει το payment routing (π.χ. Stripe Connect, Viva Wallet) ώστε τα χρήματα να πηγαίνουν απευθείας στο κατάστημα και οι ακυρώσεις να βαρύνουν εκείνο, κρατώντας εμείς μόνο ένα fee;

**5. Ερώτηση:** Πώς ακριβώς θα προσεγγίσουμε τους πρώτους 10 πελάτες;
**Γιατί είναι κρίσιμη:** Έχουμε ήδη 2 personas (Beach Bar & Festival) αλλά πώς ακριβώς θα προσεγγίσουμε τους πρώτους 10 πελάτες;
**Επίπεδο:** High
**Πεδίο:** Marketing/Sales
**Απάντηση:** →

**Prompt για AI έρευνα (copy-paste ready):**
> Για ένα QR Ordering SaaS στην Ελλάδα, ποιο είναι το πιο effective sales channel για να κλείσουμε τα πρώτα 10 beach bars πριν το καλοκαίρι; Direct sales (walking in) ή partnerships με POS providers (όπως Epsilon Net);
