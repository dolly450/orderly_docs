# Σημείωση κατάστασης

Οι παρακάτω ερωτήσεις/αναλύσεις κρατιούνται ως ιστορικό ερευνητικό υλικό. Το current product baseline είναι cloud-first web app, άρα το local-first/Tauri μέρος δεν πρέπει να διαβάζεται σαν τρέχουσα υλοποίηση.

### Ερωτήσεις Σήμερα – 2026-04-09

- Litestream τρέχει ως sidecar και στέλνει WAL σε S3 (ή MinIO local-to-cloud). Επαναφορά σε cloud instance σε δευτερόλεπτα.
- Container: Ένα multi-stage Docker με Go binary + Litestream (~20-30MB image).

### Πώς υλοποιείται το local IP + routing + sync/fallback
1. Το script εγκατάστασης (Docker/Podman ή single binary) ξεκινάει το DB + το Go backend.
2. Το Go backend στέλνει το local IP (ή mDNS) στον cloud server σου (webhook ή polling).
3. Customer app (SvelteKit): 
   - Αν είναι στο ίδιο WiFi → χρησιμοποιεί `http://<local-ip>:port` (από config που παίρνει από cloud).
   - Fallback → cloud endpoint.
4. Go backend: Προτεραιότητα local DB, αν αποτύχει → cloud (ή dual-write).
5. Sync: Turso/Litestream κάνει τη δουλειά στο background. Το cloud dashboard βλέπει πάντα up-to-date data.

### Πρακτικές συμβουλές υλοποίησης
- **Docker/Podman script**: Ένα `install.sh` που κάνει `docker compose up -d` ή κατεβάζει binary + systemd service. Podman είναι καλύτερο για rootless σε Android/Pi.
- **Android/iOS**: Αν το κινητό είναι η συσκευή, προτίμησε **embedded SQLite** (ή PocketBase σε Termux). iOS δεν τρέχει εύκολα containers → ίσως web-based kiosk mode.
- **Testing**: Ξεκίνα με PocketBase ή Turso embedded σε dev – θα δεις πόσο ελαφρύ είναι.
- **Performance**: Για QR ordering (πολλές μικρές εγγραφές orders) το SQLite είναι γρηγορότερο από Postgres σε single-node.

**Συμπέρασμα**:  
Απόφυγε Supabase/Cockroach για το local device – είναι βαριά. Πήγαινε **Turso/libSQL** αν θέλεις το πιο «smart» sync, ή **PocketBase** αν θέλεις το πιο απλό single-binary experience. Και τα δύο καλύπτουν 100% το local-first + cloud sync/fallback και ταιριάζουν τέλεια με Golang. Αν θες βοήθεια με συγκεκριμένο `install.sh` ή Docker Compose, πες μου!


### 1. Κόστος Turso Cloud όταν έχεις πολλές βάσεις (1 DB ανά κατάστημα/επιχείρηση)

Το pricing **δεν** είναι ανά database, αλλά **ανά account** (εσύ ως provider). Πληρώνεις base fee + overages σε **Monthly Active Databases** (DBs που χρησιμοποιούνται/συγχρονίζονται τον μήνα), storage, rows read/write και syncs (embedded replicas).

| Tier          | Base / μήνα | Monthly Active DBs (συμπεριλαμβάνει) | Extra Active DB | Storage (base + extra) | Row Reads (base + extra) | Row Writes | Monthly Syncs (embedded) | Σχόλιο για QR app |
|---------------|-------------|---------------------------------------|-----------------|-------------------------|---------------------------|------------|---------------------------|-------------------|
| **Free**      | $0         | 100                                   | —               | 5 GB                    | 500M                      | 10M        | 3 GB                      | Μέχρι 100 καταστήματα |
| **Developer** | $4.99      | 500                                   | +$0.20 / DB     | 9 GB + $0.75/GB         | 2.5B + $1/B               | 25M + $1/M | 10 GB + $0.35/GB          | Ιδανικό ξεκίνημα |
| **Scaler**    | $24.92     | 2.500                                 | +$0.05 / DB     | 24 GB + $0.50/GB        | 100B + $0.80/B            | 100M + $0.80/M | 24 GB + $0.25/GB      | Για scale |
| **Pro**       | $416.58    | 10.000                                | +$0.025 / DB    | 50 GB + $0.45/GB        | 250B + $0.75/B            | 250M + $0.75/M | 100 GB + $0.15/GB     | Μεγάλα volumes |
| **Enterprise**| Custom     | Unlimited                             | Custom          | Custom                  | Custom                    | Custom     | Custom                    | SLA, dedicated κλπ. |

