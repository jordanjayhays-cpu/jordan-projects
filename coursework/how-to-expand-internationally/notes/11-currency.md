# Session 11: Currency risk, convertibility and the forward (Prof. Mikel Aguirre, 16 Oct 2026) with the HBS case "Société Générale (A): The Jérôme Kerviel Affair" (9-110-029)

This unit covers the third of the three ICC contract risks (transport, credit, currency). The deck uses the rogue-trader stories (Leeson at Barings, Kerviel at Société Générale, Adoboli) to open the topic, then defines money and currency, floating versus fixed exchange rates, convertibility (UN definition and the list of hard currencies), currency futures, and the bank forward, with a worked EUR/GBP forward calculation. The case tells how one junior trader hid EUR 50 billion of positions behind fictitious trades and cost the bank EUR 4.9 billion. What the professor said matters most: your business is to sell your product, never to speculate on currency; always close or hedge an open currency position with a forward; know the forward formula and be able to calculate it; know what makes a currency convertible (UN definition) and why non-convertible currencies mean double exchange, double fees and double risk; and "with so many people controlling, at the end no one controls."

## Part 1: The deck slide by slide

### Slide 1: Risk Management: Currency Risk, Session 11
- Title slide. The unit is currency risk inside the course's risk-management block.

### Slide 2: Rogue Trader (video links)
- Two YouTube links to the film **Rogue Trader** (1999, Ewan McGregor as Nick Leeson). The professor shows the segment 1:15:49 to 1:19:34.
- Purpose: show a trader fighting a falling market (the Nikkei) by buying more, and going bust in seconds.

### Slide 3: Barings Bank
- Picture: the Barings crest and the 1805 portrait "Sir Francis Baring with Brother John Baring" by Sir Thomas Lawrence.
- **Barings Bank (1762 to 1995)** was the oldest merchant bank in London, founded and owned by the Baring family.
- It collapsed in **1995** after employee **Nick Leeson** lost **GBP 827 million (USD 1.3 billion)** through speculative investing at the bank's **Singapore** office.

### Slide 4: Rogue Trader (newspaper scan)
- Picture only: a scanned British tabloid page, "Exactly 10 years ago rogue City trader Nick Leeson was revealed as the man who broke Barings bank after he foolishly gambled GBP 862 million on the stock market", showing Leeson rebuilding his life in a remote Irish village, "still in demand as the 'worst gambler in the world'". Side panel: "Leeson's fall from grace" timeline.
- Point: the loss figure quoted by the press (GBP 862 million) differs slightly from the slide 3 figure (GBP 827 million); the case-level fact to remember is about GBP 0.8 billion, USD 1.3 billion.

### Slide 5: Soc Gen Case Questions to be answered (first question highlighted)
- What caused this affair?
- Could this situation be repeated in the future? How can financial institutions prevent it?
- What makes a currency convertible?

### Slide 6: Rogue Trader (cartoon)
- Picture only: a French cartoon by Vidberg, "Jérôme Kerviel retrouve la liberté" (Kerviel regains his freedom). At the exit desk of the Prison de la Santé the guard reads back his belongings: "a bracelet, a Casio watch, two metro tickets... and five billion euros in small notes".
- Point: the joke is that Kerviel never had the money; he gained nothing personally (the case confirms this).

### Slide 7: S&P ratings screen (standardandpoors.com)
- Picture: a screenshot of the S&P Global ratings page (Spanish interface) for Société Générale. Four lines:
  - Long term, local currency: **A**, rating changed 23-Jan-2012, last review 24-Jun-2025, outlook **Stable**.
  - Short term, local currency: **A-1**, changed 07-May-2009.
  - Long term, foreign currency: **A**, Stable.
  - Short term, foreign currency: **A-1**.
- Point: every bank rating comes in four versions (long and short term, local and foreign currency). The one to quote is **long-term local currency**.

### Slide 8: Soc Gen Case Questions (second question highlighted)
- Same three questions; emphasis on "Could this be repeated? How can financial institutions prevent it?"

### Slide 9: Rogue Trader (the three faces)
- Photos of the three rogue traders with their losses as written on the slide:
  - **Nick Leeson (1996, USD 1.4 billion)**
  - **Jérôme Kerviel (2008, EUR 4.9 billion)**
  - **Kweku Adoboli (2011, USD 2 billion)** (spelled "Abdoli" on the slide)
- Note the slide's Leeson figures (1996, USD 1.4 billion) differ from slide 3 (1995, USD 1.3 billion). The case-consistent answer for Barings is 1995; for Kerviel always EUR 4.9 billion.

### Slide 10: The Liquidity of the Financial System
- **Cash ratio** (also called **liquidity coverage ratio** or **cash asset ratio**): total dollar value of **cash and marketable securities divided by current liabilities**.
- For a **bank**: the cash held by the bank as a proportion of the **deposits** in the bank.
- It measures the extent to which a corporation or other entity can quickly liquidate assets and cover short-term creditors.
- Picture: Scrooge McDuck diving into his money bin (liquidity as a pile of cash).

### Slide 11: Currency Concept (16.02.2007)
- Picture only: cover of The Economist, 17 to 23 February 2007, "The end of the cash era", a dinosaur made of coins with banknote pterodactyls.
- Point: physical cash is a shrinking part of money; introduces the next slides on money versus currency.

### Slide 12: Currency Concept (definition)
- The term **currency** can mean either a particular currency (for example the US dollar) or the **coins and banknotes** of a currency, which are the physical part of a nation's money supply.
- The other part of the money supply is **money deposited in banks** ("deposit money"), whose ownership is transferred by cheques or by transfers such as credit and debit cards.
- Deposit money and currency are both money (both accepted as a means of exchange), but **money need not be currency**.

### Slide 13: Currency Concept (history)
- Historically money in the form of currency predominated: usually gold or silver coins with intrinsic value matching the monetary unit.
- **Modern currency is intrinsically worthless.** One currency prevails over another in commodity-money systems usually because the government decrees that only particular monetary units are accepted **in payment of taxes**.

### Slide 14: Circulating currencies
- A currency is a unit of exchange, hence a kind of money and a medium of exchange. It includes paper or polymer banknotes and metal coins.
- Countries generally have a **monopoly** on issuing currency, though some share a currency with others.
- Different countries may use the same name for different currencies (many "dollars"); a territory that is technically part of another country may use a different currency (example: **Hong Kong Dollar**).

### Slide 15: Exchange Rates (overview)
- **182 official currencies** for **193 UN member states**.
- Each central bank has monopoly control over the supply and production of its own currency. To allow trade between currency zones there are **exchange rates**: the prices at which currencies (and the goods and services of each zone) are exchanged.
- Currencies are classified as **floating** or **fixed** by exchange-rate regime.

### Slide 16: Exchange Rates: floating currency
- **Floating currency**: value set by the free market; it changes constantly with supply and demand for the currency and with the amount held in foreign reserves.
- Advantage: tends to be more **economically efficient**.
- Disadvantage: tends to be more **volatile**; it may appreciate or depreciate with market swings.
- Most major currencies are floating.

### Slide 17: Exchange Rates: fixed exchange rate
- **Fixed (pegged) exchange rate**: the government links the currency's value to another value or to a commodity such as **gold**. It does not change with market conditions.
- A government fixes its currency by **holding reserves of the peg asset** in the central bank. Example: a country that fixes to the USD must hold enough dollars to cover all its currency in circulation.

