download_from_google_drive() {
    url="$1"
    output_name="$2"

    echo "Processing Google Drive link: $url"
    FILE_ID=$(echo "$url" | sed -n 's/.*\/d\/\([^\/]*\).*/\1/p' | head -n1)

    if [ -z "$FILE_ID" ]; then
        FILE_ID=$(echo "$url" | sed -n 's/.*id=\([^&]*\).*/\1/p' | head -n1)
    fi

    if [ -n "$FILE_ID" ]; then
        echo "  File ID: $FILE_ID"
        GDRIVE_URL="https://drive.google.com/uc?export=download&id=$FILE_ID"

        CONFIRM=$(wget --quiet --save-cookies /tmp/cookies_${FILE_ID}.txt --keep-session-cookies --no-check-certificate "$GDRIVE_URL" -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1/p')

        if [ -n "$CONFIRM" ]; then
            echo "  Large file detected, using confirmation token"
            wget --load-cookies /tmp/cookies_${FILE_ID}.txt \
                 --no-check-certificate \
                 "https://drive.google.com/uc?export=download&confirm=$CONFIRM&id=$FILE_ID" \
                 -O "$output_name"
        else
            echo "  Downloading directly"
            wget --no-check-certificate "$GDRIVE_URL" -O "$output_name"
        fi

        rm -rf /tmp/cookies_${FILE_ID}.txt

        if [ -f "$output_name" ] && [ -s "$output_name" ]; then
            echo "  Successfully downloaded: $output_name"
            chmod 644 "$output_name"
            ls -lh "$output_name"
            return 0
        else
            echo "  ERROR: Failed to download"
            rm -f "$output_name"
            return 1
        fi
    else
        echo "  ERROR: Could not extract file ID"
        return 1
    fi
}

download_from_url() {
    url="$1"
    output_name="$2"

    echo "Downloading from direct URL: $url"
    wget --no-check-certificate "$url" -O "$output_name"

    if [ -f "$output_name" ] && [ -s "$output_name" ]; then
        echo "  Successfully downloaded: $output_name"
        chmod 644 "$output_name"
        ls -lh "$output_name"
        return 0
    else
        echo "  ERROR: Failed to download"
        rm -f "$output_name"
        return 1
    fi
}

if [ -n "$VIDEO_SOURCE_URL" ]; then
    echo "Starting video download process..."
    cd /usr/share/nginx/videos

    OLD_IFS="$IFS"
    IFS=','

    for url_entry in $VIDEO_SOURCE_URL; do
        url_entry=$(echo "$url_entry" | xargs)

        if [ -z "$url_entry" ]; then
            continue
        fi

        echo ""
        echo "Processing: $url_entry"

        if echo "$url_entry" | grep -q '|'; then
            url=$(echo "$url_entry" | cut -d'|' -f1 | xargs)
            filename=$(echo "$url_entry" | cut -d'|' -f2 | xargs)
        else
            url="$url_entry"
            filename=$(basename "$url" | sed 's/[?&].*//' | sed 's/%20/ /g')

            if ! echo "$filename" | grep -q '\.mp4$'; then
                filename="video_$(date +%s).mp4"
            fi
        fi

        echo "  URL: $url"
        echo "  Output filename: $filename"

        if echo "$url" | grep -q "drive.google.com"; then
            download_from_google_drive "$url" "$filename"
        else
            download_from_url "$url" "$filename"
        fi
    done

    IFS="$OLD_IFS"

    echo ""
    echo "Download process completed. Files in videos directory:"
    ls -lah /usr/share/nginx/videos/

    sync
    sleep 1

    echo "Files are ready to serve"
else
    echo "No VIDEO_SOURCE_URL set. Using existing videos in directory."
    ls -lah /usr/share/nginx/videos/
fi