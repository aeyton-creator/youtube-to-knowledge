# Market Structure & Pricing Mechanics

This chapter sets out the toolkit used in every later chapter: how futures curves are formed, what spreads mean, and how physical and paper markets connect. Commodity-specific chapters assume this vocabulary.

## Cost of carry and the forward curve

For a storable commodity, the theoretical forward price is bounded by the **full carry**:

> **F = S × e^((r + u − y) × T)** where *r* = financing rate, *u* = storage + insurance cost, *y* = convenience yield, *T* = time. Contango can never sustainably exceed full carry, because a trader could buy spot, store it, sell forward and lock in a riskless profit. Backwardation has **no theoretical limit**, because you cannot borrow physical barrels from the future.

- **Contango** (deferred > prompt): ample inventories, low convenience yield. Deep contango approaching full carry means storage is filling and the market is paying someone to hold stock.
- **Backwardation** (prompt > deferred): scarce prompt supply, high convenience yield. Inventories and spreads are inversely related; the inventory–spread relationship (the "Working curve") is one of the most reliable relationships in commodities.
- **Convenience yield** is the implied benefit of holding the physical: avoiding a plant shutdown, meeting a contract, keeping a refinery running.

## Spreads: the language of fundamentals

| Spread type | Example | What it tells you |
|---|---|---|
| Calendar / time | CL Dec–Jan, ZC Jul/Dec | Prompt tightness, storage economics, old-crop vs new-crop |
| Location | WTI–Brent, LME vs SHFE copper, KC–Chicago wheat | Freight, arbitrage windows, regional balance |
| Quality | Brent–Dubai, Arabica–Robusta, 62%–58% Fe ore | Sweet/sour, grade premiums, demand by product |
| Processing / margin | 3-2-1 crack, soy crush, spark/dark spread, hog crush | Margin of the converter; predicts run rates |
| Inter-commodity | Gold/silver ratio, corn/wheat, soyoil/heating oil (BOHO) | Substitution and relative value |

**Rule of thumb:** outright prices tell you *what* the market thinks; spreads tell you *why*. A rally on falling spreads is usually speculative or macro-driven; a rally led by the front spread is usually physical tightness.

## Basis and physical pricing

- **Basis = local cash price − futures price.** Physical deals are typically priced as futures + basis (grains: "Dec + 30 over"), or index + differential (crude: "Dated Brent + $1.20").
- Hedgers trade **basis risk** for flat-price risk. A grain elevator long cash/short futures profits when basis strengthens.
- Basis drivers: local supply/demand, freight, storage, quality, delivery logistics, and the convergence mechanism of the contract.
- **EFP / EFRP** (exchange for physical / related position) links an OTC physical deal to a futures position and is how much physical volume enters the exchange.

## Delivery and settlement

- **Physically delivered** contracts (WTI, Henry Hub, CBOT grains, COMEX metals, LME metals, ICE softs) force convergence through delivery; watch first notice day (FND) and the delivery mechanics, as positions must be rolled or offset beforehand.
- **Cash-settled** contracts (Brent, feeder cattle, lean hogs, iron ore SGX, JKM) settle against an index; convergence depends on index integrity.
- **Squeezes** happen when deliverable supply is small relative to open interest near expiry. Classic cases: LME nickel March 2022, Hunt brothers silver 1980, WTI April 2020 negative price (storage full at Cushing).

## Roll yield and index economics

- Total return of a futures position = spot return + **roll yield** + collateral yield.
- Long-only index funds (GSCI, BCOM) roll in a published window (BCOM / GSCI around the 5th–9th business day). The "Goldman roll" can pressure the front spread predictably.
- Backwardated markets pay positive roll yield to longs; contango markets bleed.

## Positioning and flows

- **CFTC Commitments of Traders** (Fridays, data as of Tuesday): Disaggregated report splits Producer/Merchant, Swap Dealers, Managed Money and Other Reportables. Extreme managed-money positioning is a contrarian signal, but positioning can stay extreme for long periods.
- **ICE Europe COT** covers Brent, gasoil, London softs; **LME COTR** covers base metals.
- CTAs (trend followers) amplify moves; know the moving-average levels where their signals flip.
- Options: open interest at round strikes creates pinning and gamma-driven hedging flows near expiry.

## Volatility characteristics

- Commodity volatility skew is often **call-skewed** (upside fear) in supply-shock markets — ags in summer weather season, natural gas into winter, cocoa/coffee in deficits — unlike equities' put skew.
- Seasonal implied volatility: corn/soy implied vol rises into the June–August pollination window and collapses after the August WASDE once yield is clearer.
- Mean-reversion in spreads, trend in outrights is a useful heuristic but not a law.

