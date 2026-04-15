# 6. Οδικός Χάρτης MVP (MVP Roadmap)

Σχέδιο δράσης για την ανάπτυξη και την πρώτη δοκιμή του συστήματος, έχοντας ως βάση το ήδη υλοποιημένο Demo Orderly (37 λειτουργίες, 4 ρόλοι, 5 SSE κανάλια, 2 γλώσσες).

```mermaid
gantt
    title Σχέδιο Δράσης MVP (Προτεινόμενο)
    dateFormat  YYYY-MM-DD
    section Φάση 1: Core (Ολοκληρώθηκε στο Demo)
    Βασικό UI & Ordering       :done, a1, 2026-04-01, 20d
    Database Schema & API      :done, a2, 2026-04-01, 15d
    Staff Dashboard & Admin    :done, a3, 2026-04-10, 10d
    section Φάση 2: Operations
    E2E Testing Suite         :a4, 2026-04-20, 10d
    Payment Integration       :a5, 2026-04-25, 10d
    Floor Plan Editor         :a6, 2026-05-01, 15d
    section Φάση 3: Connectivity
    Offline Local Sync         :a7, 2026-05-10, 20d
    Push Notifications         :a8, 2026-05-20, 10d
    section Φάση 4: Testing & Scale
    Pilot Test (Small Event)   :crit, a9, 2026-06-15, 7d
    Refining based on feedback :a10, 2026-06-22, 14d
```

## Σχέδιο Δράσης (Action Plan) & Insights

Η πλατφόρμα είναι σε προχωρημένο στάδιο. Βάσει των insights, τα παρακάτω είναι "Low-Hanging Fruits" (Σχεδόν έτοιμα):

1. **E2E Testing Suite & CI Pipeline:** Η υποδομή (Vitest, i18n checks) είναι έτοιμη. Απαιτείται ολοκλήρωση των test workflows.
2. **Analytics:** Tα ωριαία γραφήματα χρησιμοποιούν ήδη πραγματικά δεδομένα από τη DB. Απαιτείται απλώς αφαίρεση τυχόν υπολειπόμενων mock data.
3. **Per-Role Feature Configuration:** Το Feature Registry υπάρχει. Λείπει μόνο το UI διαχείρισης στο Admin panel.
4. **Floor Plan Visual Editor:** Οι συντεταγμένες (x, y) υπάρχουν στη βάση. Χρειάζεται ένα drag-and-drop UI.
5. **Payment Integration & Push Notifications:** Η υποδομή billing (tabs/pay_now) και τα SSE channels υπάρχουν, έτοιμα να δεχθούν τα αντίστοιχα external APIs.

## Σχετικές Σημειώσεις

- [[v1_scope]] — Εύρος MVP
- [[market_strategy]] — Στρατηγική αγοράς
- [[deck]] — Pitch deck
- [[The long road of turning your idea toa successful startup]] — Στρατηγική ανάπτυξης

## Επόμενες Ενέργειες

- [ ] Δημιουργία issues στο repository για τα 5 "Σχεδόν Έτοιμα" insights (π.χ. E2E tests, Floor Plan editor).