### Slide 18: Turkish Lira
- A long depreciation series, 1 US dollar in Turkish lira:
  - 1966: 9
  - 1980: 90
  - 1988: 1,300
  - 1995: 45,000
  - 2001: 1,650,000
  - 2005: 1.29 **new Turkish lira** (the new lira dropped **six zeroes**, introduced 2005)
  - 2010: 1.55
  - 2012: 1.79
  - 20/09/2022: 18.30 TRY
  - 15/10/2025: 41.82 TRY
  - 08/10/2026: 49.22 TRY
- Point: a non-convertible, chronically depreciating currency; a redenomination (dropping zeroes) does not stop the trend.

### Slide 19: Circulating currencies (the list)
- The list of circulating currencies contains roughly **180** current official or de facto currencies of:
  - the **193** UN member states,
  - **1** UN observer state,
  - **4** partially recognized sovereign states,
  - **6** unrecognized countries, and
  - **32** dependencies.

### Slide 20: Convertible Currencies (table)
| Currency | Code | Country |
|---|---|---|
| Euro (*) | EUR | 21 of the 27 EU members |
| United States Dollar | USD | USA |
| Canadian Dollar | CAD | Canada |
| New Zealand Dollar | NZD | New Zealand |
| Japanese Yen | JPY | Japan |
| Pound Sterling | GBP | United Kingdom |
| Franc | CHF | Switzerland + Liechtenstein |
| Krona | SEK | Sweden |
| Krone | DKK | Denmark |
| Krone | NOK | Norway |
- Ten currencies on the slide. Not on it: Chinese yuan, Indian rupee, Russian ruble, Turkish lira (all treated in class as non-convertible). The Australian dollar is not on this slide either.

### Slide 21: Convertible Currency (definition, CX3-11)
- **Convertibility**: the degree of ease by which a currency or security can be bought, sold, or exchanged for other currencies or securities.
- Sites: xe.com and x-rates.com (the professor uses x-rates.com because it is free and covers every currency, not just hard currencies).

### Slide 22: Soc Gen Case Questions (third question)
- Same three questions; emphasis on "What makes a currency convertible?"

### Slide 23: United Nations definition (CX3-11)
- A currency is **freely convertible** when it complies with one or more of:
  - a) The government of the currency's country allows **residents and non-residents to purchase unlimited foreign currency** with the domestic currency.
  - b) **No special authorization is needed from the Central Bank** to exchange the domestic currency for other currencies or gold.
  - c) The currency is **traded in international foreign exchange markets and widely used in international transactions**.
- Source: "Acceptance of Local Currency from Developing Countries in Payment of Assessed Contributions", FAO Finance Committee, Rome 2005.

### Slide 24: Convertible Currency (explanation, part 1)
- A convertible currency is any currency that can be quickly bought or sold **without permission from a central bank**; it can be used to obtain other currencies or to buy gold.
- At one point only a few currencies were convertible; now the majority are, and can be traded on a forex market or exchanged privately as local law allows.
- Why investors buy or sell convertible currency: to take advantage of projected trends. Example: a political regime change in an election year or an overthrow of the government may reduce demand for the currency, so holders sell before it falls to minimize losses.

### Slide 25: Convertible Currency (explanation, part 2, CX3-11)
- Buying can also pay: a favorable economic outlook can push the exchange rate up; an investor who buys early and holds through the upswing can realize a significant return.
- The skill is knowing **when to buy, how long to hold, and when to sell**; predicting when a currency will level off or fall matters as much as spotting the rise. Regular currency traders develop a sense for balancing buying and selling.

### Slide 26: Currency Future
- A **currency future** (FX future, foreign exchange future) is a **futures contract** to exchange one currency for another at a **specified future date** at a price (exchange rate) **fixed on the purchase date**.
- Typically one of the currencies is the **US dollar**; the price is then quoted in **US dollars per unit of the other currency**, which can differ from the spot-market quoting convention.
- The **trade unit** is a set amount of the other currency, for instance **EUR 125,000**.
- Most contracts have **physical delivery** (actual payments in each currency if held to the last trading day), but **most are closed out before delivery**; investors can close out any time before the delivery date.

### Slide 27: Forward (the 2026 example)
- The formula as on the slide:
  - **Swap points = (SONIA − EURIBOR) × Days × Spot / (36,000 + (LIBOR × Days))**
  - **Forward price = Spot + Swap points**
- "LIBOR" in the denominator is the old label (the professor said in class the slide needs amending; the rate in the denominator is the same 180-day rate used in the numerator, see Part 3).
- Example: "currency insurance" GBP / EUR, **180 days**.
  - **Spot 08/10/2026: 1 EUR = 0.8479 GBP**
  - **ECB Euribor 180 days: 3.013%** (08/10/2026, from euribor-rates.eu, 6-month Euribor)
  - **BoE SONIA 180 days: 3.732%** (08/10/2026, from global-rates.com)
  - Forward 08/04/2027: 1 EUR = XXXX GBP (to be calculated)
- **SONIA** = Sterling Overnight Index Average (the sterling rate that replaced LIBOR).
- Worked calculation (as done on the board in class):
  - Rate difference: 3.732 − 3.013 = **0.719**
  - Times days: 0.719 × 180 = **129.42**
  - Times spot: 129.42 × 0.8479 = **109.735**
  - Denominator: 36,000 + 3.013 × 180 = 36,000 + 542.34 = **36,542.34**
  - Swap points: 109.735 / 36,542.34 = **0.0030**
  - Forward: 0.8479 + 0.0030 = **0.8509 GBP per EUR** for 08/04/2027.
  - (If the denominator uses SONIA instead: 36,000 + 671.76 = 36,671.76; 109.735 / 36,671.76 = 0.0030; forward still 0.8509. The answer does not change at four decimals.)
- Reading: the swap points are positive because SONIA is higher than EURIBOR, so the forward is above spot and **the euro appreciates** against the pound in the forward (1 EUR buys more GBP in April than in October). If the two rates were equal the swap points would be zero and forward = spot.

### Slide 28: Forward (the 2022 example)
- Same formula written with LIBOR: Swap points = (LIBOR − EURIBOR) × Days × Spot / (36,000 + (LIBOR × Days)); Forward = Spot + Swap points.
- GBP / EUR, 180 days:
  - Spot 20.09.2022: 1 EUR = 0.8755 GBP
  - ECB Euribor 180 days: 1.672% (16/09/2022)
  - BoE Libor 180 days: 3.518%
- Kept as the older version of the same exercise (LIBOR has since been replaced by SONIA for sterling). Arithmetic: (3.518 − 1.672) = 1.846; × 180 = 332.28; × 0.8755 = 290.91; / (36,000 + 3.518 × 180 = 36,633.24) = 0.0079; forward about 0.8834.

### Slide 29: Forward Rates (Bloomberg FRD screen, CX3-11)
- Picture: Bloomberg "Curncy FRD" spot and forward rates screen for **EUR-USD**, pricing date **27 Jan 2003**, source CMPN Composite (NY), price type "Calculated via USD", display conventional bid/offer.
- Spot: **1.0858 bid / 1.0860 offer**.
- Forward points (pips) are **negative at every tenor**: ON −0.47, 1W −3.30, 1M −13.90, 2M −27.75, 3M −40.25, 6M −75.60, 9M −105.50, **1Y −128.70**, 2Y −163.00, 3Y −136.00, 4Y −105.00, 5Y −51.00 (bid side).
- Outright forwards: 1M 1.084410, 3M 1.081775, 6M 1.078240, **1Y 1.072930**, 2Y 1.069500.
- Point: in 2003 the euro traded at a **forward discount** to the dollar (negative points, because euro rates were above dollar rates), and the bid-offer spread **widens with tenor**. Right-hand panels show broken dates and forward-forward quotes. The sign of the swap points depends on which currency's rate is higher.

