# Εύρος MVP v1 (MVP v1 Scope)

Βασικά χαρακτηριστικά και λειτουργίες που πρέπει να περιλαμβάνει η πρώτη έκδοση.

## Στενό Αρχικό Use Case

Μετά τις mentor σημειώσεις, το MVP πρέπει να στοχεύσει πρώτα σε ένα πολύ συγκεκριμένο σενάριο: **high-volume self-service / counter-service venue** όπου υπάρχει ορατή ουρά και γρήγορη επανάληψη παραγγελιών. Παραδείγματα: self-service καφέ, beach bar counter, festival bar.

Στόχος δεν είναι να αποδείξουμε όλο το product vision. Στόχος είναι να αποδείξουμε ότι το QR ordering μειώνει την ουρά, αυξάνει throughput/τζίρο και κάνει το staff workflow πιο γρήγορο με μετρήσιμα δεδομένα.

Το v1 μήνυμα πρέπει να μείνει καθαρό: **Scan -> Order -> Done**. Οτιδήποτε μπερδεύει αυτή τη ροή μπαίνει σε stretch goal ή επόμενο tier.

Μετά το meeting με τον Σάββα Γεωργίου, υπάρχει σημαντική διευκρίνιση: το payment δεν εξετάζεται μόνο ως monetization ή checkout feature, αλλά ως **operational signal** για commitment, prioritization και table turnover. Στο τρέχον MVP αυτό καλύπτεται από την επιλογή στο καλάθι: **πληρώνω τώρα** ή **μπαίνει στον λογαριασμό/tab μου**. Αν ο πελάτης επιλέξει πληρωμή τώρα, δηλώνει **μετρητά** ή **κάρτα**, ώστε να το διαχειριστεί το staff. Δεν χτίζουμε ακόμα βαρύ payment product.

## Βασικές Λειτουργίες