**Παραδείγματα κόστους (μόνο για Active DBs – τα πιο συνηθισμένα):**
- 200 καταστήματα → Developer tier: $4.99 + (200-500) = **$4.99** (δωρεάν extra).
- 600 καταστήματα → Developer: $4.99 + (600-500)×$0.20 = **~$105**/μήνα.
- 3.000 καταστήματα → Scaler: $24.92 + (3.000-2.500)×$0.05 = **~$49.92**/μήνα.
- Storage/reads/writes είναι **πολύ φθηνά** σε QR ordering (μικρές εγγραφές orders). Συνήθως < $10-20 επιπλέον ακόμα και σε 1.000+ καταστήματα.

**Embedded Replicas (local-first)**: **Απεριόριστα και δωρεάν** σε όλα τα tiers (ακόμα και Free). Πληρώνεις μόνο τα **syncs** (δεδομένα που ανεβαίνουν/κατεβαίνουν). Αυτό είναι το κλειδί για το μοντέλο σου.

### 2. Περιορισμοί & scaling
- **Scaling**: Απεριόριστα DBs σε Developer και πάνω. Το μόνο που «πιέζει» είναι τα Active DBs, αλλά οι τιμές πέφτουν δραματικά όσο μεγαλώνεις (Scaler/Pro).
- **Performance**: SQLite + embedded replicas = microsecond reads τοπικά. Writes πηγαίνουν σε cloud + sync.
- **Limits**: Δεν υπάρχει hard limit σε συνολικά DBs (μόνο active). Αν έχεις 10.000+ καταστήματα πας σε Pro/Enterprise.

### 3. SDKs & έτοιμες λειτουργικότητες (SSE, type-safe, RLS, Auth)

**Official SDKs** (άψογα για το stack σου):
- **Go** → `@libsql/client-go` (επίσημο, για το Golang backend σου).
- **TypeScript** → `@libsql/client` (για SvelteKit) – δουλεύει τέλεια σε server + edge.

**Type-safe queries**:
- **Drizzle ORM** → Επίσημη και άψογη υποστήριξη για libSQL/Turso (TS). Έχεις πλήρη type-safety, migrations, relations κλπ. Ιδανικό για SvelteKit.
- Στο Go → Χρησιμοποίησε `database/sql` + `sqlc` ή raw queries (δεν υπάρχει Drizzle-equivalent, αλλά πολύ εύκολο).

**SSE / Realtime**:
- **Δεν έχει built-in realtime** (όπως Supabase Realtime). Δεν υπάρχει native SSE endpoint για queries.
- Λύση: Υλοποιείς **SSE** μόνος σου στο Golang backend σου (πολύ εύκολο, 20 γραμμές κώδικα) ή χρησιμοποιείς `/listen` experimental endpoint + custom polling. Δεν είναι deal-breaker για QR ordering (orders δεν χρειάζονται live updates σε ms).

**RLS (Row Level Security)**:
- **Δεν υπάρχει native RLS** (είναι SQLite fork).  
  Η προτεινόμενη λύση της Turso είναι **database-per-tenant** (1 DB ανά κατάστημα) → πλήρης isolation χωρίς RLS.  
  Αν θες RLS, υπάρχουν community wrappers (π.χ. Cloudflare Worker) ή το υλοποιείς application-level.

