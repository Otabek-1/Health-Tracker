# Health Tracker Telegram Bot

A comprehensive health tracking Telegram bot with real-time monitoring dashboard, designed for deployment on Replit.

## 🌟 Features

### Health Tracking
- **Weight Management**: Log and track weight changes over time
- **Activity Monitoring**: Daily step counting and exercise time logging
- **Hydration Tracking**: Water intake monitoring with daily goals
- **Sleep Analysis**: Sleep duration tracking with quality insights
- **Mood Tracking**: Daily mood rating on a 1-10 scale
- **Data Export**: CSV export of all health data

### Bot Features
- **Interactive Commands**: Easy-to-use Telegram commands
- **Keyboard Interface**: Quick access buttons for common actions
- **Smart Reminders**: Customizable daily health tracking reminders
- **Statistics Dashboard**: Comprehensive health analytics
- **Profile Management**: User preferences and settings

### Technical Features
- **Real-time Dashboard**: Web-based monitoring interface
- **SQLite Database**: Persistent data storage
- **Keep-alive System**: 24/7 uptime on Replit
- **Error Handling**: Robust error management and logging
- **Responsive Design**: Mobile-friendly dashboard interface

## 🚀 Quick Start

### Prerequisites
- Telegram Bot Token (from @BotFather)
- Replit account for hosting

### Environment Variables
Set these variables in Replit's environment settings:

```bash
BOT_TOKEN=your_telegram_bot_token_here
DATABASE_PATH=health_tracker.db
LOG_LEVEL=INFO
TIMEZONE=UTC
