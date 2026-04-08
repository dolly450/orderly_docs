# Orderly — Σύνοψη Startup (Απρίλιος 2026)

Αυτό το έγγραφο συγκεντρώνει όσα είναι **έτοιμα και σίγουρα** για την Orderly, ώστε ένας AI agent να μπορεί να βρει σχετικά insights από εξωτερικά έγγραφα, έρευνες αγοράς και case studies.

---

## 1. Τι Είναι η Orderly

Η Orderly είναι μια **cloud-based πλατφόρμα ψηφιακής παραγγελιοληψίας (QR ordering)** για τον χώρο της ελληνικής φιλοξενίας (hospitality). Ο πελάτης σκανάρει ένα QR code στο τραπέζι ή στο stand, βλέπει το μενού στο κινητό του (χωρίς εγκατάσταση app ή login), παραγγέλνει, πληρώνει, και παρακολουθεί την κατάσταση της παραγγελίας του — όλα από τον browser.

**Ordering-first approach**: Δεν είμαστε POS. Είμαστε ένα ordering layer που λύνει λειτουργικά προβλήματα (ουρές, αναμονή, λάθη, γλωσσικά εμπόδια) και ενσωματώνεται με υπάρχοντα POS.

---

## 2. Πρόβλημα που Λύνουμε

- **Ουρές και αναμονή** σε crowded venues (beach bars, festivals, self-service).
- **Λάθη παραγγελιών** λόγω παράλειψης ή λανθασμένης μεταφοράς.
- **Γλωσσικό φράγμα** — 40M+ τουρίστες ετησίως στην Ελλάδα, σε ένα σύστημα που τρέχει κυρίως με χειρόγραφα ή μόνο ελληνικά.
- **Καθυστέρηση πληρωμής** — αναμονή σερβιτόρου/POS ειδικά στην αναχώρηση.
- **Ελλειπής ψηφιακός μετασχηματισμός** — η ελληνική εστίαση υστερεί σε τεχνολογία σε σχέση με Δ. Ευρώπη.

---

## 3. Target Market (Επιβεβαιωμένο)

### Κοινό-Στόχος
| Τύπος Venue | Menu | Σερβιτόρος | Self-Service | Queues | Call Button | Booking |
|---|---|---|---|---|---|---|
| Full-service cafe | ✅ | ✅ | Conf | ✅ | Conf | Conf |
| Beach bar | ✅ | ✅ | Conf | ✅ | Conf | Conf |
| Festival / Event | ✅ | ❌ | Conf | ✅ | ❌ | ❌ |
| Self-service cafe | ✅ | ❌ | Conf | ✅ | ❌ | ❌ |
| Πανηγύρι | ✅ | ✅ | Conf | ✅ | Conf | Conf |

### Μέγεθος Αγοράς
- **73.000–75.000** επιχειρήσεις εστίασης στην Ελλάδα.
- **10,73 δις €** κύκλος εργασιών (2025).
- **40M+ τουρίστες/έτος**, 25% του ΑΕΠ από τουρισμό.
- **Στόχος 3-ετίας**: 800+ πελάτες (Base) — 2.000 (Optimistic).

---

## 4. Main Selling Points (Επιβεβαιωμένα)

1. **Operational Efficiency**: λιγότερα λάθη, γρηγορότερο service, περισσότερες πωλήσεις, αποσυμφόρηση προσωπικού.
2. **Multilingual μενού** — αυτόματη μετάφραση (DeepL API), Ελληνικά/Αγγλικά MVP, μετά Γερμανικά, Γαλλικά, Ιταλικά.
3. **Offline λειτουργία** — υβριδικό μοντέλο cloud+local server για νησιά/βουνά με κακό σήμα.
4. **Batch Preparation Logic** — οι παραγγελίες χωρίζονται σε κατηγορίες (ποτά/φαγητό) και ομαδοποιούνται στην κουζίνα για μέγιστο throughput.
5. **Zero-friction για τον πελάτη** — δεν χρειάζεται download, login, ή εγγραφή (anonymous by default, GDPR compliant).
6. **Greek-first**: Συμμόρφωση myDATA/ΑΑΔΕ, Viva Wallet integration, εποχιακή τιμολόγηση.

---

