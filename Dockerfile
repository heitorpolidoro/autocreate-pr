#FROM alpine
#
#RUN apk add --no-cache \
#    bash \
#    git \
#    github-cli
#
#COPY create_pr.sh /create_pr.sh
#
#RUN chmod +x /create_pr.sh
#
#ENTRYPOINT ["/create_pr.sh"]