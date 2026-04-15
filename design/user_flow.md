# 1. Διαδρομή Πελάτη (User Flow)
Η εμπειρία του πελάτη από το σκανάρισμα του QR code μέχρι την παραλαβή της παραγγελίας, με πρόβλεψη για τη λειτουργία σε τοπικό δίκτυο (Offline Fallback).

### Ροή Πελάτη (Customer Flow)
```
QR Scan → Επαλήθευση Τραπεζιού → Μενού → Προϊόν/Customization → Καλάθι → Checkout → Order Tracking (real-time SSE)
```
- Το καλάθι αποθηκεύεται σε `localStorage` με 6ωρο expiry.
- Αν αλλάξει τραπέζι (νέο QR), το καλάθι καθαρίζεται αυτόματα.
- Υποστηρίζεται `pay_now` ή `add_to_tab` billing mode.
- Το Pricing snapshot κλειδώνει τις τιμές τη στιγμή της παραγγελίας.

### Real-Time System (SSE)
Η επικοινωνία σε πραγματικό χρόνο επιτυγχάνεται με Server-Sent Events (SSE) (στα endpoints `/api/orders/sse`, `/api/tabs/sse`, κλπ.) με auto-reconnection και polling fallback.

### Οπτικοποίηση

```mermaid
graph TD
    A[Έναρξη: Σκανάρισμα QR ή NFC στο τραπέζι ή stand] --> B{Υπάρχει Internet}
    
    B -- Ναι --> C[Mobile App ή Web Interface]
    B -- Όχι --> D[Σύνδεση σε τοπικό WiFi Offline Mode]
    
    C --> E[Επαλήθευση Τραπεζιού & Πλοήγηση στο μενού]
    D --> E
    
    E --> F{Τρόπος πληρωμής / Billing mode}
    
    F -- pay_now (Online Card ApplePay) --> G[Επιτυχής πληρωμή]
    F -- add_to_tab (Λογαριασμός / Μετρητά) --> H[Παραγγελία σε κατάσταση pending]
    
    G --> I[Αποστολή στο Staff Dashboard / SSE updates]
    H --> I
    
    I --> J[Ο πελάτης λαμβάνει αριθμό παραγγελίας και order tracking]
    
    J --> K{Έτοιμη η παραγγελία}
    
    K -- Ναι --> L[Ειδοποίηση SSE ή Status Update]
    
    L --> M[Παραλαβή στο Stand και ταυτοποίηση]
    
    M --> N[Ολοκλήρωση παραγγελίας]
```

## Σχετικές Σημειώσεις
- [[staff_workflow]] — Ροή εργασίας προσωπικού
- [[v1_scope]] — Εύρος MVP

## Επόμενες Ενέργειες
- [ ] Έλεγχος UI/UX για το `localStorage` clear sequence όταν αλλάζει το QR/τραπέζι.
