#!/bin/bash
set -e

echo "Starting PostgreSQL..."
sudo service postgresql start

echo "Container ready. Attach with: docker exec -it klaios-core bash"
exec sleep infinity