## 5. Ανταγωνισμός (Χαρτογραφημένος)

### Ελληνικοί
| Ανταγωνιστής | Χαρακτηριστικά |
|---|---|
| **Butler.gr** | Πιο άμεσος ανταγωνιστής. QR menu, ordering, πληρωμή, POS, staff management. |
| **BringFood.gr** | Cloud POS-first. QR ordering ως add-on. Ισχυρό σε φορολογική συμμόρφωση. |
| **DigiApp.gr** | Απλούστερο QR menu/ordering, χωρίς πληρωμές, χωρίς POS. |
| **mintQR, MenuMaster, Ecomenu** | Menu-only εργαλεία. |

### Διεθνείς
| Ανταγωνιστής | Χαρακτηριστικά |
|---|---|
| **me&u** | 6.000+ venues, μηδενική παρουσία Ελλάδα. |
| **Sunday** | Εστίαση σε πληρωμές, αποχώρησε από Ν. Ευρώπη (2022). |
| **Flipdish** | 15+ χώρες, υψηλό κόστος (subscription + commission). |

### Διαφοροποίηση Orderly
1. Greek-first design (myDATA, Viva Wallet)
2. Εξειδίκευση σε Beach Bars & Festivals
3. Digital Queue + Ordering system
4. Offline mode (υβριδικό)
5. AI chatbot (μελλοντικά)

---

## 6. Business Model & Τιμολόγηση (Αποφασισμένο Framework)

### Στρατηγική Εισόδου
**Hybrid model**: Ξεκινάμε με **commission-based (1–3% per sale)** για χαμηλό barrier to entry → μετά switch σε **tiered subscription**.

### Tiered Subscription (Τρέχουσα Πρόταση)
| Tier | €/μήνα | Περιλαμβάνει |
|---|---|---|
| Free (Starter) | €0 | Digital Menu, ≤5 τραπέζια, Orderly branding |
| Basic | €19 | Παραγγελιοληψία, ≤20 τραπέζια, πολυγλωσσικό menu |
| Pro | €39 | POS Integration, unlimited τραπέζια, analytics, upselling |
| Enterprise | €69+ | Multi-location, API, dedicated support |

### Εποχιακή Στρατηγική
- Summer Plans: 5 μήνες prepay → 20% έκπτωση
- Pause/Resume: αναστολή χειμώνα
- Transaction-based εναλλακτική για εποχιακά venues

### Revenue Streams
1. SaaS Subscription (κύρια)
2. Transaction Fees (Phase 2)
3. Hardware Sales (servers/tablets)

### Margin Στόχοι
- Gross margin: **~80%**
- Net margin: **0–30%** (αρχικά χαμηλά λόγω growth investment)

---

## 7. Go-to-Market Strategy (Επιβεβαιωμένο)

### Phase 1 (τώρα)
1. **Cold outreach / Walking in** — επίσκεψη σε bars/cafes αυτοπροσώπως με tablet demo.
2. **Demo calls** + pitch + data από ερωτηματολόγιο + traction analytics.
3. **CRM** — consistent follow-ups, emails, relationship building.
4. **Incentives** — δωρεάν πρώτοι μήνες, δωρεάν setup.
5. **Organic** — SEO, social media content (όχι paid ads αρχικά).
6. **Referrals** — στόμα σε στόμα + affiliate συνεργασίες με accountants/προμηθευτές εστίασης (~€100/deal).
7. **PR/Community** — παρουσία σε hospitality events, community building σε groups.

### Phase 2 (Long-term)
- Event hosting (δικά μας meetups)
- Paid ads μόνο αν αποδειχτεί ROI

### Validation Πριν Κλίμακα
- Πιλοτικό σε 5 venues → metrics → proof of concept
- Ερωτηματολόγιο σε πελάτες (draft ετοιμάστηκε: pain points αναμονής, γλώσσας, menu clarity, order status)
- Demo MVP

---

## 8. Τεχνική Αρχιτεκτονική (Σίγουρα)

### MVP Stack
- **Frontend**: Next.js 14+ (App Router), PWA
- **Backend/DB**: Supabase (Auth, Realtime, Storage)
- **Styling**: Tailwind CSS + shadcn/ui
- **Deployment**: Vercel
- **Realtime**: SSE (Server-Sent Events) — 95% server-to-client
- **Push**: Web Push (Android), PWA-based (iOS 16.4+), fallback audio alerts + SMS (Twilio)

