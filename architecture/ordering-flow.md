# Σχεδιασμός Ροής Παραγγελίας (Ordering Flow Design)

Αυτή είναι η λεπτομερής ροή παραγγελίας, από το scan του QR κωδικού (QR code) μέχρι την παράδοση (Delivery).

### Οπτικοποίηση

```mermaid
sequenceDiagram
    participant C as Customer (PWA)
    participant S as Server (SvelteKit / Go API)
    participant K as Kitchen Display (Local)
    participant P as POS / Fiscal (Local/Cloud)

    C->>S: Scan QR & Fetch Menu
    S-->>C: Return Menu (LLM/Google Translated Cached)
    C->>S: Submit Order (Cart items & Table Info)
    S->>S: Create Order (Status: Pending)

    rect rgb(200, 220, 240)
        Note over S,P: Integration Layer (POS Phase 2)
        S->>P: Send to POS / Tax Verification
        P-->>S: Confirmed & Receipt URL
    end

    S->>K: Emit SSE/Local DB Sync: New Order
    S-->>C: Order Success & Estimated Time

    K->>S: Update Status (Preparing)
    S-->>C: SSE/Poll: Preparing (Ενημέρωση UI)

    K->>S: Update Status (Ready/Delivered)
    S-->>C: SSE/Poll: Ready! (Ειδοποίηση πελάτη)

    opt Offline Mode
        Note over C,K: Τοπικό δίκτυο: Τα αιτήματα πηγαίνουν απευθείας στο Local Gateway (Tauri)
    end
```

## Σχετικές Σημειώσεις

- [[user_flow]] — Διαδρομή πελάτη (υψηλού επιπέδου)
- [[order_lifecycle]] — Κύκλος ζωής παραγγελίας (state machine)
- [[staff_workflow]] — Ροή εργασίας προσωπικού (batch preparation)
- [[data_model]] — Μοντέλο δεδομένων

## Επόμενες Ενέργειες

- [ ] Validation Experiment: Σχεδιασμός ενός mock API (στοχεύοντας το Epsilon Net/SBZ Systems API) για να επιβεβαιώσουμε τη βιωσιμότητα του integration. -> [[architecture/pos_compliance.md]]
