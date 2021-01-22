##
## Copyright (c) 2021 Be The Match.
##
## This file is part of BLEAT 
## (see https://github.com/nmdp-bioinformatics/b-leader).
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU Lesser General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Lesser General Public License for more details.
##
## You should have received a copy of the GNU Lesser General Public License
## along with this program. If not, see <http://www.gnu.org/licenses/>.
##
FROM node:14-alpine as angular-builder

LABEL maintainer="NMDP Bioinformatics"

COPY webapp/package.json webapp/package-lock.json ./
RUN npm ci && mkdir /ng-app

WORKDIR /ng-app
COPY ./webapp/ .
RUN npm install -g @angular/cli && npm install
ARG CONFIGURATION=production
RUN npm run ng build -- --configuration=$CONFIGURATION



FROM python:3.8-alpine

LABEL maintainer="nmdp-bioinformatics"
RUN apk update && apk add nginx --no-cache
RUN mkdir -p /run/nginx && rm -rf /usr/share/nginx/html/*

COPY . /app
WORKDIR /app
RUN rm -r /app/webapp/*
RUN mkdir -p /app/logs/

RUN pip install -r requirements.txt

COPY --from=angular-builder ./ng-app/dist/bleader /usr/share/nginx/html
COPY webapp/nginx-conf/default.conf /etc/nginx/conf.d/
COPY docker-entrypoint-unified-prod.sh /usr/local/bin/


ENTRYPOINT [ "/usr/local/bin/docker-entrypoint-unified-prod.sh" ]