### Slide 30: Big Mac Index (link)
- Link to The Economist's Big Mac index page (15 Jan 2020).

### Slide 31: Big Mac Index (chart, CX3-11)
- Picture: The Economist chart "Local currency under(−)/over(+) valuation against the dollar, %", prices at market exchange rates on **30 Jan 2013**, US Big Mac **USD 4.37** as base.
- Overvalued: **Norway 7.84** (about +79%), **Switzerland 7.12** (+63%), Brazil 5.64 (+29%), Canada 5.39, Australia 4.90, Euro area 4.88 (+12%).
- Undervalued: Britain 4.25 (−3%), Japan 3.51 (−20%), Mexico 2.90, Indonesia 2.86, China 2.57 (−41%), Russia 2.43, Egypt 2.39, Hong Kong 2.19 (−50%), South Africa 2.03, **India 1.67 (−62%, Maharaja Mac)**.
- Point: the Big Mac index is a light-hearted **purchasing power parity (PPP)** test: if a Big Mac costs more in local currency converted at market rates than in the US, the currency is overvalued. Footnotes: euro area is a weighted average of members; US is an average of four cities; China of five.

### Slide 32: Currency Wars
- Picture: cover of James Rickards, "Currency Wars: The Making of the Next Global Crisis", plus a link to an Inquirer article "Currency wars back on international agenda".
- Point: **currency war** = competitive devaluation, countries pushing their currency down to help exports (the class discussion of China keeping the yuan weak and the Trump administration wanting a weaker dollar fits here).

## Part 2: The case section by section

### Opening (page 1, partly garbled in the extraction)
- Epigraph from Kerviel: "I told myself that Société Générale would never fire someone who was generating this much cash."
- On **24 January 2008** Société Générale announced that 2007 net income would be reduced by a **EUR 4.9 billion loss** from a trading fraud by a single trader, **Jérôme Kerviel**.
- The announcement followed the "quiet" unwinding of his positions, which amounted to about **EUR 50 billion**, over a **three-day** period during which global stock markets fell sharply on US economic worries.
- Nicolas Rutsaert (Dexia analyst): "At first this seemed like a joke"; Société Générale "was a leader in derivatives and was considered one of the best risk managers in the world."
- Politics: President **Nicolas Sarkozy** called for the resignation of CEO and Chairman **Daniel Bouton** and was furious at being kept in the dark; Prime Minister **François Fillon** insisted the incident was distinct from the financial market turmoil; skeptics suspected Kerviel was a **scapegoat** to disguise the bank's subprime exposure; Finance Minister **Christine Lagarde** asked the banking regulator to strengthen control mechanisms; the French public sympathized with Kerviel as a victim of a greedy, profit-obsessed bank.
- Case by Professor François Brochet (HBS), rev. 23 April 2010, based on published sources, mainly the bank's "Mission Green" report.

### Company History
- Founded **1864**, one of the oldest banks in France; initially served French industrialists and financed itself almost entirely with own resources.
- **1871** listed on the French stock exchange; **1945 nationalized**.
- Post-war: expanded services, specialized in lending, reorganized as an international banking group (Italy, Mexico), pioneered finance leasing and ad hoc credit subsidiaries; IT investment drove growth.
- **29 July 1987**: the government sold its stake; shares traded on the Paris Bourse (privatized).
- **Daniel Bouton** joined in **1991** as Executive Vice President: brilliant, analytical, cold and blunt; product of the French meritocracy (Institut d'Études Politiques, ENA), Budget Director at the Finance Ministry 1988-1990. CEO in **1993** (succeeding Marc Vienot, same schools), Chairman as well in **1997**.
- **1997**: bought **Crédit du Nord**, a network of regional banks, boosting French retail banking; then international acquisitions and a separate international retail division.
- Under Bouton the priority was **corporate and investment banking**: equities, M&A, fixed income, brokerage on organized futures markets.

### Company Structure
- Three main divisions: **Retail Banking and Financial Services**; **Global Investment Management and Services**; **Corporate and Investment Banking (SGCIB)**.
- Retail: 37 countries (Central and Eastern Europe, Mediterranean, Africa, French overseas territories); **2,795 branches, 40,000 employees, 8.8 million** individual customers, over **730,000** businesses.
- Global Investment Management and Services: five lines: Asset Management, Private Banking, Securities Services, **Newedge** (multi-asset brokerage), **Boursorama** (online banking). In 2008: 11,000 staff, **EUR 336 billion** assets under management.
- **SGCIB** had three departments: **Global Equities and Derivatives Solutions (GEDS)**; **Fixed Income, Currency and Commodities (FICC)**; **Capital Raising and Financing**.
- In **2006 SGCIB's return on equity was 48%** against **26%** for the whole group (Exhibit 1).
- Functions in GEDS and FICC: research, sales, engineering, trading. Traders price and execute for clients or for the bank (**proprietary trading**); they must anticipate market moves; their skills, decision-making under pressure and ability to design complex transactions are core strategic assets.

### GEDS and the derivatives culture
- The true engine of success was the **equity derivatives trading division of GEDS**.
- **Derivatives**: securities whose payoffs depend on the value of other assets; main categories **options, forwards and swaps**; used mainly for hedging and risk management, but also for speculation thanks to leverage.
- Of the **1,365** GEDS employees, **385** worked in arbitrage or volatility trading. **Arbitrage** = spotting mispricing and buying undervalued / selling overvalued products. Main arbitrage activities: **index arbitrage** (index constituents versus index futures), **equity borrowing or lending** (to hedge derivative positions or supply clients), **relative value arbitrage** (risk arbitrage, fund arbitrage).
- Derivatives trading was about **20% of the bank's total profit in 2007** (analyst estimate). Merrill Lynch: SocGen equity derivatives "probably the best in the world qualitatively and quantitatively".
- The division had profits **every quarter since 1993**; between 2003 and 2006 only **13 days** with losses over EUR 5 million; its **59 profit centers** were all profitable in 2006, none over 10% of revenues.
- Edge built on heavy **IT** investment and a centralized trading system since the mid-1980s, and on hiring graduates of France's top engineering schools. Named "**Equity Derivatives House of the Year**" repeatedly, most recently by Risk magazine in January 2008. World leader in **equity warrants** with **18.4%** market share in 2006.
- Culture: more willing than peers to take **proprietary risk**; traders encouraged to make risky bets with the bank's money. The founding teams of engineers and mathematicians were nicknamed the "**soldier-monks**" (after the crusading monks) for discipline and fierce competitiveness; they believed their complex computer models managed the risk.

### The Delta One Listed Products Desk
- **Delta One** was a subdivision of the arbitrage division. "Delta one" products are derivatives whose value **moves to the same extent as the underlying** (same or opposite direction): exchange-traded funds, equity swaps. Most trading houses have a delta one group.
- Head of Delta One: **Martial Rouyère**, staff of **24**: **8** on the **Listed Products** desk, **10** on the **Index Tracking** desk.
- **Eric Cordelle**, 36, became desk head of **Delta One Listed Products (DLP)** in **April 2007** after four years in the Tokyo office; experienced in **structuring** products, **not in trading** them.

### Jérôme Kerviel
- Chain of command (Exhibit 2): Kerviel reported to Cordelle, who reported to Rouyère.
- Joined SocGen in **2000** on a **13-month contract for about EUR 32,000**, in the **Middle Office**; praised as "efficient", "rigorous and autonomous", excellent at IT.
- **2002**: moved to the trading floor as a **trading assistant** (answering phones, keeping records for senior traders). His skill at designing derivative strategies got him onto the **DLP trading desk in 2005**, specializing in **turbo warrants**: stock options with a **knock-out barrier**, first introduced in Germany in 2001, popular because **less sensitive to volatility** than regular options (Exhibit 3).
- His path from **Middle Office to Front Office was highly unusual**. France's system: ordinary universities must admit any Baccalauréat holder; the **Grandes Écoles** have competitive entrance exams prepared over two to three years. Almost all CEOs of the 40 largest French companies went to Grandes Écoles; trading floors are dominated by Polytechnique, Centrale, HEC, ESSEC, ESCP Europe graduates. Cordelle was a graduate of **Polytechnique** and **ENSAE**.
- Kerviel had **no Grande École** degree: a degree from the **IUP of Nantes** (trade-school equivalent), an internship at SocGen, then a programme in investment banking oversight at the University of Lyons (he had failed the Sciences Po Lille entrance exam). Once promoted he felt he had to **prove himself** and felt like an outsider from his first team meeting.

### Kerviel's build-up of large directional positions
- **July 2005**: short position of about **EUR 10 million in Allianz**, outside his turbo-warrant mandate; it coincided with the **London terrorist bombings** and he made large profits as the insurer's stock fell.
- **2006**: directional equity position of about **EUR 135 million**, with over EUR 5 million each in Allianz and two German photovoltaic companies (**SolarWorld, Q-Cells**); also began futures on the **DAX**.
- **Early 2007**, as the subprime crisis developed: short DAX futures position of **EUR 850 million on 24 January 2007**, **EUR 2.6 billion** end of February, **EUR 5.6 billion** end of March. DAX hit an all-time high in July; his short peaked at **over EUR 30 billion**. Unwound in August, rebuilt a similar short in the fall; individual stock positions up to **EUR 350 million**.
- **November and December 2007**: unwound DAX and EUROSTOXX futures; all large index positions **zero on 31 December 2007**.
- **2 to 18 January 2008**: built a **long** position on index futures of **EUR 49 billion**.

### "Cash Machine"
- In 2007 Kerviel's **reported** earnings were **EUR 25 million from proprietary trading**, far above the roughly **EUR 3 million** from his official job (arbitrage on competitors' turbo warrants). His earnings grew **sixfold** 2006 to 2007 and were **59% of the DLP desk's** total 2007 earnings (Exhibit 4).
- Colleagues called him a "**cash machine**" or "star". Even his inflated reported earnings were far below his **actual** earnings of **EUR 1.5 billion** (Exhibit 5).
- No personal gain: salary on joining the desk **EUR 48,000**; 2006 bonus **EUR 60,000** (senior traders: about EUR 1,000,000). For 2007 he asked for **EUR 600,000**; his supervisor would recommend only **half**. Modest lifestyle. At a happy hour he asked Cordelle how to get a EUR 500,000 bonus and whether EUR 50 million of earnings would do; Cordelle said it was "not entirely out of the question".

