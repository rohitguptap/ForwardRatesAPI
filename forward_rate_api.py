import sqlite3
import pandas as pd
from fastapi import FastAPI, HTTPException
import uvicorn

class ForwardRateAPI:
    def __init__(self):
        self.app = FastAPI()
        self.conn = sqlite3.connect('forward_rates.db')

        # forward_rates API
        @self.app.post('/forward_rates/')
        async def forward_rates(payload: dict):
            # Validate payload
            required_keys = ['maturity_date', 'reference_rate', 'rate_floor', 'rate_ceiling', 'rate_spread']
            if not all(key in payload for key in required_keys):
                raise HTTPException(status_code=400, detail='Invalid payload')

            # Validate maturity date & reference_rate
            try:
                maturity_date = pd.to_datetime(payload['maturity_date']).date()
            except ValueError:
                raise HTTPException(status_code=400, detail='Invalid maturity date format')

            if payload['reference_rate'] == 'SOFR':
                rate_column = 'OneMonthSOFR'
            else:
                raise HTTPException(status_code=400, detail='Unsupported reference rate')

            # Load rates from the database, filtering up to maturity date
            query = "SELECT * FROM ForwardCurve WHERE ResetDate <= ?"
            rates = pd.read_sql_query(query, self.conn, params=[maturity_date])

            # Convert rate column to numeric
            rates[rate_column] = pd.to_numeric(rates[rate_column], errors='coerce')

            # Filter rows with valid dates and rates only
            rates = rates.dropna(subset=['ResetDate', rate_column])

            # Apply rate floor, ceiling, and spread, then format the output
            rate_curve = []
            for _, row in rates.iterrows():
                rate = row[rate_column] / 100  # Convert percentage by dividing by 100 for rate
                rate = max(payload['rate_floor'], min(rate, payload['rate_ceiling']))  # Apply floor and ceiling
                rate += payload['rate_spread']  # Add spread

                rate_curve.append({
                    'date': row['ResetDate'],
                    'rate': round(rate, 4)
                })

            return rate_curve

if __name__ == "__main__":
    api = ForwardRateAPI()
    uvicorn.run(api.app, host='0.0.0.0', port=8000, log_level="info")
