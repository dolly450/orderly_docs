# Στρατηγική Αποθήκευσης Δεδομένων (Database Strategy: Turso vs Supabase)

Η ανάλυση και απόφαση για το επίπεδο αποθήκευσης (Data Layer) είναι κρίσιμη για την αρχιτεκτονική του SkipQ, ειδικά όσον αφορά την αποδοτικότητα (Performance) και το κόστος (Cost) σε scale.

## Επιλογή: Turso/libSQL

Βασιζόμαστε στο Turso (libSQL) αντί για το κλασικό Supabase, για τους εξής λόγους:

### 1. Κόστος & Τιμολόγηση
Το Turso χρησιμοποιεί ένα μοντέλο τιμολόγησης ανά βάση (Per DB), αλλά είναι βελτιστοποιημένο για Edge.
- **Developer Tier:** $4.99/μήνα (περιλαμβάνει 500 DBs).
- **Scaler Tier:** $24.92/μήνα (περιλαμβάνει 2.500 DBs).
- Επιπλέον DBs κοστίζουν ελάχιστα.
- **Storage/Reads/Writes:** Πολύ φθηνά σε QR ordering (συνήθως < $10-20 επιπλέον ακόμα και σε 1.000+ καταστήματα).
- Το κλειδί είναι τα **Embedded Replicas** (local-first) τα οποία είναι απεριόριστα και δωρεάν.

### 2. Περιορισμοί & Scaling
- Δεν υπάρχει hard limit σε συνολικά DBs (μόνο active DBs).
- **Performance:** SQLite + embedded replicas = microsecond reads τοπικά. Τα writes πηγαίνουν στο cloud και γίνονται sync.

### 3. SDKs & Έτοιμες Λειτουργικότητες
- **Go / TypeScript SDKs:** Εξαιρετική υποστήριξη (`@libsql/client`).
- **Drizzle ORM:** Άψογη συνεργασία με Turso, πλήρης type-safety, migrations, και relations. (Στο Go, προτείνεται `database/sql` + `sqlc`).
- **SSE / Realtime:** Το Turso ΔΕΝ έχει built-in realtime (όπως το Supabase). Απαιτείται custom υλοποίηση SSE στο Go backend (για orders δεν είναι deal-breaker).
- **RLS (Row Level Security):** Δεν υπάρχει native RLS. Η λύση είναι **database-per-tenant** (1 DB ανά κατάστημα) για πλήρη απομόνωση.
- **Auth:** Δεν έχει built-in Auth. Απαιτείται εξωτερικός πάροχος (π.χ. Better Auth / Clerk) + JWT.

### 4. Εναλλακτική: Self-hosted (libsql-server)
Αν το κόστος σε scale (>1000 καταστήματα) αυξηθεί, υπάρχει δυνατότητα migration σε self-hosted VPS με docker: `ghcr.io/tursodatabase/libsql-server`. Αυτό μειώνει το κόστος, αλλά αυξάνει τη διαχείριση (DevOps).

### Τελική Σύσταση
**Ξεκινάμε με Turso Cloud (Developer tier)** (άμεσο, μηδενικό ops, εύκολο scaling) και χρησιμοποιούμε Drizzle ORM. Αν χρειαστεί, μεταβαίνουμε σε self-hosted στο μέλλον.
