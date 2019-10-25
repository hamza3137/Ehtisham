@echo off

echo running cutting bleeder .....

python cutting_bleeder.py %1

echo running negative_bleeder .....

python negative_bleeder.py %1

echo running bid optimization ......

python ppc_bid_optimizations_all.py %1

echo running budget optimization ...........

python ppc_budget_optimization.py %1

@echo on