# Theory of Storage

> **Source:** summarised from Ilia Bouchouev, *An Introduction to the Theory of Storage*, CQL Working Paper No. 3 (Pentathlon Investments and CQL, November 2026). The text below is a paraphrase; see the original paper for its figures and full argument. The final "Trading takeaways" section is desk commentary, not from the paper.

The theory of storage explains how inventories drive the gap between spot and futures prices. The paper traces it from the carry trade, through the classic equilibrium models, to treating prices as derivatives of inventories, and ends with how banks use it to forecast oil.

## Carry trade and convenience yield

- **Carry arbitrage:** a futures price can't exceed spot by more than the cost of carry. Otherwise a trader borrows money, buys and stores the physical, sells futures, and delivers at expiry for a riskless profit. In absolute terms: **F ≤ S + R + U** (R = borrowing cost, U = storage cost).
- **Why it is only an inequality for commodities:** in stocks and bonds the reverse trade also works (borrow the asset, sell it, buy futures), which makes the relationship an equality. For commodities that reverse carry fails when inventories are depleted, because there is no physical to borrow.
- **Kaldor (1939)** closed the gap with the **convenience yield**, Y: **F = S + R + U − Y**. It is the benefit of holding the physical commodity rather than a futures claim, roughly the commodity's equivalent of a dividend yield. It moves constantly with physical supply and demand.
- **Spot decomposition:** **S = F + (S − F) = F + (Y − R − U)**. The long-dated futures price is fairly stable and anchored by the marginal cost of production. The spot–futures spread (the basis) is the volatile part, and it is driven mainly by convenience yield, which in turn depends on inventories.
- **Low inventories** → high convenience yield → spot above futures (**backwardation**).
- **High inventories** → convenience yield near zero → spread set by storage and financing costs → spot below futures (**contango**).
- **Inconvenience yield** (Bouchouev, 2012): in super-contango, when storage is full, holding the physical becomes a burden. This matters most for energy, where storage capacity is limited.

## Working's storage curve

- Holbrook Working (1930s–1940s, mainly grain markets) documented empirically that the spot–futures spread varies **inversely with inventories**.
- The curve is strongly **non-linear at low inventories**. At a **stock-out** (zero inventories) both the spot price and the spread can, in principle, rise without limit.
- At the other extreme, **tank tops** (storage full), the curve bends more gently.
- Early research focused on stock-outs because ags and metals are easy to store and shortages hurt the wider economy. Tank tops mattered later, for energy.
- *Sign convention:* Working used futures minus spot. The paper, like modern energy markets, uses spot minus futures, so a positive spread means a high convenience yield.

## The canonical theory of storage

Formal models started with **Gustafson (1958)**, motivated by US efforts to manage farm reserves and dampen price volatility. The most widely used version builds on **Deaton and Laroque (1992)**. Key references: Williams and Wright (1991), Routledge, Seppi and Spatt (2000), Pirrong (2012).

- **Two sources of demand:** consumption, which follows the inverse demand curve, and storage, which follows carry economics. Storing today cuts today's supply and adds to tomorrow's, so supply and demand become **intertemporal**.
- **The Robinson Crusoe problem:** allocate what's available now between eating today and saving for tomorrow, when tomorrow's harvest is uncertain. With supply Z, demand D and carry-out inventory x:
  - availability today: **a(t) = Z(t) + x(t − dt) = D(t) + x(t)**
  - availability tomorrow: **a(t + dt) = Z(t + dt) + a(t) − D(t)**
- **Price–inventory feedback loop:** the inverse demand curve links each period's price to its availability. The carry trade links prices across periods while stocks exist, and the supply–demand identity links availability across periods. Prices and inventories must therefore be solved together, by stochastic dynamic programming over many periods.
- **Two regions in the solution:**
  - **Stock-out region (no inventories):** price is set purely by immediate supply and demand.
  - **Investment region (inventories available):** price is set by carry arbitrage. Storage demand lifts and flattens the demand curve, so prices become much less sensitive to inventories.
- **Key implication:** while inventories exist, forward prices are driven mainly by financial arbitrage, not by forecasts of future supply and demand.

### Why the canonical model struggles in practice (especially oil)

1. **Sensitivity to the demand curve:** the solution depends heavily on its shape. For oil, short-run demand is nearly inelastic (the curve is almost vertical), so large price moves are needed to shift consumption even slightly.
2. **Data:** global supply data are incomplete, late and revised, and global demand is mostly inferred from supply and stock changes. **Inventories are the only key fundamental that can be measured directly**, which argues for modelling inventories directly.

## Prices as derivatives of stochastic inventories

Bouchouev's alternative (from *Virtual Barrels*, 2023) treats **inventories as a stochastic state variable** and commodity prices as **derivatives of inventories**.

