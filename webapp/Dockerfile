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
FROM node:14-alpine as builder

LABEL maintainer="NMDP Bioinformatics"

COPY package.json package-lock.json ./

RUN npm ci && mkdir /ng-app && mv ./node_modules ./ng-app

WORKDIR /ng-app

COPY . .

ARG CONFIGURATION=production
RUN npm run ng build -- --configuration=$CONFIGURATION


FROM nginx:1.19-alpine

LABEL maintainer="NMDP Bioinformatics"

RUN rm -rf /usr/share/nginx/html/*

## The "ng build" creates artifact in  dist/bleader directory, should be updated 
COPY --from=builder ./ng-app/dist/bleader /usr/share/nginx/html
COPY nginx-conf/default.conf /etc/nginx/conf.d/

EXPOSE 80

ENTRYPOINT ["nginx", "-g", "daemon off;"]