**Auth**:
- **Δεν έχει built-in Auth** (όπως Supabase/PocketBase).  
  Χρησιμοποιείς εξωτερικό (Clerk, Auth.js, Supabase Auth, Firebase) + JWT. Το libSQL driver δέχεται auth token, οπότε είναι trivial.

**Συμπέρασμα λειτουργικότητας**: Το Turso είναι **raw & lightweight** (όχι full BaaS). Με Drizzle + custom Auth + SSE στο Go = 100% κάλυψη, αλλά χρειάζεσαι λίγο παραπάνω κώδικα από PocketBase.

### 4. Εναλλακτική: Self-hosted σε remote server + local copies

**Ναι, μπορείς 100%** και είναι πολύ δημοφιλής λύση.

**Πώς δουλεύει**:
1. Τρέχεις **libsql-server** (πρώην sqld) σε **ένα VPS** σου (Docker: `ghcr.io/tursodatabase/libsql-server`).
2. Δημιουργείς όσες βάσεις θες στο self-hosted server.
3. Στον ιδιοκτήτη δίνεις **embedded replica** (το ίδιο script με cloud, απλά αλλάζεις το URL να δείχνει στο δικό σου server).
4. Το local device τρέχει το ίδιο embedded replica + sync με το self-hosted σου.

**Πλεονεκτήματα vs Cloud**:
- **Κόστος**: Μόνο το VPS σου (~$5-20/μήνα για μικρό, $40-80 για μεγαλύτερο). **Κανένα per-DB fee**. Κερδίζεις πολύ όταν έχεις 1.000+ καταστήματα.
- **Control**: Πλήρες (backups, custom config, encryption κλπ.).

**Μειονεκτήματα / περιορισμοί**:
- Εσύ κάνεις **όλη τη διαχείριση** (uptime, scaling, security patches, backups, monitoring).
- Δεν έχεις τα managed features του Cloud (automatic PITR, global replicas, SOC2/HIPAA εύκολα, audit logs).
- Scaling: Αν μεγαλώσεις πολύ, θα χρειαστείς cluster ή multiple servers (δεν είναι τόσο «set & forget»).
- Embedded replicas δουλεύουν **ακριβώς το ίδιο** (ίδιο protocol).

**Πότε το προτείνω**: Αν έχεις ήδη DevOps γνώση ή θες να κρατήσεις κόστος χαμηλό μακροπρόθεσμα. Αλλιώς Turso Cloud είναι πιο «fire & forget».

**Τελική σύσταση για το app σου**:
- **Ξεκίνα με Turso Cloud (Developer tier)** → μηδενικό ops, εύκολο scaling, embedded replicas δωρεάν.
- Αν δεις >500-1.000 καταστήματα και θες να γλιτώσεις χρήματα → μετανάστευσε σε self-hosted libsql-server (migration είναι trivial, ίδιο protocol).

