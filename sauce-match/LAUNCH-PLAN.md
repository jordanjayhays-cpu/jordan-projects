# Sauce Match — Launch Plan v1 (2026-09-07)

**Decision (Jordan):** Sauce Match is a **quiz + affiliate** product. No stock. Focus lane from today.
**Launched =** one paying customer who is not a friend. Two routes, both pursued:
- Route A: first affiliate commission (a stranger takes the quiz, clicks out, buys).
- Route B: first sauce maker paying for a featured slot in the quiz results (B2B, Jordan's BD skill).
**Market:** undecided. Default = wherever traffic lands, links geo-switched (Amazon.es for EU visitors, Amazon.com for US) plus maker-direct links.

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
