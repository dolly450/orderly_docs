# Εύρος MVP v1 (MVP v1 Scope)

Βασικά χαρακτηριστικά και λειτουργίες που πρέπει να περιλαμβάνει η πρώτη έκδοση.

## Βασικές Λειτουργίες

1. Μενού (Menu) + εικόνες (configurable)
2. Καλάθι (Cart) → Παραγγελία (Order)
3. Διαδικασία παραγγελίας (Ordering Process) — ποιοι παραγγέλνουν;
4. Πληροφορίες για κατάσταση παραγγελίας (Order Status) + ουρά αναμονής (Queue) με χρονική εκτίμηση
5. Σύνδεση με εκτυπωτές → χαρτάκια παραγγελίας
6. Πληροφορίες για WiFi και το μαγαζί
7. Κουμπί κλήσης σερβιτόρου (Call Button) με cooldown — configurable
8. Κρατήσεις / Bookings — με αυθεντικοποίηση (Authentication)
9. Μόνο cloud, όχι localhost
10. Αναλυτικά στοιχεία χρήσης (Analytics) για το τι χρησιμοποιούν οι χρήστες από το UI — ενσωμάτωση εργαλείων όπως PostHog/Mixpanel από την 1η μέρα για παρακολούθηση QR scans, cart additions και drop-offs. → [[Product Design]]
11. Τέσσερις σελίδες: Χρήστες/Πελάτες, Σερβιτόρος, Κουζίνα, Admin
12. Διαφημιστική σελίδα (Landing Page) — live demo από ψεύτικο κατάστημα
13. Δοκιμαστική περίοδος (Trial) π.χ. 15 ημέρες → αγορά συνδρομής (Subscription) από admin
    - Τα subscriptions θα τρέχουν σε EC2 instance (αξιόπιστο) ως Docker containers
    - Τα trials θα τρέχουν σε ξεχωριστό VM ως Docker containers (δωρεάν)
    - Επιπλέον χρέωση (Extra Fee) για service / maintenance
14. Καλή γνώση για **POS / PDA ενσωμάτωση (Integration)** → [[pos_compliance]]
15. Πολυγλωσσικότητα (Multilingual) → [[features#4. Πολυγλωσσικότητα (Multilingual)]]
16. Ζωντανή διαθεσιμότητα / πληρότητα μαγαζιού (Live Capacity)

> **Σημείωση:** Απλό και εύκολο στη χρήση (Simple and easy to use) — αυτό αναφέρεται και ως θετικό του [[competitive_analysis|Butler]].

## Πίνακας Λειτουργιών ανά Τύπο Venue

| Τύπος Επιχείρησης | Μενού | Σερβιτόρος | Self-Service | Ουρές | Κλήση Σερβιτόρου | Κράτηση |
|---|---|---|---|---|---|---|
| Full-service καφετέρια | ✅ | ✅ | Conf | ✅ | Conf | Conf |
| Beach bar | ✅ | ✅ | Conf | ✅ | Conf | Conf |
| Φεστιβάλ (Festival) | ✅ | ❌ | Conf | ✅ | ❌ | ❌ |
| Self-service καφετέρια | ✅ | ❌ | Conf | ✅ | ❌ | ❌ |
| Πανηγύρι | ✅ | ✅ | Conf | ✅ | Conf | Conf |

## Stretch Goals (Μελλοντικοί Στόχοι)

- Μαζική εκτύπωση QR codes σε σελίδα A4 (QR Code Mass Print)
- Επιλογή checkout ως επισκέπτης / αυθεντικοποίηση / έλεγχος μέσω SMS — μέτρα ασφαλείας
- Configurable καλάθι (Cart)
- Τοπική βάση δεδομένων Master/Slave (Local DB) + Service Workers για λειτουργία εκτός σύνδεσης (Offline Mode) → [[features#3. Όταν Πέφτει το Internet]]
- AI chatbot / έξυπνες προτάσεις (Smart Suggestions) → [[startup_synopsis#4. Main Selling Points (Επιβεβαιωμένα)]]

## Σχετικές Σημειώσεις

- [[features]] — Λεπτομέρειες λειτουργιών
- [[user_flow]] — Διαδρομή πελάτη
- [[staff_workflow]] — Ροή εργασίας προσωπικού
- [[pricing_model]] — Μοντέλο τιμολόγησης
- [[roadmap]] — Χρονοδιάγραμμα ανάπτυξης

## Επόμενες Ενέργειες

- [ ] Οριστικοποίηση λίστας χαρακτηριστικών ανά tier (Free/Basic/Pro/Enterprise) → [[pricing_model#Tiered subscription]]
- [ ] Δημιουργία wireframes για τις 4 βασικές σελίδες (Πελάτης, Σερβιτόρος, Κουζίνα, Admin)
- [ ] Δοκιμή "Fake MVP": Πριν χτιστεί πλήρως το backend, δημιουργία mockup στο κινητό για demo/walk-in σε beach bars. Στόχος: μέτρηση άμεσου ενδιαφέροντος (Ναι/Όχι).
- [ ] Έρευνα (Validation experiment): Παρουσίαση του Fake MVP σε 5 beach bars. Μετρική επιτυχίας: ≥3 επιχειρήσεις να δεχτούν να συμμετέχουν στο δωρεάν trial.