```

**Τίτλος Έρευνας:** Ποιο θα είναι το όνομα του startup μας;
**Γιατί είναι κρίσιμη:** Έχουμε καταλήξει ότι το "Orderly" είναι πολύ safe και ότι χρειαζόμαστε κάτι που να εκπέμπει ταχύτητα και καλοκαίρι. Χωρίς brand name δυσκολευόμαστε να φτιάξουμε τα pitch decks.
**Επίπεδο:** High
**Πεδίο:** Branding
**Απάντηση:** Ο χρήστης δεν θυμάται ακριβώς, αλλά έχει σημειώσει προηγουμένως ιδέες (TapServe, EasyTab, QResto, Breeze, Velo, Kima, Lio, Zeno). Χρειάζεται τελική επιλογή (π.χ. με ψηφοφορία στην ομάδα).

**Prompt για AI έρευνα (copy-paste ready):**
> Φτιάχνουμε ένα B2B2C startup για QR ordering σε beach bars, χωρίς app install (web). Ψάχνουμε για 1-3 συλλαβές brand names που να είναι "Airplane test approved" (να καταλαβαίνει κάποιος πώς γράφεται αν το ακούσει στο τηλέφωνο). Δώσε μου 5 επιλογές με διαθέσιμα .io ή .com domains.

**Τίτλος Έρευνας:** Πώς θα διαχειριστούμε την επιστροφή χρημάτων (refunds) και το payment routing;
**Γιατί είναι κρίσιμη:** Πώς θα διαχειριστούμε την επιστροφή χρημάτων (refunds) αν ο πελάτης ακυρώσει ή αν το προϊόν δεν υπάρχει, χωρίς να έχουμε εμείς την ευθύνη των χρημάτων (liability);
**Επίπεδο:** High
**Πεδίο:** Business/Finance
**Απάντηση:** →

**Prompt για AI έρευνα (copy-paste ready):**
> Είμαστε ένα marketplace ordering platform όπου ο πελάτης πληρώνει μέσω κινητού. Ποιος είναι ο καλύτερος τρόπος να γίνει το payment routing (π.χ. Stripe Connect, Viva Wallet) ώστε τα χρήματα να πηγαίνουν απευθείας στο κατάστημα και οι ακυρώσεις να βαρύνουν εκείνο, κρατώντας εμείς μόνο ένα fee;
**Τίτλος Έρευνας:** Στρατηγική Προϊόντος: Αντικατάσταση ή Ενσωμάτωση PDA;
**Γιατί είναι κρίσιμη:** Αν προσπαθήσουμε να αντικαταστήσουμε τα υπάρχοντα PDA, μπαίνουμε σε ευθεία σύγκρουση με τους παρόχους POS. Αν ενσωματωθούμε, λειτουργούμε ως add-on. Αυτό καθορίζει το Phase 2 MVP.
**Επίπεδο:** High
**Πεδίο:** Marketing/Sales
**Απάντηση:** → Direct sales.

**Prompt για AI έρευνα (copy-paste ready):**
> Είμαστε startup παραγγελιοληψίας με QR. Στην ελληνική αγορά, είναι καλύτερο να προσπαθήσουμε να αντικαταστήσουμε τα υπάρχοντα PDA των σερβιτόρων με δικό μας interface (Staff Dashboard), ή να στέλνουμε τις παραγγελίες κατευθείαν στο υπάρχον POS (π.χ. Epsilon Net) και να λειτουργούμε μόνο ως self-service layer; Ποιο έχει το μικρότερο friction adoption;


**Τίτλος Έρευνας:** Διαχωρισμός χαρακτηριστικών στις βαθμίδες συνδρομής (Tiered Pricing Features)
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


**Τίτλος Έρευνας:** Ενσωμάτωση myDATA API (ΦΗΜΑΣ)
**Γιατί είναι κρίσιμη:** Τα ελληνικά beach bars υφίστανται αυστηρούς ελέγχους (Theros campaign). Αν η πλατφόρμα μας υποστηρίζει αυτόματη έκδοση παραστατικών τύπου 8.6 και MARK, αποκτάμε ένα τεράστιο ανταγωνιστικό πλεονέκτημα και μειώνουμε τον φόβο ελέγχου.
**Επίπεδο:** High
**Πεδίο:** Compliance/Development
**Απάντηση:** →

**Prompt για AI έρευνα (copy-paste ready):**
> Σχεδιάζουμε ένα SvelteKit app παραγγελιοληψίας για ελληνικά beach bars. Πώς μπορούμε να ενσωματώσουμε το myDATA REST API της ΑΑΔΕ για να εκδίδουμε αυτόματα αποδείξεις (παραστατικά τύπου 8.6), να λαμβάνουμε MARK αριθμό και να παράγουμε QR codes για τις αποδείξεις; Ποιες είναι οι βασικές τεχνικές προκλήσεις και ποια είναι τα απαραίτητα B2B credentials;
