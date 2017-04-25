#!/bin/bash

pg_dump --username=postgres --host=database --format=plain --data-only --no-owner --file="/backups/polish-lody-`date +%Y-%m-%d-%H%M`.sql" polishlody
