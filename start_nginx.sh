sudo docker run \
--rm \
--network service-centre \
--name service_nginx \
-v /Users/ron/nginx_config/nginx.conf:/etc/nginx/nginx.conf \
-v /Users/ron/nginx_config/nginx_service.conf:/etc/nginx/conf.d/nginx_service.conf \
-v /Users/ron/service_centre_static:/usr/share/nginx/html \
-p 8088:80 nginx:1.17-alpine

