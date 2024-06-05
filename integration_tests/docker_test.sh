
set -e 

docker build -f Dockerfile.test -t weave_test .
docker run -it --rm -e TOGETHER_API_KEY=$TOGETHER_API_KEY weave_test
