# Fantasy Football Draft League Analytics

A comprehensive analytics dashboard for Fantasy Premier League Draft competitions built with [Marimo](https://marimo.io/). This interactive web application provides in-depth statistical analysis and visualizations for your draft league performance, player statistics, and transfer activity.

## 🚀 Features

- **League Standings & Performance**: Interactive charts showing league standings progression across gameweeks
- **Gameweek Analysis**: Detailed breakdown of performance for specific gameweeks
- **Transfer Analytics**: Comprehensive transfer success rates and player demand analysis
- **Head-to-Head Comparisons**: Direct manager comparisons with detailed statistics
- **Player Performance**: Advanced player statistics with position-based filtering
- **Team Composition**: Squad analysis showing formation and player positions

## 📋 Prerequisites

- Python 3.12 or higher
- A Fantasy Premier League Draft league ID
- Internet connection (for fetching live data from FPL API)

## 🛠️ Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd Fantasy-Football
```

2. Install dependencies using uv (recommended) or pip:
```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r pyproject.toml
```

## 🏃 Running the Application

1. Start the Marimo application:
```bash
marimo run app.py
```

2. Open your browser and navigate to the displayed URL (typically `http://localhost:2718`)

3. Enter your Fantasy Draft League ID when prompted

4. Navigate through different analysis pages using the sidebar menu

## 🎯 Usage

### Getting Your League ID
Your League ID can be found in your Fantasy Premier League Draft URL:
- Go to your draft league on the FPL website
- The URL will look like: `https://draft.premierleague.com/entry/XXXXXX/league/YYYYYY`
- Your League ID is the `YYYYYY` part

### Environment Configuration (Optional)
You can set your League ID as an environment variable to avoid entering it each time:

1. Create a `.env` file in the project root:
```bash
LEAGUE_ID=your_league_id_here
```

### Navigation
The application features a sidebar with the following sections:

- **⚙️ League Details**: Enter your league ID
- **📊 League Standings**: View league progression over time
- **🏆 Top Performances**: See best gameweek performances by manager
- **⏱️ Gameweek Results**: Analyze specific gameweek results
- **🔄 Transfers**: Comprehensive transfer analysis and success rates
- **👥 Head-to-Head**: Compare two managers directly
- **⚡ Player Performance**: Search and filter player statistics
- **📋 Team Composition**: Analyze team formations and squad details

## 🏗️ Architecture

The application is built using:

- **[Marimo](https://marimo.io/)**: Reactive Python notebook framework for the web interface
- **[Polars](https://pola.rs/)**: High-performance DataFrame library for data processing
- **[DuckDB](https://duckdb.org/)**: In-memory SQL database for complex queries
- **[Plotly](https://plotly.com/python/)**: Interactive visualization library
- **[HTTPX](https://www.python-httpx.org/)**: Modern HTTP client for API requests

### Data Sources
The application fetches data from the official Fantasy Premier League API endpoints:
- League details and manager information
- Historical performance data
- Transfer transactions
- Player statistics and information
- Live gameweek data

## 🔧 Key Components

### Data Processing
- **League Data**: Fetches and processes league entries and manager information
- **Historical Data**: Aggregates performance data across all gameweeks
- **Transfer Data**: Analyzes transfer attempts, successes, and player demand
- **Player Data**: Processes detailed player statistics and performance metrics

### Visualizations
- **Line Charts**: League standings progression over time
- **Bar Charts**: Transfer activity, gameweek performance comparisons
- **Scatter Plots**: Player performance analysis with multiple dimensions
- **Interactive Tables**: Detailed data views with sorting and filtering

### Interactive Features
- **Gameweek Selectors**: Choose specific gameweeks or ranges for analysis
- **Manager Dropdowns**: Select managers for head-to-head comparisons
- **Player Search**: Find specific players with text search and position filtering
- **Team Analysis**: Detailed squad composition for any gameweek

## 📊 Data Features

- **Real-time Data**: Fetches live data from FPL API
- **Historical Analysis**: Complete season performance tracking
- **Transfer Intelligence**: Success rates and player demand metrics
- **Performance Metrics**: Points per game, consistency analysis
- **Comparative Analysis**: Manager and player comparisons

## 🤝 Contributing

This is a personal project, but suggestions for improvements are welcome! Feel free to:
- Open issues for bugs or feature requests
- Submit pull requests for improvements
- Contact the maintainer for additional functionality requests

## 📝 License

This project is for personal use and educational purposes. All Fantasy Premier League data is owned by the Premier League.

## 🔮 Future Roadmap

Potential features for future development:
- Historical season comparisons
- Advanced statistical modeling
- Export functionality for data and charts
- Mobile-responsive design improvements
- Additional visualization types
- Integration with other fantasy football platforms

---

*Made with ❤️ and Marimo ⚽*