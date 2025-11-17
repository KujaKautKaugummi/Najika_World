# Najika World - Admin Guide

Admin guide for managing the Najika World backend and systems.

---

## Admin Dashboard Access

Access the admin dashboard at:
```
http://your-domain.com/api/v1/admin/
```

Login with admin credentials.

---

## User Management

### View All Users
```
GET /api/v1/admin/users
```

### Update User
```
PATCH /api/v1/admin/users/{user_id}
Body: { "is_active": true, "is_admin": false }
```

### Ban/Unban User
```
POST /api/v1/admin/users/{user_id}/ban
POST /api/v1/admin/users/{user_id}/unban
```

---

## Training Management

### View All Training Jobs
```
GET /api/v1/admin/training/jobs
```

### Cancel Training Job
```
POST /api/v1/admin/training/jobs/{job_id}/cancel
```

### View Training Queue
```
GET /api/v1/admin/training/queue
```

---

## System Monitoring

### View System Stats
```
GET /api/v1/admin/stats
```

Response:
```json
{
  "total_users": 42,
  "active_users": 38,
  "total_characters": 56,
  "total_training_jobs": 128,
  "running_training_jobs": 3,
  "database_size_mb": 250,
  "uptime_seconds": 86400
}
```

### View Logs
```
GET /api/v1/admin/logs?level=ERROR&limit=100
```

---

## Maintenance

### Database Backup
```bash
# PostgreSQL backup
pg_dump -U najika najika_world > backup.sql

# Restore
psql -U najika najika_world < backup.sql
```

### Clear Old Jobs
```
POST /api/v1/admin/maintenance/clear-old-jobs
Body: { "max_age_days": 30 }
```

---

## Security

### View Security Logs
```
GET /api/v1/admin/security/logs
```

### Block IP Address
```
POST /api/v1/admin/security/block-ip
Body: { "ip": "192.168.1.1" }
```

---

**Admin Guide Version:** 1.0.0
**Last Updated:** 2025-01-17
