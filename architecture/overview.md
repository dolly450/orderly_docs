# Architecture Overview

Το σύστημα παραγγελιοληψίας (Orderly) ακολουθεί μια υβριδική αρχιτεκτονική (Cloud & Local Offline Sync), ώστε να εξασφαλίζει αδιάλειπτη λειτουργία σε περιβάλλοντα με κακή σύνδεση (π.χ. Beach bars, φεστιβάλ).

## Βασικά Στοιχεία (Core Components)
1. **Cloud Υποδομή:** Το κεντρικό API, η κύρια βάση δεδομένων και η διαχείριση ταυτοποίησης / πληρωμών.
2. **Local Gateway:** Τοπικό δίκτυο στο μαγαζί (router / local DB) που επιτρέπει offline παραγγελιοληψία και συγχρονίζεται με το Cloud όταν υπάρχει διαθέσιμο δίκτυο.
3. **Client Apps:**
   - *Customer App:* Web-based (QR scan) για τον πελάτη (PWA / Mobile web).
   - *Staff App:* Tablet-based dashboard για σερβιτόρους / κουζίνα.

---

## Σχετικές Σημειώσεις
- [[architecture/system_architecture.md]]: Λεπτομερές διάγραμμα και ροή δεδομένων του συστήματος.
- [[architecture/data_model.md]]: Η δομή της βάσης δεδομένων και τα entities.
- [[architecture/ordering-flow.md]]: Ο σχεδιασμός του ordering state machine.
- [[architecture/pos_compliance.md]]: Συμμόρφωση με συστήματα POS (π.χ. myDATA, ΑΑΔΕ).

## Υποθέσεις & Validation Experiments (Needs Review)
- **Υπόθεση:** Ένα τοπικό Raspberry Pi / Mini PC λειτουργώντας ως Local DB/Gateway αρκεί για να χειριστεί τον όγκο ενός μεγάλου beach bar (π.χ. 300+ ταυτόχρονοι χρήστες) χωρίς lag.
- **Validation Experiment:**
  - **Ενέργεια:** Στήσιμο ενός stress-test περιβάλλοντος προσομοιώνοντας 500 requests/sec προς τον τοπικό server.
  - **Κριτήριο Επιτυχίας:** Ο χρόνος απόκρισης του local server να παραμένει κάτω από 200ms στο 95% των περιπτώσεων (p95 < 200ms).