- Prices then satisfy a **Black–Scholes-type equation with respect to inventories**. The paper leaves out the market-price-of-risk term needed for a non-tradable state variable.
- **Boundary conditions come from the two extremes:**
  - **Stock-out:** as inventories approach zero, spot price approaches +∞, as shorts with nothing to deliver bid without limit.
  - **Tank tops:** as storage fills, price approaches −∞, as longs with nowhere to store must sell at ever lower prices. The real-world example is **WTI at about −$40/bbl in April 2020**.
- These boundaries are rarely reached, but like boundaries in other dynamic systems they **shape behaviour throughout the interior**.
- Modelling the boundaries as **Dirac delta** impulses turns the pricing equation into the **Kolmogorov (diffusion) equation** for a probability density, a link that goes back to **Bachelier (1900)**.
- **Result:** the spot–futures spread equals the **probability-weighted value of a squeeze at either boundary**, an upside squeeze (stock-out) or a downside squeeze (tank tops). A simple formula links the two.
- **Example:** the paper calibrates the model to WTI using Cushing inventories, modelled as a mean-reverting (Ornstein–Uhlenbeck) process, with the **WTI M1–M2 spread** as the tradable proxy for spot minus futures. It highlights the **2020 tank-top squeeze** and the **2026 stock-out squeeze** in that spread.

## How banks forecast oil prices

The standard bank framework applies storage theory directly.

1. **Split spot into two parts:** the long-dated futures price plus the spot–futures spread.
2. **Long-dated price ≈ marginal cost of production.** Over the past decade, five-year WTI futures closely tracked **shale breakeven costs** (Dallas Fed survey). The exception is periods of unusual hedging pressure (see *Producer and consumer flows and the curve* in Market Structure).
3. **Spread as a function of inventories:** regress the **one-year Brent spread** on **OECD inventories measured as the gap from their five-year average**. The paper finds a long-run correlation of about **−0.60**.
4. **The forecast** combines expected inventory changes, from analysts' supply–demand balance models ("barrel counters"), with the regression slope.
5. **Caveat:** the lookback period and the way inventories are scaled can change the slope materially, and they are sometimes chosen to produce the answer someone wants.

### When the framework breaks: the geopolitical premium

- The gap between market spreads and what the inventory model implies is usually labelled a **geopolitical risk premium**.
- The model tracked well apart from **2022** (Russia–Ukraine) and **2026** (the war in Iran). In 2026 the premium swung between **about $5 and $40/bbl**.
- In 2026 the premium was linked anecdotally to **hedge-fund positioning**. China's sharp cut in imports initially lowered it, and a **surge in freight costs** later raised it again.
- **The rolling correlation between Brent spreads and OECD inventories is now close to zero.** If the slope is flat, inventory forecasts don't translate into price forecasts, which raises the question of what barrel counting is still worth. The paper leaves open whether the framework survives or needs replacing.

## Trading takeaways

*Desk commentary, not from the paper.*

- **Think in distance to the boundaries, not the inventory level:** a front spread behaves like an option on inventories. It is convex near operational minimums (for example, Cushing tank bottoms) and near full capacity, and fairly insensitive in between.
- **Squeeze risk is asymmetric by market:** stock-out risk dominates for ags and metals, which are easy to store. Energy carries both tails, because storage capacity is finite.
- **The back of the curve is a separate problem:** it is anchored by marginal cost and moved by hedging flows. The front is where inventories matter.
- **Monitor the model, not just the market:** track the rolling correlation and the residual between Brent spreads and OECD stocks. A large or persistent residual usually means positioning or risk premium, so cross-check with the COT report, options skew and freight.
- **Be sceptical of bank forecasts built on an inventory regression** while that correlation is near zero.

## Further reading

- Bouchouev, I. (2012). Inconvenience yield, or the theory of normal contango. *Quantitative Finance*.
- Bouchouev, I. (2023). *Virtual Barrels: Quantitative Trading in the Oil Market*. Springer.
- Deaton, A. and Laroque, G. (1992). On the behavior of commodity prices. *Review of Economic Studies*.
- Kaldor, N. (1939). Speculation and economic stability. *Review of Economic Studies*.
- Pirrong, C. (2012). *Commodity Price Dynamics: A Structural Approach*. Cambridge University Press.
- Routledge, B., Seppi, D. and Spatt, C. (2000). Equilibrium forward curves for commodities. *Journal of Finance*.
- Williams, J. and Wright, B. (1991). *Storage and Commodity Markets*. Cambridge University Press.
- Working, H. (1948, 1949). Theory of the inverse carrying charge; The theory of price of storage.

## Desk notes

> Add your own observations here.
