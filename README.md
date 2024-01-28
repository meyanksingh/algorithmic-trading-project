# Algorithmic Trading Project

## Introduction

This Python-based algorithmic trading project is designed for non-directional trading strategies. It seamlessly integrates with the Shoonya API for market data, enabling the implementation of a strangle trading strategy. The project automates order placement and provides stop-loss handling. Additionally, it offers monitoring functionality for tracking performance.

## Project Structure

- **main.py**: The primary script for running the algorithm, implementing trading strategies, and monitoring execution.
- **core.py**: Contains core functions for interacting with the Shoonya API, placing orders, and managing trade-related tasks.
- **monitor.py**: A module for real-time monitoring of performance metrics.
- **cred.py**: Safely stores API credentials and sensitive information (keep this file secure).
- **requirements.txt**: Lists the required Python libraries for easy installation.

## Features

- **Non-Directional Trading**: Implement non-directional trading strategies that can profit from market volatility regardless of the price direction.

- **Shoonya API Integration**: Seamlessly interact with the Shoonya API for accessing real-time market data, including stock prices and index information.

- **Strangle Trading Strategy**: Implement the strangle trading strategy, a popular non-directional options strategy involving both call (CE) and put (PE) options.

- **Automated Order Placement**: Automate the placement of strangle orders based on your specified parameters, including quantity, strike prices, and more.

- **Stop-Loss Handling**: Incorporate stop-loss orders to manage risk and protect your positions from unfavorable market movements.

- **Performance Monitoring**: Utilize the monitoring functionality to track the performance of your trading strategy in real-time.

## Usage (main.py)

### Running the Algorithm

To execute the algorithm, run the `main.py` script. It performs the following steps:

1. Logs in to the Shoonya API with your credentials.
2. Fetches live index information and calculates strike prices.
3. Places strangle orders based on specified parameters.
4. Checks order statuses and places stop-loss orders.
5. Monitors the algorithm's execution.

### Configuration

- `QTY`: Quantity of options to trade.
- `SL`: Stop-loss value.

## Monitoring (monitor.py)

The `monitor.py` module provides real-time monitoring of the trading algorithm's performance. It includes:

- Real-time data visualization.
- Alerts and notifications for critical events.
- Logging and analysis of trade-related information.
- Risk management features to protect capital.

## Contributing

Feel free to contribute to this project by opening issues, providing feedback, or submitting pull requests. Your contributions are welcome and appreciated!

## License

This project is licensed under the MIT License.

## Contact


- LinkedIn: [Meyank Singh](https://www.linkedin.com/in/meyank-singh)

---
