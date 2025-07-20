# yahtzee simulation

a python simulation to test different yahtzee playing strategies and determine which ones work best

project by: Tyler Netek & Rishi Karia

## overview

this project simulates thousands of yahtzee games using different strategies to determine which approach yields the highest scores - the simulation collects comprehensive statistics on each strategy's performance including average scores consistency and success rates for specific categories

install dependencies with:
```bash
pipenv shell
pip3 install matplotlib numpy
```

## implemented strategies

1.) **greedy upper section** - 
focuses on maximizing upper section scores to get the 35-point bonus

2.) **hybrid probability** - 
balances between upper and lower section opportunities
3.) **yahtzee or bust** - 
high-risk, high-reward strategy focused on getting yahtzees
4.) **lower section priority** - 
prioritizes high-value categories in the lower section
5.) **adaptive strategy** - 
changes strategy based on game phase (early, mid, late game)

## files

- `constant.py` - game constants and category definitions
- `logic.py` - core game mechanics and scoring functions
- `strats.py` - strategy implementations
- `util.py` - shared utility functions
- `sim.py` - main simulation runner with statistical analysis
- `analyze.py` - additional analysis tools for strategy comparison
- `visualize.py` - detailed visualization for individual strategies

### how to run
run the main simulation with all strategies:

```bash
python3 sim.py
```

this will simulate 10,000 games for each strategy and output comprehensive statistics.

### advanced analysis

for more detailed analysis and comparisons:

```bash
python3 analyze.py
```

this tool provides:
- head to head comparisons between strategies
- consistency analysis for individual strategies
- tournament mode where each strategy plays against all others

### strategy visualization

for detailed visualization of a specific strategy:

```bash
python3 visualize.py
```

## visualization

the simulation generates visualization files:
- `score_distribution.png` - histogram of score distributions for each strategy
- `strategy_comparison.png` - bar chart comparing key metrics across strategies
- `tournament_results.png` - heatmap of head-to-head win rates (when using analyze.py)
- `[strategy]_analysis.png` - detailed analysis of individual strategies

output will be populated in the output directory, corresponding to the inner directories titles respectively
