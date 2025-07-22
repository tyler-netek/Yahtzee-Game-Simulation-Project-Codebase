# Yahtzee simulation

A python simulation to test different yahtzee playing strategies and determine which ones work best

Project by: Tyler Netek & Rishi Karia

## Overview

This project simulates thousands of yahtzee games using different strategies to determine which approach yields the highest scores - the simulation collects comprehensive statistics on each strategy's performance including average scores consistency and success rates for specific categories

Install dependencies with:
```bash
pipenv shell
pip3 install matplotlib numpy
```

## Implemented strategies

1.) **Greedy upper section** - 
Focuses on maximizing upper section scores to get the 35-point bonus

2.) **Hybrid probability** - 
Balances between upper and lower section opportunities

3.) **Yahtzee or bust** - 
High-risk, high-reward strategy focused on getting yahtzees

4.) **Lower section priority** - 
Prioritizes high-value categories in the lower section

5.) **Adaptive strategy** - 
Changes strategy based on game phase (early, mid, late game)

## Files

- `constant.py` - Game constants and category definitions
- `logic.py` - Core game mechanics and scoring functions
- `strats.py` - Strategy implementations
- `util.py` - Shared utility functions
- `sim.py` - Main simulation runner with statistical analysis
- `analyze.py` - Additional analysis tools for strategy comparison
- `visualize.py` - Detailed visualization for individual strategies

### How to run
Run the main simulation with all strategies:

```bash
python3 sim.py
```

This will simulate 10,000 games for each strategy and output comprehensive statistics.

### Advanced analysis

For more detailed analysis and comparisons:

```bash
python3 analyze.py
```

This tool provides:
- Head to head comparisons between strategies
- Consistency analysis for individual strategies
- Tournament mode where each strategy plays against all others

### Strategy visualization

For detailed visualization of a specific strategy:

```bash
python3 visualize.py
```

## Visualization

The simulation generates visualization files:
- `score_distribution.png` - Histogram of score distributions for each strategy
- `strategy_comparison.png` - Bar chart comparing key metrics across strategies
- `tournament_results.png` - Heatmap of head-to-head win rates (when using analyze.py)
- `[strategy]_analysis.png` - Detailed analysis of individual strategies

Output will be populated in the output directory, corresponding to the inner directories titles respectively