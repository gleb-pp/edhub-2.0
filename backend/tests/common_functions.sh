#!/bin/bash

get_http_code() {
    curl -s -o /dev/null -w "%{http_code}" "$@"
}

success_test() {
    local name="$1"
    shift
    local http_code
    http_code=$(get_http_code "$@")
    if [ "$http_code" -eq 200 ]; then
        echo "✓ Successful $name"
    else
        echo "ERROR: $name failed with HTTP $http_code"
        exit 1
    fi
}

fail_test() {
    local name="$1"
    shift
    local http_code
    http_code=$(get_http_code "$@")
    if [ "$http_code" -ge 400 ]; then
        echo "✓ Successfully rejected $name"
    else
        echo "ERROR: $name expected to fail, but got HTTP $http_code"
        exit 1
    fi
}

login_and_get_token() {
    local name="$1"; shift
    local body="/tmp/login_body.json"
    local code
    code=$(curl -sS -o "$body" -w "%{http_code}" "$@")
    if [[ "$code" =~ ^[0-9]{3}$ ]] && [ "$code" -ge 200 ] && [ "$code" -lt 300 ]; then
    echo "✓ Successful $name"
    TOKEN=$(python3 -c 'import sys,json; print(json.load(open(sys.argv[1])).get("access_token",""))' "$body")
    if [ -z "$TOKEN" ] || [ "$TOKEN" = "null" ]; then
        echo "ERROR: $name did not return a valid token"
        head -c 500 "$body" || true
        exit 1
    else
        echo "✓ Extracted token: $TOKEN"
    fi
    else
    echo "ERROR: $name failed with HTTP $code"
    head -c 500 "$body" || true
    exit 1
    fi
}

json_exact_match_test() {
    local name="$1"
    local json_response="$2"
    local expected_json="$3"
    local sort_fields_str="${4:-}"

    IFS=' ' read -r -a sort_fields <<< "$sort_fields_str"

    local jq_sort_key=""
    if [ ${#sort_fields[@]} -gt 0 ] && [ -n "${sort_fields[0]}" ]; then
        jq_sort_key="["
        local first=1
        for field in "${sort_fields[@]}"; do
            if [ $first -eq 1 ]; then
                jq_sort_key+=".${field}"
                first=0
            else
                jq_sort_key+=", .${field}"
            fi
        done
        jq_sort_key+="]"
    fi

    local jq_prog='(if type=="array" then . else [.] end)'
    if [ -n "$jq_sort_key" ]; then
        jq_prog+=' | sort_by('"$jq_sort_key"')'
    fi

    local sorted_response
    sorted_response=$(echo "$json_response" | jq -S "$jq_prog")
    local sorted_expected
    sorted_expected=$(echo "$expected_json" | jq -S "$jq_prog")

    if [ "$sorted_response" = "$sorted_expected" ]; then
        echo "✓ Successful $name"
    else
        echo "ERROR: $name failed."
        echo "Expected:"
        echo "$sorted_expected"
        echo "Received:"
        echo "$sorted_response"
        exit 1
    fi
}

json_partial_match_test() {
    local name="$1"
    local json_response="$2"
    local expected_json="$3"
    local sort_fields_str="${4:-}"
    local ignore_fields_str="${5:-}"

    IFS=' ' read -r -a sort_fields <<< "$sort_fields_str"
    IFS=' ' read -r -a ignore_fields <<< "$ignore_fields_str"

    local jq_sort_key=""
    if [ ${#sort_fields[@]} -gt 0 ] && [ -n "${sort_fields[0]}" ]; then
        jq_sort_key="["
        local first=1
        for field in "${sort_fields[@]}"; do
            if [ $first -eq 1 ]; then
                jq_sort_key+=".${field}"
                first=0
            else
                jq_sort_key+=", .${field}"
            fi
        done
        jq_sort_key+="]"
    fi

    local jq_del_args=""
    if [ ${#ignore_fields[@]} -gt 0 ] && [ -n "${ignore_fields[0]}" ]; then
        local first=1
        for field in "${ignore_fields[@]}"; do
            if [ $first -eq 1 ]; then
                jq_del_args+=".${field}"
                first=0
            else
                jq_del_args+=", .${field}"
            fi
        done
    fi

    local jq_prog='(if type=="array" then . else [.] end)'
    if [ -n "$jq_sort_key" ]; then
        jq_prog+=' | sort_by('"$jq_sort_key"')'
    fi
    if [ -n "$jq_del_args" ]; then
        jq_prog+=' | map(del('"$jq_del_args"'))'
    fi

    local filtered_response
    filtered_response=$(echo "$json_response" | jq -S "$jq_prog")
    local filtered_expected
    filtered_expected=$(echo "$expected_json" | jq -S "$jq_prog")

    if [ "$filtered_response" = "$filtered_expected" ]; then
        echo "✓ Successful $name"
    else
        echo "ERROR: $name failed"
        echo "Expected (sorted & ignored fields removed):"
        echo "$filtered_expected"
        echo "Received (sorted & ignored fields removed):"
        echo "$filtered_response"
        exit 1
    fi
}

extract_field() {
    local field="$1"
    python3 -c "import sys, json; print(json.load(sys.stdin).get('$field', ''))"
}
