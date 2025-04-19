#!/bin/bash

ngrok http 5173 --host-header="localhost:5173" --request-header-add="ngrok-skip-browser-warning:true"