### Production (Υβριδική Αρχιτεκτονική)
- Cloud Layer: Admin Dashboard + Sync API + Global DB
- Local Venue Layer: Local WiFi Router + Local Server (Raspberry Pi) + Kitchen Display System + Printers
- Auto-sync μέσω SSE/WebSockets

### Φορολογική Συμμόρφωση
- **MVP**: Ordering-only layer (πληρωμή στο ταμείο → αποφεύγουμε ΦΗΜΑΣ)
- **Phase 2**: POS integration μέσω SBZ Systems REST API
- **Phase 3**: Συνεργασία με Παρόχους (Epsilon Net, Oxygen)

### Πληρωμές
- Κύρια: **Viva Wallet** (ελληνική υποστήριξη, Apple/Google Pay, χαμηλές χρεώσεις, Ν.5167/2024)
- Εναλλακτικά: **Stripe** (καλύτερο dev experience)
- Υβριδικό: Online + Cash στο ταμείο

### Data Model (Σχεδιασμένο)
Entities: Canteen → Category → Product → Order → OrderItem → Inventory → User

---

## 9. Ομάδα

| Μέλος | Ρόλος |
|---|---|
| **AP** (Angelos P) | Dev & Infra |
| **AF** (Antonis Frs) | Dev & Infra |
| **ML** (Marios L) | Business |
| **NT** (Nikos Tsaata) | Business |

---

## 10. MVP Roadmap (Timeline)

| Φάση | Περιγραφή | Timeline |
|---|---|---|
| Phase 1: Core | UI + Ordering + Database/API | Απρ 2026 (20d) |
| Phase 2: Operations | Staff Dashboard (KDS), QR Management | Απρ-Μάι 2026 (25d) |
| Phase 3: Connectivity | Offline Sync, Hybrid Payments | Μάι-Ιούν 2026 (35d) |
| Phase 4: Testing | Pilot Test + Refining | Ιούν-Ιούλ 2026 (21d) |

**Κρίσιμος στόχος**: Ιούνιος 2026 → pilot πριν την κορύφωση της θερινής σεζόν.

---

## 11. Εργαλεία & Υποδομή (Λειτουργικά)

- **Documentation**: Obsidian Vault → GitHub (`dolly450/orderly_docs`) → Auto-sync
- **Communication**: Discord Server (Orderly Startup Hub) + OrderlyBot (AI-powered)
- **Project Management**: Planka boards
- **Mentors**: Αξιολόγηση 20+ μεντόρων ολοκληρωμένη — top picks: Γιώργος (Blue Functor/MVP), Nina Hrelja (B2B Sales/Hospitality), Γ. Νικολάου (Fundraising)

---

## 12. Αποφάσεις που Έχουν Ληφθεί

1. ✅ Commission-first → subscription switch
2. ✅ Ordering layer (όχι POS) στο MVP
3. ✅ Πράσινο χρώμα logo
4. ✅ Anonymous ordering (χωρίς login)
5. ✅ Beach bars + festivals + self-service ως πρώτο κοινό
6. ✅ Cold outreach / walking in ως primary GTM
7. ✅ Εποχιακά pricing plans
8. ✅ SSE αντί WebSockets για real-time
9. ✅ Supabase + Next.js + Vercel stack
10. ✅ Viva Wallet ως primary payment provider

---

## 13. Τι Δεν Έχει Αποφασιστεί Ακόμα (Open)

- Οριστικό brand name
- Business Model Canvas (κενό — ειδικά Value Proposition)
- Tier features σε λεπτομέρεια
- Funding model: VC vs Bootstrapping
- POS integration timeline + partners
- Ερωτηματολόγιο (draft, δεν έχει πάει live)
- Ακριβή COGS αριθμοί
- Competitive comparison table λεπτομερή
- Influencer/affiliate στρατηγική (αμφιβολία αν ταιριάζει στο niche)
- Overheads budget (εκτίμηση ~€200-300/μήνα)

---

*Τελευταία ενημέρωση: 8 Απριλίου 2026*
