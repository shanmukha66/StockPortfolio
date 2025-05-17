
# 📊 Stock Portfolio Manager

## 🔍 Overview
The Smart Stock Portfolio Manager is a Python-based desktop application designed to help users make informed investment decisions. With a minimum investment of $5000 USD, users can select from various investment strategies and receive intelligent portfolio allocations based on historical performance, risk metrics, and market data. The application provides real-time portfolio tracking, performance visualization, and detailed stock analytics.

## 👥 Team Members

Rishabh Malviya SJSU ID:018190419

Shanmukha Manoj Kakani SJSU ID:018195645

Vineela Mukkamala(018217992)

Adityaraj Kaushik (017631471)



## 🚀 Features

### 1. Investment Strategies:
- **Ethical Investing**: Focus on companies with strong ESG practices (AAPL, ADBE, NSRGY)
- **Growth Investing**: Target high-growth potential companies (TSLA, NVDA, AMZN)
- **Index Investing**: Track market indexes through ETFs (VTI, IXUS, ILTB)
- **Quality Investing**: Established companies with strong fundamentals (MSFT, JNJ, V)
- **Value Investing**: Undervalued companies with solid foundations (BRK-B, JPM, PG)

### 2. Smart Portfolio Allocation:
- Intelligent fund distribution based on historical performance
- Risk-adjusted returns calculation using Sharpe Ratio
- Market cap and volume trend consideration
- Minimum allocation thresholds for diversification

### 3. Real-Time Analytics:
- Live stock price updates via yfinance API
- Dynamic portfolio value calculation
- 5-day historical performance tracking
- Detailed stock metrics and market data

### 4. Interactive Visualization:
- Portfolio distribution pie charts
- Historical performance line graphs
- Trading data tables with 5-day history
- Comprehensive stock information display

### 5. Additional Features:
- Multiple strategy combination support
- Risk metrics analysis
- Market trend visualization
- Detailed stock fundamentals

## 💻 Technologies Used
- **Python**: Core application development
- **PyQt5**: GUI framework
- **yfinance**: Real-time stock data API
- **pandas**: Data manipulation and analysis
- **matplotlib**: Data visualization
- **numpy**: Numerical computations

## ⚙️ How It Works

### 1. Input:
- Enter investment amount (minimum $5000)
- Select up to two investment strategies

### 2. Processing:
- Fetches real-time stock data
- Calculates smart allocation based on multiple factors
- Generates portfolio metrics and visualizations

### 3. Output:
- Detailed portfolio breakdown
- Interactive charts and graphs
- Real-time value updates
- Historical performance tracking

## 🛠️ Setup Instructions

### Prerequisites:
- Python 3.8+
- Required libraries:
   PyQt5,yfinance,pandas,matplotlib,numpy



### Running the Application


clone the repository or unzip it
go the the folder
use the following commands on terminal : 
1. python3 -m venv venv
2. source venv/bin/activate
3. pip install -r requirements.txt
4. python main.py

