# Σχεδιασμός Συστήματος Παραγγελιοληψίας (Refine)

Αυτό το έγγραφο περιέχει τον ολοκληρωμένο σχεδιασμό και την οπτικοποίηση του συστήματος παραγγελιοληψίας για εκδηλώσεις (καντίνες, φεστιβάλ, κλπ.) βασισμένο στην έρευνα και τις συζητήσεις "Refine".

---

## 1. Διαδρομή Πελάτη (User Flow)
[Λεπτομέρειες στο αρχείο: design/user_flow.md](file:///home/harold/.openclaw/workspace/projects/orderly_docs/design/user_flow.md)

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

## 2. Αρχιτεκτονική Συστήματος (Υβριδικό Μοντέλο)
[Λεπτομέρειες στο αρχείο: architecture/system_architecture.md](file:///home/harold/.openclaw/workspace/projects/orderly_docs/architecture/system_architecture.md)

```mermaid
graph LR

    Customer[Customer Phone]
    Gateway[Local Router Gateway]
    LocalDB[(Local Database)]
    Staff[Staff Tablet]
    Display[Pickup Screen]

    API[Backend API]
    CloudDB[(Cloud Database)]
    Auth[Payment Services]

    Customer -->|Scan QR| Gateway
    Gateway -->|Offline Access| LocalDB
    Gateway -->|Sync| API

    Staff -->|Manage Orders| LocalDB
    Staff -->|Sync| CloudDB

    Display -->|Show Status| LocalDB

    API --> CloudDB
    API --> Auth
```

---

## 3. Κύκλος Ζωής Παραγγελίας (State Machine)
[Λεπτομέρειες στο αρχείο: design/order_lifecycle.md](file:///home/harold/.openclaw/workspace/projects/orderly_docs/design/order_lifecycle.md)

```mermaid
stateDiagram-v2
    [*] --> Δημιουργήθηκε
    Δημιουργήθηκε --> Πληρώθηκε: Επιτυχία Πληρωμής
    Δημιουργήθηκε --> Εκκρεμεί_Μετρητά: Επιλογή Μετρητών
    Εκκρεμεί_Μετρητά --> Πληρώθηκε: Επιβεβαίωση από Υπάλληλο
    
    Πληρώθηκε --> Προετοιμάζεται: Έναρξη από Υπάλληλο
    Προετοιμάζεται --> Έτοιμη: Ολοκλήρωση Προετοιμασίας
    
    state Έτοιμη {
        [*] --> Αναμονή_Παραλαβής
        Anamoni_Paralavis --> Ειδοποίηση_Εστάλη
    }
    
    Έτοιμη --> Ολοκληρώθηκε: Παράδοση & Ταυτοποίηση
    Έτοιμη --> Εγκαταλείφθηκε: Timeout / Μη Παραλαβή
    
    Δημιουργήθηκε --> Ακυρώθηκε: Από τον Πελάτη
    Πληρώθηκε --> Επιστροφή_Χρημάτων: Από τον Υπάλληλο
    
    Ολοκληρώθηκε --> [*]
    Εγκαταλείφθηκε --> [*]
    Ακυρώθηκε --> [*]
    Επιστροφή_Χρημάτων --> [*]
```

---

## 4. Επιχειρησιακή Ροή Υπαλλήλων (Batch Preparation)
[Λεπτομέρειες στο αρχείο: design/staff_workflow.md](file:///home/harold/.openclaw/workspace/projects/orderly_docs/design/staff_workflow.md)

```mermaid
sequenceDiagram
    participant C as Πελάτης
    participant S as Σύστημα
    participant SP as Υπάλληλος (Προετοιμασία)
    participant SD as Υπάλληλος (Παράδοση)
    
    C->>S: Παραγγελία (3 Μπύρες, 1 Σάντουιτς)
    S->>S: Διαχωρισμός (Ποτά: Α, Φαγητό: Β)
    S-->>SP: Εμφάνιση στις αντίστοιχες Ουρές
    
    Note over SP: 10 Παραγγελίες Μπύρας στην Ουρά Α
    SP->>SP: Batch Action: Άνοιγμα 10 Μπουκαλιών
    SP->>S: Σήμανση Ποτών ως 'Έτοιμα'
    
    S-->>C: Update: "Τα ποτά σας είναι έτοιμα"
    
    Note over SP: Προετοιμασία Σάντουιτς (Ουρά Β)
    SP->>S: Σήμανση Παραγγελίας #123 ως Πλήρως Έτοιμη
    S-->>C: Ειδοποίηση: "Η Παραγγελία #123 είναι έτοιμη για παραλαβή"
    
    C->>SD: Επίδειξη Κωδικού/QR #123
    SD->>SD: Ταυτοποίηση & Παράδοση
    SD->>S: Σήμανση ως Ολοκληρωμένη
```

---

## 5. Ανάλυση Αγοράς (Market Analysis & Strategy)
[Λεπτομέρειες στο αρχείο: business/market_strategy.md](file:///home/harold/.openclaw/workspace/projects/orderly_docs/business/market_strategy.md)

```mermaid
mindmap
  root((Σύστημα Παραγγελιοληψίας))
    Στόχοι
      Αύξηση Throughput
      Μείωση Ουρών
      Μείωση Λαθών Πληρωμής
    Κοινό Στόχος
      Beach Bars
      Καντίνες Συναυλιών
      Food Festivals
      Στάδια
    Ανταγωνιστικό Πλεονέκτημα
      Offline Λειτουργία
      Batch Preparation Logic
      Υβριδική Πληρωμή (App + Cash)
    Προκλήσεις
      Crowd Behaviour
      Internet Reliability
      Staff Training
```

---

## 6. Οδικός Χάρτης MVP (MVP Roadmap)
[Λεπτομέρειες στο αρχείο: business/roadmap.md](file:///home/harold/.openclaw/workspace/projects/orderly_docs/business/roadmap.md)

```mermaid
gantt
    title Σχέδιο Δράσης MVP (Προτεινόμενο)
    dateFormat  YYYY-MM-DD
    section Φάση 1: Core
    Βασικό UI & Ordering       :a1, 2026-04-01, 20d
    Database Schema & API      :done, a2, 2026-04-01, 15d
    section Φάση 2: Operations
    Staff Dashboard (KDS)     :a3, 2026-04-20, 15d
    QR Management & ID logic   :a4, 2026-04-25, 10d
    section Φάση 3: Connectivity
    Offline Local Sync         :a5, 2026-05-10, 20d
    Hybrid Payments (Cash/Stripe): a6, 2026-05-20, 15d
    section Φάση 4: Testing
    Pilot Test (Small Event)   :crit, a7, 2026-06-15, 7d
    Refining based on feedback :a8, 2026-06-22, 14d
```

---

## 7. Μοντέλο Δεδομένων (ERD)
[Λεπτομέρειες στο αρχείο: architecture/data_model.md](file:///home/harold/.openclaw/workspace/projects/orderly_docs/architecture/data_model.md)

```mermaid
erDiagram

    CANTEEN {
        string id
        string name
        string location
    }

    CATEGORY {
        string id
        string name
        string canteenId
    }

    PRODUCT {
        string id
        string name
        float price
        string categoryId
    }

    USER {
        string id
        string name
        string phone
    }

    ORDER {
        string id
        string status
        float totalAmount
        string paymentStatus
        datetime createdAt
        string customerName
    }

    ORDER_ITEM {
        string id
        string orderId
        string productId
        int quantity
        string prepStatus
    }

    INVENTORY {
        string productId
        int stockLevel
    }

    CANTEEN ||--o{ CATEGORY : has
    CATEGORY ||--o{ PRODUCT : contains
    USER ||--o{ ORDER : places
    ORDER ||--o{ ORDER_ITEM : includes
    PRODUCT ||--o{ ORDER_ITEM : ordered_as
    PRODUCT ||--|| INVENTORY : tracked_by
```
