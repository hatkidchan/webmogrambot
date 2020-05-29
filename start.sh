docker run -d \
    --restart always \
    --name webmogrambot \
    -e TG_TOKEN="AAAAAAAAAAAAAAAAAAAAAAAAAAAAA" \
    -e NO_REPORT="no" \
    webmogrambot:latest

