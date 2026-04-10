# 5. Ανάλυση Αγοράς & Στρατηγική (Market Analysis & Strategy)

Πού στοχεύει το προϊόν και ποιο είναι το ανταγωνιστικό του πλεονέκτημα.

## Βασικά Insights & Υποθέσεις (Key Assumptions)

**Το Κενό (The Gap):** Λύσεις όπως η παραγγελιοληψία μέσω QR (QR Ordering) δεν εφαρμόζονται παντού λόγω δισταγμού των διαχειριστών (Manager Hesitation), υψηλού κόστους λογισμικού ή κακού μάρκετινγκ — **όχι** λόγω τεχνικών προβλημάτων.

**Η Ευκαιρία (The Opportunity):** Δεν υπάρχει ακόμα μια κυρίαρχη, προϊοντοποιημένη (Productized) λύση. Όπου υπάρχει βελτίωση που δεν έχει εφαρμοστεί παντού, υπάρχει επιχειρηματική ευκαιρία.

**Υπόθεση (Assumption):** Η Τεχνητή Νοημοσύνη (AI — πρόβλεψη παραγγελιών, δυναμικά μενού, upselling) και η τιμολόγηση βάσει προμήθειας (Commission Pricing) δίνουν ξεκάθαρη, μετρήσιμη αξία (Measurable Value) στον καταστηματάρχη.

> ⚠️ **Αυτή η υπόθεση δεν έχει τεκμηριωθεί ακόμα (Unvalidated Assumption)** — απαιτεί επικύρωση μέσω πιλοτικών (Pilot Validation).

> **Επιπτώσεις για την Ομάδα:**
> Πρέπει να μετατοπίσουμε την προσοχή μας από το «πώς θα το χτίσουμε τέλεια» στο «πώς θα μάθουμε γρήγορα». Το κλειδί είναι η λογική Build-Measure-Learn. Εφόσον στοχεύουμε σε zero-friction (χωρίς login), χρειαζόμαστε άμεσα εργαλεία analytics (PostHog/Mixpanel) για να μετράμε το scan-to-order conversion rate και τα drop-offs. → [[Product Design]]

### Οπτικοποίηση

```mermaid
flowchart TD
    A[Unvalidated Assumption:\nAI & Commission Pricing\nφέρνουν Measurable Value] --> B{Validation Experiment}
    B -->|Ερωτηματολόγιο| C[Feedback από 100+ venues]
    B -->|Walking-in Demos| D[Demo σε 5 venues]
    C --> E[Data & Insights]
    D --> E
    E --> F[Proof of Concept]
    F --> G[Traction & Scaling]
```

## Στρατηγική Εισόδου στην Αγορά (Go-to-Market Strategy)

