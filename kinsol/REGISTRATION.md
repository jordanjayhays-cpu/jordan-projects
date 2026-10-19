# Kinsol LLC — registration record

Verified from the Northwest Registered Agent account, 2026-10-01.

| Field | Value |
| --- | --- |
| Legal name | **Kinsol LLC** |
| Entity type | Limited liability company |
| Jurisdiction | **Colorado** |
| Registered agent / filing service | **Northwest Registered Agent** |
| Filing | Standard processing, approved ~2026-09-04 |
| Registered address | Northwest's Denver address (home address shielded) |
| **EIN** | **32-0871752** |
| EIN name control | **KINS** (needed for e-filing) |
| EIN assigned by IRS | **2026-09-28** |
| EIN letter received at Northwest | 2026-10-01 — held in Northwest → Documents (2 pages) |
| Member | Jordan Hays |

## On recording the EIN here

Jordan asked for it on the record, 2026-10-19, and it is above. Two notes:

**It is not a secret of the SSN class.** The IRS notice itself says you may share a copy
"with anyone asking for proof of your EIN." It goes on every W-9, to every client who pays
you, and to every bank and vendor. Treating it as unshareable was over-cautious of me.

**It is also not nothing.** An EIN plus a company name is the raw material for business
identity theft — opening credit or filing returns in the company's name. This repo is
private; keep it that way, and do not put the EIN in anything public (a website, an invoice
template that gets shared around, a pitch deck).

The signed IRS notice itself stays in Northwest → Documents. A copy belongs in a password
manager, not in git — an image of the letter committed here could never be fully removed.

## What the EIN unblocks, in order

1. **Business bank account** — Mercury or Relay. Needs the EIN letter plus the Articles. **Unblocked — you have everything.**
2. **Stripe on Kinsol LLC** — needed before the first real sale of anything.
3. **Meta Business verification** — which lifts Massage Club's WhatsApp sending ceiling to 250/day.
4. **Invoicing** for both Massage Club and Amigo Sales, which is the reason Kinsol exists.

Steps 2, 3 and 4 all sit behind step 1. The bank account is the single next action.

## Structure decision (recorded 2026-09-01, unchanged)

One LLC only. Consulting runs directly as Kinsol LLC — no DBA needed. Massage Club becomes a
Colorado trade name / DBA under Kinsol (~$25) when required, using Kinsol's LLC + EIN, and
graduates to its own LLC later if it earns it.

## Contracts

`jordan-projects/kinsol/contracts/` — Placewell referral agreement and Amigo Sales billing
agreement, drafts v1 (2026-09-07). State of formation now filled in as Colorado.

Still open before either can be sent:
1. Placewell International's exact legal name and registration number
2. Eleanor Escueta — spelling and title (**UNSURE**, must be confirmed)
3. Clause 5.2 payment trigger: 30 days from statement (better for Kinsol) vs after employer pays
