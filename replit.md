# Health Tracker Bot

## Overview

A Telegram bot designed to track daily health metrics with AI-powered analysis and insights. The bot collects user data including sleep time, physical activity, aggression levels, and mood ratings, then provides personalized health recommendations based on pattern analysis. Features include user registration, daily data collection, automated reminders, and comprehensive health analytics.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Bot Framework
- **aiogram**: Modern Telegram Bot API framework for Python with async support
- **Finite State Machine (FSM)**: Memory-based state management for multi-step user interactions
- **Router-based handlers**: Modular message handling system for different bot commands and states

### Data Management
- **SQLite Database**: Local file-based database (`HealtTracker.db`) for user and health data storage
- **aiosqlite**: Async SQLite wrapper for non-blocking database operations
- **Data Models**: Structured dataclasses for User and health data with serialization support

### Database Schema
- **users table**: Stores user profile information (telegram_id, full_name, age, timestamps)
- **health_data table**: Daily health metrics with foreign key relationship to users
- **Unique constraints**: Prevents duplicate daily entries per user

### Core Features
- **User Registration**: Multi-step registration process collecting name and age
- **Daily Data Collection**: Structured input flow for sleep, activity, aggression, and mood data
- **Health Analysis**: Pattern recognition and correlation analysis using basic statistical methods
- **Automated Scheduling**: Daily reminder system at configurable times
- **Personalized Insights**: AI-powered recommendations based on historical data trends

### State Management
- **Registration States**: `waiting_name`, `waiting_age` for user onboarding
- **Data Input States**: `waiting_sleep`, `waiting_activity`, `waiting_aggression`, `waiting_mood`
- **Temporary Storage**: In-memory storage for multi-step data collection processes

### Analytics Engine
- **Pattern Analysis**: Sleep, activity, mood, and aggression trend analysis
- **Correlation Detection**: Cross-metric relationship identification
- **Recommendation Generation**: Personalized health advice based on data patterns
- **Minimum Data Requirements**: Configurable threshold for meaningful analysis

### Scheduling System
- **Asyncio-based Scheduler**: Non-blocking reminder system
- **Daily Reminders**: Automated notifications for data collection
- **Smart Reminders**: Conditional reminders that skip users who already submitted daily data
- **Error Handling**: Graceful handling of blocked/deleted users

## External Dependencies

### Telegram Integration
- **Telegram Bot API**: Primary interface for user interactions
- **Bot Token**: Environment-based authentication for Telegram services
- **Message Formatting**: Markdown support for rich text responses

### Development Environment
- **Replit Deployment**: Optimized for continuous operation on Replit platform
- **Environment Variables**: Secure token management through environment configuration
- **Logging System**: Comprehensive logging with file and console output

### Runtime Dependencies
- **Python 3.7+**: Core runtime environment
- **asyncio**: Asynchronous programming support
- **numpy**: Statistical analysis for health data patterns
- **pathlib**: Modern file path handling
- **datetime**: Time-based operations and scheduling

### Configuration Management
- **Environment-based Configuration**: BOT_TOKEN from environment variables
- **Configurable Parameters**: Reminder times, timezone settings, analysis thresholds
- **Message Templates**: Centralized message content management
- **Database Path Configuration**: Flexible database file location