### Société Générale's internal controls
- Desk managers' two main tasks: (1) check the desk's **net position** stays within its risk limit (**EUR 125 million for DLP**); (2) consult databases on traders' activity and P&L.
- Internal directive of **2 June 2000**: Front Office managers to do "a daily analysis of the coherence of risks, earnings and positions". 2007 procedures: each trader must know his market-risk limits and be able to present them; any breach remedied immediately. **January 2008** update: each Risk Manager and desk manager responsible for a **daily control of net and gross positions** for all products.
- Before 2007 his first supervisor **tolerated intraday directional positions** outside his mandate and unjustified for his junior level. When Kerviel boasted of the Allianz gain, the supervisor only said "be careful, you could as easily have lost". That supervisor **resigned in January 2007**.
- For the **two and a half months until Cordelle arrived on 1 April 2007**, the head of Delta One set up **no monitoring**; the most senior trader validated monthly earnings and Kerviel even **validated his own earnings in March**. Exhibit 6: unauthorized positions jumped when supervision lapsed.
- **Cordelle managed by trust**, assuming traders answered truthfully. Rouyère knew Cordelle lacked trading-management experience but gave no guidance; in the second half of 2007 both were busy with **high staff turnover** and subprime-hit equities.
- Other controls were **fragmented among departments**, each acting within its own purview, designed to check **correct execution rather than detect fraud**. Back and Middle Offices: (1) administrative and financial handling of transactions, (2) first-level controls, (3) financial reporting, (4) operational risk. Each trader's **assistant** belonged hierarchically to Middle/Back Office, so was a first layer of control.
- Risk Management set firm-wide tolerance but desks had discretion; at Delta One **gross positions had no limit**; large **intraday** directional positions were tolerated as long as no large **net overnight** position was kept.
- Indirect control: mandatory **two-week vacation** each year so someone else runs the book. Kerviel cited his father's recent death to skip it; he took only **four days off in 2007** (France guarantees a minimum of 30 paid vacation days).
- Growth: Delta One volumes **doubled in twelve months**; Front Office staff grew **from 4 to 23 in two years**. Internal controls were audited in 2007 by **Ernst & Young and Deloitte**: **no concerns** reported.

### Alerts regarding Kerviel's activity
- Between end 2006 and early 2008 control agents received **74 alerts** on anomalies in his trading. They followed procedure, closed the alerts, and never verified his assertions. Procedures often **did not include his superiors**, or only an e-mail to the manager.
- **April and May 2007**: Middle Office told Rouyère and his superior of discrepancies between Front Office and accounting records. **July 2007**: Rouyère did not react to an alert on **abnormally high cash borrowings** by Kerviel.
- **External alerts from Eurex** (leading European derivatives exchange): **October 2007** e-mails to Cordelle on Kerviel's purchase of **6,000 forward contracts in two hours** (Cordelle: he got 200 to 300 e-mails a day and did not read it in detail). **November 2007**: two letters of inquiry to Cordelle and compliance. Kerviel told Cordelle Eurex was "stupid" but told his broker privately he was "in trouble, making too much money". Compliance offered a conference call; Eurex did not follow up. Eurex asked about **strategy and procedures** (many trades went through the London subsidiary **FIMAT Futures Limited**), **not about volume**; SocGen's answers were deemed appropriate.

