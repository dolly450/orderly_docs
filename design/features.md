# Επιχειρησιακές Εξαιρέσεις & Λειτουργίες (Operational Features & Edge Cases)

Λεπτομέρειες που καθορίζουν την επιτυχία στην πράξη. Το Demo Orderly περιέχει **37 πλήρως υλοποιημένα features** οργανωμένα ανά ρόλο.

## Λίστα Λειτουργιών (Feature Registry)

### Πελάτης (10 features)
| Feature | Περιγραφή |
|---|---|
| QR Table Entry | Είσοδος μέσω QR, επαλήθευση τραπεζιού |
| Menu Browser | Περιήγηση μενού με φίλτρα & quick-add |
| Product Detail | Λεπτομέρειες προϊόντος, variants, modifiers, σημειώσεις |
| Shopping Cart | Καλάθι με ποσότητες, αφαίρεση, σύνολα |
| Checkout | Επιλογή πληρωμής, τοποθέτηση παραγγελίας |
| Order Tracking | Real-time timeline κατάστασης παραγγελίας |
| Client Tab View | Ανοιχτός λογαριασμός τραπεζιού |
| Call Waiter | Κλήση σερβιτόρου με cooldown |
| Table Reservations | Φόρμα κράτησης με ζώνες |
| Venue Info | Πληροφορίες χώρου (Wi-Fi, ωράριο) |

### Σερβιτόρος (10 features)
| Feature | Περιγραφή |
|---|---|
| Order Queue Panel | Ουρά παραγγελιών (pending/in-progress/ready) |
| Order Status Manager | Προώθηση κατάστασης παραγγελίας |
| Waiter Calls Panel | Ενεργές κλήσεις σερβιτόρου |
| Staff Reservations | Κρατήσεις με confirm/cancel |
| Staff Workforce | Βάρδιες, claims, ζώνες |
| Open Tabs | Ανοιχτοί λογαριασμοί ανά τραπέζι |
| Queue/InProgress/Ready Lists | Granular toggles ανά section |

### Κουζίνα (3 features)
| Feature | Περιγραφή |
|---|---|
| Kitchen Ticket Board | Board tickets με SLA timer |
| Station Filter | All/Kitchen/Bar φίλτρα |
| Quick Status Actions | One-tap delivered chips |

### Admin (7 features)
| Feature | Περιγραφή |
|---|---|
| Dashboard KPIs | Revenue, orders, occupancy, avg prep time |
| Menu Manager | CRUD μενού με advanced editor (variants, modifiers) |
| Reservations Manager | Διαχείριση κρατήσεων |
| Analytics View | Ωριαία γραφήματα (πραγματικά δεδομένα) |
| Table/QR Manager | CRUD τραπεζιών, ζώνες, floor plan, QR codes |
| Venue Settings | Wi-Fi, service fees, workflow, assignment strategy |
| Translations Manager | AI-powered bulk μεταφράσεις μενού |

### Shared / Global (7 features)
- 4 SSE κανάλια (orders, occupancy, reservations, tabs)
- Demo Mode Toggle
- Demo Data Seed
- Reservation Create Form (shared μεταξύ client & staff)

## Βασικές Αρχές

### 1. Πληρωμές: Viva Wallet (Προτίμηση)
Η **Viva Wallet (Viva.com)** είναι η ιδανική επιλογή:
- Ελληνική υποστήριξη και φορολογική συμβατότητα
- Υποστήριξη Apple Pay / Google Pay
- Χαμηλές προμήθειες (Νόμος 5167/2024: 0,5% για συναλλαγές <20€)
- *Εναλλακτικά:* Stripe (καλύτερο Dev Experience)

### 2. GDPR & Ιδιωτικότητα (Privacy)
- **Ανώνυμη χρήση εξ ορισμού (Anonymous by Default):** Δεν χρειάζεται εγγραφή ή σύνδεση (Login) για την παραγγελία
- **Κρυπτογράφηση δεδομένων (Tokenization):** Τα δεδομένα πληρωμής δεν αποθηκεύονται
- **Τοπική αποθήκευση (Local Storage):** Χρήση EU-based servers

### 3. Όταν Πέφτει το Internet & Local-First Architecture (Offline Fallback)
Το μεγαλύτερο πρόβλημα αντιμετωπίζεται με τη Local-First αρχιτεκτονική του Tauri v2+:

```mermaid
flowchart TD
    A[Συσκευή Καταστήματος\n(Laptop / Mobile / RPi)] -->|1-Click Setup| B[Local Database Running]
    B -->|Ping IP| C[Cloud Server]
    D[Χρήστης στο Local WiFi] -->|Primary Route| B
    B -.->|Background Sync| E[Cloud Database\n(Turso/libSQL)]
    D -.->|Fallback Route\n(Αν δεν είναι στο WiFi)| E
```

### 4. Διαχείριση QR Codes (QR Code Management)
- **Dynamic QR (Δυναμικά QR):** Redirect μέσω short-URLs.
- **Table Verification (Επιβεβαίωση Τραπεζιού):** Επιβεβαίωση αριθμού.
- **Durability (Αντοχή):** Πλαστικοποίηση.

## Σχετικές Σημειώσεις
- [[v1_scope]] — Εύρος MVP
- [[user_flow]] — Διαδρομή πελάτη
- [[staff_workflow]] — Ροή εργασίας προσωπικού
- [[pos_compliance]] — Φορολογική συμμόρφωση
- [[technical_stack]] — Τεχνική αρχιτεκτονική

## Επόμενες Ενέργειες
- [ ] Έρευνα κόστους LLM APIs vs Google Translate API για αυτόματη μετάφραση μενού στο Admin panel.
