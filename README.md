# Crypto Live Data Fetcher and Google Sheets Updater

## Introduction

This project fetches cryptocurrency data from the CoinGecko API and updates a Google Sheet with the latest data every 5 minutes. It uses Python and several libraries including `requests`, `pandas`, `gspread`, and `google-auth`.

---

## Requirements

- **Python 3.x**
- **Python Libraries**:
  - `requests`
  - `pandas`
  - `gspread`
  - `google-auth`
- **Google Cloud service account JSON key file**

---

## Setup

1. **Install the required libraries**:
   ```bash
   pip install requests pandas gspread google-auth
   ```

2. **Obtain a Google Cloud service account JSON key file**:
   - Save it in your project directory.

3. **Update the path to the JSON key file**:
   - Modify the path in the `authenticate_gsheet` function to point to your JSON key file.

---

## Usage

Run the script to start fetching data and updating the Google Sheet every 5 minutes:

```bash
python crypto.py
```

---

## Code Explanation

### `fetch_crypto_data`
Fetches cryptocurrency data from the CoinGecko API.

### `authenticate_gsheet`
Authenticates a Google Sheets client using a service account JSON key file.

### `update_gsheet`
Updates the specified Google Sheet with the provided DataFrame.

### Main Loop
Continuously fetches data and updates the Google Sheet every 5 minutes.

---

## License

This project is licensed under the **MIT License**.
