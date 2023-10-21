#!/bin/bash
set -e;

MONGO_NON_ROOT_ROLE="${MONGO_NON_ROOT_ROLE:-readWrite}"

if [ -n "${MONGO_CHATLOG_USERNAME:-}" ] && [ -n "${MONGO_CHATLOG_PASSWORD:-}" ]; then
	"${mongo[@]}" "$MONGO_CHATLOG_DB_NAME" <<-EOJS

		db.createCollection("$MONGO_CHATLOG_COLLECTION_MESSAGES")
		db.createCollection("$MONGO_CHATLOG_COLLECTION_SESSIONS")
		db.createCollection("$MONGO_CHATLOG_COLLECTION_TICKETS")
		db.createCollection("$MONGO_CHATLOG_COLLECTION_FEEDBACK")
		db.createUser({
			user: $(_js_escape "$MONGO_CHATLOG_USERNAME"),
			pwd: $(_js_escape "$MONGO_CHATLOG_PASSWORD"),
			roles: [ { role: $(_js_escape "$MONGO_NON_ROOT_ROLE"), db: $(_js_escape "$MONGO_CHATLOG_DB_NAME") } ]
			})


	EOJS
fi
