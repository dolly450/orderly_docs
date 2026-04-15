# Μοντέλο Δεδομένων (Data Model - ERD)

Οι σχέσεις μεταξύ των βασικών οντοτήτων (entities) για την υποστήριξη της επιχειρησιακής λογικής (business logic) του συστήματος.

### Οπτικοποίηση (Visualisation)

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

## Σχετικές Σημειώσεις
- [[system_architecture]]
- [[technical_stack]]

## Επόμενες Ενέργειες
- [ ] Επαλήθευση του μοντέλου δεδομένων (ERD) με τους developers για τυχόν παραλείψεις πριν την έναρξη του Phase 1 (MVP - Minimum Viable Product).
