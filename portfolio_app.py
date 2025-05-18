#!/usr/bin/env python3

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QComboBox, QPushButton, QLineEdit, QMessageBox,
                           QTabWidget, QTableWidget, QTableWidgetItem, QScrollArea)
from PyQt5.QtCore import Qt
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import time
from functools import lru_cache

class StockPortfolioApp(QTabWidget):
    def __init__(self):
        super().__init__()
        self.strategy_mappings = {
            'Ethical Investing': ['AAPL', 'ADBE', 'NSRGY'],
            'Growth Investing': ['TSLA', 'NVDA', 'AMZN'],
            'Index Investing': ['VTI', 'IXUS', 'ILTB'],
            'Quality Investing': ['MSFT', 'JNJ', 'V'],
            'Value Investing': ['BRK-B', 'JPM', 'PG']
        }
        
        # Create tabs
        self.input_tab = QWidget()
        self.charts_tab = QWidget()
        self.details_tab = QWidget()
        
        self.addTab(self.input_tab, "Portfolio Input")
        self.addTab(self.charts_tab, "Charts")
        self.addTab(self.details_tab, "Stock Details")
        
        self.initUI()
        
    def initUI(self):
        # Setup Input Tab
        input_layout = QVBoxLayout(self.input_tab)
        
        # Investment Amount Input
        amount_layout = QHBoxLayout()
        amount_label = QLabel('Investment Amount ($):')
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText('Enter amount (min $5000)')
        amount_layout.addWidget(amount_label)
        amount_layout.addWidget(self.amount_input)
        input_layout.addLayout(amount_layout)
        
        # Strategy Selection
        strategy_layout = QHBoxLayout()
        strategy_label = QLabel('Select Strategies:')
        self.strategy1 = QComboBox()
        self.strategy2 = QComboBox()
        
        strategies = list(self.strategy_mappings.keys())
        self.strategy1.addItems(['Select Strategy'] + strategies)
        self.strategy2.addItems(['None'] + strategies)
        
        strategy_layout.addWidget(strategy_label)
        strategy_layout.addWidget(self.strategy1)
        strategy_layout.addWidget(self.strategy2)
        input_layout.addLayout(strategy_layout)
        
        # Calculate Button
        self.calc_button = QPushButton('Calculate Portfolio')
        self.calc_button.clicked.connect(self.calculate_portfolio)
        input_layout.addWidget(self.calc_button)
        
        # Results Label with Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        self.results_label = QLabel('')
        self.results_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.results_label.setWordWrap(True)
        self.results_label.setStyleSheet("QLabel { background-color: #0a0a0a; padding: 10px; }")
        scroll_layout.addWidget(self.results_label)
        
        scroll.setWidget(scroll_content)
        input_layout.addWidget(scroll)
        
        # Setup Charts Tab
        charts_layout = QVBoxLayout(self.charts_tab)
        
        self.pie_figure = Figure(figsize=(6, 4))
        self.line_figure = Figure(figsize=(6, 4))
        
        self.pie_canvas = FigureCanvas(self.pie_figure)
        self.line_canvas = FigureCanvas(self.line_figure)
        
        charts_layout.addWidget(QLabel('Portfolio Distribution'))
        charts_layout.addWidget(self.pie_canvas)
        charts_layout.addWidget(QLabel('Historical Performance'))
        charts_layout.addWidget(self.line_canvas)
        
        # Setup Details Tab
        details_layout = QVBoxLayout(self.details_tab)
        
        # Create tables for daily data and stock info
        self.daily_table = QTableWidget()
        self.info_table = QTableWidget()
        
        details_layout.addWidget(QLabel('Last 5 Days Trading Data'))
        details_layout.addWidget(self.daily_table)
        details_layout.addWidget(QLabel('Stock Information'))
        details_layout.addWidget(self.info_table)
        
        # Initially disable the Charts and Details tabs
        self.setTabEnabled(1, False)
        self.setTabEnabled(2, False)
        
        # Set window properties
        self.setWindowTitle('Stock Portfolio Manager')
        self.setGeometry(100, 100, 1000, 800)

    def update_stock_details(self, stocks):
        # Set up daily data table
        self.daily_table.setRowCount(0)
        self.daily_table.setColumnCount(7)
        self.daily_table.setHorizontalHeaderLabels(
            ['Symbol', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        )
        
        # Set up info table
        self.info_table.setRowCount(0)
        self.info_table.setColumnCount(7)
        self.info_table.setHorizontalHeaderLabels(
            ['Symbol', 'Market Cap', 'P/E Ratio', 'Dividend Yield', '52W High', '52W Low', 'Avg Volume']
        )
        
        current_row = 0
        info_row = 0
        
        # Batch download 5-day history for all stocks
        stock_symbols = ' '.join(stocks)
        max_retries = 3
        for attempt in range(max_retries):
            try:
                hist_data = yf.download(stock_symbols, period='5d', group_by='ticker', threads=False)
                break
            except Exception as e:
                if 'Too Many Requests' in str(e) and attempt < max_retries - 1:
                    print(f"Rate limited. Retrying batch download after 5 seconds...")
                    time.sleep(5)
                else:
                    print(f"Failed to batch download: {str(e)}")
                    hist_data = None
        if hist_data is not None:
            for symbol in stocks:
                try:
                    if symbol in hist_data:
                        hist = hist_data[symbol]
                    else:
                        hist = hist_data
                    for index, row in hist.iterrows():
                        self.daily_table.insertRow(current_row)
                        self.daily_table.setItem(current_row, 0, QTableWidgetItem(symbol))
                        self.daily_table.setItem(current_row, 1, QTableWidgetItem(index.strftime('%Y-%m-%d')))
                        self.daily_table.setItem(current_row, 2, QTableWidgetItem(f"${row['Open']:.2f}"))
                        self.daily_table.setItem(current_row, 3, QTableWidgetItem(f"${row['High']:.2f}"))
                        self.daily_table.setItem(current_row, 4, QTableWidgetItem(f"${row['Low']:.2f}"))
                        self.daily_table.setItem(current_row, 5, QTableWidgetItem(f"${row['Close']:.2f}"))
                        self.daily_table.setItem(current_row, 6, QTableWidgetItem(f"{int(row['Volume']):,}"))
                        current_row += 1
                except Exception as e:
                    print(f"Error processing history for {symbol}: {str(e)}")
        
        # Stock info (still per-stock, but with retry)
        for symbol in stocks:
            for attempt in range(max_retries):
                try:
                    stock = yf.Ticker(symbol)
                    info = stock.info
                    self.info_table.insertRow(info_row)
                    self.info_table.setItem(info_row, 0, QTableWidgetItem(symbol))
                    self.info_table.setItem(info_row, 1, QTableWidgetItem(f"${info.get('marketCap', 0)/1e9:.2f}B"))
                    self.info_table.setItem(info_row, 2, QTableWidgetItem(f"{info.get('forwardPE', 'N/A')}"))
                    self.info_table.setItem(info_row, 3, QTableWidgetItem(f"{info.get('dividendYield', 0)*100:.2f}%"))
                    self.info_table.setItem(info_row, 4, QTableWidgetItem(f"${info.get('fiftyTwoWeekHigh', 0):.2f}"))
                    self.info_table.setItem(info_row, 5, QTableWidgetItem(f"${info.get('fiftyTwoWeekLow', 0):.2f}"))
                    self.info_table.setItem(info_row, 6, QTableWidgetItem(f"{info.get('averageVolume', 0):,}"))
                    info_row += 1
                    break
                except Exception as e:
                    if 'Too Many Requests' in str(e) and attempt < max_retries - 1:
                        print(f"Rate limited. Retrying info for {symbol} after 5 seconds...")
                        time.sleep(5)
                    else:
                        print(f"Error getting info for {symbol}: {str(e)}")
                        break
        
        self.daily_table.resizeColumnsToContents()
        self.info_table.resizeColumnsToContents()

    def calculate_smart_allocation(self, stocks, total_amount):
        stock_metrics = {}
        stock_symbols = ' '.join(stocks)
        max_retries = 3
        for attempt in range(max_retries):
            try:
                hist_data = yf.download(stock_symbols, period='1y', group_by='ticker', threads=False)
                break
            except Exception as e:
                if 'Too Many Requests' in str(e) and attempt < max_retries - 1:
                    print(f"Rate limited. Retrying batch download after 5 seconds...")
                    time.sleep(5)
                else:
                    print(f"Failed to batch download: {str(e)}")
                    hist_data = None
        for symbol in stocks:
            try:
                if hist_data is not None and symbol in hist_data:
                    hist = hist_data[symbol]
                else:
                    hist = hist_data
                # Check if hist is empty or too short
                if hist is None or hist.empty or len(hist['Close']) < 2:
                    print(f"Insufficient data for {symbol}, skipping metrics calculation.")
                    stock_metrics[symbol] = 0.1
                    continue
                returns = hist['Close'].pct_change()
                avg_return = returns.mean()
                volatility = returns.std()
                sharpe_ratio = (avg_return / volatility) if volatility != 0 else 0
                roi = (hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0]
                volume_trend = hist['Volume'].mean() / hist['Volume'].std() if hist['Volume'].std() != 0 else 0
                score = (
                    0.3 * sharpe_ratio +
                    0.3 * roi +
                    0.2 * avg_return +
                    0.2 * volume_trend
                )
                stock_metrics[symbol] = max(score, 0.1)
            except Exception as e:
                print(f"Error calculating metrics for {symbol}: {str(e)}")
                stock_metrics[symbol] = 0.1
        total_score = sum(stock_metrics.values())
        allocations = {
            symbol: (score / total_score) * total_amount 
            for symbol, score in stock_metrics.items()
        }
        return allocations

    def calculate_portfolio(self):
        try:
            # Validate investment amount
            amount = float(self.amount_input.text())
            if amount < 5000:
                QMessageBox.warning(self, 'Invalid Input', 'Minimum investment amount is $5,000')
                return
                
            # Get selected strategies
            strategy1 = self.strategy1.currentText()
            strategy2 = self.strategy2.currentText()
            
            if strategy1 == 'Select Strategy':
                QMessageBox.warning(self, 'Invalid Input', 'Please select at least one strategy')
                return
                
            # Get stocks for selected strategies
            stocks = []
            if strategy1 != 'Select Strategy':
                stocks.extend(self.strategy_mappings[strategy1])
            if strategy2 != 'None':
                stocks.extend(self.strategy_mappings[strategy2])
            
            # Calculate smart allocation instead of equal distribution
            allocations = self.calculate_smart_allocation(stocks, amount)
            
            # Batch download current prices for all stocks
            stock_symbols = ' '.join(stocks)
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    current_data = yf.download(stock_symbols, period='1d', group_by='ticker', threads=False)
                    break
                except Exception as e:
                    if 'Too Many Requests' in str(e) and attempt < max_retries - 1:
                        print(f"Rate limited. Retrying batch download after 10 seconds...")
                        time.sleep(10)
                    else:
                        print(f"Failed to batch download: {str(e)}")
                        current_data = None
            portfolio = {}
            total_value = 0
            result_text = "Portfolio Summary:\n\n"
            values_for_pie = []
            labels_for_pie = []
            for symbol in stocks:
                try:
                    if current_data is not None and symbol in current_data:
                        hist = current_data[symbol]
                    else:
                        hist = current_data
                    if hist is None or hist.empty or 'Close' not in hist or len(hist['Close']) == 0:
                        print(f"No current price data for {symbol}, skipping.")
                        continue
                    current_price = hist['Close'].iloc[-1]
                    allocated_amount = allocations[symbol]
                    shares = allocated_amount / current_price
                    value = shares * current_price
                    portfolio[symbol] = {
                        'shares': shares,
                        'current_price': current_price,
                        'value': value,
                        'allocation_percentage': (allocated_amount / amount) * 100
                    }
                    total_value += value
                    result_text += f"{symbol}:\n"
                    result_text += f"Allocation: ${allocated_amount:.2f} ({portfolio[symbol]['allocation_percentage']:.1f}%)\n"
                    result_text += f"Shares: {shares:.2f}\n"
                    result_text += f"Current Price: ${current_price:.2f}\n"
                    result_text += f"Value: ${value:.2f}\n\n"
                    values_for_pie.append(value)
                    labels_for_pie.append(f"{symbol}\n({portfolio[symbol]['allocation_percentage']:.1f}%)")
                except Exception as e:
                    print(f"Error processing {symbol}: {str(e)}")
            # Batch download 5-day historical data for all stocks
            end_date = datetime.now()
            start_date = end_date - timedelta(days=5)
            for attempt in range(max_retries):
                try:
                    hist_data = yf.download(stock_symbols, start=start_date, end=end_date, group_by='ticker', threads=False)
                    break
                except Exception as e:
                    if 'Too Many Requests' in str(e) and attempt < max_retries - 1:
                        print(f"Rate limited. Retrying batch download after 10 seconds...")
                        time.sleep(10)
                    else:
                        print(f"Failed to batch download: {str(e)}")
                        hist_data = None
            historical_values = pd.Series(dtype='float64')
            for symbol in stocks:
                try:
                    if hist_data is not None and symbol in hist_data:
                        hist = hist_data[symbol]
                    else:
                        hist = hist_data
                    if hist is None or hist.empty or 'Close' not in hist or len(hist['Close']) == 0:
                        print(f"No historical data for {symbol}, skipping.")
                        continue
                    shares = portfolio[symbol]['shares'] if symbol in portfolio else 0
                    hist_values = hist['Close'] * shares
                    if historical_values.empty:
                        historical_values = hist_values
                    else:
                        historical_values = historical_values.add(hist_values, fill_value=0)
                except Exception as e:
                    print(f"Error processing historical data for {symbol}: {str(e)}")
            result_text += "5-Day Portfolio History:\n"
            for date, value in historical_values.items():
                result_text += f"{date.strftime('%Y-%m-%d')}: ${value:.2f}\n"
            self.results_label.setText(result_text)
            # Update charts
            self.update_charts(labels_for_pie, values_for_pie, historical_values)
            # Update stock details
            self.update_stock_details(stocks)
            # Enable and switch to Charts tab
            self.setTabEnabled(1, True)
            self.setTabEnabled(2, True)
            self.setCurrentIndex(1)
            
        except ValueError:
            QMessageBox.warning(self, 'Invalid Input', 'Please enter a valid investment amount')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'An error occurred: {str(e)}')

    def update_charts(self, labels, values, historical_data):
        # Clear previous charts
        self.pie_figure.clear()
        self.line_figure.clear()
        
        # Create pie chart
        ax1 = self.pie_figure.add_subplot(111)
        ax1.pie(values, labels=labels, autopct='%1.1f%%')
        ax1.set_title('Portfolio Distribution')
        
        # Create line chart
        ax2 = self.line_figure.add_subplot(111)
        historical_data.plot(ax=ax2)
        ax2.set_title('Portfolio Value Over Time')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Value ($)')
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
        self.line_figure.tight_layout()
        
        # Refresh canvases
        self.pie_canvas.draw()
        self.line_canvas.draw()