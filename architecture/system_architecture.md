# Αρχιτεκτονική Συστήματος (System Architecture - Υβριδικό Μοντέλο)

Οπτικοποίηση της αλληλεπίδρασης μεταξύ Cloud, τοπικού δικτύου (Local Network) και συσκευών. Η τοπική πύλη (Gateway) υλοποιείται μέσω **Tauri v2+** (one-click install), το οποίο φιλοξενεί έναν τοπικό διακομιστή (Local Server) και μία embedded replica βάση δεδομένων (μέσω Turso/libSQL).

### Οπτικοποίηση (Visualisation)

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

## Σχετικές Σημειώσεις
- [[data_model]]
- [[technical_stack]]
- [[overview]]

## Επόμενες Ενέργειες
- [ ] Δοκιμή (Stress Test) του Gateway (Tauri v2+) σε συνθήκες offline λειτουργίας (απουσία internet) για 24 ώρες για να επιβεβαιωθεί η αξιοπιστία της τοπικής βάσης.
