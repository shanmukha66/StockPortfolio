# main.py

from portfolio_app import StockPortfolioApp
from PyQt5.QtWidgets import QApplication
import sys

def main():
    app = QApplication(sys.argv)
    window = StockPortfolioApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()