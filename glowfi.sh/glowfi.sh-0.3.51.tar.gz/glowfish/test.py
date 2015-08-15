import glowfish

glower = glowfish.Glower('lGd7XS8R64eYRRl7x77vQFaox5fm2DTN','lcxcQ7aEuJ3QMP446JkXV12aaAubgRe5')
glower.config.API_ENDPOINT = "http://api.staging.glowfi.sh/"

tr = glower.train({"feature1": [1,2,3,4,5,6,7,8,9]}, {'response': [1,2,3,4,5,6,7,8,9]})

print tr