# Create a temporary directory to store the build context
TMP_APP="tmp-app"
TMP_SQL="tmp-sql"

mkdir -p "$TMP_APP"
mkdir -p "$TMP_SQL"

# Copy the file that you need to the temporary directory
cp ../requirements.txt "$TMP_APP"
cp ../Authentication.py "$TMP_APP"
cp ../Modules.py "$TMP_APP"
cp ../Monitor.py "$TMP_APP"
cp ../QueueSystem.py "$TMP_APP"
cp ../tests/tests.py "$TMP_APP"
cp ../self_driving_car.py "$TMP_APP"

cp ../API_DB/schema.sql "$TMP_SQL"
cp entrypoint.sh "$TMP_SQL"
cp init.sh "$TMP_SQL"

# Build the image from the temporary directory
docker-compose build

# Remove the temporary directory
rm -rf tmp-app
rm -rf tmp-sql

