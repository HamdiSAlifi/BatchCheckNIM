\# BATCH CHECK NIM FROM PDDIKTI



This project is created due to cross check every name of my friends and seniors in one of some committee which I join into. Why cross check you'd say? Basically it is because human error, and I don't want to blame my colleague if there are some error in the database and I know it. I would rather to blame the wrong to the government because their lack of consistency. So that I use some scratch API that actually not so legal but whatever, do it with your own risk.



\## Requirements



* Python 3.4
* pddiktipy



\## Installation 



1. Clone the repository

```bash

  git clone https://github.com/HamdiSAlifi/BatchCheckNIM.git
  cd <your-repo>

```



2\. Install Dependencies

```bash

  pip install pddiktipy

```



\## Usage

```bash

  python checkBatch.py

```



\## Configuration

| Variable | Description | Default |

|----------|-------------|---------|

| `TARGET\_UNIVERSITY` | University to filter | `andalas` |

| `TARGET\_MAJOR` | Major to filter | `informat` |



you could change the name of the university and the major to filter out



\## Notes



* Make sure `pddiktipy` is installed before running
* Data is fetched from PDDIKTI API



\## Author



Hamdi

* GitHub: https://github.com/HamdiSAlifi

