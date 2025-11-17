# Najika World - Troubleshooting Guide

Common issues and solutions for Najika World.

---

## Installation Issues

### Problem: "Module not found" error
**Solution:**
```bash
pip install -r requirements.txt
# or
npm install
```

### Problem: Database connection error
**Solution:**
```bash
# Check DATABASE_URL in .env
DATABASE_URL=postgresql://user:pass@localhost/najika_world

# Test connection
psql -U najika -d najika_world -c "SELECT 1;"
```

---

## Runtime Issues

### Problem: API returns 500 error
**Solution:**
1. Check logs: `tail -f logs/najika.log`
2. Check database connection
3. Verify environment variables
4. Restart server: `systemctl restart najika-backend`

### Problem: WebSocket connection fails
**Solution:**
1. Check JWT token is valid
2. Use `ws://` for local, `wss://` for HTTPS
3. Check firewall rules
4. Verify WebSocket URL: `/api/v1/voice/ws/{token}`

---

## Performance Issues

### Problem: Slow API response
**Solution:**
1. Enable Redis caching
2. Check database query performance
3. Increase workers: `--workers 8`
4. Enable database connection pooling

### Problem: High memory usage
**Solution:**
1. Reduce max concurrent training jobs
2. Clear old training data
3. Optimize LOD settings
4. Check for memory leaks in logs

---

## Training Issues

### Problem: Training job stuck in "queued"
**Solution:**
1. Check scheduler status: `GET /api/v1/training/queue`
2. Restart training scheduler
3. Check max_concurrent_jobs setting
4. View logs for errors

### Problem: Training fails immediately
**Solution:**
1. Check training script exists
2. Verify dataset path
3. Check GPU availability
4. Review error logs

---

## Contact Support

For additional help:
- GitHub Issues: https://github.com/YourRepo/najika_world/issues
- Email: support@najika.example.com
- Discord: discord.gg/najika

---

**Troubleshooting Guide Version:** 1.0.0
**Last Updated:** 2025-01-17
