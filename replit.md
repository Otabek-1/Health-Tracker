# Health Tracker Telegram Bot

## Overview

This is a comprehensive health tracking Telegram bot with a real-time monitoring dashboard. The application allows users to track various health metrics including weight, daily steps, water intake, exercise time, sleep duration, and mood through an interactive Telegram interface. The system features persistent data storage, customizable reminders, data export capabilities, and a web-based dashboard for monitoring bot status and user analytics. The application is specifically designed for deployment on Replit with 24/7 uptime capabilities.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Bot Framework and Communication
- **Telegram Bot Integration**: Built using python-telegram-bot library for handling user interactions through Telegram's messaging platform
- **Asynchronous Operations**: Utilizes asyncio for handling concurrent user requests and maintaining responsive bot performance
- **Command-based Interface**: Implements structured command handlers for different health tracking functionalities (/weight, /steps, /water, etc.)
- **Interactive Keyboards**: Provides quick access buttons and keyboard interfaces for improved user experience

### Data Persistence Layer
- **SQLite Database**: Local database storage for user profiles and health records with proper schema design
- **Database Abstraction**: Dedicated Database class handling all data operations with connection management and error handling
- **Data Models**: Structured tables for users and health_records with proper relationships and indexing
- **Context Management**: Safe database operations using connection context managers to prevent data corruption

### Web Dashboard and Monitoring
- **Flask Web Server**: Lightweight web interface for real-time bot status monitoring and analytics
- **Health Check Endpoints**: RESTful API endpoints providing bot status, user counts, and recent activity metrics
- **Bootstrap Frontend**: Responsive web dashboard with real-time updates and interactive charts
- **Static Asset Management**: Organized CSS, JavaScript, and HTML files for the monitoring interface

### Application Configuration
- **Environment-based Config**: Centralized configuration management using environment variables for deployment flexibility
- **Validation System**: Configuration validation with required and optional settings, including health tracking limits
- **Timezone Support**: Configurable timezone settings for proper data recording and reminder scheduling
- **Deployment Settings**: Webhook and keep-alive configurations optimized for Replit hosting

### Error Handling and Logging
- **Comprehensive Logging**: Multi-level logging system with file and console output for debugging and monitoring
- **Graceful Error Recovery**: Robust error handling throughout the application to maintain bot availability
- **User State Management**: Conversation state tracking for multi-step interactions and data entry flows

### Keep-Alive and Deployment
- **Replit Optimization**: Dedicated keep-alive server to maintain 24/7 uptime on Replit's platform
- **Thread Management**: Separate threads for bot operations and web server to prevent blocking
- **Health Monitoring**: Continuous status checking with automatic recovery mechanisms

## External Dependencies

### Core Frameworks
- **python-telegram-bot**: Primary library for Telegram Bot API integration and message handling
- **Flask**: Lightweight web framework for the monitoring dashboard and health check endpoints
- **SQLite3**: Built-in Python database engine for local data persistence

### Frontend Libraries
- **Bootstrap 5.1.3**: CSS framework for responsive dashboard design and mobile compatibility
- **Font Awesome 6.0.0**: Icon library for dashboard user interface elements
- **Chart.js** (referenced): JavaScript charting library for health analytics visualization

### Python Standard Library
- **asyncio**: Asynchronous programming support for concurrent bot operations
- **sqlite3**: Database connectivity and operations
- **logging**: Application logging and debugging capabilities
- **threading**: Multi-threaded execution for keep-alive functionality
- **datetime**: Date and time handling for health record timestamps

### Platform Integration
- **Telegram Bot API**: External service for bot communication and user interaction
- **Replit Platform**: Cloud hosting environment with specific keep-alive requirements and environment variable management