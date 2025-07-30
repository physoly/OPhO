# OPhO

# Get Real Values from discord
```
cat > .env << EOF
x=y
EOF
```

# Make local Postgres Instance
```
docker network create opho-net
```

# Build
```
docker build -t opho .
```

# Run Site
```
docker run --rm \
  --network opho-net \
  --env-file .env \
  -p 8000:8000 \
  opho
```

# Run Scripts/Py files
```
docker run --rm \
  --network opho-net \
  --env-file .env \
  opho \
  python3 scripts/x.py (disregard scripts if its not in scripts, or switch folder)
```

# You will most likely have to initialize the db table before performing any operations via the scripts
```
docker exec -it opho-db psql -U opho-admin -d opho -c "\dt"
```
# This cmd should show opho-admin as superuser