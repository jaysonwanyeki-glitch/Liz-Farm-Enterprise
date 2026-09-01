# 🌾 Liz Farm Enterprise - Complete Management System

A beautiful, interactive farm management dashboard built with **Streamlit** and **SQLite**.

![Farm Dashboard](https://img.shields.io/badge/Streamlit-1.30+-red?style=for-the-badge&logo=streamlit)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)
![SQLite](https://img.shields.io/badge/SQLite-3-green?style=for-the-badge&logo=sqlite)

## 🌟 Features

### 🏠 Dashboard
- Real-time KPIs (eggs, revenue, livestock, profit)
- Revenue breakdown with donut charts
- Expense analytics
- Weather trends
- Task progress tracking

### 🐔 Livestock Management
- Auto-calculating totals (Male + Female = Total)
- Health status tracking
- Visual distribution charts

### 🍊 Orange Orchard
- Tree-by-tree harvest tracking
- Grade A/B distribution
- Revenue analytics

### 🛒 Cereal Shop
- Sales transaction history
- **Inventory stock tracking** with min/max levels
- Low stock alerts
- Profit by cereal type

### 🥚 Egg Production
- Daily production tracking
- Quality grade monitoring
- Sales & revenue logs

### 👤 Employee Management
- Employee profiles
- Monthly payment history

### 🐾 Pet Care
- Feeding schedule & logs
- Cat meal menus
- Mortality tracking

### 💰 Financial Overview
- Income vs expense tracking
- Category breakdown
- Payment method analytics

### 📦 Feed Inventory
- Stock level monitoring
- Reorder alerts

### 📊 Reports
- Excel export for all 16 datasets
- Financial summaries

### 💾 Backup & Restore
- One-click database backup
- Restore from uploaded backup
- Quick reset option

## 🎨 Design Features
- **Animated farm background** with floating particles
- **Glassmorphism UI** with backdrop blur effects
- **Animated sidebar** with walking chicken & swaying trees
- **Animated counters** with pop-in effects
- **Transparent charts** showing the beautiful background

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/liz-farm-enterprise.git
cd liz-farm-enterprise

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

## 📁 Project Structure

```
liz-farm-enterprise/
├── app.py                  # Main Streamlit application
├── database.py             # SQLite database layer
├── requirements.txt        # Python dependencies
├── Procfile               # Deployment config
├── .gitignore             # Git ignore rules
├── README.md              # This file
└── .streamlit/
    └── config.toml        # Streamlit configuration
```

## 🗄️ Database

The app uses **SQLite** with 19 tables:

| Table | Description |
|-------|-------------|
| `farm_overview` | Farm settings & info |
| `inventory` | Livestock inventory |
| `orchard` | Orange tree tracking |
| `orange_harvest` | Harvest logs |
| `cereal_shop` | Sales transactions |
| `cereal_inventory` | Stock levels |
| `employees` | Staff information |
| `employee_payments` | Salary records |
| `egg_production` | Daily egg counts |
| `egg_sales` | Egg sales history |
| `fruit_production` | General fruit tracking |
| `chicks` | Hatchery records |
| `pet_feeding` | Pet feeding logs |
| `cat_menu` | Cat meal schedules |
| `mortality` | Loss tracking |
| `finance` | Income & expenses |
| `feed_inventory` | Feed stock levels |
| `tasks` | Daily task management |
| `weather` | Weather conditions |

## 🛠️ Tech Stack

- **Frontend**: Streamlit with custom CSS animations
- **Backend**: Python 3.9+
- **Database**: SQLite3
- **Charts**: Plotly.js (via plotly)
- **Data**: Pandas

## 📦 Deployment

### Streamlit Cloud
1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Deploy!

### Vercel
1. Push to GitHub
2. Import project in Vercel
3. Framework: Other
4. Build Command: `pip install -r requirements.txt`
5. Output Directory: `.`

## 👤 Owner

**Liz** - Kenya 🇰🇪
- Est. 2020
- Farming with love 🌾

## 📄 License

This project is open source and available for personal use.

---

*Built with ❤️ using Streamlit*
