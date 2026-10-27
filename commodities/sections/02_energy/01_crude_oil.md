# Crude Oil

The world's largest commodity market by value. Around 100+ million barrels per day (mb/d) are consumed globally. Price formation runs through three benchmark families: **Brent** (Atlantic Basin / waterborne), **WTI** (US inland and US Gulf exports), and **Dubai/Oman/Murban** (Middle East crude into Asia).

## Contract specifications

| Contract | Venue / ticker | Size | Tick | Settlement | Notes |
|---|---|---|---|---|---|
| WTI Light Sweet | NYMEX CL | 1,000 bbl | $0.01 = $10 | Physical, Cushing, OK | Expires 3 business days before the 25th calendar day of the month before delivery |
| Brent | ICE B | 1,000 bbl | $0.01 = $10 | Cash vs ICE Brent Index (EFP available) | Expires last business day of the second month before delivery |
| WTI Houston (MEH) | NYMEX / ICE | 1,000 bbl | $0.01 | Physical / differential | US Gulf export pricing |
| Oman | GME (ex-DME) | 1,000 bbl | $0.01 | Physical | Sets Oman OSP |
| Murban | ICE Futures Abu Dhabi | 1,000 bbl | $0.01 | Physical, Fujairah | ADNOC prices Murban off this |
| Shanghai crude | INE SC | 1,000 bbl | ¥0.1 | Physical, medium-sour basket | Yuan-denominated |

**Dated Brent** (Platts) is the physical benchmark for roughly two-thirds of world crude. Basket: Brent, Forties, Oseberg, Ekofisk, Troll, and since mid-2023 **WTI Midland** delivered into Rotterdam, which now frequently sets the Dated price. The complex runs Dated → Forward (cash BFOETM) → ICE futures, linked by CFDs (contracts for difference) and EFPs.

## The Brent basket: deliverable grades

"Brent" today is not one crude but a basket of light sweet grades. Platts assesses each grade for cargoes loading 10 days to one month ahead, adjusts for quality, and **the most competitive (cheapest) grade sets Dated Brent**. The same grades can be delivered against forward (cash) Brent contracts, which is what ICE Brent futures ultimately settle against.

| Grade | Origin / loading | Approx. API / sulfur | Role in the basket |
|---|---|---|---|
| Brent | UK, Sullom Voe (Shetland) | ~38° / ~0.4% | The original grade; now tiny volumes |
| Forties | UK, Hound Point (Forth) via the Forties Pipeline System | ~40° / ~0.6–0.8% | Highest sulfur in the basket (Buzzard field); carries a sulfur de-escalator; historically set Dated most often |
| Oseberg | Norway, Sture | ~37° / ~0.2–0.3% | Higher quality; earns a quality premium, so rarely sets Dated |
| Ekofisk | Norwegian fields, landed at Teesside (UK) | ~38° / ~0.2% | Quality premium; rarely sets Dated |
| Troll | Norway, Mongstad | ~35–36° / ~0.1–0.2% | Added in 2018; quality premium |
| WTI Midland | US Permian, assessed delivered (CIF) Rotterdam | ~40–44° / ~0.1–0.2% | Added for June 2023 deliveries; by far the largest volume, and now sets Dated most of the time |

(API and sulfur figures are approximate and drift as field mixes change; check the latest Platts methodology.)

### How quality adjustments work

- **Quality premiums (escalators):** sellers of the better-quality grades (Oseberg, Ekofisk, Troll) receive a premium when delivering against a forward Brent contract, so they compete on a quality-adjusted basis.
- **Sulfur de-escalator:** Forties sellers pay the buyer a discount for each increment of sulfur above a threshold. Watch the Forties sulfur level when Buzzard output changes.
- **Freight normalisation for WTI Midland:** Midland is priced delivered into Rotterdam and netted back to a North Sea basis using transatlantic Aframax freight. A move in that freight rate changes Midland's competitiveness, and with it Dated Brent itself.

### Why the grade mix matters to traders

- **Liquidity and squeeze risk:** North Sea output has been declining for decades. Each grade was added (Forties/Oseberg 2002, Ekofisk 2007, Troll 2018, Midland 2023) to keep enough deliverable cargoes in the basket to resist squeezes. Thin months can still be squeezed by one buyer accumulating cargoes.
- **US export economics now drive Dated:** with Midland usually the cheapest grade, Dated Brent is effectively linked to Permian output, the WTI–Brent arbitrage, Gulf Coast export capacity and transatlantic freight.
- **Spreads to watch:**
  - Grade differentials: Forties vs Dated, Midland vs Dated, Ekofisk/Oseberg premiums.
  - **CFDs** (Dated vs forward Brent, weekly) and **DFL** (Dated-to-frontline): the market's measure of how tight physical cargoes are compared with paper.
  - **North Sea "window" activity:** bids and offers in the Platts Market-on-Close window. A single trader buying many cargoes is a classic early sign of a squeeze.
