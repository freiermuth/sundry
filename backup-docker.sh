#!/bin/bash

BACKUP_LABEL=us.freiermuth.backup
BACKUP_CONTAINERS=$(docker ps -qaf "label=$BACKUP_LABEL")
DATE=$(date '+%Y-%m-%d')
BACKUP_DIR=/backup
RETENTION_DAYS=30


for c in $BACKUP_CONTAINERS
do
        echo "Stopping container $c..."
        docker stop "$c"

        IFS="
        "
        # Do backup
        for each in `sudo docker inspect $c | jq '.[].Mounts[] | "\(.Name) \(.Source)"'`;
        do
                unset IFS
                line=`echo $each | sed s/\"//g`
                line=($line)
                volume_name=${line[0]}
                backup_file=$BACKUP_DIR/$volume_name-$DATE.tar.gz
                mountpoint=${line[1]}
                echo Backing up volume $volume_name at $mountpoint to $backup_file...
                tar czvf $backup_file $mountpoint
        done


        docker start $c
done

# clean up old backups
sudo find /backup -mtime +$RETENTION_DAYS -name *.tar.gz -exec rm {} \;
