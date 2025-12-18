#!/bin/bash

export PYTHONDONTWRITEBYTECODE=1

set -e

cleanup() {
    cd ../../
    rm -rf build
    rm -rf src/app/templates/mainpages/mainpage/mainpage.js
    rm -rf src/app/templates/profiles/editstudprofile/editstudprofile.js
    rm -rf src/app/templates/profiles/edittutprofile/edittutprofile.js
}

npm install  typescript

node_modules/.bin/tsc src/app/templates/mainpages/mainpage/mainpage.ts --target es2015 --outDir src/app/templates/mainpages/mainpage
node_modules/.bin/tsc src/app/templates/profiles/editstudprofile/editstudprofile.ts --target es2015 --outDir src/app/templates/profiles/editstudprofile
node_modules/.bin/tsc src/app/templates/profiles/edittutprofile/edittutprofile.ts --target es2015 --outDir src/app/templates/profiles/edittutprofile

npm install

npm run prettier:fix
npm run prettier:check
npm run eslint:fix
npm run eslint:check
npm run stylelint:fix
npm run stylelint:check

trap cleanup EXIT INT TERM

npm run esbuild

cd src/app

uvicorn main:app --host 0.0.0.0 --port 80