- **Γρήγορη είσοδος για κατάληψη αγοράς (Rapid Market Capture)** (λογική eFood): μπαίνουμε γρήγορα πριν γεμίσει η αγορά.
- **Επικύρωση πριν την κλίμακα (Validation Before Scale):** Πιλοτικό σε 5 καταστήματα/venues/ερωτηματολόγια → μετρήσεις (Metrics) → απόδειξη ιδέας (Proof of Concept) → επιχείρημα πώλησης (Selling Point). → Δέσιμο (Traction) → [[deck#6. Traction]]
- **Άμεση έρευνα αγοράς (Market Research):** Συνομιλία με 10 μαγαζιά για ανατροφοδότηση (Feedback) πριν οριστικοποιηθεί οτιδήποτε.

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

## Κανάλια Μάρκετινγκ (Marketing Channels)

### Πληρωμένη Απόκτηση (Paid Acquisition)
Πληρώνεις μια πλατφόρμα/εκδήλωση ώστε να σε φέρει μπροστά σε δυνητικούς πελάτες → π.χ. **Διαφημίσεις Facebook (FB Ads)**

### Πωλήσεις (Sales)
Πληρώνεις ένα _πρόσωπο_ να πείσει πελάτες να εγγραφούν → π.χ. **Sales rep κάνει cold calls σε bar owners**

1. **Cold Outreach (Ψυχρή Προσέγγιση):** Είτε αυτοπροσώπως, είτε με email — μπορούμε να το κάνουμε κι εμείς.
2. **Demo Calls (Επίδειξη Προϊόντος):** Παρουσίαση + pitch + δεδομένα [[Questionnaire]] + traction analytics.
3. **CRM (Customer Relationship Management — Διαχείριση Σχέσεων Πελατών):** Consistent emails, ενημερωτικά, follow-ups σε σωστούς χρόνους → **Πάρα πολύ σημαντικό**.
4. **Walking In (Αυτοπρόσωπη Επίσκεψη):** Κυριολεκτικά επισκεπτόμαστε bars και cafés με ένα tablet demo. Προφανές αλλά υποτιμημένο — οι ιδιοκτήτες εστίασης ανταποκρίνονται σε ανθρώπους, όχι σε emails.

### Κίνητρα (Incentives)
Δίνεις κάτι _δωρεάν_ για να κάνεις την εγγραφή λιγότερο ρίσκο → π.χ. **Δωρεάν πρώτος μήνας**

1. Δωρεάν πρώτοι μήνες
2. Δωρεάν εξοπλισμός, εγκατάσταση (Setup) κ.λπ.
3. Δωρεάν υπηρεσίες από συνεργαζόμενες εταιρείες (π.χ. ίντερνετ ή άλλες υπηρεσίες)
4. Πακέτα τύπου 1+1 ή κάτι τύπου πιστότητας (Loyalty) με πόντους

### Οργανικό (Organic — Μακροπρόθεσμη Παρουσία)

1. **SEO (Search Engine Optimization — Βελτιστοποίηση Μηχανών Αναζήτησης)**
2. **Δημιουργία περιεχομένου Social Media (Social Media Content Creation)**
3. **Ενημερωτικά δελτία μέσω email (Email Newsletters)**

### Παραπομπές (Referrals)

1. Από τον έναν manager στον άλλο — αξιολόγηση επιτυχίας (Success Review)
2. Συνεργασία με μέλη του οικοσυστήματος εστίασης — π.χ. τους προμηθευτές, τους λογιστές (Accountants), και στοχευμένα μέλη που «γνωρίζουν» καλά το κοινό μας, το κοινό μας τους εμπιστεύεται, και έμμεσα αγοράζουμε αυτή την εμπιστοσύνη (~€100/deal) — σαν affiliate.

### Άλλες Ιδέες

- **PR (Δημόσιες Σχέσεις):** Εμφάνιση σε groups, εφημερίδες, εκδηλώσεις εστίασης, ανεξάρτητοι φορείς (δημοσιογράφοι, podcasts κ.λπ.) → «δωρεάν» visibility
- **Community Building (Δημιουργία Κοινότητας):** Δημιουργία Facebook group ή forum για ιδιοκτήτες bar/cafe
- **Events (Εκδηλώσεις):** Διοργάνωση δικών μας hospitality meetups

### Σχετικό ερώτημα
Έχουν θέση οι influencers και affiliates δεδομένης της φύσης μας; → [[open-questions#Συνεργασίες & Marketing]]

## Συνοπτική Στρατηγική (Summary)

### Αρχική Φάση (Phase 1)
1. Cold outreach / Walking in κ.λπ.
2. Demo calls + Demo Pitch + Δεδομένα [[Questionnaire]] + Traction μελλοντικά από analytics
3. CRM
4. Organics + Incentive (παραδείγματα αναλυτικά πιο πάνω)
5. Referrals, PR, Community Building, Event Joining — κορυφαία σημασία

### Μακροπρόθεσμη Φάση (Phase 2 — Long Term)
- Event building (Διοργάνωση δικών μας εκδηλώσεων)

> **Τα Paid Ads (Πληρωμένες Διαφημίσεις)** είναι πανάκριβα και ειδικά για το εξειδικευμένο κοινό μας (Niche) δεν νομίζουμε ότι μας δίνουν αρκετό όφελος, εκτός από την περίπτωση Referral/Affiliate.

## Σχετικές Σημειώσεις

- [[Questionnaire]] — Ερωτηματολόγιο επικύρωσης
- [[competitive_analysis]] — Ανάλυση ανταγωνισμού
- [[pricing_model]] — Μοντέλο τιμολόγησης
- [[COGS, CACs, overheads]] — Κόστη
- [[deck]] — Pitch deck
- [[mentors]] — Μέντορες

## Επόμενες Ενέργειες

- [ ] Μιλάμε σε μαγαζιά, φίλους, γενικά για την ιδέα, να δούμε τι παίζει (π.χ. μπαρ στην Κύπρο που κάνει κάτι αρκετά παρόμοιο + McDonalds)
- [ ] Ερωτηματολόγιο (5-6 απλές ερωτήσεις τύπου ΝΑΙ/ΟΧΙ και πολλαπλής επιλογής, θα το πλασάρουμε σε φίλους, groups) → [[Questionnaire]]
- [ ] Demo MVP → [[roadmap]]
- [ ] Pitch σε μαγαζιά πιλοτικά (στην αρχή ως δωρεάν service) + για traction (**Προϋπόθεση:** να γίνει πρώτα το demo και το ερωτηματολόγιο, ώστε να έχουμε πιο πειστικό approach) → [[deck#6. Traction]]

### Ορισμοί Αγοράς (Market Definitions)
- **Total market:** Όλοι όσοι έχουν το πρόβλημα που εμείς λύνουμε.
- **Addressable market:** Όλοι όσοι θα μπορούσαν να χρησιμοποιήσουν το προϊόν μας για να λύσουν το πρόβλημα.
- **Target market:** Εκεί που κάνουμε launch (κάπου συγκεκριμένα, π.χ. στο Παγκράτι).

### Implementation Logic: Phase 1 Sales (Acquiring First 10 Customers)
- **Primary Method:** Direct Sales (Walking In).
- **Target Profiles:** Beach Bars and Festival Organizers.
- **Pitch Focus:** Time saved, queue reduction, immediate ROI.
- **Conversion Strategy:** Provide a free, no-obligation "Fake MVP" demo directly on the venue owner's mobile device to demonstrate the zero-friction experience.
- **Tooling Constraint:** Use a simple CRM (e.g., Planka) to track touchpoints and follow-up reminders. Avoid complex automated email sequences initially; focus on face-to-face trust.
