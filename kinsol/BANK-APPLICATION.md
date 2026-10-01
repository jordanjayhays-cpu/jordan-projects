# Kinsol LLC — business bank account

Drafted 2026-10-01, the day the EIN letter arrived.

## Conclusion

**Chase is out. Use Mercury. Open Wise Business as a second rail within the first month.**

Chase requires a branch visit for LLC account opening — their own page states that authorised
individuals who cannot be present must appear **at a branch within 30 days** with ID. You are in
Madrid and then Manila. That is not a paperwork problem you can argue your way past; it is the
product's design. Same for Bank of America and Wells Fargo.

Mercury is fully remote, built for exactly this case, and takes a US LLC + EIN.

## Assumptions I am working from — correct me if any is wrong

1. **You are a US person with an SSN.** Inferred from the 2026-09-01 record: *"get a FREE EIN at
   IRS.gov (SSN, ~15 min)."* If you do NOT have an SSN this still works, but the application path
   and the questions change, so say so.
2. You currently reside in **Madrid**, and move to **Manila January–June 2027**.
3. Kinsol LLC, Colorado, EIN letter received 2026-10-01.

## The options, honestly

| Bank | Remote? | Verdict |
| --- | --- | --- |
| **Mercury** | Fully remote, no branch | **Do this one.** Built for US LLCs with founders abroad |
| **Wise Business** | Remote | **Second rail.** Good for EUR↔USD and Madrid reality. Not a bank — not FDIC insured directly — so do not park a balance |
| **Relay** | Remote, but | **Third.** Multiple reports of Relay now demanding a physical US address at signup, and of accounts opened then closed weeks later |
| **Chase / BofA / Wells** | **No** | Branch visit required within 30 days. Dead for you until you are physically in the US |
| Novo, Lili, Found | Remote | Thinner, and no advantage over Mercury here |

## Two landmines — read these before you touch the form

### 1. Do NOT give the Northwest Denver address as the principal place of business

Mercury's eligibility page is explicit: *"residential addresses are accepted, but **registered agent
addresses, P.O. boxes, and UPS Store addresses are not**."*

Your Kinsol address of record IS Northwest's Denver address. Putting it in the "physical address"
field is the single most common cause of rejection for this exact setup.

**The correct split:**
- **Legal / registered address** → Northwest's Denver address. Correct and expected here.
- **Principal place of business / physical address** → **your Madrid residential address.** Mercury
  accepts an international residential address. This is what their support tells applicants directly.

### 2. Do NOT describe Kinsol as collecting money on behalf of another business

This is the one that would actually hurt you, and it comes straight out of your own draft contract.
The Amigo billing agreement says Kinsol *"receives client payments into a Kinsol account"* and
*"remits each Amigo receipt to Amigo, net of the Service Fee."*

A bank reads that as **third-party payment processing / money transmission.** That is a restricted
industry for Mercury's banking partners. Describe it that way and you risk rejection now, or a frozen
account later — and account freezes at neobanks are common and slow to resolve.

**The accurate and safe framing is already in your contract, at clause 2.4:** Kinsol signs the client
agreement as the contracting party, and Amigo delivers. So Kinsol is not passing someone else's money
through — **Kinsol earns the revenue and pays a subcontractor.** That is ordinary business, it is true,
and it is what you should write.

Say: *consulting and business development income, and subcontracted service delivery.*
Never say: *we collect and remit funds for other businesses.*

## The application, field by field

### Business

| Field | What to enter |
| --- | --- |
| Legal business name | **Kinsol LLC** |
| Entity type | Limited Liability Company (single-member) |
| State of formation | **Colorado** |
| Date formed | ~2026-09-04 (match the Articles exactly) |
| EIN | From the EIN letter in Northwest → Documents. **Do not store it in any repo or chat** |
| Legal / registered address | Northwest Registered Agent, Denver, CO (your address of record) |
| **Principal place of business** | **Your Madrid residential address** |
| Website | See the note below |
| Phone | Your real reachable number |