### Kerviel's methods of concealment
- **1. Fictitious offsetting trades**: single fake trades that offset his real positions and latent earnings, altering risk and valuation estimates. **947** such transactions.
- **2. Fictitious pairs** offsetting in **quantity but not price**, creating fake losses to hide real gains. Example **1 March 2007**: recorded buying **2,266,500 SolarWorld shares at EUR 63** and selling the same number at **EUR 53**, a fictitious loss of **EUR 22.7 million**. **115** such transactions.
- He **cancelled** fictitious trades before controls caught them, buying time with "**technical**" counterparties (not yet in the client database), **internal** counterparties (**ClickOptions**, a wholly owned subsidiary) and trades with **deferred start dates**.
- **3. Provision flows**: positive or negative amounts meant to correct modelling bias in Front Office valuations, normally entered by assistants; **nine** fraudulent provision flows, cancelled before the **monthly** check.
- Used **different computers**; Cordelle once saw him trading at a junior's desk (it was part of the junior's training).
- Avoided dealing repeatedly with the same control agents. **Forged e-mails** when questioned: two in April 2007, three in June 2007, two on 17-18 January 2008; he reused real e-mails, keeping headers and changing the text.
- Possible **collusion** with his assistant **Thomas Mougard**: about **15%** of the fraudulent transactions were recorded by Mougard, and an e-mail from Mougard showed knowledge of the fictitious trades.

### Discovery of Kerviel's trading activities
- Under new **Basel II** guidelines, the **Cooke ratio** (a capital-adequacy measure) for the counterparty on **eight forward contracts** was abnormally high and alerted SGCIB's **Accounting and Regulatory Reporting** team.
- Asked to name the counterparty, Kerviel e-mailed: "This materialized the give-up of puts made late; I owe money to the counterparty. We'll rebook it a.s.a.p." The agent did not understand it and did not follow up. Days of scrutiny followed; Kerviel then said the counterparty was **Deutsche Bank** and forwarded two e-mails. A control agent **called Deutsche Bank**, which had **no record** of the eight transactions.
- **Saturday 19 January 2008**: Kerviel, on his way to Normandy, was summoned to headquarters. Officials avoided excessive pressure, mindful of another derivatives trader's recent suicide after questioning. **Jean-Pierre Mustier** (head of SGCIB, himself one of the bank's first equity derivatives traders) asked about his strategy; Kerviel said he had found a "**martingale**" on DAX futures (a martingale: doubling the bet after every loss to recover everything on the first win), but his strategy was not complex. He first understated his exposure, then revealed the scheme.

### Closing of the position and public disclosure
- The bank closed the positions **as quickly as possible and secretly**; senior equity derivatives trader **Maxime Kahn** did it over the next few days.
- Bouton informed the **AMF** (Autorité des Marchés Financiers, French markets regulator) and got authorization to **withhold disclosure** until the positions were closed; he also called **Christian Noyer**, governor of the Banque de France (fellow Sciences Po and ENA graduate), about liquidity.
- **24 January 2008** announcement: about **EUR 2 billion** of losses from **US subprime** exposure plus **EUR 4.9 billion** from Kerviel; group annual profit fell from **EUR 5.2 billion in 2006** to **EUR 600 to 800 million in 2007**; a **EUR 5.5 billion capital increase** needed; trading in the shares **suspended** that day.
- Later, restated SGCIB quarterly results reflecting the fictitious trades (Exhibit 7).

### Kerviel's revelations to the police
- SocGen filed a complaint for **breach of trust, falsifying documents, and unauthorized computer access**. The Paris prosecutor opened an investigation; Kerviel was questioned for **two days**.
- He admitted exceeding the desk's risk limits and concealing positions with fictitious trades.
- But he scoffed at the idea his superiors did not know: it was impossible to earn so much within his mandate; despite numerous alerts **no one reprimanded him**; he claimed the **unspoken approval** of his superiors because of his contribution to the bottom line.

### Exhibit 1: Key financial data prior to Kerviel's trading (FY 1999 versus FY 2006)
- Group net income **EUR 5,221 million in FY06**, ROE after tax **25.8%**, growth **+14.9% per year** since 1999 (1999 net income about EUR 1,980 million, ROE 19.1%).
- Reconstructed from the scrambled chart (labels and figures were separated in the extraction; pairing is the most consistent one, so treat as approximate):

| Division | 1999 | FY06 (ROE) |
|---|---|---|
| Corporate & Investment Banking | 590 (16%) | **2,340 (48%)** |
| French Networks | 697 (16%) | 1,321 (21%) |
| Global Investment Management & Services | 76 (24%) | 577 |
| Financial Services | 163 (15%) | 544 (16%) |
| Retail Banking outside France | 207 | 471 (36%) |
| Corporate Center | 247 | (balance, unclear on the exhibit) |
- Point: CIB produced almost half of group profit at an ROE of 48%, which is why the derivatives business was untouchable.
- Source: SocGen presentation of FY2006 results, 14 February 2007.

### Exhibit 2: Chain of management over Kerviel within GEDS
- Head of trading activities: **Luc François**.
- Head of arbitrage activities: **Pierre-Yves Morlat**.
- Head of Equity Finance: **Philippe Baboulin**.
- Head of Delta One: **Martial Rouyère**.
- Under Delta One: **Listed Products** desk head **Eric Cordelle** with **7 traders including Kerviel**; **Index Tracking** desk head plus 9 traders; Equity Finance Delta One head (+1 agent); Structuring Cash Flow (+2 agents).
- Structure in place until **18 December 2007**; after that the head of trading became head of GEDS and was replaced by the former head of arbitrage, who kept his previous office. Source: Mission Green report, names added by the case writer.

### Exhibit 3: Kerviel's authorized activities
- **Turbo warrants**: SG sells warrants with **knock-out** options to clients (mainly calls) and **hedges by buying the underlying**. "**Long turbos**" are calls deactivated if spot falls below the barrier; "**short turbos**" are puts deactivated if spot rises above the barrier. SG buys the underlying so the client gets **leverage** without buying the asset. Underlyings: single shares, baskets (unusual), ETFs, indices, German state bonds, currency. Maturities: **open end** (none), **closed end** (fixed at issue), **one day**. On knock-out SG resells the hedge and pays the client the difference between strike and the barrier level.
- **Arbitrage on competitors' turbo warrants**: in volatile markets DLP spotted competitors' turbos mispriced for market conditions. Buy competitors' call turbos on day D and hedge by **selling futures**; if the market opens lower at D+1 and knocks out the product, SG profits (the hedge is bought back at a gain).
- Payoff example on the exhibit: a long turbo with rebate, strike 10, knock-out barrier 11 (chart; figures not in the text).

### Exhibit 4: 2006 and 2007 earnings from Delta One trading (EUR millions)
| | 2006 | 2007 |
|---|---|---|
| Proprietary trading: Kerviel | 0 | 25 |
| Proprietary trading: Delta One | 24 | 114 |
| Kerviel's weighting | 0% | 22% |
| Client trading: Kerviel | 7 | 18 |
| Client trading: Delta One | 20 | 45 |
| Kerviel's weighting | 35% | 40% |
| Total trading (minus sales credits): Kerviel | 7 | 43 |
| Total trading: Delta One | 44 | 159 |
| Kerviel's weighting | 16% | 27% |
- Distribution of proprietary earnings of the **143 arbitrage traders** of the division: below 0: 10 traders; 0-5: 76; 5-10: 14; 10-15: 12; 15-20: 9; 20-25: 8; 25-30: 4; 30-35: 4; above 35: 6.
- With EUR 25 million Kerviel was the **15th best of 143** proprietary traders.
- (The text says 59% of DLP desk earnings; the exhibit weightings refer to all of Delta One, hence the lower 27%.)

