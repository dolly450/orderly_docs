### Ερωτήσεις Σήμερα – 2026-04-09

**1. Ερώτηση:** Ποια είναι η βέλτιστη λύση βάσης δεδομένων (Database) δεδομένου του Local-First requirement (τοπική αντιγραφή & fallback sync); (Η Supabase παραμένει υπό διερεύνηση, μαζί με λύσεις όπως το CockroachDB).
**Γιατί είναι κρίσιμη:** Ο στόχος είναι τα αιτήματα του μαγαζιού να χτυπάνε πρώτα τοπικά (μέσω τοπικού WiFi / συσκευής) για ταχύτητα και ανθεκτικότητα σε πτώση internet, και έπειτα να γίνεται sync στο cloud.
**Επίπεδο:** High
**Πεδίο:** Development/Architecture
**Απάντηση:** →

**Prompt για AI έρευνα (copy-paste ready):**
> Χτίζουμε ένα QR ordering app (SvelteKit/Golang). Έχουμε ένα αυστηρό local-first requirement: Η βάση δεδομένων πρέπει να μπορεί να τρέχει τοπικά σε μια συσκευή στο κατάστημα (π.χ. παλιό κινητό Android/iOS, laptop ή Raspberry Pi). Ο ιδιοκτήτης θα κατεβάζει ένα αρχείο/script που θα κάνει αυτόματη εγκατάσταση της τοπικής DB (σαν container). Η συσκευή θα στέλνει το local IP της στον Cloud server μας, και από εκεί και πέρα τα αιτήματα στο τοπικό WiFi θα δρομολογούνται πρώτα τοπικά για ταχύτητα, με cloud sync/fallback strategy. Αξιολόγησε λύσεις όπως η Supabase (τοπικό instance), το CockroachDB ή άλλες ελαφριές distributed databases που ταιριάζουν σε αυτό το μοντέλο.

**2. Ερώτηση:** Τι data tracking/analytics setup (π.χ. PostHog vs Mixpanel) χρειάζεται το MVP μας για να μετρήσουμε αξιόπιστα το OMTM (scan-to-order rate) χωρίς backend από την πρώτη μέρα;
**Γιατί είναι κρίσιμη:** Αν δεν μετρήσουμε, δεν μπορούμε να τρέξουμε Lean Startup (Build-Measure-Learn).
**Επίπεδο:** High
**Πεδίο:** Development/Architecture
**Απάντηση:** →

**Prompt για AI έρευνα (copy-paste ready):**
> Φτιάχνουμε frontend-heavy PWA ordering app (Svelte / SvelteKit). Θέλουμε να κάνουμε track conversion events (QR scan, add to cart, checkout error) με έμφαση στο zero-friction (no login). Σύγκρινε τεχνικά και κοστολογικά το PostHog με το Mixpanel για early stage startups και δώσε μου το ιδανικό architecture schema.

**3. Ερώτηση:** Πώς θα υλοποιήσουμε τεχνικά την εγκατάσταση (One-click install) του τοπικού Server/DB για τους ιδιοκτήτες καταστημάτων που δεν έχουν τεχνικές γνώσεις;
**Γιατί είναι κρίσιμη:** Πρέπει να είναι πανεύκολο, δωρεάν και γρήγορο για τον καταστηματάρχη να στήσει το local-first setup.
**Επίπεδο:** Medium
**Πεδίο:** Development/Architecture
**Απάντηση:** →

**Prompt για AI έρευνα (copy-paste ready):**
> Στο local-first QR ordering app μας, ο ιδιοκτήτης πρέπει να στήσει τον τοπικό κόμβο (database + server) στο κατάστημα, τρέχοντάς τον ιδανικά σε μια παλιά συσκευή (Android/iOS phone, laptop, Windows PC). Πρότεινε πώς μπορούμε να πακετάρουμε την εφαρμογή μας (π.χ. μέσω PWA, Docker executable, Tauri, ή standalone script) ώστε με ένα κλικ να ξεκινάει ο server, να βρίσκει το τοπικό IP και να το στέλνει στο Cloud backend μας, χωρίς ο χρήστης να κάνει port forwarding ή ρυθμίσεις router.

---
### Αρχειοθετημένες Ερωτήσεις & Απαντήσεις

**1. Ποιο είναι το ιδανικό brand name (Brand Name) για το startup μας; – 2026-04-08**

Απάντηση: Το όνομα "Orderly" είναι ασφαλές, αλλά λείπει ίσως το συναίσθημα. Έγινε brainstorming με βάση το Relevance workshop (1-3 συλλαβές, Airplane Test). Ιδέες: TapServe, EasyTab, QResto, Breeze, Velo, Kima.

Insights / Επιπτώσεις: Χρειαζόμαστε ένα brand name που να δείχνει ταχύτητα, καλοκαίρι και λειτουργικότητα, χωρίς να είναι περιοριστικό.

**Reference:**
- `meta/bot_questions.md`
- `notes/Business Model Canvas Initial Plan.md`
