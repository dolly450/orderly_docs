### Ερωτήσεις Σήμερα – 2026-04-09

**1. Ερώτηση:** Ποια είναι η βέλτιστη λύση βάσης δεδομένων (Database) δεδομένου ότι φεύγουμε από τη Supabase και πάμε σε SvelteKit / Golang;
**Γιατί είναι κρίσιμη:** Καθορίζει το tech stack και πρέπει να αποφασιστεί για να ξεκινήσει το development του backend. Χρειαζόμαστε Real-time ικανότητες (για το Kitchen Display System).
**Επίπεδο:** High
**Πεδίο:** Development/Architecture
**Απάντηση:** →

**Prompt για AI έρευνα (copy-paste ready):**
> Χτίζουμε ένα QR ordering app με SvelteKit (και πιθανώς Golang στο μέλλον). Εγκαταλείψαμε τη Supabase. Χρειαζόμαστε Real-time updates (WebSockets ή SSE) για το Kitchen Display System. Πρότεινε τις κορυφαίες επιλογές για Database (π.χ. PostgreSQL + κάτι άλλο, ή Cloudflare D1, κλπ) για early stage startup, εστιάζοντας σε κόστος, ταχύτητα ανάπτυξης και offline-sync δυνατότητες.

**2. Ερώτηση:** Τι data tracking/analytics setup (π.χ. PostHog vs Mixpanel) χρειάζεται το MVP μας για να μετρήσουμε αξιόπιστα το OMTM (scan-to-order rate) χωρίς backend από την πρώτη μέρα;
**Γιατί είναι κρίσιμη:** Αν δεν μετρήσουμε, δεν μπορούμε να τρέξουμε Lean Startup (Build-Measure-Learn).
**Επίπεδο:** High
**Πεδίο:** Development/Architecture
**Απάντηση:** →

**Prompt για AI έρευνα (copy-paste ready):**
> Φτιάχνουμε frontend-heavy PWA ordering app (Svelte / SvelteKit). Θέλουμε να κάνουμε track conversion events (QR scan, add to cart, checkout error) με έμφαση στο zero-friction (no login). Σύγκρινε τεχνικά και κοστολογικά το PostHog με το Mixpanel για early stage startups και δώσε μου το ιδανικό architecture schema.

**3. Ερώτηση:** Πώς θα διασφαλίσουμε την αδιάλειπτη λειτουργία (offline mode fallback) όταν το WiFi του venue "πέφτει" σε συνθήκες συνωστισμού (π.χ. φεστιβάλ);
**Γιατί είναι κρίσιμη:** Είναι το USP (Unique Selling Proposition) μας έναντι του ανταγωνισμού, και ο φόβος #1 των ιδιοκτητών.
**Επίπεδο:** Medium
**Πεδίο:** Development/Architecture
**Απάντηση:** →

**Prompt για AI έρευνα (copy-paste ready):**
> Θέλουμε να χτίσουμε ένα local network fallback (PWA + local Raspberry Pi server) για εστιατόρια που χάνουν τη σύνδεση στο Internet (cloud DB sync pending). Πρότεινε τη βέλτιστη αρχιτεκτονική για sync queue (Cloud vs Local DB) όταν το ίντερνετ επανέλθει, ώστε να μη χάνονται παραγγελίες στο SvelteKit/Golang stack.

---
### Αρχειοθετημένες Ερωτήσεις & Απαντήσεις

**1. Ποιο είναι το ιδανικό brand name (Brand Name) για το startup μας; – 2026-04-08**

Απάντηση: Το όνομα "Orderly" είναι ασφαλές, αλλά λείπει ίσως το συναίσθημα. Έγινε brainstorming με βάση το Relevance workshop (1-3 συλλαβές, Airplane Test). Ιδέες: TapServe, EasyTab, QResto, Breeze, Velo, Kima.

Insights / Επιπτώσεις: Χρειαζόμαστε ένα brand name που να δείχνει ταχύτητα, καλοκαίρι και λειτουργικότητα, χωρίς να είναι περιοριστικό.

**Reference:**
- `meta/bot_questions.md`
- `notes/Business Model Canvas Initial Plan.md`