- **Possible future additions:** Platts has consulted on adding further grades (for example, Norway's Johan Sverdrup, a medium sour crude). A sour grade in the basket would change Dated's quality and its relationship with Dubai.

## Quality fundamentals

- **API gravity** (lightness) and **sulfur** (sweet <0.5%, sour >0.5%) drive refining value.
- Light sweet yields more gasoline/diesel; heavy sour needs complex refineries (cokers, hydrocrackers) but is cheaper.
- Key differentials: **Brent–Dubai EFS** (sweet/sour, Atlantic/East arbitrage); **WTI–Brent** (US export arb, normally set by freight + pipeline costs from Cushing/Midland to the Gulf); **WCS–WTI** (Canadian heavy discount, eased since the Trans Mountain Expansion started in May 2024).

## Supply

| Group | Approx. share | Notes |
|---|---|---|
| United States | ~20% of liquids | Permian-led shale; short-cycle, price-responsive with ~6–9 month lag; consolidation has increased capital discipline |
| OPEC+ (OPEC + Russia, Kazakhstan, Oman, etc.) | ~50% | Managed supply via quotas; Saudi Arabia is the swing producer with most spare capacity |
| Saudi Arabia | ~10% | Sets monthly OSPs for Asia/Europe/US; watch Arab Light OSP to Asia |
| Russia | ~10% | Sanctions/price cap since Dec 2022; redirected to India/China; shadow fleet |
| Brazil, Guyana, Canada, Norway | growing non-OPEC | Guyana (Stabroek) and Brazil pre-salt are key growth sources |

- **Spare capacity** (mostly Saudi, UAE, Kuwait) is the market's shock absorber; low spare capacity = high geopolitical premium.
- **Decline rates** of existing fields average 4–8% a year; shale wells decline much faster (60–70% in the first year).
- **Breakevens:** marginal shale wells and fiscal breakevens of Gulf states both act as soft floors/ceilings for policy decisions.

## Demand

- Transport fuels around 60% (gasoline, diesel, jet), petchem feedstocks rising (naphtha, LPG, ethane).
- Growth is led by non-OECD Asia (India, China), the Middle East and aviation; China's growth is slowing as EVs and LNG trucks displace gasoline and diesel.
- **Refinery runs** are the real-time demand signal; watch seasonal maintenance (spring and autumn turnarounds).

## Inventories and term structure

- OECD commercial stocks vs 5-year average is the classic balance gauge; it is inversely correlated with Brent time spreads.
- **Cushing stocks** drive WTI front spreads; below ~20 mb operational minimums triggers sharp backwardation.
- Floating storage economics: contango must cover freight (VLCC time charter) + financing.
- Watch **Brent M1–M2**, **M1–M6**, **Dec–Dec** (Dec-red-Dec) spreads as balance barometers.

## Key price drivers

1. OPEC+ policy (monthly/biannual meetings; voluntary cuts and unwinds).
2. Geopolitics: Strait of Hormuz (~20% of global oil flows), Red Sea/Bab el-Mandeb, Russia/Ukraine, Libya outages, Iran/Venezuela sanctions.
3. US shale productivity and rig/frac-spread counts.
4. Chinese import quotas, stockpiling (SPR), and teapot refinery margins.
5. USD and macro risk sentiment; recession probabilities.
6. Refining margins pulling or pushing crude demand.
7. SPR releases/refills (US SPR policy).

## Seasonality

- Q2–Q3: northern-hemisphere driving season + Middle East crude burn for power → stronger demand.
- Spring and autumn refinery maintenance soften crude demand.
- Hurricane season (Jun–Nov) affects US Gulf production and refining.

## Trading notes

- Use **crack spreads** to judge whether crude strength is demand-pulled (cracks strong) or supply-pushed (cracks weak).
- Watch **Dubai spreads and Brent–Dubai EFS** for Asian demand and OPEC+ sour supply.
- Timespreads usually lead flat price at turning points.
- Big moves often occur around OPEC+ meetings, EIA Wednesdays, and geopolitical headlines; options skew flips to calls during supply scares.

## Desk notes

> Add your own observations here.
