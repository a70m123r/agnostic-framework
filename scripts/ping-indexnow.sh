#!/usr/bin/env bash
# ============================================================
# IndexNow ping for the Agnostic Framework
# ------------------------------------------------------------
# Notifies Bing + Yandex + Seznam + Naver instantly that the
# framework has new or updated content. Single ping covers all
# IndexNow-participating search engines.
#
# Usage:
#   bash scripts/ping-indexnow.sh                     # ping the homepage + key high-traffic surfaces
#   bash scripts/ping-indexnow.sh <url1> <url2> ...   # ping specific URLs
#
# Examples:
#   bash scripts/ping-indexnow.sh
#     # → pings: homepage, timeline, llms.txt, llms-full.txt,
#     #         manifest.json, both animated artifacts
#
#   bash scripts/ping-indexnow.sh \
#     https://a70m123r.github.io/agnostic-framework/continuations/28.md \
#     https://a70m123r.github.io/agnostic-framework/CHANGELOG.md
#     # → pings just those two URLs
#
# IndexNow API spec: https://www.indexnow.org
# ============================================================

set -euo pipefail

KEY="568fa5e82cc4459dabbfa57d220d26d8"
HOST="a70m123r.github.io"
KEY_LOCATION="https://${HOST}/agnostic-framework/${KEY}.txt"
ENDPOINT="https://api.indexnow.org/IndexNow"

# Default URL set if no arguments — the high-traffic surfaces that change often
DEFAULT_URLS=(
  "https://a70m123r.github.io/agnostic-framework/"
  "https://a70m123r.github.io/agnostic-framework/timeline/"
  "https://a70m123r.github.io/agnostic-framework/llms.txt"
  "https://a70m123r.github.io/agnostic-framework/llms-full.txt"
  "https://a70m123r.github.io/agnostic-framework/manifest.json"
  "https://a70m123r.github.io/agnostic-framework/primitives.json"
  "https://a70m123r.github.io/agnostic-framework/CHANGELOG.md"
  "https://a70m123r.github.io/agnostic-framework/for-agents/"
  "https://a70m123r.github.io/agnostic-framework/artifacts/wrapper_overlap_animated.html"
  "https://a70m123r.github.io/agnostic-framework/artifacts/michotte_launching_extension.html"
)

# Use args if provided, otherwise defaults
if [ "$#" -eq 0 ]; then
  URLS=("${DEFAULT_URLS[@]}")
else
  URLS=("$@")
fi

# Build JSON body
URL_LIST=$(printf '"%s",' "${URLS[@]}" | sed 's/,$//')
JSON_BODY=$(cat <<EOF
{
  "host": "${HOST}",
  "key": "${KEY}",
  "keyLocation": "${KEY_LOCATION}",
  "urlList": [${URL_LIST}]
}
EOF
)

echo "Pinging IndexNow with ${#URLS[@]} URL(s)..."
echo "Key location: ${KEY_LOCATION}"
echo ""

RESPONSE=$(curl -sS -X POST "${ENDPOINT}" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d "${JSON_BODY}" \
  -w "\nHTTP_STATUS:%{http_code}")

HTTP_STATUS=$(echo "${RESPONSE}" | grep "HTTP_STATUS:" | cut -d: -f2)
BODY=$(echo "${RESPONSE}" | sed '/HTTP_STATUS:/d')

case "${HTTP_STATUS}" in
  200)
    echo "✓ Success (HTTP 200): URLs accepted for indexing"
    ;;
  202)
    echo "✓ Accepted (HTTP 202): URLs received; key validation pending"
    ;;
  400)
    echo "✗ Bad request (HTTP 400): malformed JSON or invalid URL format"
    echo "${BODY}"
    exit 1
    ;;
  403)
    echo "✗ Forbidden (HTTP 403): key validation failed — confirm ${KEY_LOCATION} returns the key string"
    echo "${BODY}"
    exit 1
    ;;
  422)
    echo "✗ Unprocessable (HTTP 422): URLs don't match the verified host, or other validation issue"
    echo "${BODY}"
    exit 1
    ;;
  429)
    echo "✗ Too many requests (HTTP 429): rate-limited; back off and retry"
    exit 1
    ;;
  *)
    echo "? Unexpected status (HTTP ${HTTP_STATUS})"
    echo "${BODY}"
    ;;
esac

echo ""
echo "URLs pinged:"
printf '  %s\n' "${URLS[@]}"
echo ""
echo "Note: IndexNow ping notifies Bing + Yandex + Seznam + Naver simultaneously."
echo "      Each engine independently decides when to crawl. Typical surface time: minutes to hours."
