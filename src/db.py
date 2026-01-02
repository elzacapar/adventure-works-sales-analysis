"""
Database helpers for connecting to Microsoft SQL Server (AdventureWorks).

This module is intentionally small:
- Reads connection info from environment variables
- Exposes `read_sql()` to fetch a query into a pandas DataFrame
"""

from __future__ import annotations

import os
from urllib.parse import quote_plus

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine


def make_engine():
    """Create a SQLAlchemy engine for SQL Server using Windows authentication."""
    load_dotenv()

    server = os.getenv("SQL_SERVER", r"localhost\SQL2025")
    database = os.getenv("SQL_DATABASE", "AdventureWorks2025")

    odbc_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={server};"
        f"DATABASE={database};"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )

    return create_engine("mssql+pyodbc:///?odbc_connect=" + quote_plus(odbc_str))


# Reuse one engine across the notebook run
ENGINE = make_engine()


def read_sql(query: str, params: dict | None = None) -> pd.DataFrame:
    """Run a SQL query and return the result as a DataFrame."""
    return pd.read_sql(query, ENGINE, params=params)