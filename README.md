# Google Cloud python scripts helpers
Some python scripts for deploying your software on google cloud platform 


# gcloud-sql-add-authorized-ip

Add at your startup script on Compute Engine machines this script to allow its IP connect on your Cloud SQL

Usage: 'gcloud-sql-add-authorized-ip [instanceName] [command: add|remove] [IP-CIDR-notation]'

You can use it for add and remove current IP at startup-script and shutdown-script.