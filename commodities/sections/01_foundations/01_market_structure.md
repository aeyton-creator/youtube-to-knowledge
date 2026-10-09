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

## Desk notes

> Add your own observations here. Anything you write in this file appears in the PDF on the next build.
