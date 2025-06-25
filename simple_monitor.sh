#!/bin/bash
# Monitor simples do Render
echo "🔄 Checking Render Status..."

for i in {1..5}; do
    echo "⏰ Check $i/5 - $(date +%H:%M:%S)"
    
    response=$(curl -s "https://rog-report-v5.onrender.com/" --max-time 10)
    
    if echo "$response" | grep -q "Pool Service"; then
        echo "🎉 SUCCESS! v3.0 detected!"
        echo "✅ ROG Pool Service is live!"
        break
    elif echo "$response" | grep -q "Railway working"; then
        echo "⏳ Still old version - waiting..."
    else
        echo "❌ Unexpected response or error"
    fi
    
    if [ $i -lt 5 ]; then
        echo "💤 Waiting 60s..."
        sleep 60
    fi
    echo ""
done

echo "📋 Final check:"
curl -s "https://rog-report-v5.onrender.com/" | head -2