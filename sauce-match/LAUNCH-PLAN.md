# Sauce Match — Launch Plan v1 (2026-09-07)

**Decision (Jordan, revised 2026-09-07 pm):** Sauce Match is a **real ecommerce shop** for hot sauce,
launched in **concierge mode**. Stripe takes the money, orders land in a database and an admin page,
Jordan ships the first orders by hand from Madrid. Small stock (6-8 sauces he can actually source),
affiliate links stay on catalog sauces he does NOT stock, so the catalog can be bigger than the shelf.
Supersedes the morning's affiliate-only decision; the step-1 cleanup (fake reviews, disclosure,
analytics off the agent DB) still stands and is already shipped on branch claude/sauce-match-launch.

**Launched =** one paid order from someone who is not a friend, shipped and delivered.

## What exists
Live at sauchematch.lovable.app. Quiz + results + shop + compare + cart + checkout (charges nothing) + orders. 8 static SKUs (Sambal, Gochujang, Chili Crisp, Yuzu Kosho, Sriracha, Naga, ...) with **fabricated reviewer names**. Analytics write into the agent board DB with a hardcoded key. Stalled since Aug 16 in a design revert loop. Competitive analysis (Jul 15) in this folder.

## Premortem (top 3, fixed)
1. **Affiliate account banned or closed.** Fabricated reviews and a fake checkout violate Amazon Associates and FTC/EU rules. Fix: remove cart, checkout, orders, fake reviewers; add disclosure line; launch with maker programs too so we do not depend on Amazon's 180-day sales rule.
2. **Links that do not ship to the visitor.** Fix: geo-switch (EU → Amazon.es or maker EU shop; US → Amazon.com or maker); only list sauces available in both, or tag by region.
3. **Traffic never comes.** A quiz with no audience earns nothing. Fix: Route B does not need traffic; and the quiz is built to be shared (result card image, Reddit r/hotsauce, TikTok via the PK poster).

## Build (agents, in order)
1. **Strip fake commerce.** Delete cart, checkout, orders routes; results page links out. Remove fabricated reviewer names. Add "we may earn a commission" disclosure. Stop analytics writing to the agent DB (own Supabase table or Plausible).
2. **Real catalog v1: 24 sauces** with verified availability: 12 on Amazon.es, 12 on Amazon.com, overlap where possible; flavour profile, heat 1 to 10, region tags. Include craft makers with their own affiliate programmes (verify each: Bravado, High River, Heatonist, Fuego Box, Truff, Yellowbird, Secret Aardvark — UNSURE which have programmes; agents check).
3. **Quiz to match logic** re-tuned to the 24 (heat tolerance, flavour family, use case, region).
4. **Share card**: quiz result as an image (OG image) with "Your sauce match is X".
5. **Lock the design** (the July 4 identity Jordan restored). No more reverts.
6. Domain: check saucematch.com / .co / .es (agents check availability; Jordan buys).

## Jordan-only
- Apply for Amazon Associates (ES and US). Needs a live site with content; approval is provisional until 3 qualifying sales in 180 days.
- Apply to each maker programme once agents list them (usually a 2-minute form).
- Buy the domain.
- Pick the caption voice (task already on the board).

## Route B: maker placement (Jordan's BD)
- Offer: "Featured in Sauce Match results for your flavour profile" at **€49/month** [placeholder] or free 30-day trial then paid. Includes: top slot in matching results, brand story panel, monthly click report.
- Agents: list 15 craft makers (EU + US) with a named founder or marketing contact and a verified email; draft the pitch in house format; Jordan sends one per day.
- First paid maker = launched.

## 30-day sequence
- Week 1: strip fake commerce, disclosure, analytics fix, catalog research, domain check. Jordan: Amazon Associates applications.
- Week 2: 24-sauce catalog live with affiliate links, quiz re-tuned, share card. Maker list + pitch drafted.
- Week 3: Jordan sends 5 maker pitches. First Reddit/TikTok posts via PK poster. Track clicks.
- Week 4: first commission or first paid maker, or decide what to change.

## Numbers to track (weekly line in the brief)
Quiz completions · outbound clicks · click-through by sauce · affiliate orders · maker pitches sent / replies / paid.

**Accept when:** the live site has no fake commerce, 24 real sauces with working affiliate links, a disclosure, its own analytics, and one paying maker or one affiliate commission from a stranger.

---

## Revision 2 — real shop, concierge fulfilment (2026-09-07 pm)

### Backend to build (agents)
1. **Supabase project of its own** (never the agent board, never the Massage Club DB). Tables:
   `sauces` (name, maker, origin, heat 1-10, flavour tags, price, stock_qty, stocked bool, buy_url_eu, buy_url_us, image, active),
   `orders` (customer, email, phone, address, items jsonb, subtotal, shipping, total, currency, stripe_payment_intent, status: paid/packed/shipped/delivered/refunded, tracking, notes, created_at),
   `order_items`, `quiz_results` (answers, matched sauce ids, email optional, session),
   `events` (quiz_completed, sauce_viewed, add_to_cart, checkout_started, purchased, affiliate_click).
   RLS: public read on active sauces only; inserts via edge functions; admin behind auth.
2. **Stripe Checkout** via an edge function (`create-checkout-session`) + webhook (`stripe-webhook`) that writes the paid order. Test mode until Jordan's Stripe account is live. Never put a secret key in the client bundle.
3. **Cart + checkout restored**, but real: stock check, shipping options, address capture, order confirmation page and email (Resend, server-side).
4. **Admin page** `/admin` behind Supabase auth: add/edit sauces, set stock and price, see orders, mark packed/shipped with tracking, refund link. This is what makes it operable without Claude.
5. **Hybrid catalog**: `stocked = true` sauces get the real Buy button; the rest keep the affiliate outbound link with the disclosure.
6. **Transactional emails**: order confirmation, shipped-with-tracking. Plain, in Jordan's voice.

### Legal and practical (before the first real sale)
- Spain/EU: selling packaged food needs the seller's details, allergen info and ingredients visible per product; distance-selling rules give a 14-day withdrawal right (food that spoils is exempt, sealed sauce is not). Terms, privacy and returns pages required. **UNSURE on the exact Spanish registration needed for resale of packaged food — Jordan to confirm with his gestor/CPA before the first sale.**
- Stripe needs Kinsol LLC (or a Spanish sole-trader registration) with a bank account. Ties to the EIN task already on the board.
- Shipping: bottles are heavy and glass. Get 3 courier quotes (Correos, SEUR, MRW) for a 2-bottle and a 4-bottle box.

### First 8 sauces (agents research, Jordan approves)
Sourceable in Madrid or shippable to Madrid within a week, ideally with a wholesale or trade price. Mix of heat levels and origins so the quiz has range.

### Sequence
- Week 1: Supabase project + schema + admin page + Stripe test-mode checkout. Agents research the 8 sauces and courier costs.
- Week 2: Jordan approves the 8, orders a small first batch, Stripe goes live, packaging and labels sorted.
- Week 3: soft launch to the quiz traffic + Reddit/TikTok. First real order shipped by hand.
- Week 4: 3 to 5 orders shipped, or change the offer.

### Jordan-only
- Stripe account on Kinsol LLC (needs EIN + bank) or a Spanish alternative.
- Confirm with a gestor what is required to resell packaged food in Spain.
- Buy the first batch of sauces (budget to set) and packaging.
- Approve the 8-sauce shortlist and the retail prices.
- Domain purchase.

**Accept when:** a stranger completes checkout with a card, the order appears in the admin page, Jordan ships it, and the customer confirms delivery.