### "What does your business do?" — the field that decides it

Write plainly and specifically. Vague answers get manual review; buzzwords get rejected.

> Kinsol LLC is a business development and consulting company. It earns referral commissions from
> international recruitment and staffing firms for introducing employer clients, and consulting fees
> from B2B sales and market-entry work. Clients are companies in the United States, Spain and the
> Philippines. Where a client contracts with Kinsol directly, Kinsol subcontracts delivery to
> specialist providers and pays them as subcontractors.

### "Do you have or plan operations in the US / US customers?" — answer YES, with a name

Mercury requires existing or planned US operations **and** serving US customers within two years.
You have a real answer, so use it:

> Kinsol's active commercial discussion is with a US locums physician staffing firm (formerly Zulu
> Locums) whose end client is a US hospital group, Incompass Health. Kinsol is negotiating a
> commission arrangement on placements into US hospitals. Additional US customers are expected
> through the same channel.

That is true, specific, and checkable. It is much stronger than "planned".

### Money movement

| Field | Answer |
| --- | --- |
| Expected monthly incoming | Be realistic and low. **Under $5,000/month to start** — you have no signed revenue yet |
| Source of initial deposit | Personal funds of the member (you) |
| Where money comes from | US and EU companies paying invoices by ACH and wire |
| Where money goes | Subcontractor payments, software, professional fees, member distributions |
| International transfers? | **Yes** — say so. Spain and the Philippines. Hiding this is how accounts get frozen later |

### Ownership

| Field | Answer |
| --- | --- |
| Beneficial owners ≥25% | Jordan Hays — 100% |
| Role | Member / Manager |
| SSN | Yours (assuming assumption 1 holds) |
| ID | Passport or US driver's licence |
| Residential address | Madrid |

## Documents to have open before you start

1. **EIN letter** (CP-575) — from Northwest → Documents. **Check page 2 as well**
2. **Articles of Organization** — Colorado, from Northwest
3. **Operating Agreement** — single-member. If one does not exist, Northwest can supply a template.
   Mercury asks for it. Get this sorted before applying, not during
4. **Passport or US ID**
5. **Proof of Madrid address** — a utility bill or bank statement in your name, in case they ask

## About the website field

An empty website field on a consulting company invites manual review. You already own
`placewellinternational.net` and `amigosales.com`, but **neither is Kinsol**, and pointing Kinsol's
application at someone else's domain is worse than leaving it blank.

Cheapest honest fix: a one-page kinsol site — name, what it does, Colorado, contact. That is an
afternoon and it removes a reason to be questioned. Alternatively leave it blank and expect a
follow-up question you can answer in writing.

## Top 3 ways this goes wrong

1. **You use the Denver registered-agent address as the physical address.** Rejected, and reapplying
   with a changed address looks worse than applying correctly once. **Fix: Madrid residential for
   principal place of business, Denver for legal only.**
2. **You describe the Amigo arrangement as collecting and remitting funds.** Reads as money
   transmission, a restricted industry. **Fix: the contracting-party-and-subcontractor framing above,
   which is what clause 2.4 of your own agreement already says.**
3. **You open Mercury and keep everything in it.** Neobank compliance freezes are common, opaque and
   slow — there are many documented cases of locked funds with no explanation. **Fix: Wise Business as
   a second rail within the first month, and never hold more in Mercury than you could do without for
   a month.**

## One thing to check before January

You will move to Manila in January. Mercury will have your Madrid address on file and you will need to
update it. **Whether the Philippines creates any issue with Mercury's banking partners is UNSURE** —
do not assume it is fine. Ask Mercury in writing once the account is open and working, not before.

## Accept when

The Mercury account is open, Kinsol can receive an ACH payment and send a wire, the Madrid address is
on file as the principal place of business, and a second rail exists at Wise.
