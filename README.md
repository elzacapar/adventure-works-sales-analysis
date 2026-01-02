# AdventureWorks Sales Analysis

This project analyzes the **AdventureWorks** sample database using **SQL Server + Python (pandas) + matplotlib**.
The notebook answers 7 core business questions and then adds a **Product Portfolio Deep Dive (option B)**.

## What’s inside

- `notebooks/sales_analysis.ipynb` – main analysis notebook (SQL → DataFrame → visualization → insight)
- `src/db.py` – database connection + `read_sql()` helper
- `src/plot.py` – reusable plotting helpers
- `requirements.txt` – Python dependencies

## How to run

### 1) Create a `.env` file (project root)
Create a file named `.env` next to `requirements.txt`:

```env
SQL_SERVER=localhost\SQL2025
SQL_DATABASE=AdventureWorks2025
```

> Tip: the server name must match what you see in SSMS (Object Explorer).

### 2) Install dependencies
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt
```

### 3) Run the notebook
Open VS Code → open the project folder → open:
`notebooks/sales_analysis.ipynb` → Run All.

## Notes for reviewers
- Revenue is computed consistently as:
  `SUM(UnitPrice * OrderQty * (1 - UnitPriceDiscount))`
- In the product portfolio deep dive, product profitability is estimated using
  `StandardCost` from `Production.Product` as a cost proxy, due to the absence of detailed cost data.

## License
MIT