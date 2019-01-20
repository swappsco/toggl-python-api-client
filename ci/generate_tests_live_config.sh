#!/usr/bin/env bash

rm tests_live_config.json
touch tests_live_config.json

echo "{"                                                  >> tests_live_config.json
echo "      \"workspace_name\": \"${WORKSPACE_NAME}\","   >> tests_live_config.json
echo "      \"token\": \"${TOKEN}\","                     >> tests_live_config.json
echo "      \"workspace_id\": ${WORKSPACE_ID},"           >> tests_live_config.json
echo "      \"user_id\": ${USER_ID},"                     >> tests_live_config.json
echo "      \"start_date\": \"${START_DATE}\","           >> tests_live_config.json
echo "      \"end_date\": \"${END_DATE}\""                >> tests_live_config.json
echo "}"                                                  >> tests_live_config.json