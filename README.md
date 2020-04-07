

# The total population per region is available in a static remote csv file, updated yearly (
# https://api.hungermapdata.org/swe-notifications/population.csv )
# region_id	population
#    272	  1241185
# Food security (expressed as total number of food-insecure people in each region) is available
# in a REST API
# https://api.hungermapdata.org/swe-notifications/foodsecurity
# {
# 	"region_id": 341,
# 	"food_insecure_people": 52490
# },
# The API above accepts an optional query parameter ‘days_ago’ to retrieve past data
# GEThttps://api.hungermapdata.org/swe-notifications/region/{region_id}/country
# returns country information for a given region
# {"region_id": 341, "country_id": 4}
# o GEThttps://api.hungermapdata.org/swe-notifications/country/{country_id}/regions
# returns the list of regions for a given country
# {"country_id": 4, "regions": [{"region_id": 341}, {"region_id": 342}]