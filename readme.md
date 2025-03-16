# Options Chain Analytics

A modern web application for downloading and analyzing options chain data for any publicly traded company. Built with Python, Dash, and yfinance.

![Options Chain Analytics Interface](assets/preview.png)

## 🚀 Features

- **Real-time Options Data**: Fetch current options chain data for any publicly traded stock
- **Flexible Download Options**: Choose between Calls, Puts, or both
- **Custom Timeframes**: Adjust lookback period for historical analysis
- **Modern UI**: Clean, professional interface with intuitive controls
- **Instant CSV Export**: Download data in CSV format for further analysis

## 📋 Prerequisites

Before running the application, ensure you have Python 3.8+ installed. The application requires the following packages:

```bash
numpy
pandas
dash
yfinance
```

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Option-Chain-Download-Project.git
cd Option-Chain-Download-Project
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## 🚀 Usage

1. Start the application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:8050
```

3. Enter a stock ticker (e.g., AAPL, MSFT)
4. Select option type (Calls, Puts, or Both)
5. Set your desired lookback period
6. Click "Download Options Data"

## 📊 Data Format

The downloaded CSV file includes the following data for each option:

- Contract Symbol
- Strike Price
- Last Price
- Bid/Ask
- Volume
- Open Interest
- Implied Volatility
- And more...

## 🛡️ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📬 Contact

Your Name - [Your Email]

Project Link: [https://github.com/yourusername/Option-Chain-Download-Project](https://github.com/yourusername/Option-Chain-Download-Project)

##  Acknowledgments

- [yfinance](https://github.com/ranaroussi/yfinance) for providing the options data API
- [Dash](https://dash.plotly.com/) for the web framework
- [Font Awesome](https://fontawesome.com/) for the icons