1. QR web menu χωρίς app install
2. Μενού (Menu) + εικόνες (configurable), γραμμένο σε καθαρή φυσική γλώσσα αντί για static PDF
3. Καλάθι (Cart) → Παραγγελία (Order)
4. Submit order με ελάχιστα πεδία πελάτη
5. Payment intent στο καλάθι: πληρώνω τώρα με μετρητά/κάρτα ή μπαίνει στον λογαριασμό/tab
6. Πληροφορίες για κατάσταση παραγγελίας (Order Status) + ουρά αναμονής (Queue) με απλή χρονική ένδειξη
7. Staff/KDS οθόνη για νέες παραγγελίες
8. Staff/KDS ειδοποίηση νέας παραγγελίας με ήχο και έντονη χρωματική ένδειξη, ώστε να τραβάει την προσοχή του barista ή του operator
9. Basic analytics για QR scans, cart additions, order submits, drop-offs, χρόνο ολοκλήρωσης παραγγελίας και χρόνο εξυπηρέτησης. → [[Product Design]]
10. Βασικό owner/admin setup για προϊόντα, τιμές, QR και venue info
11. Πολυγλωσσικότητα (Multilingual) ως value booster για τουριστικά venues → [[features#4. Πολυγλωσσικότητα (Multilingual)]]
12. Κεντρικοί λογαριασμοί χρηστών ως τεχνική βάση για μελλοντικό loyalty/personalization, χωρίς να μπλοκάρουν το guest ordering
13. Διαφημιστική σελίδα (Landing Page) — live demo από ψεύτικο κατάστημα
14. Μόνο cloud, όχι localhost

> **Σημείωση:** Απλό και εύκολο στη χρήση (Simple and easy to use) — αυτό αναφέρεται και ως θετικό του [[competitive_analysis|Butler]].

## Εκτός v1 / Να μην μπερδέψουν το αρχικό pitch

- Full payments/commission product και πολύπλοκα payment integrations
- Room charge για ξενοδοχεία, ως μελλοντική επέκταση του tab flow
- Speech-to-text παραγγελία ή αναζήτηση στο μενού
- AI chatbot / advanced AI flows
- Κουμπί κλήσης σερβιτόρου ως core message
- Κρατήσεις / Bookings
- Complex notifications για πελάτη
- Full POS/PDA integration, εκτός αν αποδειχθεί blocker σε pilot

## MVP Metrics

Τα παρακάτω πρέπει να μετρώνται στα pilots ώστε να αποδείξουμε αξία:

- Scan-to-order conversion rate
- Μέσος χρόνος ολοκλήρωσης παραγγελίας
- Μέσος χρόνος εξυπηρέτησης από submit μέχρι ready/delivered
- Queue/wait-time reduction σε σχέση με την προηγούμενη διαδικασία
- Orders per staff hour
- Εκτίμηση μηνιαίου χρόνου που γλιτώνει το venue
- Εκτίμηση uplift σε παραγγελίες ή average order value από upselling
- Ποσοστό επιλογών πληρωμής από το καλάθι που γίνονται completed/collected orders
- Drop-offs ανά βήμα: scan, menu view, cart, order submit
- Staff feedback για σημεία τριβής στη ροή

## Πίνακας Λειτουργιών ανά Τύπο Venue

| Τύπος Επιχείρησης      | Μενού | Σερβιτόρος | Self-Service | Ουρές | Κλήση Σερβιτόρου | Κράτηση |
| ---------------------- | ----- | ---------- | ------------ | ----- | ---------------- | ------- |
| Full-service καφετέρια | ✅     | ✅          | Conf         | ✅     | Conf             | Conf    |
| Beach bar              | ✅     | ✅          | Conf         | ✅     | Conf             | Conf    |
| Φεστιβάλ (Festival)    | ✅     | ❌          | Conf         | ✅     | ❌                | ❌       |
| Self-service καφετέρια | ✅     | ❌          | Conf         | ✅     | ❌                | ❌       |
| Πανηγύρι               | ✅     | ✅          | Conf         | ✅     | Conf             | Conf    |

## Stretch Goals (Μελλοντικοί Στόχοι)

- Μαζική εκτύπωση QR codes σε σελίδα A4 (QR Code Mass Print)
- Επιλογή checkout ως επισκέπτης / αυθεντικοποίηση / έλεγχος μέσω SMS — μέτρα ασφαλείας
- Configurable καλάθι (Cart)
- Full payment settlement / light commission flow
- Room charge σε δωμάτιο ξενοδοχείου
- Κουμπί κλήσης σερβιτόρου (Call Button) με cooldown — configurable
- Κρατήσεις / Bookings — με αυθεντικοποίηση (Authentication)
- Ζωντανή διαθεσιμότητα / πληρότητα μαγαζιού (Live Capacity)
- Σύνδεση με εκτυπωτές → χαρτάκια παραγγελίας
- Τοπική βάση δεδομένων Master/Slave (Local DB) + Service Workers για λειτουργία εκτός σύνδεσης (Offline Mode) → [[features#3. Όταν Πέφτει το Internet]]
- AI chatbot / έξυπνες προτάσεις (Smart Suggestions) → [[startup_synopsis#4. Main Selling Points (Επιβεβαιωμένα)]]
- Speech-to-text παραγγελία ή αναζήτηση στο μενού
- Προσαρμοσμένο μενού ανάλογα με τις συνθήκες λειτουργίας, π.χ. προώθηση γρήγορων επιλογών όταν το venue είναι busy
- Feedback/reviews module για operational insights ή integration με Google Reviews

## Σχετικές Σημειώσεις

- [[features]] — Λεπτομέρειες λειτουργιών
- [[user_flow]] — Διαδρομή πελάτη
- [[staff_workflow]] — Ροή εργασίας προσωπικού
- [[pricing_model]] — Μοντέλο τιμολόγησης
- [[roadmap]] — Χρονοδιάγραμμα ανάπτυξης

## Επόμενες Ενέργειες

- [ ] Οριστικοποίηση λίστας χαρακτηριστικών ανά tier (Free/Basic/Pro/Enterprise) → [[pricing_model#Tiered subscription]]
- [ ] Δημιουργία wireframes για τις 3 βασικές σελίδες (Πελάτης, Staff/KDS, Admin)
- [ ] Δοκιμή "Fake MVP": Πριν χτιστεί πλήρως το backend, δημιουργία mockup στο κινητό για demo/walk-in σε beach bars. Στόχος: μέτρηση άμεσου ενδιαφέροντος (Ναι/Όχι).
- [ ] Επιλογή ενός πρώτου narrow use case για pilot, πριν προστεθούν hotel/POS/AI-heavy flows.


### Αλληλεπίδραση με υπάρχοντα POS
- Το σύστημα μας λειτουργεί αρχικά ως Staff Dashboard/αυτόνομο self-service layer, χωρίς περίπλοκα POS integrations στο MVP.
