### Ερωτήσεις Σήμερα – 2026-04-09

**1. Ερώτηση:** Ποια είναι η βέλτιστη λύση βάσης δεδομένων (Database) δεδομένου του Local-First requirement (τοπική αντιγραφή & fallback sync); (Η Supabase παραμένει υπό διερεύνηση, μαζί με λύσεις όπως το CockroachDB).
**Γιατί είναι κρίσιμη:** Ο στόχος είναι τα αιτήματα του μαγαζιού να χτυπάνε πρώτα τοπικά (μέσω τοπικού WiFi / συσκευής) για ταχύτητα και ανθεκτικότητα σε πτώση internet, και έπειτα να γίνεται sync στο cloud.
**Επίπεδο:** High
**Πεδίο:** Development/Architecture
**Απάντηση:** →

```
**Η καλύτερη λύση για το local-first QR ordering app σου (SvelteKit + Golang) είναι **Turso/libSQL** ή **PocketBase** (με SQLite/Turso backend).** Αυτές ταιριάζουν απόλυτα στο μοντέλο: ελαφριά εγκατάσταση σε container ή single binary, τρέχουν σε Raspberry Pi / παλιό laptop / Android (με Termux), ελάχιστοι πόροι, αυτόματο sync με cloud και fallback.

### Γρήγορη αξιολόγηση Supabase & CockroachDB
- **Supabase local/self-hosted**:  
  Υποστηρίζεται πλήρως με Docker Compose (clone repo → `.env` → `docker compose up`). Έχει Postgres + PostgREST + Auth + Realtime + Storage + Edge Functions – ιδανικό αν θέλεις **ακριβώς** το ίδιο stack με το cloud Supabase.  
  **Μειονεκτήματα για το μοντέλο σου**: Το stack είναι βαριά (πολλαπλά containers, συχνά >500MB-1GB+ RAM idle). Δεν είναι optimized για embedded/low-power συσκευές (Pi Zero / παλιό Android). Η εγκατάσταση είναι scriptable αλλά όχι «ένα αρχείο». Το hybrid local ↔ cloud sync **δεν** είναι built-in (χρειάζεσαι manual logical replication ή custom CDC). Το local dev CLI **δεν** προορίζεται για production/exposed traffic.  
  → Κατάλληλο μόνο αν έχεις beefy laptop/Pi 5+ και δεν σε νοιάζει η πολυπλοκότητα.

- **CockroachDB (single-node)**:  
  Μπορεί να τρέξει σε Pi 4/5 (ARM64 binaries ή Docker). Είναι distributed SQL, Postgres-wire compatible, και υποστηρίζει native multi-node (local + cloud).  
  **Μειονεκτήματα**: Πολύ πιο βαρύ από SQLite (Raft consensus, cache 25% RAM, συστάσεις 4+ vCPU / 4GB+). Idle CPU υψηλό σε tests. Εγκατάσταση πιο περίπλοκη για μη-τεχνικό ιδιοκτήτη. Δεν είναι «ελαφριά» για παλιό κινητό ή Pi Zero.  
  → Απορρίπτεται για το συγκεκριμένο local-first requirement.

### Ιδανικές ελαφριές distributed/edge λύσεις (2026)
| Λύση                  | Εγκατάσταση (owner)              | Μέγεθος / Πόροι (Pi / low-end) | Cloud Sync / Fallback          | Go support / Distributed | Σχόλια για QR app |
|-----------------------|----------------------------------|--------------------------------|--------------------------------|--------------------------|-------------------|
| **Turso / libSQL** (Embedded Replicas) | Docker (`ghcr.io/tursodatabase/libsql-server`) ή single binary / embed σε Go app | ~10-50MB RAM, SQLite file | Built-in (local replica ↔ Turso cloud primary, auto-sync, offline-first) | Εξαιρετικό (libsql/client-go) + distributed edge | **Καλύτερη επιλογή** για exact μοντέλο σου |
| **PocketBase**        | Single 15MB binary (curl → run) | <50MB RAM, τρέχει σε Pi 3/4 | Litestream (S3) ή Turso module | Native Go, extend με hooks | Απλότατο, έχει built-in Auth/Realtime/Storage |
| **SQLite + Litestream** | Embed σε Go ή Docker + binary | Ελάχιστο (SQLite ~600KB) | Streaming WAL → S3 (disaster recovery + restore) | Pure Go driver | Ultra-minimal, zero-deps |
| **rqlite / dqlite**   | Single binary (Raft)            | Πολύ ελαφρύ                    | Raft cluster (local + cloud nodes) | HTTP API / drivers | Καλή για full distributed αλλά πιο complex |
| **Postgres Docker**   | `docker run postgres` + script  | ~200-400MB RAM                 | Logical replication → cloud Postgres | Πλήρες | Αν χρειάζεσαι Postgres features |

#### 1. Turso / libSQL (top recommendation)
- **Embedded Replicas**: Το local DB είναι απλό SQLite file (ή libSQL server) που συγχρονίζεται αυτόματα με το cloud Turso. Microsecond reads τοπικά, writes πηγαίνουν σε cloud + local.
- Εγκατάσταση: Ένα Docker container ή `turso dev` / `sqld` binary. Το script που δίνεις στον ιδιοκτήτη μπορεί να είναι `curl -sSL https://get.turso.sh | sh && turso db ...`.
- Τρέχει παντού: Pi, Android (Termux), ακόμα και mobile SDKs.
- Cloud fallback: Το app σου (Go) χρησιμοποιεί `file:local.db?syncUrl=libsql://...` → αυτόματο.
- Distributed edge: Ακριβώς αυτό που ζητάς.