### Exhibit 5: Kerviel's actual versus reported earnings
- A chart (figures not in the extracted text) with three series: Kerviel's "official" earnings; actual earnings on unauthorized positions; estimated earnings generated by the offsetting index trades. Text gives the headline: reported about EUR 43 million total (25 proprietary) versus actual **EUR 1.5 billion** at end 2007.

### Exhibit 6: Unauthorized trading around the departure of his supervisor
- Two charts of unauthorized positions in Q1 2007 (EUR millions): on **DAX futures** and on **equities**, marked with **11 January 2007** (supervisor's resignation) and **26 January 2007** (effective departure). The positions rise sharply after the departure (figures not in the text; consistent with EUR 850 million on 24 January, 2.6 billion end February, 5.6 billion end March).

### Exhibit 7: Restatement of SGCIB 2007 quarterly results (EUR millions)
| | Q1 reported | Q1 restated | Q2 reported | Q2 restated | Q3 reported | Q3 restated | Q4 reported | Q4 restated |
|---|---|---|---|---|---|---|---|---|
| Net banking income | 1,947 | 1,947 | 2,077 | 2,077 | 1,159 | 1,159 | (661) | (661) |
| Operating expenses | (1,081) | (1,081) | (1,112) | (1,112) | (743) | (743) | (489) | (489) |
| Gross operating income | 866 | 866 | 965 | 965 | 416 | 416 | (1,150) | (1,150) |
| Net allocation to provisions | 29 | 29 | 31 | 31 | (9) | (9) | 5 | 5 |
| Operating income before unauthorized activities | 895 | 895 | 996 | 996 | 407 | 407 | (1,145) | (1,145) |
| Net gains/losses on unauthorized and concealed activities | 0 | (97) | 0 | (2,064) | 0 | 2,524 | (4,911) | (5,274) |
| Operating income after | 895 | 798 | 996 | (1,068) | 407 | 2,931 | (6,056) | (6,419) |
| Equity-method income | 6 | 6 | 2 | 2 | 6 | 6 | 5 | 5 |
| Net income from other assets | 1 | 1 | (1) | (1) | 2 | 2 | 24 | 24 |
| Income tax | (233) | (200) | (274) | 428 | (101) | (959) | 2,109 | 2,109 |
| Net income before minorities | 669 | 605 | 723 | (639) | 314 | 1,980 | (3,918) | (4,158) |
| Minority interests | 3 | 3 | 2 | 2 | 4 | 4 | 0 | 0 |
| **Net income** | 666 | 602 | 721 | (641) | 310 | 1,976 | (3,918) | (4,158) |
- Reading: the hidden P&L swung from −97 (Q1) to −2,064 (Q2, the short during a rising DAX) to +2,524 (Q3, the short paid off in the summer sell-off) to −5,274 (Q4 restated; the January 2008 unwinding loss was booked to Q4 2007). Sum of restated quarters = −4,911, the EUR 4.9 billion. Source: SocGen Q1 2008 results presentation, 13 May 2008.

## Part 3: What the professor added in class

### Recap: the ICC contract and the three risks
- Per the International Chamber of Commerce a contract must cover: the **parties**, the **object**, the **transport** (who pays), the **means of payment**, the **guarantees**, the **courts and legislation** (which law applies if there is a claim; with China "the Chinese will like theirs and you will like yours"), and the **risks**.
- **EXAM:** Of the hundreds of risks, the ICC says three must always be considered: **transport**, **credit** and **currency**. Transport: oil up 50% since February, freight dearer than six months ago. Credit: you get paid at 120 days, or the debtor does not pay (no liquidity, lost contract). Currency: buying from India and paying in USD leaves uncertainty about the rupee against the dollar.
- Read what you sign; many firms trade on nothing but an invoice. **The invoice is made by the seller**, so alone it proves nothing; it must be **approved by the buyer**. Use a **pro forma invoice** (a draft the buyer accepts and returns) before raising the real invoice.

### Rogue Trader, Barings and the lesson "don't fight the market"
- Film **Rogue Trader** (Ewan McGregor as Leeson, Singapore, Nikkei index, treasury desk). The friend in the cafeteria tells him twice: **don't fight the market**. When the Nikkei falls he buys to push it up; it rises for seconds, then falls again. Lesson: supply and demand set prices; you cannot beat the market.
- Currency markets are **over-the-counter**, open **24 hours**, moving every second; "currencies only have two options, up or down", which is what makes people think they can guess.
- The professor worked on **BBVA's treasury desk**; the front office just buys and sells positions.
- Barings was called "**the Bank of the Queen**" in the UK. Leeson, **without stealing a single pound**, made the bank disappear with losses of **1.3 billion**.

### Ratings (S&P screenshot)
- **EXAM:** Register free at S&P and check the rating of the bank holding your savings. Every bank rating has four lines: **long-term local currency, short-term local currency, long-term foreign currency, short-term foreign currency**. The rating to quote is **long-term local currency**. Société Générale today: **A** (stable). Germany: **AAA** (S&P rates countries as well as banks).
- **EXAM:** **BBB- and above = investment grade; below BBB- = speculative grade.**
- Three agencies: **S&P, Moody's, Fitch**. Heavily criticized in 2008 for rating Lehman Brothers AAA before it defaulted, but in 2026 still trusted because there are no alternatives (none created in Saudi Arabia, India or Spain). Check the rating of counterpart banks in Pakistan, Ivory Coast and the like.
- Next session (Banking Convergence case) builds on this; bring other agencies' ratings if you use them.

### Why the SocGen affair happened (class discussion)
- The professor quoted the loss as USD 7 billion / EUR 7.2 billion; the case figure is **EUR 4.9 billion from Kerviel plus about EUR 2 billion subprime**. Answer 4.9 billion if asked about Kerviel.
- Student answers accepted: the first time he traded outside his mandate he was not reprimanded, only told "be careful", which encouraged him; he wanted to **prove himself** (public university versus Grande École peers); his boss resigned, he was **two months without a supervisor**, the new boss was a modeller not a trader and was "left unchecked"; **74 alerts in about 13 months** all closed by procedure; he **closed the fictitious trades before each check**.
- He was **successful at first**. Analogy: a Turkish exporter paid in USD when the dollar is strong "makes more money on the currency than on the goods" and the boss says "do it again". **EXAM:** If your business is selling oil, machinery, textiles or services, **your business is not to play with currency**. Companies think short term (monthly, quarterly), so a profitable gamble gets repeated.
- Bosses who do not understand what you do are common; "he's doing well, so who cares".
- France: two years of preparation and a competitive exam to enter the elite schools; all CAC 40 general managers come from them. Spain: everyone enters university, many useless diplomas. French and Germans "like control", yet the controls failed.
- Kerviel came from the **back office**, so he knew "when the checks happen, when the screenshot is taken, what flags and what does not". Banks and international business are about **papers**: if the papers are right you get paid; the back office manages them, and nobody in an MBA wants to work there.
- **EXAM:** "**With so many people controlling, at the end no one controls.**" More regulation, KPIs and compliance officers than ever, yet each controller assumes the other will catch it. Many controls could be done by AI instead of seven compliance officers.
- He bought positions and **did not hedge**; every position went down and he had **no counterparty**. He **doubled** each time (the martingale): Amazon at 200, then 150, then 100, then 80, a friend from London or Boston says buy more; doubling in a falling market loses everything, in his case billions. Casino: betting on black again and again as red comes up.

### Hedging rules: close the position, the casino and the bank
- **EXAM:** With currencies you must **always close or hedge your position**.
- Casino analogy: enter with USD 100; the sensible way is small bets and take profits out, or do not play. Putting USD 50 on red and USD 50 on black looks stupid but is a **closed position**: 18 red, 18 black, one green zero, so only 1 in 37 of losing everything, versus 50-50 on an open bet.
- When you buy 10,000 Turkish lira from a Spanish bank to pay a Turkish supplier, the bank's trader **sells the lira at the same time**: the bank closes its position. Banks are the only entities that lend in many currencies, because they serve clients who need them; a company has no reason to hold lira except to pay a Turkish seller.
- **EXAM:** The bank's profit on currency is **not from guessing** the rate; nobody knows where EUR/GBP will be in six months. It is the **spread between the buying and selling price** ("the call and the put": you always buy at the highest price and sell at the lowest). Airport example (American Express desk, Madrid Barajas): change EUR 100 and get USD 82; change back twenty minutes later and get EUR 95; two exchanges, EUR 5 lost.
- **EXAM:** Forwards on **convertible currencies are very cheap** because the bank carries no risk (it closes both sides). Forwards on non-convertible currencies exist (**non-deliverable forwards**, for example Chile copper against Turkey) but are more sophisticated and more expensive.

### The forward exercise (slide 27)
- A forward is what the bank quotes in seconds when you say "I need to buy British pounds in six months". A future is at bottom the same thing (a standardized forward).
- Inputs are real (8 October 2026): spot **1 EUR = 0.8479 GBP**; **SONIA** (Sterling Overnight Index Average, the rate that replaced LIBOR for sterling) **3.732%**; **EURIBOR 180 days 3.013%**; **180 days**; target date **8 April 2027**. (The professor misspoke "8 February" once; the slide says 08/04/2027.)
- **EXAM:** Swap points = (SONIA − EURIBOR) × days × spot / (36,000 + rate × days); forward = spot + swap points. On the board: (3.732 − 3.013) × 180 × 0.8479 = 109.74; divided by 36,542 gives **0.0030**; **forward 0.8509**. The slide's "LIBOR" in the denominator is the old label and will be amended.
- **EXAM:** Why **36,000** and not 36,500: banks use a **360-day year** (twelve months of 30 days; "five bank holidays worldwide"); if you borrow EUR 10,000 you pay interest for 360 days. The **× 100** is because the rates are in **percent**. The same formula (capital × rate × days / 36,000) is in your credit or debit card contract for overdraft interest.
- **EXAM:** The formula essentially prices the **difference between two interest rates**. If both rates were equal the swap points would be **zero and forward = spot**; no two currencies have the same rate, which is why forwards exist. Here SONIA > EURIBOR, so swap points are **positive**, the forward is **higher** than spot, and **the euro appreciates** in the forward (0.8479 now, 0.8509 in April).
- Use: you must pay GBP in six months; the bank sells you 0.8509. If the spot on 8 April 2027 is 0.88 you "lost" (you could have bought cheaper); if it is 0.82 you "won"; either way you forget about it. **EXAM:** If your business is machinery, textiles or oil: go to the bank, buy the forward, pay for it and forget the currency.
- You can calculate a forward for any pair of convertible currencies with just the spot, the two interest rates and the tenor (USD/JPY six months, for example).

### Volatility and convertibility (x-rates demonstration)
- On x-rates.com EUR/USD showed about **1.12** USD per euro (USD 1 = about 0.88 EUR). The one-year chart shows **plenty of volatility**; the dollar strengthened over the year (the transcript's "1.75 a year ago" figure is garbled). The Chinese yuan against the dollar went straight up over the year; EUR/USD zigzagged.
- Spain's **peseta was non-convertible** until about 2000 ("26 years ago").
- Student answers on what makes a currency convertible: stability (rejected: EUR/USD is anything but stable), demand, no restriction on capital flows, accepted everywhere. **EXAM:** The answer is the **UN definition**: no government controls on buying unlimited foreign currency, no central bank authorization, **traded on international FX markets and widely used in international transactions**; in one word, **widely used** and liquid.
- **EXAM:** Convertible currencies (also called **hard currencies**) have a **direct exchange rate** with each other. Non-convertible ones (**Indian rupee, Russian ruble, Turkish lira**, Ethiopian birr) are always converted **through the US dollar**: rupee to dollar, dollar to euro. On x-rates, 1 INR = 0.009370 EUR is computed via USD. Consequence: **double exchange, double fees, double risk**. A student's example: in Ethiopia there is no birr/lira market, you must go through USD for both.
- Why the dollar: the most widely used currency for international transactions; oil (West Texas) is priced in dollars; Iran tried about four years ago to be paid for oil in euros and failed.
- Chicken and egg: a currency is convertible because it is widely used and liquid, and it is used because it is convertible. The list is really about the **euro, the dollar and the yen** (New Zealand, the Nordics and Switzerland are small). To join the list a country needs **plenty of reserves** and unlimited liquidity in foreign currency: banks in the euro area or US are assumed able to pay euros or dollars for any currency sold to them.
- **Chinese yuan**: not on the list because the **government controls it** (the professor said it cannot move more than about **15%** above or below); China is the world's biggest exporter and wants a **weak yuan**; today the opposite is happening (yuan appreciating). As China is now the biggest lender in the world, the yuan may become convertible in future, but the government does not want full convertibility.
- History: the UK was the biggest economy for 200 years, then the US; these two have dominated international transactions for 300 years, which is why their currencies are used.
- George Soros became a billionaire buying and selling pounds, but if you have no clue you lose everything. "Remember Jerome Kerviel. Remember what you are selling."

### Interest rates, exchange rates and savings (closing discussion)
- The Trump administration wants a **weaker dollar**; this year the yuan is appreciating against the dollar while the **euro is depreciating** because the euro economy is struggling (European cars become cheaper for Americans). Guessing currencies is very complicated.
- **EXAM:** Interest rates are **increasing** worldwide. Higher US rates attract savings into dollars, so the professor's personal bet is that the **dollar appreciates**: rising interest rates and currency appreciation usually go together. He buys US shares rather than European ones for two possible wins: the share and the dollar.
- The US 10-year bond pays **over 5%**; a student mentioned a proposed 6% 30-year bond. European and Asian stock markets fell last week as money moved to US bonds. Euro-area inflation is about **4%**, so 5% on a bond is a **real return of about 1%**; shares at 7-8% give about 4% real. For a risk-averse pensioner, French or US bonds at 5% are a clear good decision; for the professor 1% real is too low, but plenty of savings will move to bonds.

### Housekeeping
- Read the case and the slides before class; use AI to get the bullet points of a case in 30 seconds if needed. Watch Rogue Trader (free on YouTube). Next session: the **Banking Convergence** case; log into S&P beforehand.

## Likely exam angles
- Know that the three ICC contract risks are transport, credit and currency, and that currency risk is the uncertainty in the exchange rate between the invoice currency and your own.
- Know that Barings (1762 to 1995), the oldest merchant bank in London, collapsed in 1995 after Nick Leeson lost GBP 827 million (USD 1.3 billion) in Singapore; Kerviel cost Société Générale EUR 4.9 billion in 2008; Kweku Adoboli lost USD 2 billion in 2011.
- Know that Société Générale announced on 24 January 2008 EUR 4.9 billion from Kerviel plus about EUR 2 billion subprime, profit down from EUR 5.2 billion to EUR 600 to 800 million, a EUR 5.5 billion capital increase, and that about EUR 50 billion of positions were unwound secretly over three days.
- Know that Kerviel's January 2008 long position was EUR 49 billion, his 2007 short DAX position peaked above EUR 30 billion, his real 2007 earnings were EUR 1.5 billion against reported EUR 25 million proprietary (EUR 43 million total), and the DLP desk's net risk limit was EUR 125 million.
- Know the control failures: 74 alerts closed by procedure, no supervisor for two and a half months in 2007, Kerviel validated his own March earnings, only four days of vacation in 2007, gross positions unlimited, controls fragmented and aimed at execution not fraud, Ernst & Young and Deloitte raised no concerns.
- Know the three concealment techniques: 947 fictitious offsetting trades, 115 fictitious pairs (SolarWorld 2,266,500 shares at 63 and 53, fake loss EUR 22.7 million), 9 fraudulent provision flows; plus forged e-mails, technical and internal counterparties (ClickOptions), deferred start dates, different computers, possible collusion with assistant Thomas Mougard (15% of fake trades).
- Know that discovery came from a Basel II Cooke ratio anomaly on eight forward contracts, that Deutsche Bank had no record of them, that Kerviel was summoned on Saturday 19 January 2008, told Jean-Pierre Mustier he had a "martingale" on DAX futures, and that Maxime Kahn closed the positions while the AMF allowed delayed disclosure.
- Know that Kerviel came from the Middle Office, joined in 2000 for about EUR 32,000, had no Grande École degree, earned EUR 48,000 salary and a EUR 60,000 bonus for 2006, and asked for EUR 600,000 for 2007.
- Know the cash ratio: cash plus marketable securities over current liabilities; for a bank, cash over deposits.
- Know that deposit money is money but not currency, that modern currency is intrinsically worthless and is accepted because governments require it for taxes, and that there are 182 official currencies for 193 UN members (about 180 circulating plus 1 observer, 4 partially recognized, 6 unrecognized, 32 dependencies).
- Know floating (market-set, more efficient, more volatile) versus fixed or pegged (linked to another currency or gold, needs reserves covering the currency in circulation).
- Know the UN definition of a freely convertible currency: unlimited purchase of foreign currency by residents and non-residents, no central bank authorization, traded on international FX markets and widely used.
- Know the ten convertible currencies on the slide (EUR, USD, CAD, NZD, JPY, GBP, CHF, SEK, DKK, NOK) and that INR, RUB, TRY and CNY are not convertible; non-convertible pairs go through the USD (double fees, double risk).
- Know the forward formula and the class result: swap points = (SONIA − EURIBOR) × 180 × 0.8479 / (36,000 + rate × 180) = about 0.0030; forward = 0.8479 + 0.0030 = 0.8509; equal rates give forward = spot; 36,000 = 360 days × 100 because rates are in percent.
- Know that a currency future is a standardized exchange-traded contract, usually against USD, with a fixed trade unit (EUR 125,000), mostly closed out before delivery, while a forward is a bank quote tailored to your date and amount.
- Know that banks earn the bid-ask spread on currency, not forecasts, and that forwards on convertible currencies are cheap because the bank closes its position; non-deliverable forwards cover non-convertible currencies at higher cost.
- Know the rating facts: four ratings per issuer, quote long-term local currency, BBB- is the investment-grade floor, three agencies (S&P, Moody's, Fitch), Société Générale A, Germany AAA.
- Know that the Big Mac index is a purchasing-power-parity gauge (2013: Norway most overvalued at USD 7.84, India most undervalued at 1.67 against USD 4.37) and that the Bloomberg screen showed the euro at a forward discount to the dollar in January 2003 (1-year points −128.7, forward 1.0729).
- Know that rising interest rates tend to attract savings and appreciate a currency, that the US 10-year is above 5% and euro-area inflation about 4%, and that the Turkish lira went from 9 per dollar in 1966 to 1,650,000 in 2001, dropped six zeroes in 2005, and stood at 49.22 on 8 October 2026.

## Traps and look-alikes
- **Currency versus money**: currency is coins and notes (plus the named unit); deposit money is money but not currency. "Money need not be currency."
- **Floating versus fixed (pegged)**: floating moves with supply and demand and is efficient but volatile; fixed is linked to another currency or gold and requires reserves of the peg asset.
- **Convertible (hard) versus non-convertible currency**: convertible = no permission needed, traded internationally, direct rate with other hard currencies; non-convertible = converted via USD, double fees and double risk. Stability is not the criterion (EUR/USD is volatile yet both are hard).
- **Forward versus future**: both fix today a rate for a future date; the forward is a bank OTC quote for your amount and date; the future is exchange-traded, standardized (EUR 125,000 units), usually against USD, mostly closed out before delivery. The professor: "a future at the end is a forward".
- **Forward versus non-deliverable forward**: the plain forward is for convertible currencies and cheap; the NDF is the sophisticated, expensive product for non-convertible currencies.
- **Swap points sign**: positive when the quoted currency's rate (SONIA, for GBP) is above the base currency's rate (EURIBOR, for EUR), so forward > spot and the base currency (EUR) appreciates in the forward; negative points (Bloomberg 2003 EUR/USD) mean a forward discount.
- **36,000 versus 36,500**: banks use a 360-day year; the 100 converts percent.
- **SONIA versus LIBOR versus EURIBOR**: SONIA is the sterling overnight index average that replaced LIBOR; EURIBOR is the euro rate; the slide's "LIBOR" is a leftover label.
- **Cash ratio** (cash and marketable securities over current liabilities; for a bank cash over deposits) versus the **Cooke ratio** (a Basel capital-adequacy measure; the anomaly that exposed Kerviel).
- **Net versus gross position**: the DLP net limit was EUR 125 million; gross positions had no limit, and intraday positions were tolerated if not kept overnight.
- **Reported versus actual earnings**: Kerviel reported EUR 25 million proprietary (43 total) in 2007; actual EUR 1.5 billion; final loss EUR 4.9 billion.
- **EUR 4.9 billion versus EUR 7 billion**: 4.9 is Kerviel; about 2 billion was subprime; the professor's "7 billion" is the combined hit.
- **Leeson's figures**: slide 3 says 1995, GBP 827 million, USD 1.3 billion; slide 9 says 1996, USD 1.4 billion; the newspaper says GBP 862 million. Use 1995 and GBP 827 million / USD 1.3 billion.
- **Cordelle versus Rouyère versus Mustier versus Bouton versus Kahn**: Cordelle = direct desk head (DLP, from April 2007, structurer not trader); Rouyère = head of Delta One; Mustier = head of SGCIB who questioned Kerviel; Bouton = CEO and Chairman; Kahn = the trader who closed the positions.
- **Middle Office versus Front Office versus Back Office**: Kerviel started in the Middle Office (2000), became a trading assistant (2002), then a Front Office trader (2005); assistants belong to the Middle and Back Offices, which is why they were a control layer.
- **Long turbo versus short turbo**: long turbo = call knocked out if spot falls below the barrier; short turbo = put knocked out if spot rises above it.
- **Investment grade versus speculative grade**: BBB- and above versus below BBB-; the rating to quote is long-term local currency.
- **Big Mac over- versus undervaluation**: a local Big Mac dearer than USD 4.37 at market rates means the currency is overvalued (Norway, Switzerland); cheaper means undervalued (India, Hong Kong, China).
