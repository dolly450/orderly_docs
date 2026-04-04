# Business Model Canvas - Orderly

## Key Partners
- Πάροχοι POS (π.χ. BringFood)
- Payment Gateways (Stripe, Viva Wallet, Apple Pay, Google Pay)
- Εταιρείες Παροχής Internet & Hardware (για το Offline Local Sync routing/tablet)

## Key Activities
- Ανάπτυξη & Συντήρηση Πλατφόρμας (SaaS)
- Ενσωματώσεις με third-party (POS, ΑΑΔΕ/myDATA)
- Πωλήσεις B2B & Customer Onboarding

## Key Resources
- Η Ομάδα Ανάπτυξης (Development)
- Cloud Infrastructure (AWS / Docker)
- Αλγόριθμοι / Tech για Local Offline Sync

## Value Propositions
- **Για επιχειρήσεις:** Μείωση λαθών, αύξηση ταχύτητας εξυπηρέτησης (throughput), 100% λειτουργία offline.
- **Για πελάτες:** Καμία αναμονή για κατάλογο/σερβιτόρο, άμεση πληρωμή, πολυγλωσσικότητα.

## Customer Relationships
- B2B Προσωπικές πωλήσεις (για αρχικούς πελάτες/pilots)
- Self-serve on-boarding & Dedicated Support για Enterprise πελάτες

## Channels
- Απευθείας Πωλήσεις (Cold calling / Door-to-door σε Beach Bars/Εστιατόρια)
- Word-of-Mouth
- Social Media / B2B Marketing & Συνέδρια Εστίασης/Τουρισμού

## Customer Segments
- Εποχιακά καταστήματα (Beach Bars)
- Υψηλού όγκου / ταχύτητας venues (Στάδια, Food Festivals, Πανηγύρια)
- Full service & Self Service cafes

## Cost Structure
- Κόστη Server/Cloud hosting & Database
- Έξοδα Marketing / Πωλήσεων
- Υπηρεσίες API τρίτων (SMS validation κλπ.)
- Συντήρηση & Customer Support

## Revenue Streams
- Μηνιαία/Ετήσια Συνδρομή (SaaS: Basic, Pro, Enterprise)
- Transaction Fees (Commission-based μοντέλο, π.χ. 3-5%)
- Πωλήσεις / Ενοικιάσεις Hardware (Tablets, Routers)

---

## Σχετικές Σημειώσεις
- [[business/pricing_model.md]]: Ανάλυση του SaaS vs Commission μοντέλου.
- [[business/market_strategy.md]]: Go-to-market plan και market analysis.
- [[pitch/deck.md]]: Πώς παρουσιάζεται αυτό το μοντέλο σε investors.
- [[architecture/system_architecture.md]]: Τεχνική υποδομή που στηρίζει τα key resources.

## Υποθέσεις & Validation Experiments (Needs Review)
- **Υπόθεση:** Οι ιδιοκτήτες Beach Bars προτιμούν το commission-based (3-5%) αντί για πάγια συνδρομή γιατί δεν έχουν ρίσκο.
- **Validation Experiment:**
  - **Ενέργεια:** Cold-call / Συνεντεύξεις με 10 ιδιοκτήτες Beach Bars δίνοντας δύο επιλογές τιμολόγησης.
  - **Κριτήριο Επιτυχίας:** Τουλάχιστον 6/10 να προτιμήσουν το Commission μοντέλο για να θεωρηθεί valid το revenue stream μας.