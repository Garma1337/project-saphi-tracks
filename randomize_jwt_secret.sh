#!/bin/bash
ENV_FILE=".env"
NEW_SECRET=$(openssl rand -base64 32 | tr -d '\n')
sed -i "s/^JWT_SECRET=.*/JWT_SECRET=\"${NEW_SECRET}\"/" "$ENV_FILE"
