"""
Keep-alive server for Replit deployment
Ensures the bot stays active 24/7
"""

from flask import Flask, render_template, jsonify
import os
import logging
import sqlite3
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='static', template_folder='static')

# Health check endpoint
@app.route('/')
def home():
    """Main page with bot status and basic stats"""
    return render_template('index.html')

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Check database connection
        conn = sqlite3.connect('health_tracker.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM health_records WHERE date_for >= date('now', '-7 days')")
        recent_records = cursor.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'users': user_count,
            'recent_records': recent_records,
            'uptime': True
        })
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'timestamp': datetime.now().isoformat(),
            'error': str(e)
        }), 500

@app.route('/stats')
def bot_stats():
    """Bot statistics endpoint"""
    try:
        conn = sqlite3.connect('health_tracker.db')
        cursor = conn.cursor()
        
        # Get comprehensive stats
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM health_records")
        total_records = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT record_type, COUNT(*) as count 
            FROM health_records 
            GROUP BY record_type
        """)
        record_types = dict(cursor.fetchall())
        
        cursor.execute("""
            SELECT COUNT(DISTINCT user_id) 
            FROM health_records 
            WHERE date_for >= date('now', '-7 days')
        """)
        active_users = cursor.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            'total_users': total_users,
            'total_records': total_records,
            'active_users_week': active_users,
            'record_types': record_types,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Stats endpoint failed: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/recent-activity')
def recent_activity():
    """Get recent activity for dashboard"""
    try:
        conn = sqlite3.connect('health_tracker.db')
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT DATE(recorded_at) as date, COUNT(*) as count
            FROM health_records 
            WHERE recorded_at >= datetime('now', '-30 days')
            GROUP BY DATE(recorded_at)
            ORDER BY date DESC
            LIMIT 30
        """)
        
        activity_data = [{'date': row[0], 'count': row[1]} for row in cursor.fetchall()]
        conn.close()
        
        return jsonify(activity_data)
    except Exception as e:
        logger.error(f"Recent activity endpoint failed: {e}")
        return jsonify({'error': str(e)}), 500

def keep_alive():
    """Start the keep-alive server"""
    port = int(os.getenv('KEEP_ALIVE_PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
