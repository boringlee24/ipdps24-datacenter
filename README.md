# Interpretable Analysis of Production GPU Clusters Monitoring Data via Association Rule Mining

Paper at 2024 IEEE International Parallel and Distributed Processing Symposium (IPDPS'24)

## Setup

This repository requires Python 3.

To install required Python package, run
```
pip install -r requirements.txt
```

## Installing the package

The rule mining utilities are in ``mining_utils`` and can be installed with

```
pip install -e .
```

Then, in Python, it can be imported as 
    
```python
from mining_utils import mining_utils
```

## Association rule mining examples

The examples can be found in the ``example`` directory. 

### Dataset

We have converted the original dataset into transaction database format, as shown in ``example/transaction_*.csv``. Make sure ``git lfs`` is installed to download these transactions. 

Each row represents a transaction, corresponding to a job from the cluter trace. Then the row content represents if a item appears in the transaction (job), e.g., frequent user, low GPU utilization, job failure...

### Analyze the transactions

The two ``.ipynb`` examples show the end-to-end process from the Microsoft Philly trace and MIT Supercloud trace. 

The mined rules can be found in the ``example/rules`` directory.