# Σκοπός V1 (MVP Scope)

## Βασικά Χαρακτηριστικά (Features)
1. **Menu + Εικόνες** (configurable)
2. **Καλάθι / Παραγγελία**
3. **Ordering Process:** Καθορισμός ποιος παραγγέλνει.
4. **Κατάσταση Παραγγελίας:** Info & queue (time-related estimation).
5. **Σύνδεση με εκτυπωτές** (xartakia / KDS fallback).
6. **Πληροφορίες καταστήματος:** WiFi info κ.λπ.
7. **Κουμπί κλήσης σερβιτόρου:** (με cooldown / configurable).
8. **Analytics:** Τι χρησιμοποιούν οι πελάτες από το UI.
9. **UI / Σελίδες (4 views):**
   - Πελάτες (PWA / Web)
   - Σερβιτόρος (Tablet / PDA)
   - Κουζίνα (KDS)
   - Admin (Dashboard)
10. **Ordely (Διαφημιστικό / Landing):**
    - Live demo από fake κατάστημα.
    - Trial (π.χ. 15 μέρες) -> μετά αγορά subscription.
    - Τα subscriptions τρέχουν σε EC2 (docker), τα trials σε άλλο VM.
11. **Πολυγλωσσικότητα (Multilingual)**

*Σημείωση:* Η V1 θα είναι Cloud-first, το offline (local db master/slave) είναι προς το παρόν stretch goal / V2.

## Πίνακας Λειτουργιών ανά Επιχείρηση

| επιχείρηση     | menu | servitoros | self co | queues | call button | booking |
| -------------- | ---- | ---------- | ------- | ------ | ----------- | ------- |
| full serv cafe | yes  | yes        | conf    | yes    | conf        | conf    |
| beach bar      | yes  | yes        | conf    | yes    | conf        | conf    |
| festival       | yes  | no         | conf    | yes    | no          | no      |
| self serv cafe | yes  | no         | conf    | yes    | no          | no      |
| panigiri       | yes  | yes        | conf    | yes    | conf        | conf    |

## Stretch Goals (Μελλοντικά)
- QR code mass print σε A4.
- Επιλογή checkout as guest vs auth / έλεγχος SMS (security measures).
- Offline λειτουργία (Local DB master/slave & service workers).
- Κρατήσεις / Bookings (με auth).
- POS / PDA Integration (Deep knowledge).
- AI chat bot / Smart suggestions.

---

## Σχετικές Σημειώσεις
- [[design/features.md]]: Αναλυτική περιγραφή των features.
- [[design/user_flow.md]]: Το user journey (flow) των παραπάνω features.
- [[architecture/system_architecture.md]]: Πώς θα στηθούν τα EC2/VMs για τα trials/subscriptions.
- [[business/pricing_model.md]]: Πώς κοστολογείται το trial και τα subscriptions.

## Υποθέσεις & Validation Experiments (Needs Review)
- **Υπόθεση:** Η εγγραφή μέσω SMS (security measure) προσθέτει υπερβολικό friction στους πελάτες (τουρίστες) και μειώνει το conversion rate των παραγγελιών.
- **Validation Experiment:**
  - **Ενέργεια:** A/B Testing σε ένα live pilot (Group A: Guest checkout, Group B: SMS Validation).
  - **Κριτήριο Επιτυχίας:** Αν το Group A έχει >20% περισσότερες ολοκληρωμένες παραγγελίες και τα fake orders είναι <1%, τότε το SMS validation θα μεταφερθεί εκτός MVP ή θα γίνει προαιρετικό.