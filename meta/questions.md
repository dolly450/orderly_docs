# Κρίσιμες Ερωτήσεις Στρατηγικής & Προϊόντος

## 1. Θα αντικαταστήσουμε το PDA ή θα ενσωματωθούμε στα υπάρχοντα PDA;
- **Γιατί είναι κρίσιμη:** Καθορίζει το technical scope (integration complexity) και το αν θα φαινόμαστε ως απειλή ή βοηθητικό εργαλείο στα μάτια των POS providers και του staff.
- **Τι απόδειξη/δεδομένα χρειαζόμαστε:** Interviews με 5 ιδιοκτήτες/managers (ή waiters) για να καταλάβουμε την εξάρτησή τους από τα υπάρχοντα PDA συστήματα. [[business/market_strategy.md]]
- **Επίπεδο:** High
- **Owner:** Development/Architecture
- **Ημερομηνία προσθήκης:** 2026-04-03

## 2. Ποιο είναι το πραγματικό "pain point" του μαγαζιού (κόστος λογισμικού, δισταγμός manager, ή κάτι άλλο);
- **Γιατί είναι κρίσιμη:** Πρέπει να ξέρουμε τι ακριβώς λύνουμε για να πουλήσουμε σωστά το B2B value proposition μας (π.χ. ROI vs ευκολία).
- **Τι απόδειξη/δεδομένα χρειαζόμαστε:** Feedback/Surveys από 10 μαγαζιά σχετικά με τους λόγους που δεν έχουν βάλει QR ordering ακόμα.
- **Επίπεδο:** High
- **Owner:** Product/Business
- **Ημερομηνία προσθήκης:** 2026-04-03

## 3. Ποιος είναι ο ανταγωνισμός που δεν έχουμε ακόμα χαρτογραφήσει και πόσο καλύτεροι είμαστε από το BringFood και τους βασικούς παίκτες;
- **Γιατί είναι κρίσιμη:** Το differentiation είναι το παν. Αν δεν είμαστε σαφώς καλύτεροι/φθηνότεροι, θα χάσουμε στα B2B pitches.
- **Τι απόδειξη/δεδομένα χρειαζόμαστε:** Mystery shopping στους ανταγωνιστές, σύγκριση features & τιμών. [[business/competitive_analysis.md]]
- **Επίπεδο:** High
- **Owner:** Product/Business
- **Ημερομηνία προσθήκης:** 2026-04-03

## 4. Πόσο θα κοστίσει το MVP (ανάπτυξη + λειτουργία) και σε πόσο χρόνο γίνεται;
- **Γιατί είναι κρίσιμη:** Καθορίζει την βιωσιμότητα της ομάδας, το funding need και το αν προλαβαίνουμε τη θερινή σεζόν.
- **Τι απόδειξη/δεδομένα χρειαζόμαστε:** Τελικό αρχιτεκτονικό scope, AWS/Cloud cost estimates, man-hours breakdown. [[business/roadmap.md]]
- **Επίπεδο:** High
- **Owner:** Development/Architecture
- **Ημερομηνία προσθήκης:** 2026-04-03

## 5. Startup/VC funding (10-20% equity) ή Indie SaaS/Bootstrapping;
- **Γιατί είναι κρίσιμη:** Αλλάζει όλη την πορεία της ομάδας (agressive growth vs slow & steady control).
- **Τι απόδειξη/δεδομένα χρειαζόμαστε:** Σύνοψη εξόδων vs εσόδων από early adopters. [[business/pricing_model.md]]
- **Επίπεδο:** High
- **Owner:** Product/Business
- **Ημερομηνία προσθήκης:** 2026-04-03

## 6. Τι όνομα / branding θα επιλέξουμε οριστικά για την αγορά (π.χ. "Orderly");
- **Γιατί είναι κρίσιμη:** Απαιτείται για κατοχύρωση domain, δημιουργία εταιρείας, branding, social media, pitch deck.
- **Τι απόδειξη/δεδομένα χρειαζόμαστε:** Domain availability check, User polling (A/B testing ονομάτων). [[meta/idea-dump.md]]
- **Επίπεδο:** Medium
- **Owner:** Product/Business
- **Ημερομηνία προσθήκης:** 2026-04-03

## 7. Πώς θα εξασφαλίσουμε την αξιοπιστία στο τοπικό Offline Mode (Wifi);
- **Γιατί είναι κρίσιμη:** Τα beach bars/panigiria (το target group μας) έχουν συχνά κακό internet, οπότε το offline fallback είναι USP.
- **Τι απόδειξη/δεδομένα χρειαζόμαστε:** Load testing του local router gateway/DB σε simulated "κακό δίκτυο". [[architecture/system_architecture.md]]
- **Επίπεδο:** High
- **Owner:** Development/Architecture
- **Ημερομηνία προσθήκης:** 2026-04-03

## 8. Πώς χειριζόμαστε τα ακυρωμένα / "fake" orders (Security Measures / SMS Validation);
- **Γιατί είναι κρίσιμη:** Κίνδυνος να χάσουν λεφτά τα μαγαζιά από trolling orders (κρίσιμο friction point για B2B sales).
- **Τι απόδειξη/δεδομένα χρειαζόμαστε:** AB testing: Guest checkout vs SMS validation (επίπτωση στο conversion rate των παραγγελιών). [[design/v1_scope.md]]
- **Επίπεδο:** High
- **Owner:** Development/Architecture
- **Ημερομηνία προσθήκης:** 2026-04-03

## 9. Ποια είναι τα ακριβή metrics επιτυχίας του πιλοτικού προγράμματος (Pilots);
- **Γιατί είναι κρίσιμη:** Χωρίς clear KPIs (π.χ. αύξηση τζίρου, μείωση χρόνου αναμονής), δεν μπορούμε να πουλήσουμε μετά.
- **Τι απόδειξη/δεδομένα χρειαζόμαστε:** Καθορισμός baseline metrics πριν βάλουμε το σύστημα και σύγκριση μετά από 1-2 εβδομάδες χρήσης. [[business/market_strategy.md]]
- **Επίπεδο:** Medium
- **Owner:** Product/Business
- **Ημερομηνία προσθήκης:** 2026-04-03

## 10. Θα πάμε με πάγια συνδρομή (SaaS) ή Transaction-based (Commission);
- **Γιατί είναι κρίσιμη:** Αλλάζει τελείως το value proposition. To commission-based (3-5%) έχει μηδενικό ρίσκο για μαγαζάτορες.
- **Τι απόδειξη/δεδομένα χρειαζόμαστε:** Αξιολόγηση μέσω A/B pricing models κατά τη διάρκεια του pre-sales / cold calling. [[business/pricing_model.md]]
- **Επίπεδο:** High
- **Owner:** Product/Business
- **Ημερομηνία προσθήκης:** 2026-04-03
