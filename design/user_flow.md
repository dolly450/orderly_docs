# 1. Διαδρομή Πελάτη (User Flow)
Η εμπειρία του πελάτη από το σκανάρισμα του QR code μέχρι την παραλαβή της παραγγελίας, με πρόβλεψη για τη λειτουργία σε τοπικό δίκτυο (Offline Fallback).

```mermaid
graph TD
    A[Έναρξη: Σκανάρισμα QR ή NFC στο τραπέζι ή stand] --> B{Υπάρχει Internet}
    
    B -- Ναι --> C[Mobile App ή Web Interface]
    B -- Όχι --> D[Σύνδεση σε τοπικό WiFi Offline Mode]
    
    C --> E[Πλοήγηση στο μενού και επιλογή προϊόντων]
    D --> E
    
    E --> F{Τρόπος πληρωμής}
    
    F -- Online Card ApplePay --> G[Επιτυχής πληρωμή]
    F -- Μετρητά στο ταμείο --> H[Παραγγελία σε κατάσταση Εκκρεμεί]
    
    G --> I[Αποστολή στο Staff Dashboard]
    H --> I
    
    I --> J[Ο πελάτης λαμβάνει αριθμό παραγγελίας και εκτιμώμενο χρόνο]
    
    J --> K{Έτοιμη η παραγγελία}
    
    K -- Ναι --> L[Ειδοποίηση SMS ή Status Update]
    
    L --> M[Παραλαβή στο Stand και ταυτοποίηση]
    
    M --> N[Ολοκλήρωση παραγγελίας]
```

---

## Σχετικές Σημειώσεις
- [[architecture/ordering-flow.md]]: Technical Architecture of the Ordering Flow