## Hedging basics

1. **Producer hedge:** short futures/forwards or buy puts; collar (buy put, sell call) to cut premium.
2. **Consumer hedge:** long futures or buy calls; airlines hedge jet via Brent/heating oil (cross-hedge with basis risk).
3. **Hedge ratio** = Cov(ΔS, ΔF) / Var(ΔF); cross-hedges need an empirically estimated ratio.
4. Margin calls on hedges can create liquidity crises even when the hedge is economically correct (Metallgesellschaft 1993).

## Producer and consumer flows and the curve

Hedging flows mostly move the **back** of the curve, while inventories set the **front**: *"the front is physical, the back is financial."*

- **Producers sell forward** (oil and gas companies, farmers, miners), usually 6–36 months out. This weighs on deferred prices: backwardation steepens and contango flattens.
- **Consumers buy forward** (airlines, utilities, food processors, fabricators), lifting deferred prices. Consumers usually hedge shorter-dated and more opportunistically than producers.
- **Speculators take the other side** and are paid for it. Keynes's *normal backwardation*: when producer hedging dominates, deferred futures trade below the spot price expected later, and the gap is the speculator's risk premium. It reverses when consumers dominate.

| Flow | When it happens | Effect on the curve |
|---|---|---|
| Producer hedging | Into rallies: producers sell at budget or breakeven levels | Caps the back; steepens backwardation in a rally ("hedging wall") |
| Producer hedge buybacks | Into selloffs: hedges unwound or restructured | Supports the back; flattens the curve |
| Consumer hedging | On dips: buyers lock in cheap costs | Lifts the back; flattens backwardation |
| Consumer panic buying | After supply shocks, when buyers are underhedged | Front and back rally together; whole curve shifts up |
| Storage plays | When contango covers storage and financing | Buy front, sell back; caps contango at full carry |
| Long-only index rolls | Monthly roll window | Weakens the front spread during the window |

Producer hedging is **pro-cyclical**: it sells strength. That is why long-dated prices are far less volatile than prompt prices, and why a supply-shock rally lifts the front much more than the back.

### Options flows

- Producers often hedge with **collars** (buy puts, sell calls). Dealers on the other side end up **short downside puts**, which they hedge by selling futures as prices fall, so selloffs accelerate. They are also **long upside calls**, which they hedge by selling into rallies, so rallies are dampened.
- The result is put-heavy skew in producer-dominated markets and fast, air-pocket selloffs. **Mexico's annual oil hedge** is the classic example: a very large put purchase that dealers hedge in the deferred months.

### By market

- **Crude oil:** US shale producers hedge heavily 12–24 months out, historically anchoring long-dated WTI near the cost of new shale supply. Airlines are the main consumer hedgers, but irregular. When producers are underhedged, rallies can lift the back end hard.
- **Natural gas:** producers sell the 12-month strip; utilities and local distribution companies buy winter months ahead, supporting the summer–winter spread.
- **Grains:** farmer selling drives harvest pressure on new-crop contracts and weaker basis. Farmers holding grain keep the old-crop/new-crop spread firm. Elevators carry most of the commercial short.
- **Metals:** most miners no longer hedge. The unwinding of gold producers' hedge books in the 2000s removed a major seller from the back of the curve. Fabricators and cable makers are the main back-end buyers.
- **Softs:** origin selling caps rallies (Brazilian coffee farmers on a weak BRL, West African cocoa boards selling forward). A board defaulting on forward sales can invert the curve fast.

### Reading it in the data

1. **CFTC COT:** Producer/Merchant shorts and longs show hedging intensity; Swap Dealer positions show OTC hedges passed through to futures.
2. **Deferred-month open interest:** rising OI on rallies means producers are hedging.
3. **Option skew:** deepening put skew in deferred months means producers are buying protection.
4. **Company hedge books** (earnings disclosures): low hedge ratios leave the back end vulnerable to a squeeze.
5. **Curve vs inventories:** when the curve shape doesn't match what inventories imply, flows are usually the reason.

> **Rules of thumb:** backwardation plus low inventories is a genuine physical shortage. A back end that falls during a front-led rally is hedging, not bearish fundamentals. When producers stop hedging (low prices, depleted hedge books), the back end tends to be well supported.

## Desk notes

> Add your own observations here. Anything you write in this file appears in the PDF on the next build.