#### 2. PocketBase (πιο «plug & play»)
- Ένα αρχείο `pocketbase` → `./pocketbase serve`. Έχει admin UI, collections (tables), Auth, Realtime (SSE), File storage – όλα σε SQLite.
- Χρήστες το τρέχουν σε Raspberry Pi χωρίς πρόβλημα (ακόμα και Pi 3).
- Για sync: Ενσωμάτωσε Litestream ή Turso module (υπάρχουν ready modules).
- Ιδανικό για Golang (extend με Go hooks αν χρειάζεσαι custom logic).

#### 3. SQLite + Litestream (minimalist)
- Το Go app σου χρησιμοποιεί `database/sql` + `modernc.org/sqlite`.
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
```
**Συγκεντρωτική απάντηση: Η ιδανική λύση για το local-first QR ordering app σου (MVP φάση)**

Εφόσον είσαι ακόμα σε **pre-built MVP** και δεν έχεις έτοιμο server, το **Tauri v2+** είναι η **πιο one-in-all, εύκολη και future-proof** επιλογή που υπάρχει το 2026. Δεν χρειάζεται να κάνεις τίποτα περίπλοκο (ούτε Docker, ούτε port-forwarding, ούτε router settings). Ο ιδιοκτήτης κατεβάζει **ένα μόνο αρχείο** (EXE / APK / IPA / AppImage), το ανοίγει με ένα κλικ και ο server + DB + IP registration στο Cloud σου ξεκινάει αυτόματα.

### 1. Γιατί Tauri είναι η καλύτερη επιλογή για σένα τώρα
- **Cross-platform από ένα codebase**: Windows, macOS, Linux, **Android** και **iOS** (όλα μαζί).
- **One-click εκκίνηση**: Το app ξεκινάει αυτόματα τον τοπικό server, βρίσκει το local IP (LAN) και το στέλνει στο Cloud backend σου.
- **Ελαφρύ & γρήγορο**: 5-15 MB, τρέχει άνετα σε παλιές συσκευές (Android 8+, iPhone 8+).
- **Εύκολο για MVP**: Το V1 σου είναι cloud-only με **SvelteKit** → μετά μπορείς να προσθέσεις το local service χωρίς να αλλάξεις τίποτα στο frontend των πελατών.

Δεν χρειάζεται να ξέρεις Rust από τώρα. Το AI (εγώ ή οποιοδήποτε άλλο) θα σου γράψει σχεδόν όλο τον κώδικα. Είναι από τις πιο εύκολες γλώσσες να μάθεις για backend (ειδικά αν ξέρεις ήδη JavaScript/TypeScript).

### 2. Πώς θα δουλέψει η αρχιτεκτονική σου (V1 → V2)
- **V1**: Μόνο Cloud + SvelteKit (όπως σκέφτεσαι).
- **V2 (local-first)**: Το Tauri app του ιδιοκτήτη:
  - Τρέχει **τοπικό server + SQLite**.
  - Συνδέεται με το Cloud σου για licensing, updates και remote control.
  - Οι πελάτες σκανάρουν QR → Cloud δίνει το local IP → συνδέονται απευθείας στο κατάστημα (χωρίς internet μετά).

**Ενσωμάτωση**: Πολύ εύκολη. Το Tauri μπορεί να καλεί το ίδιο API που έχεις ήδη στο SvelteKit Cloud. Απλά προσθέτεις ένα endpoint `/register-node` και `/validate-license`.

### 3. Ασφάλεια – Updates – Licensing (όλα εφικτά και εύκολα)
- **Ασφάλεια**: Το Rust είναι **μία από τις πιο ασφαλείς** γλώσσες (memory-safe, χωρίς buffer overflows). Το Tauri έχει built-in permissions system (least privilege). Δεν χρειάζεται να είναι 100% Rust για να είναι ασφαλές, αλλά το Rust δίνει **πολύ μεγαλύτερη ασφάλεια και απόδοση** από Node/Go/Python. Δεν είναι υποχρεωτικό, αλλά **σου το προτείνω ανεπιφύλακτα** γιατί θα μάθεις γρήγορα και θα σου λύσει πολλά προβλήματα μακροπρόθεσμα.
- **Εύκολα updates**: Το Tauri έχει **built-in auto-updater** (με ψηφιακή υπογραφή). Μπορείς να στείλεις νέα έκδοση από το Cloud σου και το app να αναβαθμιστεί αυτόματα. Ο ιδιοκτήτης δεν χρειάζεται να κάνει τίποτα.
- **Licensing & remote control** (ακριβώς αυτό που θες):
  - **Lifetime license 300€**: Το app στο startup ελέγχει online (ή offline με JWT) αν έχει άδεια. Αν ναι, τρέχει για πάντα.
  - **Συνδρομή**: Αν δεν πληρώνει, το app σταματάει (ή μπαίνει σε read-only mode).
  - **Remote cut-off**: Μπορείς να απενεργοποιήσεις απομακρυσμένα οποιοδήποτε node μέσω Cloud (χωρίς να μπορεί ο χρήστης να πειράξει τον κώδικα). Όλα γίνονται με απλά HTTP calls από Rust.
  - **Δεν μπορεί να επέμβει**: Ο κώδικας είναι compiled binary. Δεν έχει source code μέσα.

Είναι **πλήρως εφικτό** και χρησιμοποιείται ήδη από πολλές εταιρείες (υπάρχουν έτοιμα εργαλεία όπως Keyforge για Tauri).

### 4. Tauri Sidecar: Τι είναι και πώς δουλεύει
Αν δεν θες να ξαναγράψεις τον server σου σε Rust από την αρχή:
- Γράφεις τον server σε **όποια γλώσσα θέλεις** (Go, Node, Python κ.λπ.).
- Το Tauri το **bundle-άρει** αυτόματα σαν **sidecar** (ένα ξεχωριστό executable μέσα στο app).
- Όταν ανοίξει το Tauri app, ξεκινάει αυτόματα το sidecar + το δικό σου Rust κομμάτι για IP registration και licensing.

**Πλεονεκτήματα**:
- Δεν χρειάζεται refactor τώρα.
- Compile σε **όλες τις πλατφόρμες** (desktop + Android + iOS) από ένα project.

**Μειονεκτήματα / κρυφά προβλήματα** (δεν κρύβει πολλά):
- Το app γίνεται λίγο μεγαλύτερο (ακόμα <30 MB συνήθως).
- Στα κινητά (ειδικά iOS) υπάρχει περιορισμός background execution (πρέπει το app να είναι ανοιχτό ή να χρησιμοποιείς foreground service).
- Αν το sidecar είναι Python/Go, χρειάζεται να είναι standalone binary (χωρίς εξωτερικές dependencies).

**Αξίζει το ρίσκο;** Ναι, 100%. Είναι η πιο ώριμη λύση αυτή τη στιγμή για ακριβώς το use-case σου. Χιλιάδες developers το χρησιμοποιούν επιτυχώς.

### Τελική σύσταση (για τις σημειώσεις σου)
**Πήγαινε με Tauri v2 + Rust backend (ή sidecar αν θες να ξεκινήσεις γρήγορα)**.  
Είναι το **πιο all-in-one σύστημα**: εύκολο install, εύκολα updates, πλήρης remote control, licensing (lifetime ή subscription), υψηλή ασφάλεια και απόδοση.  
Το V1 σου (SvelteKit Cloud) ενσωματώνεται άψογα.  
Μπορείς να ξεκινήσεις **ακόμα και σήμερα** χωρίς να ξέρεις Rust – το AI θα σου δίνει έτοιμο κώδικα βήμα-βήμα.


```

---
### Αρχειοθετημένες Ερωτήσεις & Απαντήσεις

**1. Ποιο είναι το ιδανικό brand name (Brand Name) για το startup μας; – 2026-04-08**

Απάντηση: Το όνομα "Orderly" είναι ασφαλές, αλλά λείπει ίσως το συναίσθημα. Έγινε brainstorming με βάση το Relevance workshop (1-3 συλλαβές, Airplane Test). Ιδέες: TapServe, EasyTab, QResto, Breeze, Velo, Kima.

Insights / Επιπτώσεις: Χρειαζόμαστε ένα brand name που να δείχνει ταχύτητα, καλοκαίρι και λειτουργικότητα, χωρίς να είναι περιοριστικό.

**Reference:**
- `meta/bot_questions.md`
- `notes/Business Model Canvas Initial Plan.md`
