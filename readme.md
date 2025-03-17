# Financial Data Analytics Dashboard v2.0

## Overview
A powerful web-based dashboard for downloading and analyzing financial market data, including stocks, options chains, and futures contracts. Built with Python and Dash, this application provides an intuitive interface for accessing market data through Yahoo Finance.

## New Features in v2.0
- **Multi-Page Layout**: Organized interface with dedicated pages for stocks, options, and futures data
- **Enhanced UI/UX**: 
  - Modern, responsive design with a consistent color scheme
  - Intuitive navigation bar
  - Professional hero sections for each page
  - Interactive form controls with validation
- **Comprehensive Futures Reference**: 
  - Collapsible sections for different futures categories
  - Easy-to-reference symbols for various market segments
  - Categories include:
    - Energy Futures
    - Metal Futures
    - Agricultural Futures
    - Index Futures
    - Currency Futures
    - Interest Rate Futures

## Features

### Stock Price Analytics
- Download historical stock price data
- Flexible time period selection (1 month to 5 years)
- Complete OHLCV (Open, High, Low, Close, Volume) data
- CSV format export

### Options Chain Analytics
- Download options chain data for any publicly traded company
- Filter by calls, puts, or both
- Customizable lookback period
- Comprehensive options data including strikes, expiration dates, and Greeks

### Futures Market Analytics
- Download futures contract data
- Extensive symbol reference guide
- Support for major futures markets:
  - Energy (CL=F, BZ=F, NG=F, etc.)
  - Metals (GC=F, SI=F, HG=F, etc.)
  - Agriculture (ZC=F, ZW=F, ZS=F, etc.)
  - Indices (ES=F, NQ=F, YM=F, etc.)
  - Currencies (6E=F, 6J=F, 6B=F, etc.)
  - Interest Rates (ZN=F, ZF=F, ZT=F, etc.)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/financial-data-dashboard.git
cd financial-data-dashboard
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python Baccarat.py
```

## Dependencies
- dash==2.14.0
- pandas==2.1.0
- yfinance==0.2.28
- numpy==1.24.3
- plotly==5.17.0

## Usage

1. Navigate to `http://localhost:8050` in your web browser
2. Select the desired data type (Stocks, Options, or Futures)
3. Enter the required symbol and parameters
4. Click the download button to receive your data in CSV format

## Error Handling
- Input validation for all fields
- Clear error messages for invalid symbols
- Graceful handling of API failures
- User-friendly feedback messages

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- Data provided by Yahoo Finance
- Built with Plotly Dash
- Icons from Font Awesome

## Future Enhancements
- Real-time data streaming
- Interactive charts and visualizations
- Additional data sources
- Portfolio tracking functionality
- Advanced analytics tools

## Contact
For questions and support, please open an issue in the GitHub repository.

---
*Note: This project is for educational and research purposes only. Please ensure compliance with all relevant financial data usage terms and conditions.* 
